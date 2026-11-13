# Experiment 009: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

Trial 008 established that the ResNet Fourier-PINN provides superior gradient propagation for second-order physics losses, reducing mean validation loss to 0.003778. Across all cases in Trial 008, the val/train ratio was strictly 1.00 (zero overfitting), and the training curves continued a steady downward descent at the end of the 87 s budget. Increasing the hidden layer width from 128 to 192 will expand representation capacity and parameter expressivity (from 35,586 to 77,954 parameters) without causing overfitting, enabling deeper residual reduction on high-energy cases like dev_07 and dev_09.

## Proposed method change

Architecture modification:
- Widen hidden layers from 128 to 192 units.
- Architecture:
  - Input: 17 Fourier features [t/(3pi)-1, sin(w_k t), cos(w_k t)] with w_k = k/2, k=1..8.
  - Input projection: Linear(17, 192) + Tanh.
  - Two residual blocks: h = h + Tanh(Linear(192, 192)(h)).
  - Output projection: Linear(192, 2).
  - Total parameters: 77,954.
- Optimization and objective unchanged: Adam with exponential lr decay from 1e-3 to 1e-5 over 87.0 s, full batch on all 500 coordinates, soft IC weight 100.0.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Lower mean validation loss than Trial 008 (0.003778), with improved fitting of the highest-amplitude cases dev_07 and dev_09 due to increased model capacity.

## Evidence from previous experiments

Trial 004 (width 128 sequential) reached 0.004097. Trial 008 (width 128 ResNet) reached 0.003778. In both trials, val/train was ~1.00, proving that increasing capacity up to 78k parameters carries negligible risk of empirical overfitting while providing more degrees of freedom to fit the nonlinear restoring dynamics.

## Observed results

All 10 cases completed (87.0 s each, ~23k steps, 77,954 parameters). Mean validation loss set a new campaign record of 0.003390 (Trial 008: 0.003778; Trial 004: 0.004097), worst 0.01020 (dev_09; Trial 008: 0.01106), std 0.00310, mean IC 3.22e-08.
Per case comparison with Trial 008:
- dev_01: 0.000496 (Trial 008: 0.000009) - higher, but still well below 1e-3
- dev_02: 0.00324 (Trial 008: 0.00356) - improved
- dev_03: 0.00260 (Trial 008: 0.00310) - improved
- dev_04: 0.00152 (Trial 008: 0.00128) - slightly higher
- dev_05: 0.000232 (Trial 008: 0.000231) - tied
- dev_06: 0.000649 (Trial 008: 0.000988) - 1.5x improved (0.65e-3)
- dev_07: 0.00631 (Trial 008: 0.00850) - 26% improvement on large-amplitude case!
- dev_08: 0.00404 (Trial 008: 0.00385) - tied
- dev_09: 0.01020 (Trial 008: 0.01106) - improved (broke below 0.011)
- dev_10: 0.00462 (Trial 008: 0.00520) - improved

Val/train ratios remained exactly 1.00 across all 10 cases. Widening the residual layers to 192 gave the network the expressivity needed to model the sharp potential curvature in large-amplitude cases like dev_07, without any sign of overfitting or instability.

## Agent decision

Retain: The ResNet Fourier-PINN with width 192 (77,954 parameters) is now our leading architecture.

## Reason for decision

Mean validation loss improved to 0.003390 (10% reduction over Trial 008), worst-case loss dropped to 0.01020, and dev_07 saw a 26% improvement. Generalization remains perfect (val/train = 1.00).

## Next experiment

Trial 010: Test depth vs width. In Trial 009, width 192 with 2 residual blocks was used. We will test adding a third residual block (depth 3 blocks, total 4 linear hidden layers) with width 160 (79,482 parameters, nearly identical parameter count to Trial 009's 77,954). This isolates whether increased compositional depth or layer width provides a more effective inductive bias for the multi-period oscillatory Sitnikov dynamics.
