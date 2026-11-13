# Experiment 042: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 038, our champion Modified PINN architecture (dual feature encoders $U, V$ with multiplicative convex gating $h_l = (1 - z_l) \odot U + z_l \odot V$) achieved our all-time best mean validation loss of 0.0002937 using an initial learning rate of $LR_0 = 1.0 \times 10^{-3}$.

Unlike additive ResNets (where gradient contributions from skip connections add linearly), the Modified PINN architecture features bilinear multiplicative interactions between the encoder weights ($W_u, W_v$) and the gating weights ($W_z$). When both sets of weights take large steps simultaneously under $LR_0 = 1.0 \times 10^{-3}$ during early training, their joint product $\Delta(z_l \odot (V - U))$ exhibits second-order step-size amplification ($\mathcal{O}(\eta^2)$). This can cause mild early parameter oscillation in high-eccentricity cases before the gating units discover their primary phase-switching trajectories.

Moderating the initial learning rate slightly by 20% to $LR_0 = 8.0 \times 10^{-4}$ (with Cosine Annealing down to $1.0 \times 10^{-6}$ over 87.0 s) will dampen early bilinear parameter volatility, allowing the dual encoders $U, V$ and the gating units $z_l$ to co-adapt smoothly into the optimal trajectory manifold.

## Proposed method change

Optimizer learning rate modification:
- Change `LR0 = 8e-4` (down from 1e-3). `LR1 = 1e-6` remains unchanged.
  `lr = LR1 + 0.5 * (LR0 - LR1) * (1.0 + math.cos(math.pi * frac))`
- Restore symmetric Tanh encoders from Trial 038:
  `self.u_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
  `self.v_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
  `self.in_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
  Two gating stages ($z_1, z_2$) with `WIDTH = 192` (84,874 parameters).
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Loss weighting: Asymmetric IC annealing from Trial 034/038 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=8e-4, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=8e-4, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 038 (mean 0.0002937, worst 0.0008230). Dampening early bilinear step sizes should improve training smoothness across the initial 20 seconds, targeting mean validation loss below 0.00027 and compressing worst-case error on dev_08 below 0.00075.

## Evidence from previous experiments

Trial 013 showed that LR0 = 2e-3 was unstable, while LR0 = 1e-3 was stable. In bilinear architectures like the Modified PINN (Trial 038), calibrating the peak learning rate to 8e-4 evaluates whether slightly moderated initial step sizes optimize the co-adaptation of encoders and gates.

## Observed results

All 10 development cases completed (87.0 s each, ~20.4k steps, 84,874 parameters). Moderating the initial learning rate to LR0 = 8.0e-4 degraded performance across the benchmark:
- Mean validation loss increased from 0.0002937 (Trial 038) to 0.0003568 (+21.5% degradation).
- Worst-case validation loss broke through the sub-1e-3 ceiling, increasing from 0.0008230 to 0.001056 (dev_08).
- Nearly every individual development case performed worse than Trial 038:
  - dev_01: 4.45e-06 vs 3.15e-06 in Trial 038 (41% worse)
  - dev_02: 0.000447 vs 0.000390 in Trial 038 (15% worse)
  - dev_03: 0.000264 vs 0.000230 in Trial 038 (15% worse)
  - dev_04: 3.43e-05 vs 2.18e-05 in Trial 038 (57% worse)
  - dev_05: 2.98e-08 vs 1.48e-08 in Trial 038 (2x worse)
  - dev_06: 0.000388 vs 0.000324 in Trial 038 (20% worse)
  - dev_07: 0.000564 vs 0.000464 in Trial 038 (22% worse)
  - dev_08: 0.001056 vs 0.000823 in Trial 038 (28% worse)
  - dev_09: 0.000277 vs 0.000169 in Trial 038 (64% worse)
  - dev_10: 0.000535 vs 0.000513 in Trial 038 (4% worse)

Physical and optimization explanation: In the 87.0-second training budget, the first 15-20 seconds are crucial for the learnable Fourier frequencies self.omega to migrate from their initial grid positions into the true non-linear orbital harmonics of each case. A peak learning rate of 1.0e-3 provides the exact kinetic energy required to rapidly overcome initial spectral misalignments. Moderating LR0 to 8.0e-4 throttles this initial migration speed, causing the optimizer to lag behind schedule throughout the entire Cosine decay trajectory. LR0 = 1.0e-3 is the true optimal peak learning rate.

## Agent decision

Reject: LR0 = 8.0e-4 degraded all 10 development cases. Revert immediately to LR0 = 1.0e-3 from champion Trial 038.

## Reason for decision

Mean validation loss degraded by 21.5% and worst case broke the 1e-3 threshold. Full peak learning rate (1.0e-3) is necessary for rapid early frequency and orbital adaptation.

## Next experiment

Trial 043: Width Scaling in Modified PINN (Testing WIDTH = 224 vs 192).
In Trial 038, our Modified PINN used WIDTH = 192, yielding 84,874 parameters and ~20,433 steps per case. The allowed parameter budget is 250,000 parameters. Sizing WIDTH = 224 in the 2-stage Modified PINN yields:
3 * (17 * 224 + 224) + 2 * (224 * 224 + 224) + 224 * 2 + 2 + 8 ≈ 112,650 parameters.
This remains well below the 250k ceiling while increasing hidden layer width by 16.7%. In multi-frequency PINNs, wider hidden layers provide more parallel linear combinations of the gated Fourier modes (U and V), allowing finer spatial resolution of steep curvature regions without adding sequential depth. We will test whether width 224 improves upon Trial 038's 0.0002937 benchmark.
