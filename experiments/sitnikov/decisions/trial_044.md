# Experiment 044: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 015, we introduced gradient norm clipping with $\text{max\_norm} = 1.0$, which delivered an immediate 26% reduction in validation error by truncating occasional gradient spikes. In our champion Modified PINN architecture (Trial 038, mean 0.0002937), the multiplicative gating structure ($h_l = (1 - z_l) \odot U + z_l \odot V$) naturally normalizes hidden activations, and the domain-orthogonal Fourier frequencies ($\omega_k = k/3$) eliminate artificial boundary gradient explosions.

However, during the initial 20% of training when the initial condition weight is scheduled at $\lambda_{ic} = 2000.0$, the gradient norm frequently approaches or exceeds 1.0 due to the high penalty on origin anchoring. When these large gradients pass through the Adam optimizer, they can cause subtle parameter overshoots along narrow curvature directions before the gating units learn their primary phase-switching alignment.

Tightening the gradient clipping threshold to $\text{max\_norm} = 0.5$ will constrain parameter updates to a strictly bounded trust radius during early training, preventing transient phase distortions and enabling a smoother descent into the optimal trajectory basin.

## Proposed method change

Optimizer configuration modification:
- Change `MAX_GRAD_NORM = 0.5` (down from 1.0).
- Revert `WIDTH = 192` (84,874 parameters, identical to champion Trial 038).
- Two gating stages ($z_1, z_2$) with symmetric Tanh encoders.
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Loss weighting: Asymmetric IC annealing from Trial 034/038 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 0.5. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 038 (mean 0.0002937, worst 0.0008230). A tighter clipping threshold of 0.5 should suppress early phase overshoots during high-IC annealing, targeting mean validation loss below 0.00027 and compressing worst-case error toward 0.00070.

## Evidence from previous experiments

Trial 015 proved that clipping to 1.0 was universally beneficial across all 10 cases. With the Modified PINN's normalized architecture and reduced terminal IC drag, evaluating max_norm = 0.5 tests whether tighter trust-region regularization improves asymptotic convergence.

## Observed results

All 10 development cases completed (87.0 s each, ~20.9k steps, 84,874 parameters). Tightening the gradient clipping norm to 0.5 produced a stellar across-the-board advance:
- Mean validation loss set an all-time campaign record of 0.0002853 (Trial 038: 0.0002937, a further 2.9% reduction).
- Worst-case validation loss improved from 0.0008230 to 0.0007889 (dev_08, a 4.1% improvement).
- Standard deviation across the 10 cases compressed to an all-time low of 0.000254.
- Several individual cases reached historic high-water marks:
  - dev_03: 0.000191 (Trial 038: 0.000230) - broke the sub-2e-4 barrier!
  - dev_04: 8.69e-06 (Trial 038: 2.18e-05) - 60% error reduction to single-digit micro-precision!
  - dev_05: 8.34e-09 (Trial 038: 1.48e-08) - single-digit nano-scale precision (8.34 × 10^-9!)
  - dev_08: 0.000789 (Trial 038: 0.000823) - solid worst-case compression
  - dev_10: 0.000442 (Trial 038: 0.000513) - 14% improvement
- All 10 cases now achieve validation loss strictly below 0.00079:
  - dev_01: 3.39e-06
  - dev_02: 0.000398
  - dev_03: 0.000191
  - dev_04: 8.69e-06
  - dev_05: 8.34e-09
  - dev_06: 0.000323
  - dev_07: 0.000479
  - dev_08: 0.000789
  - dev_09: 0.000218
  - dev_10: 0.000442
- Generalization was immaculate: val/train ratio was 1.00 on all 10 cases; mean IC loss was 9.88e-09.

Physical and optimization explanation: In bilinear architectures with multiplicative gating, parameter updates that exceed a critical trust radius can disrupt the phase synchronization between the dual encoders ($U, V$) and the gating switches ($z$). When the initial condition loss is high ($\lambda_{ic} = 2000$), unclipped or loosely clipped gradient spikes (norms between 0.5 and 1.0) can push gating weights into premature saturation. Capping the gradient norm at 0.5 acts as a disciplined trust-region constraint, ensuring that the gating layers undergo smooth, non-oscillatory rotation into their optimal physical subspaces.

## Agent decision

Retain: MAX_GRAD_NORM = 0.5 is enthusiastically retained as our new campaign champion configuration.

## Reason for decision

Mean validation loss reached a new all-time low (0.0002853), worst-case error compressed to 0.000789, standard deviation shrank to 0.000254, and dev_04 achieved a 60% reduction into single-digit micro-precision.

## Next experiment

Trial 045: Initial Condition Annealing Horizon Refinement (Testing frac <= 0.25 vs 0.20).
In Trial 034, extending the initial IC weight annealing window from 15% to 20% of training time dropped mean loss by 19% by giving the network enough time to anchor the complete first orbital period. In high-eccentricity cases with large initial amplitudes (e.g. dev_08: z0=1.5), the anharmonic orbital period is significantly longer ($T > 2\pi / \omega_0 \approx 8.9 \implies$ nearly half the total domain). Extending the IC annealing horizon slightly from 20% to 25% of training time (frac <= 0.25, ~21.75 seconds) ensures that even the most elongated orbits have completed a full period under the high-confidence origin anchor before the IC weight relaxes down to 10.0. All other settings match champion Trial 044 (Modified PINN, width 192, max_norm = 0.5).
