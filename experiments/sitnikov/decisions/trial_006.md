# Experiment 006: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trials 001–005, initial conditions were softly enforced through an IC penalty term 100 * ((z(0)-z0)^2 + (v(0)-v0)^2). Although the resulting soft IC error was small, gradient signals from the IC penalty compete with the interior collocation physics residuals, especially early in training. By enforcing exact hard initial conditions directly through the architecture:
z(t) = z0 + (1 - exp(-t)) * v0 + (1 - exp(-t))^2 * N_z(t)
v(t) = v0 + (1 - exp(-t)) * N_v(t)
both z(0) = z0, v(0) = v0, and dz/dt(0) = v0 are satisfied identically by construction. This eliminates the IC loss term completely (IC error = 0), allowing the optimizer to dedicate 100% of gradient updates to satisfying the governing differential equation throughout the interval [0, 6π].

## Proposed method change

Architecture modification:
- Embed known initial conditions (z0, v0) from `case` directly into the model forward pass.
- Let phi(t) = 1 - exp(-t).
- Output representation:
  z(t) = z0 + phi(t) * v0 + (phi(t)^2) * N_z(t)
  v(t) = v0 + phi(t) * N_v(t)
  where [N_z(t), N_v(t)] is produced by a 3x128 tanh MLP on Fourier features [t/(3pi)-1, sin(w_k t), cos(w_k t)] with w_k = k/2 for k=1..8 (35,586 parameters).
- Training schedule: Pure Adam optimizer with learning rate exponentially decaying from 1e-3 to 1e-5 over the 87 s wall-clock budget.
- 11 time-spaced progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points from `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2 (which evaluates to 0.0 identically due to the hard constraint).
Coefficients: physics weight 1.0, IC weight 100.0 (constant). Full batch of all 500 training coordinates every step, no curriculum, no case-specific weighting. Learning rate schedule: lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Zero IC loss (evaluator metric val_ic = 0.0), reduced physics residual across development cases, and potentially lower mean validation loss than Trial 004 (0.004097) by removing boundary-interior gradient conflict.

## Evidence from previous experiments

Trial 004 demonstrated that Fourier features and 3x128 width drop validation loss by 9x over plain MLP (mean 0.0041 vs 0.0365). Trial 005 revealed that L-BFGS is prone to line-search stalling in float32, making smooth Adam scheduling preferable. Hard IC constraints guarantee consistency at t=0 and free the network capacity to focus on the interior ODE residual.

## Observed results

All 10 cases completed (87.0 s training each). Mean validation loss degraded severely to 0.3570 (Trial 004: 0.004097) with a catastrophic worst case of 3.2160 (dev_08; Trial 004: 0.01097), std 1.01, mean IC loss 0.0 (strictly 0 by construction).
Per case:
- dev_01: 0.000241 (Trial 004: 0.000399) - improved
- dev_02: 0.0238 (Trial 004: 0.00417) - worse
- dev_03: 0.0308 (Trial 004: 0.00340) - worse
- dev_04: 0.1440 (Trial 004: 0.00148) - 100x worse, val/train ratio 2.73
- dev_05: 0.000108 (Trial 004: 0.000216) - 2x improved
- dev_06: 0.1050 (Trial 004: 0.00216) - 50x worse, re-collapsed to escape mode
- dev_07: 0.00758 (Trial 004: 0.00930) - improved
- dev_08: 3.2160 (Trial 004: 0.00408) - catastrophic blow-up, val/train ratio 36,394
- dev_09: 0.00319 (Trial 004: 0.01097) - 3.4x improved
- dev_10: 0.0397 (Trial 004: 0.00480) - 8x worse

In dev_08, training loss reached an extraordinarily low 8.8e-5, but validation loss blew up to 3.22. Prediction plots reveal that the quadratic-damping ansatz z(t) = z0 + phi*v0 + phi^2*Nz forced a rapid acceleration away from the plane early on, causing the trajectory to escape to z ~ 4.0 (where gravitational restoring forces are weak). The network overfit the discrete training points with high inter-sample curvature, leading to a massive generalization gap on the validation grid.

## Agent decision

Reject this hard IC ansatz completely. The soft IC formulation used in Trial 004 remains vastly superior in preserving global physical stability across all cases.

## Reason for decision

While hard IC enforcement achieved lower residuals on four cases (dev_01, 05, 07, 09), it induced severe physical instability, catastrophic escape modes, and collocation overfitting on dev_04, dev_06, dev_08, and dev_10. For second-order oscillatory systems, rigid algebraic IC damping often distorts the initial phase space gradient landscape.

## Next experiment

Trial 007: Return to the stable soft IC formulation of Trial 004. In Trial 004, the worst cases were dev_09 (0.011) and dev_07 (0.0093), which have the highest oscillation frequencies and largest initial displacement amplitudes (z0 = 1.25 and 1.50). We will test expanding the Fourier frequency bank from 8 frequencies (w_k = 0.5..4.0) to 14 frequencies (w_k = 0.5..7.0) with step 0.5 to better capture the higher harmonic content of large-amplitude nonlinear Sitnikov oscillations.
