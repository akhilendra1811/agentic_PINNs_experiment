"""Agent-editable KdV PINN method. No reference solution, validation or test access.

Must expose build_model(case) -> torch.nn.Module and
train_model(model,case,train_t,context) -> None.

train_t.next() returns fresh 4096 (t,x) uniformly drawn from [0,1]x[-1,1].
context.physics_components(model,tx,case) -> (PDE MSE, IC MSE)
context.optimizer_step(optimizer) performs one counted optimizer step.
context.should_stop(), context.remaining_seconds(), context.steps,
context.record(step, reported_training_loss, note='') are provided.
"""

import math

import torch
from torch import nn

WIDTH = 176
HIDDEN_LAYERS = 8
LEARNING_RATE = 1.15e-3
IC_WEIGHT = 1.0
INV_WEIGHT = 0.1
INV_SLICES = 8
INV_POINTS = 512
CURRICULUM_FRAC = 0.35
ALPHA_MAX = 2.0



class SinActivation(nn.Module):
    """Sinusoidal activation function (SIREN; Sitzmann et al., NeurIPS 2020)."""

    def forward(self, x):
        return torch.sin(x)


class KdVPINN(nn.Module):
    """KdV PINN with Targeted Dual-Harmonic Fourier Coordinate Projection.

    Reference: Wang, Wang, Perdikaris (CMAME 2021, arXiv:2012.10047)
    Targets the exact physical frequencies of the two-soliton collision system (k in {1, 2}):
    [sin(pi*x), cos(pi*x), sin(2*pi*x), cos(2*pi*x)]
    """

    def __init__(self, case):
        super().__init__()
        self.a1 = float(case["amplitude_1"])
        self.f1 = float(case["frequency_1"])
        self.a2 = float(case["amplitude_2"])
        self.f2 = float(case["frequency_2"])

        in_dim = 7

        self.in_linear = nn.Linear(in_dim, WIDTH)
        self.hidden = nn.ModuleList(
            [nn.Linear(WIDTH, WIDTH) for _ in range(HIDDEN_LAYERS - 1)]
        )
        self.out_proj = nn.Linear(WIDTH, 1)
        self.alpha = nn.Parameter(torch.tensor(1.0))

    def u0_and_ux(self, x):
        c1 = torch.cos(self.f1 * math.pi * x)
        s1 = torch.sin(self.f1 * math.pi * x)
        c2 = torch.cos(self.f2 * math.pi * x)
        s2 = torch.sin(self.f2 * math.pi * x)

        u0 = self.a1 * c1 + self.a2 * c2
        u0_x = -self.a1 * (self.f1 * math.pi) * s1 - self.a2 * (self.f2 * math.pi) * s2
        return u0, u0_x

    def forward(self, tx):
        t = tx[:, 0:1]
        x = tx[:, 1:2]

        u0, u0_x = self.u0_and_ux(x)

        # Targeted dual-harmonic coordinate features: k in {1, 2}
        pix = math.pi * x
        features = torch.cat(
            [
                t,
                torch.sin(pix),
                torch.cos(pix),
                torch.sin(2.0 * pix),
                torch.cos(2.0 * pix),
                u0,
                u0_x / math.pi,
            ],
            dim=1,
        )

        h = torch.sin(self.in_linear(features))
        for layer in self.hidden:
            h = h + torch.sin(layer(h))
        net_out = self.out_proj(h)

        # Bounded hyperbolic tangent temporal ansatz with learnable timescale
        return u0 + torch.tanh(self.alpha * t) * net_out


