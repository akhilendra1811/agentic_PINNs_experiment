# Experiment 022: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trials 014–021, Cosine Annealing decayed to a terminal learning rate floor of lr1 = 1.0e-6. While a floor of 1e-6 prevents parameter oscillation at the end of training, it reduces the step size by three orders of magnitude during the final 10–15 seconds (f > 0.85). In smooth PINN optimization where the residual landscape is quadratic near a local minimum, a learning rate of 1e-6 can become too small to overcome finite numerical gradient precision, prematurely freezing parameter updates. Raising the terminal learning rate floor from 1e-6 to 1e-5:
lr(f) = 1e-5 + 0.5 * (1e-3 - 1e-5) * (1 + cos(pi * f))
will maintain sufficient parameter mobility in the final phase of training, potentially allowing the network to descend further down the residual valley before time expires.

## Proposed method change

Optimization modification for learning rate floor:
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 learnable Fourier frequencies, Tanh activations (84,490 parameters, identical to Trial 021).
- Cosine Annealing schedule with terminal floor lr1 = 1.0e-5 (raised from 1.0e-6):
  lr(f) = 1e-5 + 0.5 * (1e-3 - 1e-5) * (1 + cos(pi * f))
  over the 87.0 s budget.
- Gradient norm clipping: max_norm = 1.0.
- Annealed IC loss weight: lambda_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10).
- Objective: L(θ) = physics + lambda_ic * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10). Adam learning rate follows Cosine Annealing lr(f) = 1e-5 + 0.5 * (1e-3 - 1e-5) * (1 + cos(pi * f)) over 87.0 s budget. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against Trial 021 (terminal floor lr1 = 1e-6, mean 0.0008753, worst 0.001601). If parameter freezing in the final seconds was limiting convergence, raising the floor to 1e-5 will lower mean validation loss further. If 1e-5 causes terminal parameter jitter around the minimum, validation loss will increase slightly.

## Evidence from previous experiments

Trial 021 showed training curves leveling off noticeably during the final 2 snapshots (when lr was below 1e-5). Testing whether this flattening was due to learning rate starvation or true convergence is an important optimization diagnostic.

## Observed results

All 10 cases completed (87.0 s each, ~20.5k steps, 84,490 parameters). Mean validation loss was 0.001048 (Trial 021: 0.0008753), worst 0.002142 (dev_02; Trial 021: 0.001601), std 0.000770, mean IC 4.36e-09.
Per case comparison with Trial 021 (terminal floor lr1 = 1e-6):
- dev_01: 5.18e-05 (Trial 021: 2.54e-05) - higher
- dev_02: 0.002142 (Trial 021: 0.001601) - higher
- dev_03: 0.001010 (Trial 021: 0.000717) - higher
- dev_04: 0.000182 (Trial 021: 0.000202) - slightly improved
- dev_05: 3.08e-06 (Trial 021: 3.81e-07) - higher
- dev_06: 0.000785 (Trial 021: 0.000641) - higher
- dev_07: 0.001850 (Trial 021: 0.001310) - higher
- dev_08: 0.001450 (Trial 021: 0.001430) - practically tied
- dev_09: 0.001550 (Trial 021: 0.001270) - higher
- dev_10: 0.001460 (Trial 021: 0.001550) - slightly improved

Trial 021 with terminal floor 1e-6 outperformed Trial 022 with floor 1e-5 on 8 out of 10 cases. An asymptotic floor of 1e-5 maintained too much parameter velocity during the final 15% of training, inducing minor gradient jitter around the basin minimum rather than allowing the model to settle.

## Agent decision

Reject lr1 = 1e-5. Retain terminal floor lr1 = 1e-6 as the optimal asymptotic convergence rate for Cosine Annealing.

## Reason for decision

A lower terminal learning rate (1e-6) provides crucial asymptotic damping, allowing parameter vectors to settle tightly into the true basin minimum without limit-cycle jitter.

## Next experiment

Trial 023: Physics-Informed Spectral Initialization (Kepler-Natural Harmonic Grid). In Trials 017–022, the 8 learnable Fourier frequencies were initialized at an arbitrary linear grid [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]. In the Sitnikov problem, the governing physical frequencies are not linearly spaced; they are determined by the Keplerian primary forcing frequency (\omega_{orb} = 1.0) and the vertical natural oscillation frequency (\omega_z = \sqrt{2} \approx 1.4142), along with their nonlinear intermodulation beat frequencies (\omega_{orb} + \omega_z \approx 2.4142, 2\omega_z \approx 2.8284, 2\omega_{orb} + \omega_z \approx 3.4142). Initializing the learnable frequencies directly at this physically derived harmonic basis:
omega_init = [0.5, 1.0, 1.4142, 2.0, 2.4142, 2.8284, 3.0, 3.4142]
will seed gradient descent inside the exact physical resonance basin, accelerating spectral alignment and reducing residual errors across all development cases. All other elements match champion Trial 021.
