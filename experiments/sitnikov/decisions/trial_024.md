# Experiment 024: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 021, our champion Highway Input Injection architecture with width 192 achieved an all-time best mean validation loss of 0.0008753, with a worst-case error of only 0.001601 and zero generalization gap (val/train ~ 1.00). Expanding the layer width from 192 to 224 increases parameter capacity from 84,490 to 112,906. Width 224 is an exact multiple of 32 (7 * 32), aligning with warp-level SIMD execution units on modern GPUs/MPS. This expanded feature dimension provides a richer latent representation for the concatenated highway skip connections, potentially pushing mean validation loss lower without sacrificing step throughput or causing empirical overfitting.

## Proposed method change

Architecture modification to scale width to 224:
- Increase hidden width from 192 to 224 in `HighwayInputInjectionResNet`.
- Architecture:
  - Input: 17 Fourier features [t/(3pi)-1, sin(wt), cos(wt)] with 8 learnable frequencies (initialized on uniform grid 0.5*k).
  - Initial projection: Linear(17, 224) + Tanh.
  - Two residual blocks with Highway Input Injection:
    `h = h + Tanh(Linear(224 + 17, 224)([h, feats]))`
    `h = h + Tanh(Linear(224 + 17, 224)([h, feats]))`
  - Output projection: Linear(224, 2).
  - Total parameters: 112,906 (< 250k budget).
- Optimization and schedule identical to champion Trial 021: Adam with Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6), gradient norm clipping (max_norm = 1.0), annealed IC loss weight (1000 -> 100 over first 10% of budget), full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10) over first 10% of budget. Adam learning rate follows Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)) over 87.0 s budget. Gradient updates clipped to maximum L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against Trial 021 (width 192, mean 0.0008753, worst 0.001601). If width 224 increases expressive power without overfitting, mean validation loss will decrease below 0.00085.

## Evidence from previous experiments

Progressive width scaling from 48 -> 128 -> 192 consistently reduced validation loss with zero overfitting (val/train ~ 1.00). Testing width 224 directly explores the upper capacity regime for the Highway Input Injection architecture.

## Observed results

All 10 cases completed (87.0 s each, ~20.6k steps, 112,906 parameters). Mean validation loss was 0.001096 (Trial 021: 0.0008753), worst 0.002296 (dev_09; Trial 021: 0.001601), std 0.000864, mean IC 5.38e-10.
Per case comparison with Trial 021 (width 192):
- dev_01: 4.81e-05 (Trial 021: 2.54e-05) - higher
- dev_02: 0.001280 (Trial 021: 0.001601) - 20% improvement
- dev_03: 0.000734 (Trial 021: 0.000717) - practically tied
- dev_04: 0.000141 (Trial 021: 0.000202) - 30% improvement
- dev_05: 2.14e-06 (Trial 021: 3.81e-07) - both in micro/sub-micro range
- dev_06: 0.000883 (Trial 021: 0.000641) - higher
- dev_07: 0.002130 (Trial 021: 0.001310) - higher
- dev_08: 0.001640 (Trial 021: 0.001430) - practically tied
- dev_09: 0.002300 (Trial 021: 0.001270) - higher
- dev_10: 0.001800 (Trial 021: 0.001550) - slightly higher

While dev_02 and dev_04 saw improvements, the larger model suffered an ~18% throughput penalty (~20.6k steps vs ~24.3k steps in Trial 021). The extra 28k parameters in width 224 did not provide additional physical expressivity, and the reduced number of gradient steps slightly impaired convergence on dev_07 and dev_09.

## Agent decision

Reject width 224. Retain width 192 (Trial 021) as our champion width.

## Reason for decision

Width 192 (84,490 parameters) delivers a 25% lower mean validation loss (0.000875 vs 0.001096) and a tighter worst-case error (0.00160 vs 0.00230) due to 18% higher step throughput and optimal parameter compactness.

## Next experiment

Trial 025: Linear Learning Rate Warmup. In all trials so far, training started immediately at the peak learning rate (1e-3) at step 1 when Adam's first and second moment estimates (m and v) are uninitialized (zeros). Early physics residuals are huge (~50–150), causing initial gradient updates to make uncalibrated parameter jumps before running statistics stabilize. We will test adding a 5% linear warmup phase (from 1e-4 to 1e-3 over the first 5% of training time, ~4.3 s), followed by Cosine Annealing from 1e-3 down to 1e-6 over the remaining 95% of the budget, on our champion width 192 Highway Input Injection architecture.
