"""The ONLY Python file the research agent may change.

Interface, fixed by experiment.py:
  build_model(case: dict) -> torch.nn.Module
  train_model(model, case, train_t, context) -> None

`case` contains e, z0, v0 and case_id. `train_t` contains the allowed
500 physics training coordinates on the selected torch device.

`context` exposes:
  .device, .deadline, .remaining_seconds(), .time_exceeded()
  .physics_components(model, times, case) -> (physics_loss, ic_loss)
  .record(step, train_loss, note='')  [snapshots weights, does NOT reveal validation]

Agent may change architecture, optimiser, loss weighting, training schedule,
training point ordering/mini-batching etc, but not read reference data,
validation data, or change the fixed evaluator. All training points must be
selected from `train_t`; no extra labelled trajectories or ODE integrator.
"""
import math
import time
import torch
from torch import nn

TRAIN_SECONDS = 87.0      # stay safely below the 90 s budget
N_SNAPSHOTS = 12          # evaluator maximum
IC_W_BASE = 10.0          # relaxed baseline IC weight
IC_W_INIT = 2000.0        # strengthened initial IC weight for first 20% of training
LR0, LR1 = 1e-3, 1e-6     # Cosine Annealing: start 1e-3, terminal floor 1e-6
WIDTH = 192               # width 192
N_FREQ = 8                # 8 domain-orthogonal learnable Fourier frequencies (k=1..8)
MAX_GRAD_NORM = 0.5       # tighter gradient clipping threshold
BETAS = (0.99, 0.99)      # momentum saturation limit (tau = 100 steps)


class ModifiedPINN(nn.Module):
    """Paris Perdikaris Modified PINN Architecture with Symmetric Tanh Feature Encoders."""
    def __init__(self):
        super().__init__()
        # Exact domain-orthogonal Fourier basis on [0, 6*pi]: omega_k = k / 3.0
        init_omega = (torch.arange(1, N_FREQ + 1, dtype=torch.float32) / 3.0).reshape(1, -1)
        self.omega = nn.Parameter(init_omega)
        n_feats = 1 + 2 * N_FREQ
        # Symmetric Tanh encoders
        self.u_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())
        self.v_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())
        self.in_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())
        self.z1 = nn.Sequential(nn.Linear(WIDTH, WIDTH), nn.Tanh())
        self.z2 = nn.Sequential(nn.Linear(WIDTH, WIDTH), nn.Tanh())
        self.out_proj = nn.Linear(WIDTH, 2)

    def forward(self, t):
        wt = t * self.omega
        feats = torch.cat([t / (3 * torch.pi) - 1, torch.sin(wt), torch.cos(wt)], dim=1)
        u = self.u_proj(feats)
        v = self.v_proj(feats)
        h = self.in_proj(feats)
        z1 = self.z1(h)
        h = (1.0 - z1) * u + z1 * v
        z2 = self.z2(h)
        h = (1.0 - z2) * u + z2 * v
        return self.out_proj(h)


def build_model(case):
    return ModifiedPINN()


def train_model(model, case, train_t, context):
    budget = min(TRAIN_SECONDS, context.remaining_seconds() - 2.0)
    t_start = time.monotonic()
    optim = torch.optim.Adam(model.parameters(), lr=LR0, betas=BETAS)
    next_snap, step = 0, 0
    while True:
        frac = (time.monotonic() - t_start) / budget
        if frac >= 1.0 or context.time_exceeded() or context.remaining_seconds() < 1.5:
            break
        # Cosine Annealing schedule
        lr = LR1 + 0.5 * (LR0 - LR1) * (1.0 + math.cos(math.pi * frac))
        for pg in optim.param_groups:
            pg['lr'] = lr
        # Asymmetric IC loss weight: 2000 -> 10 over first 20%
        ic_w = IC_W_BASE + (IC_W_INIT - IC_W_BASE) * max(0.0, 1.0 - frac / 0.20)
        optim.zero_grad(set_to_none=True)
        physics, ic = context.physics_components(model, train_t, case)
        loss = physics + ic_w * ic
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=MAX_GRAD_NORM)
        optim.step()
        step += 1
        if next_snap < N_SNAPSHOTS - 1 and frac >= next_snap / (N_SNAPSHOTS - 1):
            context.record(step, float(loss.detach()), note=f'lr={lr:.2e} ic_w={ic_w:.0f}')
            next_snap += 1
    physics, ic = context.physics_components(model, train_t, case)
    context.record(step, float((physics + 100.0 * ic).detach()), note='final full-batch')
