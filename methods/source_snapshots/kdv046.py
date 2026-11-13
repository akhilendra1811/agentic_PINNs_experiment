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

WIDTH = 160
HIDDEN_LAYERS = 8
LEARNING_RATE = 1.08e-3
IC_WEIGHT = 1.0


class KdVPINN(nn.Module):
    def __init__(self, case):
        super().__init__()
        self.a1 = float(case["amplitude_1"])
        self.f1 = float(case["frequency_1"])
        self.a2 = float(case["amplitude_2"])
        self.f2 = float(case["frequency_2"])

        self.in_proj = nn.Sequential(nn.Linear(5, WIDTH), nn.Tanh())
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

        # Periodic input representation with normalized initial gradient scale
        features = torch.cat(
            [t, torch.sin(math.pi * x), torch.cos(math.pi * x), u0, u0_x / math.pi],
            dim=1,
        )

        h = self.in_proj(features)
        for layer in self.hidden:
            h = h + torch.tanh(layer(h))
        net_out = self.out_proj(h)

        # Bounded hyperbolic tangent temporal ansatz with learnable timescale
        return u0 + torch.tanh(self.alpha * t) * net_out


def build_model(case):
    return KdVPINN(case)


def train_model(model, case, train_t, context):

    optimizer = torch.optim.AdamW(
        model.parameters(), lr=LEARNING_RATE, betas=(0.9, 0.99), weight_decay=5e-5
    )

    next_snapshot_frac = 0.1
    latest_loss = None

    while not context.should_stop():
        if context.remaining_seconds() < 3.0:
            break

        fraction = 1.0 - context.remaining_seconds() / context.seconds

        # Fresh 4096 physics points
        tx = train_t.next()

        # Linear temporal curriculum: expand time domain from [0, 0.05] to [0, 1.0] over first 35%
        if fraction < 0.35:
            t_scale = 0.05 + 0.95 * (fraction / 0.35)
            tx = torch.cat([tx[:, 0:1] * t_scale, tx[:, 1:2]], dim=1)

        optimizer.zero_grad(set_to_none=True)

        physics_loss, ic_loss = context.physics_components(model, tx, case)

        # Soft initial-condition enforcement
        loss = physics_loss + IC_WEIGHT * ic_loss

        loss.backward()

        if context.should_stop():
            break

        context.optimizer_step(optimizer)
        latest_loss = float(loss.detach())

        fraction = 1.0 - context.remaining_seconds() / context.seconds
        if fraction < 0.35:
            lr_curr = LEARNING_RATE
        else:
            phase2_frac = min((fraction - 0.35) / 0.65, 1.0)
            lr_curr = 1e-7 + 0.5 * (LEARNING_RATE - 1e-7) * (
                1.0 + math.cos(math.pi * phase2_frac)
            )
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr_curr

        if context.steps == 1 or (
            fraction >= next_snapshot_frac and len(context.snapshots) < 11
        ):
            context.record(context.steps, latest_loss, note="cosine decay")

            if context.steps != 1:
                next_snapshot_frac += 0.1

    # Final checkpoint
    if latest_loss is not None and len(context.snapshots) < 12:
        context.record(context.steps, latest_loss, note="final")
