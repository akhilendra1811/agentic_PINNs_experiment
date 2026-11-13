"""Trial 056: SR1 Krylov cubic regularisation on score-component loss weights on width256 RWF/FiLM with immediate density evolution with hidden time FiLM, then full-pool PR+.

Belief-based variance update adapted from Zhuang et al.'s reference algorithm:
https://github.com/juntang-zhuang/Adabelief-Optimizer
Minimal variant: no rectification, AMSGrad or decay; epsilon is explicit.
RWF precedent: https://arxiv.org/abs/2210.01274 ; five hidden weights only.
Train log scales and directions; no unit-norm constraint.
Refinement: zero density hold and direct t gate on the nonnegative-time domain.
Width256 refinement; depth, objective, pools and full-pool PR+ finish are unchanged.
Repeated input concatenation skips inspired by NeRF: https://arxiv.org/abs/2003.08934 .
FiLM precedent: https://arxiv.org/abs/1709.07871 ; local bounded time conditioning.
Snake activation x+sin(x)^2: https://arxiv.org/abs/2006.08195 ; fixed alpha=1.
"""
# BSD 2-Clause License
#
# Copyright (c) 2021, Juntang Zhuang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import math
import torch
from torch import nn


class SnakeActivation(nn.Module):
    def forward(self, x):
        return x+torch.sin(x).square()


def feature_modulate(hidden, pair):
    return (1+0.5*torch.tanh(pair[:, 0]))*hidden + 0.5*torch.tanh(pair[:, 1])


class FactorizedLinear(nn.Module):
    """Independent RWF log-scale parameterisation, W=diag(exp(s))*V."""
    def __init__(self, fresh_linear):
        super().__init__()
        self.in_features = fresh_linear.in_features
        self.out_features = fresh_linear.out_features
        log_scale = 1.0 + 0.1*torch.randn(self.out_features)
        self.log_scale = nn.Parameter(log_scale)
        self.direction = nn.Parameter(fresh_linear.weight.detach().clone()/log_scale.exp()[:, None])
        self.bias = nn.Parameter(fresh_linear.bias.detach().clone())

    def forward(self, x):
        weight = self.log_scale.exp()[:, None]*self.direction
        return torch.nn.functional.linear(x, weight, self.bias)


class PaperModel(nn.Module):
    def __init__(self, case):
        super().__init__()
        self.length = float(case['length'])
        self.rho0 = float(case['rho0'])
        self.startup_dt = 0.0
        seq = [nn.Linear(19, 256)]
        for _ in range(5):
            seq += [SnakeActivation(), nn.Linear(256, 256)]
        seq += [SnakeActivation(), nn.Linear(256, 5)]
        self.net = nn.Sequential(*seq)
        for module in self.net:
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.constant_(module.bias, 0.01)

        # Expand only after fresh parent-shaped initialisation; copy no trained state.
        for index, module in enumerate(self.net):
            if isinstance(module, nn.Linear) and module.in_features == 256 and module.out_features == 256:
                expanded = nn.Linear(256+19, 256)
                with torch.no_grad():
                    expanded.weight[:, :256].copy_(module.weight)
                    expanded.weight[:, 256:].zero_()
                    expanded.bias.copy_(module.bias)
                self.net[index] = expanded

        # Factorise only five hidden affine weights after fresh expansion.
        for index, module in enumerate(self.net):
            if isinstance(module, nn.Linear) and module.in_features == 275:
                self.net[index] = FactorizedLinear(module)

        # Identity conditioning at initialisation; preserve main seed-map first.
        self.conditioner = nn.Sequential(nn.Linear(1, 32), SnakeActivation(),
                                         nn.Linear(32, 6*2*256))
        nn.init.xavier_uniform_(self.conditioner[0].weight)
        nn.init.constant_(self.conditioner[0].bias, 0.01)
        nn.init.zeros_(self.conditioner[-1].weight)
        nn.init.zeros_(self.conditioner[-1].bias)

    def raw_from_features(self, features, time):
        modulation = self.conditioner(time).reshape(-1, 6, 2, 256)
        hidden = features
        activation_index = 0
        for module in self.net:
            if isinstance(module, SnakeActivation):
                hidden = module(feature_modulate(hidden, modulation[:, activation_index]))
                activation_index += 1
            else:
                if isinstance(module, (nn.Linear, FactorizedLinear)) and module.in_features == 275:
                    hidden = module(torch.cat([hidden, features], dim=1))
                else:
                    hidden = module(hidden)
        return hidden

    def forward(self, q):
        t = q[:, 3:4]
        f = []
        for j in range(3):
            for k in range(1, 4):
                phase = 2 * math.pi * k * q[:, j:j+1] / self.length
                f += [torch.sin(phase)/math.sqrt(k), torch.cos(phase)/math.sqrt(k)]
        out = self.raw_from_features(torch.cat(f + [t], 1), t)
        dt = t
        rho = self.rho0 * torch.exp(torch.clamp(dt*out[:, :1], -4., 4.))
        return torch.cat([rho, out[:, 1:]], 1)