class SOAPAdEMAMix(torch.optim.Optimizer):
    """SOAP-AdEMAMix: ShampoO with AdEMAMix in Preconditioner's Eigenbasis.

    References:
    - Vyas et al. (arXiv:2409.11321, 2024): SOAP optimizer combining Shampoo preconditioning with Adam in rotated eigenbasis.
    - Wei, Wang, Bhartari, Li, Perdikaris (arXiv:2502.00604, Feb 2025): Gradient Alignment in PINNs: A Second-Order Optimization Perspective.
    - Pagliardini et al. (Apple, arXiv:2409.03137, 2024): AdEMAMix dual-EMA fast and slow momentum.
    """

    def __init__(
        self,
        params,
        lr=1e-3,
        betas=(0.9, 0.99, 0.999),
        alpha=2.0,
        eps=1e-8,
        weight_decay=0.0,
        precondition_frequency=80,
    ):
        defaults = dict(
            lr=lr,
            betas=betas,
            alpha=alpha,
            eps=eps,
            weight_decay=weight_decay,
            precondition_frequency=precondition_frequency,
        )
        super().__init__(params, defaults)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()

        for group in self.param_groups:
            lr = group["lr"]
            beta1, beta2, beta3 = group["betas"]
            alpha = group["alpha"]
            eps = group["eps"]
            weight_decay = group["weight_decay"]
            freq = group["precondition_frequency"]

            for p in group["params"]:
                if p.grad is None:
                    continue
                grad = p.grad
                if grad.is_sparse:
                    raise RuntimeError("SOAP-AdEMAMix does not support sparse gradients")

                state = self.state[p]
                if len(state) == 0:
                    state["step"] = 0
                    state["m1"] = torch.zeros_like(p)
                    state["m2"] = torch.zeros_like(p)
                    state["v"] = torch.zeros_like(p)
                    if p.dim() == 2:
                        d_out, d_in = p.shape
                        state["L"] = torch.eye(d_out, device=p.device)
                        state["R"] = torch.eye(d_in, device=p.device)
                        state["Q_L"] = torch.eye(d_out, device=p.device)
                        state["Q_R"] = torch.eye(d_in, device=p.device)

                state["step"] += 1
                step = state["step"]

                m1 = state["m1"]
                m2 = state["m2"]
                v = state["v"]

                if weight_decay != 0.0:
                    p.mul_(1.0 - lr * weight_decay)

                bc1 = 1.0 - (beta1**step)
                bc2 = 1.0 - (beta2**step)
                bc3 = 1.0 - (beta3**step)

                if p.dim() == 2:
                    d_out, d_in = p.shape
                    L = state["L"]
                    R = state["R"]
                    L.mul_(beta2).addmm_(grad, grad.T, alpha=1.0 - beta2)
                    R.mul_(beta2).addmm_(grad.T, grad, alpha=1.0 - beta2)

                    if step % freq == 0:
                        _, Q_L = torch.linalg.eigh(L + eps * torch.eye(d_out, device=L.device))
                        _, Q_R = torch.linalg.eigh(R + eps * torch.eye(d_in, device=R.device))
                        state["Q_L"] = Q_L
                        state["Q_R"] = Q_R

                    Q_L = state["Q_L"]
                    Q_R = state["Q_R"]

                    # Project gradient into preconditioner eigenbasis
                    grad_proj = Q_L.T @ grad @ Q_R

                    m1.mul_(beta1).add_(grad_proj, alpha=1.0 - beta1)
                    m2.mul_(beta3).add_(grad_proj, alpha=1.0 - beta3)
                    v.mul_(beta2).addcmul_(grad_proj, grad_proj, value=1.0 - beta2)

                    m_mix = (m1 / bc1 + alpha * (m2 / bc3)) / (1.0 + alpha)
                    denom = (v.sqrt() / math.sqrt(bc2)).add_(eps)
                    step_proj = m_mix / denom

                    # Project update back to parameter space
                    update = Q_L @ step_proj @ Q_R.T
                    p.add_(update, alpha=-lr)
                else:
                    m1.mul_(beta1).add_(grad, alpha=1.0 - beta1)
                    m2.mul_(beta3).add_(grad, alpha=1.0 - beta3)
                    v.mul_(beta2).addcmul_(grad, grad, value=1.0 - beta2)

                    m_mix = (m1 / bc1 + alpha * (m2 / bc3)) / (1.0 + alpha)
                    denom = (v.sqrt() / math.sqrt(bc2)).add_(eps)
                    p.addcdiv_(m_mix, denom, value=-lr)

        return loss


