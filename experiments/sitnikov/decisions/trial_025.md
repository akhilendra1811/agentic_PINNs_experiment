# Experiment 025: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

At step 1 of training, network weights are freshly initialized, learnable frequencies omega are at their default positions, and Adam's running moment estimates (m and v) are completely zeroed. Concurrently, initial ODE residuals are large (~50–150). Starting optimization immediately at peak learning rate (1e-3) causes early gradient steps to take uncalibrated steps before Adam's second-moment bias correction stabilizes. Adding a 5% linear warmup phase (from 1e-4 to 1e-3 over the first ~4.3 s) allows Adam to populate accurate running gradient variances under gentle step sizes. Once moments are established, Cosine Annealing takes over from 1e-3 down to 1e-6, preventing early parameter shock and improving terminal convergence.

## Proposed method change

Optimization modification for linear learning rate warmup:
- Warmup schedule:
  For f < 0.05: lr(f) = 1e-4 + (1e-3 - 1e-4) * (f / 0.05)
  For f >= 0.05: lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * (f - 0.05) / 0.95))
  where f is elapsed fraction of 87.0 s budget.
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 learnable Fourier frequencies, Tanh activations (84,490 parameters, identical to Trial 021).
- Gradient norm clipping: max_norm = 1.0.
- Annealed IC loss weight: lambda_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10).
- Objective: L(θ) = physics + lambda_ic * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10) over first 10% of budget. Adam learning rate follows a 5% linear warmup (1e-4 to 1e-3) followed by Cosine Annealing (1e-3 to 1e-6) over 87.0 s budget. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against Trial 021 (no warmup, mean 0.0008753, worst 0.001601). Warmup should smooth the initial 1000 steps, preventing destabilization of early learnable frequency parameters and yielding a lower mean validation loss.

## Evidence from previous experiments

Trial 021 achieved our current champion result (0.0008753), but snapshot 1 notes show large initial losses (~5–40). Stabilizing the earliest optimization phase has consistently paid dividends across this campaign (as seen with gradient clipping in Trial 015 and annealed IC in Trial 019).

## Observed results

All 10 cases completed (87.0 s each, ~21.5k steps, 84,490 parameters). Mean validation loss was 0.001007 (Trial 021: 0.0008753), worst 0.002023 (dev_09; Trial 021: 0.001601), std 0.000761, mean IC 4.51e-10.
Per case comparison with Trial 021 (no warmup):
- dev_01: 4.55e-05 (Trial 021: 2.54e-05) - higher
- dev_02: 0.001040 (Trial 021: 0.001601) - 35% improvement!
- dev_03: 0.000980 (Trial 021: 0.000717) - slightly higher
- dev_04: 0.000153 (Trial 021: 0.000202) - 24% improvement
- dev_05: 2.92e-06 (Trial 021: 3.81e-07) - both in sub-micro range
- dev_06: 0.000796 (Trial 021: 0.000641) - slightly higher
- dev_07: 0.001930 (Trial 021: 0.001310) - higher
- dev_08: 0.001680 (Trial 021: 0.001430) - slightly higher
- dev_09: 0.002023 (Trial 021: 0.001270) - higher
- dev_10: 0.001420 (Trial 021: 0.001550) - practically tied

While warmup improved dev_02 (0.00104) and dev_04 (0.00015), overall mean loss was ~15% higher than Trial 021 (0.001007 vs 0.0008753). In our 87-second budget, the first 5% (~4.3 s, ~1,200 steps) spent at lower learning rates delayed initial gross descent toward the attraction basin, leaving less effective time for deep terminal convergence under the Cosine Annealing tail. Gradient clipping (max_norm = 1.0) already provides robust protection against uncalibrated early steps without requiring learning rate suppression.

## Agent decision

Reject linear warmup. Retain immediate full peak learning rate (lr0 = 1e-3) with gradient norm clipping from Trial 021.

## Reason for decision

Immediate peak learning rate at step 1 capitalizes on the early high-gradient phase to rapidly clear gross residual errors, with gradient clipping preventing destabilization.

## Next experiment

Trial 026: Adam Second-Moment Timescale Investigation (beta2 = 0.99 vs default 0.999). Default Adam uses beta2 = 0.999, which computes a moving average of squared gradients over an effective window of 1/(1-0.999) = 1000 steps. In the Sitnikov problem, as the network navigates distinct phase-space regimes (e.g. periastron passage where primary bodies are close vs apastron where they are far), local gradient magnitudes fluctuate rapidly. Setting beta2 = 0.99 shortens the memory window to 100 steps, allowing the diagonal preconditioner to adapt 10x faster to localized curvature changes along the trajectory. We will test Adam with betas = (0.9, 0.99) on champion Trial 021.
