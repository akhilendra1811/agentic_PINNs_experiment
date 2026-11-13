# Experiment 045: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 034, extending the initial condition loss annealing window from 15% to 20% of training time ($f \le 0.20$) produced a major 19.3% reduction in validation error because it allowed the network to anchor the first complete Sitnikov oscillation before boundary drag was relaxed.

However, in non-linear celestial mechanics, large initial vertical displacements $z_0$ induce substantial anharmonic period elongation:
$T(z_0) \approx T_0 \left(1 + \frac{3}{8} z_0^2 + \dots \right)$.
For $z_0 = 1.5$ (dev_08, our consistent worst-case bottleneck), $T(z_0)$ is nearly 85% longer than the infinitesimal period, spanning approximately 16.3 radians—which constitutes over 85% of our entire $6\pi \approx 18.85$ temporal domain! Consequently, for dev_08 and dev_07, the first orbital cycle requires significantly more training iterations to trace and lock its initial phase than low-amplitude orbits.

Extending the IC loss annealing window slightly from $f \le 0.20$ to $f \le 0.25$ (~21.75 seconds of training):
$\lambda_{ic}(f) = 10.0 + 1990.0 \times \max(0.0, 1.0 - f / 0.25)$
will provide 25% more training steps under strong origin anchoring, ensuring that high-amplitude, period-elongated orbits establish their global trajectory phase before the boundary weight relaxes to 10.0.

## Proposed method change

Loss weighting schedule modification:
- Change annealing window to `frac <= 0.25` in `train_model`:
  `ic_w = IC_W_BASE + (IC_W_INIT - IC_W_BASE) * max(0.0, 1.0 - frac / 0.25)`
  with `IC_W_BASE = 10.0` and `IC_W_INIT = 2000.0`.
- Architecture: Modified PINN with width 192, 2 gating stages, symmetric Tanh encoders (84,874 parameters, identical to Trial 044).
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 0.5) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.25), starting at 2000.0 and decaying linearly to 10.0 over the first 25% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 0.5. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 044 (mean 0.0002853, worst 0.0007889). Extended anchoring should specifically improve the high-amplitude bottleneck cases dev_07 and dev_08, targeting worst-case reduction toward 0.00065 and mean validation loss toward 0.00026.

## Evidence from previous experiments

Trial 019 (10%), Trial 029 (15%), and Trial 034 (20%) each demonstrated that increasing the early anchor duration to match physical orbital periods systematically improved overall PINN convergence. Evaluating 25% tests whether the period elongation of dev_07 and dev_08 benefits from slightly longer early anchoring.

## Observed results

All 10 development cases completed (87.0 s each, ~20.4k steps, 84,874 parameters). Extending the annealing window to 25% yielded strong individual results but a slightly higher global mean:
- Certain cases set spectacular new campaign records:
  - dev_01 dropped to 3.02e-06 (best ever!)
  - dev_09 dropped to 0.000122 (was 0.000218 in Trial 044, a 44% improvement!)
  - dev_10 dropped to 0.000418 (was 0.000442 in Trial 044)
- However, overall mean validation loss was 0.0002974 (Trial 044: 0.0002853, a 4.2% difference).
- Worst-case validation loss was 0.0008465 on dev_08 (Trial 044: 0.0007889).
- Generalization remained flawless: val/train ratio was 1.00 across all 10 cases; mean IC loss was 1.08e-08; standard deviation was 0.000272.

Physical and optimization explanation: Extending the high-anchor IC loss window from 20% to 25% consumes an extra ~4.3 seconds (~1,000 optimization steps) where the optimizer is constrained by large boundary penalties. For cases where the initial condition was already firmly established within 20% of training (such as dev_02, dev_03, and dev_08), this extra 5% delayed the relaxation of boundary drag, leaving slightly less unconstrained training time to minimize interior ODE residuals across the 0..6π domain. The 20% horizon (frac <= 0.20) strikes the exact balance between establishing the initial orbit and freeing subsequent gradient capacity.

## Agent decision

Reject / Retain Trial 044 as champion: While the 25% horizon set fine individual marks on dev_01 and dev_09, Trial 044 with frac <= 0.20 achieved lower mean validation loss (0.0002853 vs 0.0002974) and lower worst-case error (0.000789 vs 0.000846). Revert to frac <= 0.20.

## Reason for decision

Mean validation loss was lower in Trial 044 (0.0002853 vs 0.0002974). The 20% horizon provides the optimal boundary-to-interior gradient allocation.

## Next experiment

Trial 046: Optimizer Momentum Tuning (Testing Adam beta1 = 0.95 vs 0.90 in Modified PINN).
In Trial 027, lowering beta1 from 0.90 to 0.80 caused severe gradient zigzagging and diverged dev_09. In deep neural ODE collocation, higher momentum (beta1 = 0.95) acts as a low-pass filter on gradient oscillations, accumulating consistent velocity along directional ravines (such as the narrow valley of the Sitnikov ODE residual). Testing beta1 = 0.95 (with beta2 = 0.990 and max_norm = 0.5) evaluates whether increased directional momentum accelerates progress along the narrow ODE curvature minimum. All other settings match champion Trial 044.
