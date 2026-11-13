# Experiment 037: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In all trials since Trial 014, the terminal learning rate floor for Cosine Annealing has been fixed at $lr_1 = 1.0 \times 10^{-6}$. In Trial 022, we tested raising this floor to $1.0 \times 10^{-5}$ and observed that it caused terminal parameter jitter, degrading performance and confirming that lower terminal learning rates are beneficial.

In Trial 034, our champion configuration (mean validation loss 0.0003971) showed that for all 10 development cases, validation error was strictly monotonically decreasing through snapshots 10, 11, and 12, indicating that the network was still descending into the local curvature minimum when the 87.0 s budget ended. Under Adam optimization with $\beta_2 = 0.99$, the coordinate-wise update step size is $\Delta \theta_i \approx \frac{\eta}{\sqrt{v_t} + \epsilon} m_t$. With $\eta = 1.0 \times 10^{-6}$, the effective parameter step size can still exceed $10^{-5}$ for parameters with small gradient variance, which can prevent the weights from settling at the exact bottom of the steep ODE loss valley.

Lowering the terminal learning rate floor by one order of magnitude to $lr_1 = 1.0 \times 10^{-7}$ will provide an ultra-fine convergence tail during the final 5% of training ($f \in [0.95, 1.0]$), allowing the optimizer to freeze in optimal curvature alignments without perturbing delicate phase relationships.

## Proposed method change

Optimizer learning rate schedule modification:
- Change `LR1 = 1e-7` (down from 1e-6). `LR0 = 1e-3` remains unchanged.
  `lr = LR1 + 0.5 * (LR0 - LR1) * (1.0 + math.cos(math.pi * frac))`
- Revert Trial 036 output bias initialization back to default unbiased initialization (`self.out_proj = nn.Linear(WIDTH, 2)`).
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 domain-orthogonal learnable Fourier frequencies (ω_k = k / 3.0), single-layer unscaled residual branches, Tanh activations (84,490 parameters, identical to Trial 034).
- Loss weighting: Asymmetric IC annealing from Trial 034 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-7, gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-7. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 034 (mean 0.0003971, worst 0.0008162). Lowering the learning rate floor to 1e-7 should allow deeper terminal settling during the final seconds of training, targeting mean validation loss below 0.00037.

## Evidence from previous experiments

Trial 022 demonstrated that raising the floor to 1e-5 degraded results due to parameter jitter. Trial 034 showed that the loss curves were still sloping downwards at the final snapshot, suggesting that further damping terminal step size will improve asymptotic convergence.

## Observed results

All 10 development cases completed (87.0 s each, ~23.1k steps, 84,490 parameters). Lowering the learning rate floor to lr1 = 1.0e-7 produced mixed results with an overall net degradation:
- Mean validation loss increased to 0.0004444 (Trial 034: 0.0003971, an 11.9% degradation).
- Worst-case validation loss increased from 0.0008162 (dev_08 in Trial 034) to 0.0009133 (dev_10 in Trial 037).
- Although certain high-eccentricity cases achieved stellar gains (dev_09 plummeted from 0.000674 to 0.000194, a 71% improvement, and dev_07 improved to 0.000474), cases dev_02 and dev_06 suffered severe stalling:
  - dev_02: 0.000880 vs 0.000273 in Trial 034 (3.2x worse)
  - dev_06: 0.000790 vs 0.000249 in Trial 034 (3.2x worse)
  - dev_04: 7.98e-05 vs 3.59e-05 in Trial 034 (2.2x worse)
  - dev_01: 1.00e-05 vs 9.93e-06 in Trial 034 (tied)
  - dev_03: 0.000397 vs 0.000381 in Trial 034 (tied)
  - dev_07: 0.000474 vs 0.000761 in Trial 034 (38% improvement)
  - dev_08: 0.000704 vs 0.000816 in Trial 034 (14% improvement)
  - dev_09: 0.000194 vs 0.000674 in Trial 034 (71% improvement)

Physical and optimization explanation: Dropping the learning rate floor to 1e-7 causes the step size to drop below 1e-7 in the final 5-10% of training. On cases where the network was actively descending a gentle gradient slope towards its global minimum (such as dev_02, dev_04, and dev_06), the parameter updates prematurely froze before reaching the bottom of the basin. The floor lr1 = 1.0e-6 maintains sufficient gradient drift to allow continuous descent throughout the entire 87.0 s budget without premature freezing.

## Agent decision

Reject: lr1 = 1e-7 causes premature parameter freezing on moderate-eccentricity cases, increasing mean validation error from 0.0003971 to 0.0004444. Revert to lr1 = 1e-6 from champion Trial 034.

## Reason for decision

Mean validation loss degraded by 11.9% and worst case increased from 0.000816 to 0.000913 due to premature optimization stalling. The lr1 = 1e-6 floor strikes the ideal balance between terminal stability and ongoing descent.

## Next experiment

Trial 038: Paris Perdikaris Modified PINN Architecture (Multiplicative Encoder Gating).
In Trial 021, we introduced Highway Input Injection (concatenating feats to each residual block). In pioneering PINN literature, Wang, Teng & Perdikaris (SIAM SISC 2021) introduced the Modified MLP: two feature encoder projections U = tanh(Linear(feats)) and V = tanh(Linear(feats)) are computed, and each hidden layer is gated via point-wise convex combination:
h_l = (1 - z_l) * U + z_l * V, where z_l = tanh(Linear(h_{l-1})).
This multiplicative gating structure mathematically bounds hidden gradients, eliminates gradient pathologies across deep networks, and allows the network to dynamically switch harmonic frequency content across layers. We will construct a 2-block Modified PINN with width 192 (84,874 parameters), preserving our domain-orthogonal basis (ω_k = k/3) and champion IC schedule (2000 -> 10 over 20%, Adam betas=(0.9, 0.99), lr0=1e-3, lr1=1e-6).
