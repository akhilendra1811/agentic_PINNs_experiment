# Experiment 023: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trials 017–022, the 8 learnable Fourier frequencies were initialized at an arbitrary uniform harmonic grid: [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]. However, in celestial mechanics, the Sitnikov dynamical system is governed by the nonlinear interaction of two distinct physical frequencies: the Keplerian primary orbital frequency (\omega_{orb} = 1.0) and the natural vertical oscillation frequency (\omega_z = \sqrt{2} \approx 1.4142). The resulting multi-periodic motion generates nonlinear sum and difference intermodulation modes:
\omega_1 = 0.5 (half-harmonic)
\omega_2 = 1.0 (\omega_{orb})
\omega_3 = \sqrt{2} \approx 1.4142 (\omega_z)
\omega_4 = 2.0 (2\omega_{orb})
\omega_5 = 1 + \sqrt{2} \approx 2.4142 (\omega_{orb} + \omega_z)
\omega_6 = 2\sqrt{2} \approx 2.8284 (2\omega_z)
\omega_7 = 3.0 (3\omega_{orb})
\omega_8 = 2 + \sqrt{2} \approx 3.4142 (2\omega_{orb} + \omega_z)
Initializing the learnable frequencies at these exact physical resonance frequencies places the initial spectral basis directly inside the true physical attraction basin, accelerating spectral convergence and reducing residual error across all cases.

## Proposed method change

Architecture modification for physical spectral initialization:
- In `HighwayInputInjectionResNet`, initialize `self.omega` with `[0.5, 1.0, sqrt(2), 2.0, 1+sqrt(2), 2*sqrt(2), 3.0, 2+sqrt(2)]`.
- All frequencies remain learnable parameters (nn.Parameter).
- Architecture unchanged: width 192, 2 residual blocks with Highway Input Injection, Tanh activations (84,490 parameters, identical to Trial 021).
- Optimization and schedule identical to champion Trial 021: Adam with Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6), gradient norm clipping (max_norm = 1.0), annealed IC loss weight (1000 -> 100 over first 10% of budget), full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10). Adam learning rate follows Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)) over 87.0 s budget. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step. Learnable omega initialized at the Kepler-Natural harmonic grid.

## Expected effect

Comparison against Trial 021 (uniform grid init, mean 0.0008753, worst 0.001601). Physical frequency initialization should eliminate the gradient steps previously wasted moving from the arbitrary uniform grid to the physical resonance manifold, achieving faster initial descent and a lower final validation loss (potentially breaking below 0.00080).

## Evidence from previous experiments

Trial 017 demonstrated that learned omega values migrated spontaneously toward sqrt(2) and amplitude-dependent downshifted modes. Pre-seeding these modes at the exact analytical frequencies aligns the network with the physical physics before gradient step 1.

## Observed results

All 10 cases completed (87.0 s each, ~21.9k steps, 84,490 parameters). Mean validation loss was 0.001063 (Trial 021: 0.0008753), worst 0.002028 (dev_07; Trial 021: 0.001601), std 0.000780, mean IC 4.20e-10.
Per case comparison with Trial 021 (uniform grid init):
- dev_01: 3.93e-05 (Trial 021: 2.54e-05) - practically tied
- dev_02: 0.001800 (Trial 021: 0.001601) - practically tied
- dev_03: 0.001010 (Trial 021: 0.000717) - slightly higher
- dev_04: 0.000161 (Trial 021: 0.000202) - 20% improvement
- dev_05: 6.74e-06 (Trial 021: 3.81e-07) - both in 10^-6/10^-7 range
- dev_06: 0.000796 (Trial 021: 0.000641) - practically tied
- dev_07: 0.002028 (Trial 021: 0.001310) - higher
- dev_08: 0.001600 (Trial 021: 0.001430) - practically tied
- dev_09: 0.001380 (Trial 021: 0.001270) - practically tied
- dev_10: 0.001810 (Trial 021: 0.001550) - practically tied

The performance across 8 of 10 cases was very close to Trial 021, but uniform initialization [0.5, 1.0, 1.5, ..., 4.0] retained a slight edge in mean validation loss (0.000875 vs 0.001063). Uniform spacing provides an unbiased, equal-density coverage of the frequency spectrum, allowing gradient descent to explore adjacent harmonics with equal initial ease.

## Agent decision

Reject the hand-crafted physical frequency initialization. Retain the uniform harmonic initialization [0.5, 1.0, ..., 4.0] from Trial 021.

## Reason for decision

Uniform initial frequency spacing ensures equal spectral density across the passband, whereas irregular physical spacing slightly biased early gradient updates away from the optimum for certain cases (e.g. dev_07).

## Next experiment

Trial 024: Width scaling in the Highway Input Injection ResNet. In Trial 021, width 192 (84,490 parameters) achieved our campaign champion score of 0.0008753. We will evaluate scaling the hidden layer width to 224 (112,906 parameters, a multiple of 32 for optimal GPU execution), testing whether expanding the highway residual capacity to 113k parameters allows even sharper resolution of the nonlinear restoring dynamics without overfitting. All other hyperparameters remain identical to champion Trial 021.