class UnrectifiedAdaBelief(torch.optim.Optimizer):
    """Minimal belief variance algorithm; epsilon accumulates as upstream."""
    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), eps=1e-12):
        if lr <= 0 or eps <= 0 or not all(0 <= b < 1 for b in betas):
            raise ValueError('Invalid AdaBelief settings')
        super().__init__(params, dict(lr=lr, betas=betas, eps=eps))

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            b1, b2 = group['betas']
            eps = group['eps']
            for parameter in group['params']:
                if parameter.grad is None:
                    continue
                gradient = parameter.grad
                if gradient.is_sparse:
                    raise RuntimeError('Sparse gradients are unsupported')
                state = self.state[parameter]
                if not state:
                    state['step'] = 0
                    state['mean'] = torch.zeros_like(parameter)
                    state['variance'] = torch.zeros_like(parameter)
                state['step'] += 1
                t = state['step']
                mean, variance = state['mean'], state['variance']
                mean.mul_(b1).add_(gradient, alpha=1-b1)
                residual = gradient - mean
                variance.mul_(b2).addcmul_(residual, residual, value=1-b2)
                variance.add_(eps)
                denominator = variance.sqrt().div_(math.sqrt(1-b2**t)).add_(eps)
                parameter.addcdiv_(mean, denominator, value=-group['lr']/(1-b1**t))
        return loss


def build_model(case):
    return PaperModel(case)


class GradientDifferenceAdan(torch.optim.Optimizer):
    """Adan recurrence with first difference zero; no decay or clipping.

    Xie et al. https://arxiv.org/abs/2208.06677 .
    """
    def __init__(self, params, lr=0.001, betas=(0.98, 0.92, 0.99), eps=1e-8):
        if lr <= 0 or eps <= 0 or not all(0 <= b < 1 for b in betas):
            raise ValueError('Invalid Adan settings')
        super().__init__(params, dict(lr=lr, betas=betas, eps=eps))

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            b1, b2, b3 = group['betas']
            for parameter in group['params']:
                if parameter.grad is None:
                    continue
                gradient = parameter.grad
                if gradient.is_sparse:
                    raise RuntimeError('Sparse gradients are unsupported')
                state = self.state[parameter]
                if not state:
                    state['step'] = 0
                    state['previous'] = gradient.clone()
                    state['mean'] = torch.zeros_like(parameter)
                    state['difference'] = torch.zeros_like(parameter)
                    state['variance'] = torch.zeros_like(parameter)
                state['step'] += 1
                t = state['step']
                delta = gradient-state['previous']
                mean, difference, variance = state['mean'], state['difference'], state['variance']
                mean.mul_(b1).add_(gradient, alpha=1-b1)
                difference.mul_(b2).add_(delta, alpha=1-b2)
                extrapolated = gradient+b2*delta
                variance.mul_(b3).addcmul_(extrapolated, extrapolated, value=1-b3)
                denominator = (variance/(1-b3**t)).sqrt().add_(group['eps'])
                numerator = mean/(1-b1**t)+b2*difference/(1-b2**t)
                parameter.addcdiv_(numerator, denominator, value=-group['lr'])
                state['previous'].copy_(gradient)
        return loss


class FullBatchDeadline(Exception):
    pass


@torch.no_grad()
def set_parameters(parameters, vector):
    offset = 0
    for parameter in parameters:
        size = parameter.numel()
        parameter.copy_(vector[offset:offset+size].view_as(parameter))
        offset += size


