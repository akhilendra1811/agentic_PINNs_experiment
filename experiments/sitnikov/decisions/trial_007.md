# Experiment 007: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 004 (our best overall result: mean 0.004097, worst 0.01097), the residual was dominated by high-amplitude, high-energy cases dev_09 (0.01097) and dev_07 (0.00930), which have large starting displacements (z0 = 1.25 and 1.49). In the nonlinear Sitnikov potential, larger amplitude oscillations induce significant higher-harmonic components in both z(t) and v(t). Expanding the Fourier bank from 8 frequencies (0.5 to 4.0 rad/s) to 14 frequencies (0.5 to 7.0 rad/s in steps of 0.5) will improve the model's capacity to represent these higher harmonics without causing instability.

## Proposed method change

Revert completely to the stable soft IC architecture of Trial 004, but increase the number of Fourier frequencies:
- Frequencies: w_k = 0.5 * k for k = 1..14 (14 pairs of sin/cos features, spanning 0.5 to 7.0 rad/s).
- Input dimension: 1 + 2 * 14 = 29 features.
- Architecture: 3 hidden layers of width 128 with Tanh activations (37,122 parameters total, well within the 250k limit).
- Optimization: Adam with learning rate decaying exponentially from 1e-3 to 1e-5 over 87.0 s wall-clock budget.
- 11 evenly spaced progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Improved fit on high-amplitude cases dev_09 and dev_07, lowering the worst-case validation loss below 0.010 and bringing mean validation loss below Trial 004's 0.004097. Minimal risk of overfitting as long as the frequency cutoff (7.0 rad/s) remains well below the Nyquist rate of the 500-point collocation grid.

## Evidence from previous experiments

Trial 004 proved that adding 8 Fourier frequencies reduced validation loss by 9x over plain time input with zero generalisation gap (val/train ratio ~ 1.00). In Trial 004, all cases except dev_07 and dev_09 reached losses below 0.005. Trial 006 showed that rigid algebraic hard IC ansatzes cause instability, confirming that soft IC with Fourier features is the robust foundation.

## Observed results

All 10 cases completed (87.0 s each, ~28.2k steps). Mean validation loss was 0.004235 (Trial 004: 0.004097), worst 0.01252 (dev_09; Trial 004: 0.01097), std 0.00390, mean IC 6.2e-08.
Per case comparison with Trial 004:
- dev_01: 0.000524 (Trial 004: 0.000399) - slightly worse
- dev_02: 0.00376 (Trial 004: 0.00417) - slightly improved
- dev_03: 0.00344 (Trial 004: 0.00340) - practically identical
- dev_04: 0.00144 (Trial 004: 0.00148) - practically identical
- dev_05: 0.000215 (Trial 004: 0.000216) - practically identical
- dev_06: 0.00225 (Trial 004: 0.00216) - practically identical
- dev_07: 0.00931 (Trial 004: 0.00930) - practically identical
- dev_08: 0.00414 (Trial 004: 0.00408) - practically identical
- dev_09: 0.01252 (Trial 004: 0.01097) - slightly worse
- dev_10: 0.00475 (Trial 004: 0.00480) - practically identical

Val/train ratios remained ~1.00–1.01 across all cases, confirming good generalization. However, extending the frequency bank from 8 to 14 frequencies did not improve the large-amplitude cases (dev_07 and dev_09) and slightly degraded the worst-case and mean losses.

## Agent decision

Reject the expanded 14-frequency bank and revert to the 8-frequency bank (w_k = 0.5..4.0) of Trial 004.

## Reason for decision

The physical frequencies in the Sitnikov oscillator on [0, 6π] are concentrated below 4 rad/s. Adding high-frequency components up to 7.0 rad/s increased the parameter space without providing useful physical modes, slightly slowing Adam optimization and worsening convergence on dev_09. 8 frequencies is well-matched to the system bandwidth.

## Next experiment

Trial 008: Test Residual Connections (ResNet MLP). In Trial 004, a plain sequential MLP with 3 hidden layers of width 128 was used. The Sitnikov loss requires second-order automatic differentiation through the network (d/dt of v, which itself is an output, and dz/dt which is compared to v). Plain MLPs suffer from gradient attenuation during backpropagation through higher-order graph unrolling. Introducing skip/residual connections across the hidden layers should facilitate gradient flow for second derivatives and accelerate convergence.
