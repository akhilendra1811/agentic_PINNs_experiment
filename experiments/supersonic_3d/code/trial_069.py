"""Historical supersonic Trial 069: periodic residual model and staged Adam training."""
import math
import torch
from torch import nn

WIDTH = 256
DEPTH = 10


class ResPINN(nn.Module):
    def __init__(self, case):
        super().__init__()
        self.L = float(case['length'])
        self.rho0 = float(case['rho0'])
        self.startup_dt = 0.0
        self.in_layer = nn.Linear(19, WIDTH)
        self.hidden = nn.ModuleList([nn.Linear(WIDTH, WIDTH) for _ in range(DEPTH)])
        self.out_layer = nn.Linear(WIDTH, 5)
        for layer in [self.in_layer, self.out_layer, *self.hidden]:
            nn.init.xavier_uniform_(layer.weight)
            nn.init.constant_(layer.bias, 0.01)

    def forward(self, q):
        t = q[:, 3:4]
        feat = []
        for j in range(3):
            for k in range(1, 4):
                phi = 2*math.pi*k*q[:, j:j+1]/self.L
                feat += [torch.sin(phi)/math.sqrt(k), torch.cos(phi)/math.sqrt(k)]
        h = torch.sin(self.in_layer(torch.cat(feat+[t], 1)))
        for layer in self.hidden:
            h = h + .50*torch.sin(1.5*layer(h))
        raw = self.out_layer(h)
        rho = self.rho0*torch.exp(torch.clamp(t*raw[:, :1], -4., 4.))
        return torch.cat([rho, raw[:, 1:]], 1)


def build_model(case):
    return ResPINN(case)


def train_model(model, case, train_domain, train_ic, context, resume=None):
    if resume is not None:
        raise ValueError('The frozen B baseline is freshly trained for every comparison')
    lr_start, lr_max, lr_min = 1e-4, 1e-3, 1e-5
    opt = torch.optim.Adam(model.parameters(), lr=lr_start)
    step, last, next_mark = 0, 0.0, .25
    while context.remaining_seconds() > (0.2 if context.quick else 2.0):
        f = context.cumulative_fraction()
        if f < .05:
            lr = lr_start + (lr_max-lr_start)*f/.05
        else:
            f2 = min(1., (f-.05)/.95)
            lr = lr_min + .5*(lr_max-lr_min)*(1+math.cos(math.pi*f2))
        for pg in opt.param_groups:
            pg['lr'] = lr
        n = 16 if context.quick else 1024
        ic, targets = context.sample_ic(n)
        opt.zero_grad(set_to_none=True)
        if f < .20:
            delta = model(ic)[:, 1:4] - targets
            loss = delta.square().mean() / targets.square().mean().clamp_min(1e-12)
        else:
            candidates = context.sample_domain(2*n, mode='fresh')
            early = torch.nonzero(candidates[:, 3] <= .2, as_tuple=False).flatten()
            middle = torch.nonzero((candidates[:, 3] > .2) &
                                   (candidates[:, 3] <= .5), as_tuple=False).flatten()
            late = torch.nonzero(candidates[:, 3] > .5, as_tuple=False).flatten()
            if len(early) < 5*n//16 or len(middle) < n//4 or len(late) < 7*n//16:
                candidates = torch.cat([candidates, context.sample_domain(4*n, mode='fresh')], 0)
                early = torch.nonzero(candidates[:, 3] <= .2, as_tuple=False).flatten()
                middle = torch.nonzero((candidates[:, 3] > .2) &
                                       (candidates[:, 3] <= .5), as_tuple=False).flatten()
                late = torch.nonzero(candidates[:, 3] > .5, as_tuple=False).flatten()
            q = torch.cat([candidates[early[:5*n//16]],
                           candidates[middle[:n//4]],
                           candidates[late[:7*n//16]]], 0)
            p = context.physics_components(model, q, ic, case, ic_targets=targets)
            blend = min(1., (f-.20)/.20)
            poisson_blend = min(1., (f-.20)/.05)
            physics = (blend*(3.5*p['continuity'] + 7.5*p['momentum'])
                       + poisson_blend*6.0*p['poisson'])
            loss = physics + (1.+32.*blend)*p['ic_relative_mse']
        if not bool(torch.isfinite(loss).item()):
            raise FloatingPointError('Nonfinite winner training loss')
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=.5)
        opt.step()
        step += 1
        last = float(loss.detach())
        if context.cumulative_fraction() >= next_mark and len(context.snapshots) < 11:
            context.record(step, last, f'Experiment B winner Adam lr={lr:.3g}')
            next_mark += .25
    context.record(step, last, 'final baseline')
    return {'optimizer': opt.state_dict(), 'step': step}
