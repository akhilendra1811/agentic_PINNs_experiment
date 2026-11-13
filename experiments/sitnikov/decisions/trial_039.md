# Experiment 039: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 038, the Paris Perdikaris Modified PINN architecture (dual feature encoders $U, V$ with multiplicative convex gating $h_l = (1 - z_l) \odot U + z_l \odot V$) established a dramatic new campaign record, dropping mean validation loss to 0.0002937 with all cases sub-1e-3.

Trial 038 used 2 gating stages ($z_1, z_2$) at width 192. In the original Wang et al. (2021) paper, deeper Modified MLPs with 3 or 4 gating stages showed superior expressive power on stiff multi-scale dynamics because each successive gating stage performs a refined spatial-temporal filtering of the Fourier representations $U$ and $V$. Unlike standard deep MLPs (where gradients decay exponentially with depth), the Modified PINN architecture maintains direct first-order gradient flow from the loss back to the encoders $U$ and $V$ at every stage regardless of depth.

We hypothesize that expanding to 3 gating stages ($z_1, z_2, z_3$) at width 160 (86,250 parameters, precisely matched in capacity to Trial 038's 84,874 parameters) will provide a 3-tier hierarchical resolution of the Sitnikov trajectory:
1. Stage 1 ($z_1$): captures the macroscopic orbital envelope and initial condition anchoring;
2. Stage 2 ($z_2$): resolves binary orbital harmonics ($k=3, \omega=1.0$) and quarter-period quadrature;
3. Stage 3 ($z_3$): models sharp localized acceleration pulses when the primaries pass pericenter.

## Proposed method change

Architecture depth expansion:
- In `ModifiedPINN`:
  - Set `WIDTH = 160`.
  - Add third gating layer:
    `self.z3 = nn.Sequential(nn.Linear(WIDTH, WIDTH), nn.Tanh())`
  - In `forward`:
    ```python
    h = self.in_proj(feats)
    z1 = self.z1(h)
    h = (1.0 - z1) * u + z1 * v
    z2 = self.z2(h)
    h = (1.0 - z2) * u + z2 * v
    z3 = self.z3(h)
    h = (1.0 - z3) * u + z3 * v
    return self.out_proj(h)
    ```
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$ (86,250 parameters, well within 250k ceiling).
- Loss weighting: Asymmetric IC annealing from Trial 034/038 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 038 (mean 0.0002937, worst 0.0008230). The third gating layer will enhance localized non-linear resolution around pericenter passages, targeting worst-case reduction on dev_08 and dev_10 and aiming to push mean validation loss below 0.00025.

## Evidence from previous experiments

Trial 038 proved that multiplicative gating is overwhelmingly superior to additive concatenation. Evaluating 3-stage gating tests whether the depth benefits reported in Perdikaris's original work translate to our 87-second training regime without throughput penalty.

## Observed results

All 10 development cases completed (87.0 s each, ~16.8k steps, 86,250 parameters). Expanding from 2 to 3 gating stages degraded performance:
- Mean validation loss increased from 0.0002937 (Trial 038) to 0.0003971 (+35.2% degradation).
- Worst-case validation loss increased from 0.0008230 (dev_08 in Trial 038) to 0.0009319 (dev_08 in Trial 039).
- Optimization throughput dropped from ~20,433 steps in Trial 038 to ~16,777 steps in Trial 039 (an 18% reduction in optimization step count).
- 9 of 10 development cases degraded compared to Trial 038:
  - dev_01: 3.75e-06 vs 3.15e-06 in Trial 038
  - dev_03: 0.000292 vs 0.000230 in Trial 038 (27% worse)
  - dev_04: 4.79e-05 vs 2.18e-05 in Trial 038 (2.2x worse)
  - dev_05: 6.84e-07 vs 1.48e-08 in Trial 038 (46x worse)
  - dev_06: 0.000522 vs 0.000324 in Trial 038 (61% worse)
  - dev_07: 0.000671 vs 0.000464 in Trial 038 (45% worse)
  - dev_08: 0.000932 vs 0.000823 in Trial 038 (13% worse)
  - dev_09: 0.000504 vs 0.000169 in Trial 038 (3x worse)
  - dev_10: 0.000642 vs 0.000513 in Trial 038 (25% worse)
  - dev_02: 0.000356 vs 0.000390 in Trial 038 (slightly better)

Physical and optimization explanation: In the Sitnikov problem, the state space is 2-dimensional: $(z, v)$. The two feature encoders $U(t)$ and $V(t)$ learn the two fundamental quadrature modes. Two gating stages ($z_1, z_2$) provide exactly the necessary degrees of freedom to dynamically modulate position and velocity representations. Introducing a third stage adds unnecessary structural depth that slows down the second-derivative autograd computation graph, reducing training throughput by 3,700 steps without providing new physical expressivity. The 2-stage architecture is the exact sweet spot of expressivity and optimization speed.

## Agent decision

Reject: 3-stage gating suffered an 18% throughput penalty and increased mean validation loss from 0.0002937 to 0.0003971. Revert immediately to 2-stage Modified PINN (WIDTH = 192) from champion Trial 038.

## Reason for decision

Mean validation loss degraded by 35% across 9 of 10 cases due to computational depth overhead. The 2-stage configuration is structurally optimal and faster.

## Next experiment

Trial 040: Initial Encoder Projection Activation (Linear vs Tanh Encoders in Modified PINN).
In Trial 038, both feature encoder branches were defined as U = tanh(Linear(feats)) and V = tanh(Linear(feats)). In Paris Perdikaris's original formulation, the feature encoders are sometimes linear projections: U = Linear(feats) and V = Linear(feats), leaving all non-linearity to the hidden gating units z_l = tanh(Linear(h_{l-1})). A linear encoder preserves the exact amplitudes of the Fourier features (including large-amplitude swings at low frequencies) without compressing them through the saturating non-linearity of Tanh before gating. We will test linear encoders (U, V without Tanh) vs Tanh encoders to see if preserving uncompressed Fourier amplitudes enhances non-linear phase interpolation. All other settings match champion Trial 038.