def build_model(case):
    return KdVPINN(case)


def train_model(model, case, train_t, context):
    # SOAP-AdEMAMix: Kronecker-preconditioned dual-EMA optimizer with alpha warmup (Perdikaris et al., 2025; Vyas et al., 2024)
    optimizer = SOAPAdEMAMix(
        model.parameters(),
        lr=LEARNING_RATE,
        betas=(0.9, 0.99, 0.999),
        alpha=0.0,
        weight_decay=0.0,
        precondition_frequency=80,
    )

    device = next(model.parameters()).device
    exact_energy = float(case["amplitude_1"]) ** 2 + float(case["amplitude_2"]) ** 2
    x_grid = torch.linspace(-1.0, 1.0, INV_POINTS, device=device).unsqueeze(1)

    next_snapshot_frac = 0.1
    latest_loss = None

    while not context.should_stop():
        if context.remaining_seconds() < 3.0:
            break

        fraction = 1.0 - context.remaining_seconds() / context.seconds

        # Fresh 4096 physics points
        tx = train_t.next()

        # Linear temporal curriculum: expand time domain from [0, 0.05] to [0, 1.0] over first CURRICULUM_FRAC
        if fraction < CURRICULUM_FRAC:
            t_scale = 0.05 + 0.95 * (fraction / CURRICULUM_FRAC)
            tx = torch.cat([tx[:, 0:1] * t_scale, tx[:, 1:2]], dim=1)
        else:
            t_scale = 1.0

        optimizer.zero_grad(set_to_none=True)

        physics_loss, ic_loss = context.physics_components(model, tx, case)

        # Dense Hamiltonian conservation regularizer (S=8 time slices)
        t_slices = torch.rand((INV_SLICES, 1), device=device) * t_scale
        t_expanded = t_slices.repeat_interleave(INV_POINTS, dim=0)
        x_expanded = x_grid.repeat(INV_SLICES, 1)
        tx_inv = torch.cat([t_expanded, x_expanded], dim=1)
        u_inv = model(tx_inv).view(INV_SLICES, INV_POINTS)

        # Mass conservation: \int_{-1}^1 u dx = 0
        mass_loss = (u_inv.mean(dim=1) * 2.0).square().mean()
        # L2 energy conservation: \int_{-1}^1 u^2 dx = a1^2 + a2^2
        energy_loss = (
            (u_inv.square().mean(dim=1) * 2.0) - exact_energy
        ).square().mean()
        inv_loss = mass_loss + energy_loss

        # Combined composite loss
        loss = physics_loss + IC_WEIGHT * ic_loss + INV_WEIGHT * inv_loss

        loss.backward()

        if context.should_stop():
            break

        context.optimizer_step(optimizer)
        latest_loss = float(loss.detach())

        fraction = 1.0 - context.remaining_seconds() / context.seconds
        if fraction < CURRICULUM_FRAC:
            lr_curr = LEARNING_RATE
            alpha_curr = ALPHA_MAX * (fraction / CURRICULUM_FRAC)
        else:
            alpha_curr = ALPHA_MAX
            phase2_frac = min((fraction - CURRICULUM_FRAC) / (1.0 - CURRICULUM_FRAC), 1.0)
            lr_curr = 1e-7 + 0.5 * (LEARNING_RATE - 1e-7) * (
                1.0 + math.cos(math.pi * phase2_frac)
            )
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr_curr
            param_group["alpha"] = alpha_curr

        if context.steps == 1 or (
            fraction >= next_snapshot_frac and len(context.snapshots) < 11
        ):
            context.record(
                context.steps,
                latest_loss,
                note="zero-decay dense invariant cosine decay",
            )

            if context.steps != 1:
                next_snapshot_frac += 0.1

    # Final checkpoint
    if latest_loss is not None and len(context.snapshots) < 12:
        context.record(context.steps, latest_loss, note="final")
