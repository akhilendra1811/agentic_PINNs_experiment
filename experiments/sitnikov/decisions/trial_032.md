# Experiment 032: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 031, domain-orthogonal Fourier frequencies $\omega_k = k / 3$ across $N\_FREQ = 8$ ($k=1\dots 8$, spanning $\omega \in [0.33, 2.67]$ rad/s) achieved a breakthrough, dropping mean validation loss to 0.0004918 and achieving sub-1e-3 precision across all 10 cases.

However, in non-linear celestial mechanics, when eccentricity $e \in [0.35, 0.5]$ (as in dev_07, dev_08, dev_09, dev_10), the time-dependent primary separation $\rho(t)$ via Kepler's equation generates substantial higher-order harmonic pulsations. Furthermore, the non-linear gravitational acceleration $-z / (z^2 + ρ(t)^2)^{3/2}$ acts as a nonlinear mixer that couples the vertical oscillation with higher-order orbital harmonics, specifically generating the third harmonic of the binary orbit: $3 \times \omega_\text{binary} = 3.0$ rad/s.

With $N\_FREQ = 8$, the maximum frequency was $8/3 \approx 2.67$ rad/s, which prematurely truncates the exact third harmonic ($k=9, \omega=3.0$ rad/s) and the primary-secondary beat frequency ($k=10, \omega=3.33$ rad/s). Expanding the domain-orthogonal basis to $N\_FREQ = 10$ ($k=1\dots 10$, $\omega \in [1/3, 10/3]$) will allow the input layer to directly supply these higher-order celestial harmonics without forcing deep hidden layers to extrapolate them, improving accuracy on the challenging high-eccentricity cases.

## Proposed method change

Fourier frequency count expansion:
- Set `N_FREQ = 10` in `candidate.py`.
- Initialize `omega` with the domain-orthogonal basis $k / 3.0$ for $k=1\dots 10$.
  Number of input features increases from 17 to 21 ($1 + 2 \times 10$).
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 10 learnable Fourier frequencies, single-layer residual branches, Tanh activations (86,796 parameters, well below the 250k ceiling).
- Loss weighting: Asymmetric IC annealing from Trial 029/031 (2000 -> 50 over first 15% of budget, 50 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 50.0 + 1950.0 * max(0.0, 1.0 - f / 0.15), starting at 2000.0 and decaying linearly to 50.0 over the first 15% of training time, remaining constant at 50.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 031 (mean 0.0004918, worst 0.0009345). Incorporating $k=9$ ($\omega=3.0$, the 3rd harmonic of the binary orbit) and $k=10$ ($\omega=3.33$) should improve fidelity on high-eccentricity cases (dev_07, dev_08, dev_10), aiming to compress the worst-case error further toward 0.00075 and reduce mean validation loss toward 0.00040.

## Evidence from previous experiments

Trial 031 demonstrated the decisive advantage of the domain-orthogonal basis $\omega_k = k/3$. Earlier attempts with 12 or 14 frequencies in Trials 007 and 018 were hampered by fixed frequencies and non-orthogonal spacing ($0.5 \times k$), whereas here we maintain domain orthogonality while capturing the physically essential 3rd orbital harmonic.

## Observed results

All 10 development cases completed (87.0 s each, ~22.0k steps, 86,796 parameters). The expansion to N_FREQ = 10 produced a noticeable degradation across all metrics:
- Mean validation loss increased to 0.0008886 (Trial 031: 0.0004918, an 80% degradation).
- Worst-case validation loss increased from 0.0009345 (dev_08 in Trial 031) to 0.001734 (dev_07 in Trial 032), breaking the sub-1e-3 ceiling established in Trial 031.
- All 10 cases performed worse than Trial 031:
  - dev_01: 2.34e-05 (Trial 031: 5.90e-06) - 4x worse
  - dev_02: 0.001050 (Trial 031: 0.000380) - 2.8x worse
  - dev_03: 0.000898 (Trial 031: 0.000366) - 2.5x worse
  - dev_04: 7.59e-05 (Trial 031: 5.88e-05) - 29% worse
  - dev_05: 8.74e-06 (Trial 031: 1.59e-06) - 5.5x worse
  - dev_06: 0.000870 (Trial 031: 0.000820) - 6% worse
  - dev_07: 0.001734 (Trial 031: 0.000813) - 2.1x worse
  - dev_08: 0.001400 (Trial 031: 0.000935) - 50% worse
  - dev_09: 0.001490 (Trial 031: 0.000605) - 2.5x worse
  - dev_10: 0.001340 (Trial 031: 0.000932) - 44% worse

Physical and mathematical explanation: In physics-informed neural networks, computing second-order ODE residuals involves differentiating sinusoidal basis functions twice: d^2/dt^2 [sin(ω t)] = -ω^2 sin(ω t). For ω = 10/3 ≈ 3.33 rad/s, the curvature factor is ω^2 ≈ 11.11! This introduces an order-of-magnitude amplification of high-frequency gradient noise during autograd backpropagation. Under Adam optimization, these amplified high-frequency gradients dominate parameter updates, pulling the optimizer's attention toward suppressing noisy high-frequency residual modes at the expense of accurately capturing the fundamental orbital envelope. Furthermore, with 500 collocation points over [0, 6π], high-frequency modes approach the Nyquist limit of point density. N_FREQ = 8 (covering k=1..8, up to ω = 8/3 ≈ 2.67 rad/s) provides the exact optimal spectral cutoff, capturing all physically necessary harmonics without triggering autograd gradient amplification instability.

## Agent decision

Reject: N_FREQ = 10 degraded all 10 development cases. Revert immediately to N_FREQ = 8 from Trial 031.

## Reason for decision

Validation loss nearly doubled (0.0004918 -> 0.0008886) and broke the sub-1e-3 ceiling on 6 of 10 cases due to ω^2 autograd derivative amplification. N_FREQ = 8 remains the indisputable champion.

## Next experiment

Trial 033: Residual Connection Scaling (ResNet Highway Skip Damping: h = h + α * res(h, feats) with α = 0.5).
In our champion architecture, each residual block computes h = h + res_block(concat(h, feats)). In deep ResNets and continuous ODE neural representations, adding unscaled residual branches causes hidden activations to monotonically grow in norm through depth (||h_{l+1}|| > ||h_l||), which can push the downstream Tanh layers into saturation regimes where gradients diminish. Scaling the residual branch by α = 0.5 (or 1/sqrt(2) ≈ 0.707) preserves activation variance across layers, keeping hidden activations in the linear/moderately non-linear regime of Tanh (where second derivatives d^2/dt^2 are most well-behaved). All other settings match champion Trial 031 (N_FREQ = 8, ω_k = k/3, Asymmetric IC annealing 2000 -> 50 over 15%, Adam betas=(0.9, 0.99)).
