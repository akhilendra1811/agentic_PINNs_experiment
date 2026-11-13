# Experiment 035: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 026, reducing Adam's second-moment exponential decay rate from $\beta_2 = 0.999$ to $\beta_2 = 0.990$ yielded a 17% reduction in validation error because the effective averaging window shortened from $\tau \approx 1000$ steps to $\tau \approx 100$ steps, enabling the optimizer to adapt quickly as the PINN loss landscape shifted from coarse orbital envelope fitting to fine harmonic resolution.

However, in Trial 034, we observed that during the final third of training ($f > 0.67$), the learning rate drops below $10^{-4}$ down to $10^{-6}$. In this fine-convergence regime, the gradients are small and dominated by delicate higher-order residual curvatures. A memory window of only 100 steps ($\approx 0.37$ s of wall-clock time) can introduce stochastic fluctuations in the coordinate-wise second-moment estimates $v_t$, causing slight step-size jitter across individual weights.

Setting $\beta_2 = 0.995$ creates an intermediate memory horizon of $\tau = 1 / (1 - 0.995) = 200$ steps ($\approx 0.74$ s). This is short enough to track the macro-shifts during early training (5x faster than default 0.999), yet provides 2x more statistical smoothing in the denominator $\sqrt{v_t} + \epsilon$ during terminal fine-tuning.

## Proposed method change

Optimizer configuration modification:
- Change Adam betas from `(0.9, 0.99)` to `(0.9, 0.995)`.
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 domain-orthogonal learnable Fourier frequencies (ω_k = k / 3.0), single-layer unscaled residual branches, Tanh activations (84,490 parameters, identical to Trial 034).
- Loss weighting: Asymmetric IC annealing from Trial 034 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.995), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.995) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 034 (mean 0.0003971, worst 0.0008162). Smoother second-moment estimation in the late training phase should dampen coordinate-wise step-size jitter, helping the model settle into tighter residual minima and potentially lowering mean validation loss toward 0.00035.

## Evidence from previous experiments

Trial 026 proved that tuning beta2 had an immediate effect on PINN convergence. With our newly optimized domain-orthogonal basis (Trial 031) and reduced terminal IC drag (Trial 034), fine-tuning beta2 to 0.995 evaluates whether a 200-step memory window improves terminal asymptotic convergence.

## Observed results

All 10 development cases completed (87.0 s each, ~22.9k steps, 84,490 parameters). Increasing beta2 from 0.990 to 0.995 produced an unambiguous degradation across the board:
- Mean validation loss increased from 0.0003971 (Trial 034) to 0.0005225 (+31.6% degradation).
- Worst-case validation loss increased from 0.0008162 (dev_08 in Trial 034) to 0.0009225 (dev_02 in Trial 035).
- Key bottleneck cases suffered notable setbacks:
  - dev_02: 0.000923 vs 0.000273 in Trial 034 (3.4x worse!)
  - dev_06: 0.000847 vs 0.000249 in Trial 034 (3.4x worse!)
  - dev_03: 0.000485 vs 0.000381 in Trial 034 (27% worse)
  - dev_08: 0.000840 vs 0.000816 in Trial 034 (slightly worse)
  - dev_10: 0.000783 vs 0.000770 in Trial 034 (slightly worse)

Physical and optimization explanation: In the Sitnikov problem, as the network progressively fits lower-frequency orbital components, the loss landscape continuously shifts toward resolving sharp, localized nonlinear accelerations around primary pericenter passages. Doubling the second-moment memory window from 100 steps to 200 steps (tau = 200) forces Adam to retain obsolete gradient magnitude statistics from past phases of training. When an individual coordinate encounters a sudden steep curvature gradient, the inflated second-moment history v_t dampens the effective step size (Delta theta proportional to 1 / sqrt(v_t)), delaying parameter adaptation. The 100-step horizon (beta2 = 0.990) provides the exact level of agility needed to track the shifting PINN residual landscape.

## Agent decision

Reject: beta2 = 0.995 degraded mean validation loss by 31.6% and severely impaired cases dev_02 and dev_06. Revert immediately to beta2 = 0.990 from champion Trial 034.

## Reason for decision

Validation loss degraded from 0.0003971 to 0.0005225. PINN training requires fast second-moment responsiveness (beta2 = 0.990, 100-step memory) to navigate the non-stationary loss landscape.

## Next experiment

Trial 036: Annealing Schedule Shape (Cosine vs Polynomial/Quadratic Annealing).
In all trials since Trial 014, we have used standard Cosine Annealing: lr(f) = lr1 + 0.5 * (lr0 - lr1) * (1 + cos(pi * f)). Notice that the cosine function decelerates its decay rate in the middle regime: at f=0.5, the derivative d(lr)/df is maximal, but near f=0 and f=1, d(lr)/df is zero. Consequently, lr remains above 5e-4 for the entire first half of training (f <= 0.5), and only drops into the sub-1e-4 fine-convergence regime in the last 20% of training (f >= 0.80). What if we test a Quadratic / Power-2 decay schedule: lr(f) = lr1 + (lr0 - lr1) * (1 - f)^2? In quadratic decay, lr drops more smoothly and spends 40% of the training time in the fine-tuning regime (lr < 1e-4), giving the network twice as many steps for asymptotic residual minimization. We will test quadratic annealing while keeping all other settings matching champion Trial 034.
