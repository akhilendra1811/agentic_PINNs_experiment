# Experiment 019: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In initial-value problem PINNs, establishing the correct initial phase-space coordinates (z0, v0) early in optimization is vital because errors at t=0 propagate forward across the entire 0..6π trajectory. In Trial 017, a constant IC penalty weight of 100.0 was used throughout training. Early on, this weight allows the network to explore trajectories with non-trivial IC displacement before slowly settling down. Implementing an annealed IC weight schedule—starting at lambda_ic = 1000.0 to decisively pin the initial state during the first 10% of training (frac <= 0.10), then tapering to lambda_ic = 100.0 for the remaining 90% of training:
lambda_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10)
will anchor the initial trajectory early, preventing transient phase drift and enabling cleaner subsequent convergence on the interior ODE dynamics.

## Proposed method change

Training loss schedule modification:
- Architecture: 2-block ResNet Fourier-PINN with width 192, 8 learnable Fourier frequencies, Tanh activations (77,962 parameters, champion architecture from Trial 017).
- Scheduled IC loss weight:
  lambda_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10)
  where f is elapsed fraction of the 87.0 s budget.
- Training loss: L(θ) = physics + lambda_ic(f) * ic.
- Optimization: Adam with Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) is dynamically scheduled as λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10), starting at 1000.0 and decaying linearly to 100.0 over the first 10% of training time, remaining constant at 100.0 thereafter. Full batch on all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate following Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)), where f is elapsed fraction of 87.0 s budget. Gradient updates clipped to maximum L2 norm of 1.0.

## Expected effect

Comparison against Trial 017 (constant IC weight 100.0, mean 0.001181, worst 0.002819). Early IC anchoring should accelerate phase convergence and reduce residual errors across all development cases, potentially breaking mean validation loss below 0.0010.

## Evidence from previous experiments

Trial 017 established 8 learnable frequencies as our champion architecture (mean 0.001181). Progress curves in Trial 017 showed that the first 10% of training experiences the greatest trajectory volatility; stabilizing the t=0 anchor during this volatile initial window addresses the physical root cause of phase drift.

## Observed results

All 10 cases completed (87.0 s each, ~25.6k steps, 77,962 parameters). Mean validation loss broke the landmark sub-1e-3 barrier, achieving a staggering new record of 0.0008855 (Trial 017: 0.001181, a 25% reduction!). The worst-case validation error also dropped below 0.0020 down to 0.001994 (dev_09; Trial 017: 0.002819, a 29.3% reduction!). Std dropped to 0.000742, mean IC 3.79e-10.
Per case comparison with Trial 017 (a clean 10/10 improvement across all development cases):
- dev_01: 6.89e-05 (Trial 017: 7.12e-05) - improved
- dev_02: 0.001040 (Trial 017: 0.001400) - 26% improvement
- dev_03: 0.000867 (Trial 017: 0.001060) - 18% improvement (entered sub-1e-3 range)
- dev_04: 0.000123 (Trial 017: 0.000286) - 57% improvement
- dev_05: 1.39e-06 (Trial 017: 5.18e-06) - 3.7x improvement (reached 1.39 × 10^-6!)
- dev_06: 0.000206 (Trial 017: 0.000269) - 23% improvement
- dev_07: 0.001550 (Trial 017: 0.002210) - 30% improvement
- dev_08: 0.001550 (Trial 017: 0.001860) - 17% improvement
- dev_09: 0.001994 (Trial 017: 0.002819) - 29% improvement (worst case now < 0.002!)
- dev_10: 0.001450 (Trial 017: 0.001820) - 20% improvement

Every single development case without exception now achieves a validation loss strictly below 0.0020. Generalization remains pristine (val/train ~ 1.00–1.05). Annealing the IC loss weight from 1000 down to 100 during the first 10% of training anchored the initial trajectory firmly at t=0 before the network began fitting the full multi-cycle dynamics, completely suppressing early phase drift.

## Agent decision

Retain: Annealed IC loss weighting (1000 -> 100 over first 10% of budget) is enthusiastically retained as an essential component of our champion methodology.

## Reason for decision

A decisive 10/10 improvement across all development cases, driving mean validation error below the 1e-3 milestone to 0.0008855 and cutting the worst-case error under 0.0020. Eliminating early phase-space initialization drift directly accelerates global ODE convergence.

## Next experiment

Trial 020: Collocation Point Subsampling / Mini-Batching. In all trials so far, full-batch gradient descent was performed on all 500 coordinates every single step. In stochastic optimization and PINNs, subsampling subsets of training points (e.g. mini-batches of size 250 randomly drawn from the 500 points at each step) can introduce stochastic gradient noise that helps escape flat saddles, while doubling the iteration throughput (steps per second). We will test mini-batching with batch_size = 250 on our champion Trial 019 method.
