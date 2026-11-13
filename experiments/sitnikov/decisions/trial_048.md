# Experiment 048: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trials 046 and 047, increasing Adam's first-moment decay factor from $\beta_1 = 0.90$ to $0.95$ and then to $0.97$ delivered two consecutive 58% error drops, collapsing mean validation loss from 0.0002853 to 0.00005114 (5.11e-5). This remarkable progression demonstrated that continuous PINN ODE collocation benefits profoundly from low-pass momentum filtering to cancel cross-ravine gradient oscillations.

Testing $\beta_1 = 0.98$ pushes this momentum horizon to:
$\tau_1 = \frac{1}{1 - 0.98} = 50 \text{ steps}$
which corresponds to approximately 2.5 seconds of training time. At $\beta_1 = 0.98$, the first-moment memory window encompasses half of the second-moment window ($\tau_2 = 100$ steps for $\beta_2 = 0.99$). We hypothesize that this extended 50-step memory will either:
1. Provide even deeper along-ravine velocity integration, potentially pushing mean validation loss below $3.0 \times 10^{-5}$; OR
2. Reveal the fundamental physical limit of momentum smoothing, where 50 steps of directional inertia begins to overshoot sharp, localized curvature bends around primary pericenter passages (particularly in high-eccentricity cases dev_07, dev_08, dev_09).

## Proposed method change

Optimizer configuration modification:
- Change Adam betas from `(0.97, 0.99)` to `(0.98, 0.99)`.
- Architecture: Modified PINN with width 192, 2 gating stages, symmetric Tanh encoders (84,874 parameters, identical to Trial 047).
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Loss weighting: Asymmetric IC annealing from Trial 034/047 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.98, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 0.5) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.98, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 0.5. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 047 (mean 5.114e-05, worst 0.0001229). Testing whether a 50-step momentum memory accelerates ravine progress to break into the sub-3e-5 regime, or identifies the exact turning-point inertia ceiling.

## Evidence from previous experiments

Trials 046 ($\beta_1 = 0.95$) and 047 ($\beta_1 = 0.97$) demonstrated enormous, monotonic gains from momentum extension. Evaluating $\beta_1 = 0.98$ pinpoints the global optimum of the momentum parameter.

## Observed results

All 10 development cases completed without incident (87.0 s each, ~20.0k steps, 84,874 parameters). Increasing momentum to beta1 = 0.98 delivered another staggering leap forward, breaking the sub-1e-4 barrier across ALL ten cases:
- Mean validation loss dropped to an all-time record of 3.024e-05 (0.00003024), a further 40.9% error reduction from Trial 047!
- Worst-case validation loss across the entire 10-case benchmark broke the sub-1e-4 threshold, collapsing to 8.373e-05 (dev_08, 8.37 × 10^-5, a 31.9% reduction from Trial 047!).
- Every single one of the 10 development cases is now strictly below 8.4e-5:
  - dev_01: 9.18e-09 (single-digit nanoscale: 9.18 × 10^-9!)
  - dev_02: 2.61e-05 (Trial 047: 6.61e-05, a 60.5% reduction!)
  - dev_03: 5.69e-06 (Trial 047: 1.72e-05, a 67% reduction into single-digit micro-precision!)
  - dev_04: 3.20e-08 (Trial 047: 6.24e-07, a 19.5x reduction to sub-50 nanolevel!)
  - dev_05: 3.80e-09 (3.80 × 10^-9, campaign-best precision!)
  - dev_06: 6.09e-05 (Trial 047: 0.000123, a 50% reduction!)
  - dev_07: 4.74e-05 (Trial 047: 6.10e-05, a 22% reduction!)
  - dev_08: 8.37e-05 (Trial 047: 0.000118, a 29% reduction on our toughest bottleneck!)
  - dev_09: 1.04e-05 (Trial 047: 2.08e-05, a 50% reduction!)
  - dev_10: 6.81e-05 (Trial 047: 0.000105, a 35% reduction!)
- Standard deviation shrank to 3.21e-05.
- Mean IC loss settled at 1.42e-09, contributing only 1.42e-07 to validation score.
- Generalization was immaculate: val/train ratio was 1.00 on all 10 cases.

Physical and optimization explanation: A 50-step momentum horizon (beta1 = 0.98) acts as an exceptional spatial-temporal low-pass filter. Because the training coordinates t_i span the full integration interval [0, 6π], gradient updates from different collocation points contribute opposing high-frequency orthogonal forces to the neural network weights. Over a 50-step moving window, these mutually antagonistic force perturbations average out to virtually zero, while the shared, low-frequency gravitational trajectory consensus reinforces itself coherently. Rather than encountering directional inertia overshoots, the combination of trust-region clipping (max_norm = 0.5) and 50-step momentum keeps the optimizer tracking the exact physical Hamiltonian trajectory with unparalleled fidelity.

## Agent decision

Retain: BETAS = (0.98, 0.99) is enthusiastically retained as our undisputed new campaign champion.

## Reason for decision

Mean validation loss plummeted by 40.9% to 3.024e-05, all 10 cases broke the sub-1e-4 threshold (worst case 8.37e-5), and every single development case improved.

## Next experiment

Trial 049: Testing Momentum Saturation (Adam beta1 = 0.99 vs 0.98).
With beta1 = 0.98 delivering a mean of 3.024e-05, testing beta1 = 0.99 pushes the momentum memory horizon to tau_1 = 1 / (1 - 0.99) = 100 steps (~5 seconds of training time). Notice that at beta1 = 0.99 and beta2 = 0.99, the first-moment memory horizon matches the second-moment memory horizon exactly (tau_1 = tau_2 = 100 steps). We hypothesize that this experiment will test the absolute upper limit of momentum smoothing: whether 100 steps of momentum provides even deeper signal-to-noise amplification, or if equalizing tau_1 with tau_2 causes lag when tracking dynamic loss landscape shifts. All other settings match champion Trial 048.