def pr_direction(gradient, previous_gradient, previous_direction):
    beta = 0.0
    if previous_gradient is not None:
        beta = max(0.0, float(torch.dot(gradient, gradient-previous_gradient) /
                              torch.dot(previous_gradient, previous_gradient).clamp_min(1e-30)))
        if not math.isfinite(beta):
            beta = 0.0
    direction = -gradient if previous_direction is None else -gradient + beta*previous_direction
    slope = float(torch.dot(gradient, direction))
    norm2 = float(torch.dot(gradient, gradient))
    restart = not math.isfinite(slope) or slope >= -0.001*norm2
    if restart:
        direction = -gradient
        slope = -norm2
        beta = 0.0
    return direction, slope, beta, restart


class LimitedSR1:
    """Indefinite SR1 model from I and up to eight retained secant pairs."""
    def __init__(self, memory=8):
        self.memory, self.pairs, self.updates = memory, [], []
        self.skipped = self.added = 0

    def apply(self, vector):
        result = vector.clone()
        for u, denominator in self.updates:
            result = result+u*(torch.dot(u, vector)/denominator)
        return result

    def add(self, s, y):
        residual = y-self.apply(s)
        denominator = float(torch.dot(residual, s))
        floor = 1e-6*float(residual.norm())*float(s.norm())
        if not math.isfinite(denominator) or abs(denominator) <= max(1e-20, floor):
            self.skipped += 1
            return False
        proposed = (self.pairs+[(s.detach().clone(), y.detach().clone())])[-self.memory:]
        self.pairs, self.updates = [], []
        for si, yi in proposed:
            u = yi-self.apply(si)
            denom = float(torch.dot(u, si))
            threshold = max(1e-20, 1e-6*float(u.norm())*float(si.norm()))
            if math.isfinite(denom) and abs(denom) > threshold:
                self.pairs.append((si, yi))
                self.updates.append((u, denom))
            else:
                self.skipped += 1
        self.added += 1
        return True


def solve_small_cubic(matrix, linear, sigma):
    matrix = matrix.detach().cpu().double()
    linear = linear.detach().cpu().double()
    eigenvalues, vectors = torch.linalg.eigh((matrix+matrix.T)/2)
    b = vectors.T @ linear
    lower = max(0., -float(eigenvalues[0]))
    scale = max(1., float(eigenvalues.abs().max()))
    mask = (eigenvalues+lower).abs() <= 1e-12*scale
    coefficients = torch.zeros_like(b)
    if lower > 0 and float(b[mask].norm()) <= 1e-12*max(1., float(b.norm())):
        coefficients[~mask] = -b[~mask]/(eigenvalues[~mask]+lower)
        target = lower/sigma
        if float(coefficients.norm()) <= target:
            index = int(torch.nonzero(mask)[0])
            extra = math.sqrt(max(0., target*target-float(coefficients.square().sum())))
            coefficients[index] = -math.copysign(extra, float(b[index]))
            return vectors @ coefficients, lower, True
    def equation(mu):
        denominator = (eigenvalues+mu).clamp_min(1e-30)
        return float((b/denominator).norm())-mu/sigma
    lo = lower
    hi = max(1., lower+1., math.sqrt(sigma*float(b.norm()))+lower)
    for _ in range(100):
        if equation(hi) <= 0:
            break
        hi *= 2
    else:
        raise ArithmeticError('Cubic secular root not bracketed')
    for _ in range(80):
        mid = .5*(lo+hi)
        if equation(mid) > 0:
            lo = mid
        else:
            hi = mid
    mu = hi
    coefficients = -b/(eigenvalues+mu).clamp_min(1e-30)
    return vectors @ coefficients, mu, False


def cubic_krylov_step(gradient, curvature, sigma, maximum_dimension=6):
    norm = float(gradient.norm())
    if norm == 0:
        return torch.zeros_like(gradient), 0., 0, 0., False
    basis = [-gradient/norm]
    for _ in range(maximum_dimension-1):
        candidate = curvature.apply(basis[-1])
        scale = max(1., float(candidate.norm()))
        for _ in range(2):
            for q in basis:
                candidate = candidate-torch.dot(q, candidate)*q
        length = float(candidate.norm())
        if length <= 1e-7*scale:
            break
        basis.append(candidate/length)
    q = torch.stack(basis, dim=1)
    bq = torch.stack([curvature.apply(v) for v in basis], dim=1)
    projected = q.T @ bq
    linear = q.T @ gradient
    z, mu, hard = solve_small_cubic(projected, linear, sigma)
    direction = q @ z.to(gradient)
    bdirection = curvature.apply(direction)
    pnorm = float(direction.norm())
    predicted = -float(torch.dot(gradient, direction)+.5*torch.dot(direction, bdirection))-sigma*pnorm**3/3
    stationarity = float((projected.detach().cpu().double()@z+linear.detach().cpu().double()+sigma*float(z.norm())*z).norm())
    return direction, predicted, len(basis), stationarity, hard


