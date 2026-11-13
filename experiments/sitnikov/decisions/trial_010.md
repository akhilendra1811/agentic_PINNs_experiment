# Experiment 010: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 009, increasing model capacity via layer width (width 192, 2 residual blocks, 77,954 parameters) lowered mean validation loss to 0.003390. For multi-frequency nonlinear dynamical systems spanning 0..6π, deeper composition can capture progressive phase shifts and harmonic interactions across multiple orbital revolutions more efficiently than wider shallow networks at matched parameter counts. Testing a 3-residual-block architecture with width 160 (80,482 parameters) will isolate the effect of compositional depth versus layer width at matched parameter budgets.

## Proposed method change

Architecture modification to test greater depth at matched parameters:
- Architecture:
  - Input: 17 Fourier features [t/(3pi)-1, sin(w_k t), cos(w_k t)] with w_k = k/2, k=1..8.
  - Input projection: Linear(17, 160) + Tanh.
  - Three residual blocks (increased depth):
    h = h + Tanh(Linear(160, 160)(h))
    h = h + Tanh(Linear(160, 160)(h))
    h = h + Tanh(Linear(160, 160)(h))
  - Output projection: Linear(160, 2).
  - Total parameters: 80,482 (matched to Trial 009's 77,954 within 3%).
- Optimization and objective unchanged: Adam with lr decaying exponentially from 1e-3 to 1e-5 over 87.0 s, full batch on all 500 coordinates, soft IC weight 100.0.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

If hierarchical depth is advantageous for capturing multi-cycle phase accumulation, the 3-block network should achieve lower mean validation loss than Trial 009 (0.003390), particularly on cases with many oscillations (dev_01, dev_05, dev_06). If layer width is more critical for multi-frequency Fourier projection, Trial 009's 2-block wider structure will perform better.

## Evidence from previous experiments

Trial 008 (width 128, 2 blocks, 35k params) reached 0.003778. Trial 009 (width 192, 2 blocks, 78k params) reached 0.003390. This matched-parameter experiment cleanly tests the depth axis of the architectural search space.

## Observed results

All 10 cases completed (87.0 s each, ~20k steps, 80,482 parameters). Mean validation loss was 0.003799 (Trial 009: 0.003390), worst 0.01094 (dev_09; Trial 009: 0.01020), std 0.00310, mean IC 1.29e-08.
Per case comparison with Trial 009 (width 192, 2 blocks):
- dev_01: 0.000528 (Trial 009: 0.000496) - slightly higher
- dev_02: 0.00410 (Trial 009: 0.00324) - worse
- dev_03: 0.00382 (Trial 009: 0.00260) - worse
- dev_04: 0.00140 (Trial 009: 0.00152) - slightly improved
- dev_05: 0.000254 (Trial 009: 0.000232) - practically tied
- dev_06: 0.00262 (Trial 009: 0.000649) - 4x worse!
- dev_07: 0.00582 (Trial 009: 0.00631) - slightly improved
- dev_08: 0.00373 (Trial 009: 0.00404) - slightly improved
- dev_09: 0.01094 (Trial 009: 0.01020) - worse
- dev_10: 0.00478 (Trial 009: 0.00462) - slightly higher

The 3-block architecture achieved 20,004 steps in 87 s (vs 23,143 in Trial 009, ~15% throughput penalty). Wider 2-block architecture decisively outperformed the narrower 3-block architecture on 7 of 10 cases, notably on dev_06 (0.00065 vs 0.00262).

## Agent decision

Reject the 3-block depth increase. Retain the 2-block ResNet structure from Trial 009 as our preferred architectural topology.

## Reason for decision

At matched parameter budgets (~80k), layer width provides greater benefit than network depth for projecting and recombining Fourier frequency modes in the Sitnikov problem. Furthermore, the 2-block network computes 15% more gradient steps per second.

## Next experiment

Trial 011: Retaining the 2-block ResNet architecture of Trial 009, test further widening to width 256. At width 256 with 2 residual blocks:
Input: 17 * 256 + 256 = 4,608
Res1: 256 * 256 + 256 = 65,792
Res2: 256 * 256 + 256 = 65,792
Out: 256 * 2 + 2 = 514
Total params: 136,706 (still well within the 250k limit).
We will evaluate whether expanding the parallel projection subspace to 256 units further reduces mean and worst-case validation error.