def cubic_sigma_update(sigma, ratio):
    if ratio < .1:
        sigma = min(1e12, 4*sigma)
    elif ratio > .75:
        sigma = max(1e-6, .5*sigma)
    return sigma, math.isfinite(ratio) and ratio > .1


def train_model(model, case, train_domain, train_ic, context, resume=None):
    if resume is not None:
        raise ValueError('Every attempt is freshly trained')
    parameters = list(model.parameters())
    matrices = [m.direction for m in model.net if isinstance(m, FactorizedLinear)]
    matrix_ids = {id(p) for p in matrices}
    auxiliary = [p for p in parameters if id(p) not in matrix_ids]
    adan = GradientDifferenceAdan(matrices, lr=0.001, betas=(0.98, 0.92, 0.99), eps=1e-8)
    adaptive = UnrectifiedAdaBelief(auxiliary, lr=0.001, betas=(0.9, 0.999), eps=1e-12)
    step, last, next_mark = 0, 0.0, .25
    pde_draws = ic_draws = pde_evaluations = ic_evaluations = 0

    # Fixed training-target energy; no model evaluation or new coordinates.
    energy_sum, energy_count = 0.0, 0
    while energy_count < len(train_ic):
        iq, targets = context.sample_ic(min(4096, len(train_ic)-energy_count), mode='cycle')
        ic_draws += len(iq)
        energy_sum += float(targets.detach().cpu().double().square().sum())
        energy_count += len(iq)
    ic_energy = max(energy_sum/energy_count, 1e-12)

    def evaluate_chunk(q, ic, targets, pde_weight, ic_weight, backward):
        nonlocal pde_evaluations, ic_evaluations
        pde_evaluations += len(q)
        ic_evaluations += len(ic)
        parts = context.physics_components(model, q, ic, case, ic_targets=targets)
        physics = (parts['continuity'] + (parts['momentum_x'] + parts['momentum_y']
                   + parts['momentum_z'])/3.0 + parts['poisson'])
        initial = (parts['ic_x'] + parts['ic_y'] + parts['ic_z'])/ic_energy
        loss = pde_weight*physics + ic_weight*initial
        if not bool(torch.isfinite(loss).item()):
            raise FloatingPointError('Nonfinite training objective')
        if backward:
            loss.backward()
        return float(loss.detach())

    # Relative-IC/mean-momentum objective and the same stochastic batches; hidden matrices use Adan.
    while context.cumulative_fraction() < .5 and context.remaining_seconds() > 8.:
        n = 16 if context.quick else 1024
        q = context.sample_domain(n, mode='pool')
        ic, targets = context.sample_ic(n, mode='pool')
        pde_draws += len(q)
        ic_draws += len(ic)
        model.zero_grad(set_to_none=True)
        last = evaluate_chunk(q, ic, targets, 1., 1., True)
        adaptive.step()
        adan.step()
        step += 1
        if context.cumulative_fraction() >= next_mark and len(context.snapshots) < 10:
            context.record(step, last, f'Adan/AdaBelief before full PR+; PDE_eval={pde_evaluations}; IC_eval={ic_evaluations}')
            next_mark += .25

    # Cache each complete frozen pool once via cycle sampling. No new coordinates.
    total_pde, total_ic = len(train_domain), len(train_ic)
    chunks = []
    pde_position = ic_position = 0
    while pde_position < total_pde:
        nq = min(4096, total_pde-pde_position)
        next_ic = (pde_position+nq)*total_ic//total_pde
        ni = next_ic-ic_position
        q = context.sample_domain(nq, mode='cycle')
        ic, targets = context.sample_ic(ni, mode='cycle')
        chunks.append((q, ic, targets))
        pde_draws += len(q)
        ic_draws += len(ic)
        pde_position += nq
        ic_position = next_ic

    def evaluate_full(backward):
        if backward:
            model.zero_grad(set_to_none=True)
        value = 0.0
        for q, ic, targets in chunks:
            if context.remaining_seconds() < 4.:
                raise FullBatchDeadline()
            value += evaluate_chunk(q, ic, targets, len(q)/total_pde,
                                    len(ic)/total_ic, backward)
        return value

    curvature = LimitedSR1(memory=8)
    sigma = 1000.0
    pending = None
    attempts = accepted_steps = nonfinite_rejections = gradient_passes = value_passes = 0
    trace = []
    while context.remaining_seconds() > 12.:
        base = torch.cat([p.detach().reshape(-1) for p in parameters])
        try:
            gradient_passes += 1
            base_loss = evaluate_full(True)
            gradient = torch.cat([(p.grad.detach() if p.grad is not None else torch.zeros_like(p)).reshape(-1)
                                  for p in parameters])
            if not bool(torch.isfinite(gradient).all().item()):
                raise FloatingPointError('Nonfinite full-pool gradient')
            if pending is not None:
                old_step, old_gradient = pending
                curvature.add(old_step, gradient-old_gradient)
                pending = None
            proposal_step, predicted, dimension, stationarity, hard = cubic_krylov_step(gradient, curvature, sigma)
            if not math.isfinite(predicted) or predicted <= 0:
                raise ArithmeticError('Nonpositive Cubic predicted reduction')
            if context.remaining_seconds() < 8.:
                raise FullBatchDeadline()
            set_parameters(parameters, base+proposal_step)
            value_passes += 1
            try:
                proposal = evaluate_full(False)
            except (FloatingPointError, ValueError) as error:
                if 'finite' not in str(error).lower():
                    raise
                nonfinite_rejections += 1
                proposal = float('inf')
            actual = base_loss-proposal
            ratio = actual/predicted
            before_sigma = sigma
            sigma, accepted = cubic_sigma_update(sigma, ratio)
            attempts += 1
            step += 1
            if accepted:
                last = proposal
                accepted_steps += 1
                # Actual floating-point displacement supplies the secant pair.
                realised = torch.cat([p.detach().reshape(-1) for p in parameters])-base
                pending = (realised, gradient.detach().clone())
            else:
                set_parameters(parameters, base)
                last = base_loss
            record = {'attempt': attempts, 'sigma_before': before_sigma, 'sigma_after': sigma,
                      'predicted': predicted, 'actual': actual if math.isfinite(actual) else None,
                      'ratio': ratio if math.isfinite(ratio) else None, 'accepted': accepted,
                      'dimension': dimension, 'stationarity': stationarity, 'hard_case': hard, 'step_norm': float(proposal_step.norm()), 'pairs': len(curvature.pairs)}
            trace.append(record)
            print('CUBIC '+__import__('json').dumps(record), flush=True)
            if context.cumulative_fraction() >= next_mark and len(context.snapshots) < 10:
                context.record(step, last, f'Cubic a={attempts}; ok={accepted_steps}; sigma={sigma:.5g}; pred={predicted:.6g}; actual={actual:.6g}; ratio={ratio:.5g}; pairs={len(curvature.pairs)}')
                next_mark += .25
        except FullBatchDeadline:
            set_parameters(parameters, base)
            break
    context.record(step, last, f'final cubic; PDE_eval={pde_evaluations}; IC_eval={ic_evaluations}; PDE_draws={pde_draws}; IC_draws={ic_draws}; tr={attempts}; accepted={accepted_steps}; gp={gradient_passes}; vp={value_passes}; nf={nonfinite_rejections}; pairs={len(curvature.pairs)}; E={ic_energy:.7g}')
    return {'training_weights': {'momentum_each': 1/3, 'ic_each': 1/ic_energy, 'ic_energy': ic_energy},
            'optimizer': {'auxiliary_adabelief': adaptive.state_dict(), 'hidden_adan': adan.state_dict()}, 'step': step,
            'cubic': {'sigma': sigma, 'pairs': curvature.pairs, 'skipped': curvature.skipped,
                       'added': curvature.added, 'trace': trace, 'gradient_passes_started': gradient_passes,
                       'value_passes_started': value_passes, 'attempts': attempts, 'accepted': accepted_steps},
            'sampling': {'initial_mode': 'pool', 'full_pool_cache_mode': 'cycle',
                         'pde_draws': pde_draws, 'ic_draws': ic_draws,
                         'pde_evaluations': pde_evaluations, 'ic_evaluations': ic_evaluations,
                         'pde_per_complete_full_evaluation': total_pde,
                         'ic_per_complete_full_evaluation': total_ic, 'pde_microbatch': 4096}}
