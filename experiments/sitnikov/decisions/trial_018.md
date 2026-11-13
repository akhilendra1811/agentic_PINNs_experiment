# Experiment 018: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

Trial 017 demonstrated that making the Fourier frequency bank learnable produced a massive 34% drop in mean validation loss (down to 0.001181) because the frequencies adaptively aligned with the amplitude-dependent orbital periods. The Sitnikov system contains two coupled oscillators: the Keplerian primary forcing (\omega_{orb} = 1.0) and the vertical oscillation (\omega_z \approx 1.0–1.4 rad/s), which generate beat frequencies and sidebands (\omega_z \pm \omega_{orb}, 2\omega_z \pm \omega_{orb}, etc.). With only 8 frequencies, the spectral basis cannot capture all active sidebands. Expanding to N_FREQ = 12 learnable frequencies (initialized at w_k = 0.5*k for k=1..12, spanning 0.5 to 6.0 rad/s) will give the model the spectral richness required to capture intermodulation harmonics without fixing rigid frequency values.

## Proposed method change

Architecture modification for expanded learnable spectral features:
- Increase number of learnable Fourier frequencies from N_FREQ = 8 to N_FREQ = 12:
  `self.omega = nn.Parameter(0.5 * torch.arange(1, 13, dtype=torch.float32).reshape(1, -1))`
- Input dimension: 1 + 2 * 12 = 25 features.
- Architecture: 2 residual blocks of width 192 with Tanh activations (79,502 parameters).
- Optimization: Adam with Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Objective unchanged: L(θ) = physics + 100.0 * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate following Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)), where f is the elapsed fraction of the 87.0 s budget. Gradient updates clipped to maximum L2 norm of 1.0. All weights, biases, and the 12 spectral frequency parameters are optimized jointly.

## Expected effect

Comparison against Trial 017 (8 learnable frequencies, mean 0.001181, worst 0.002819). The 12 learnable modes should resolve intermodulation sidebands in high-eccentricity cases (e.g. dev_06 with e=0.33, dev_02 with e=0.29), potentially driving mean validation loss below 0.0010 (sub-1e-3 regime!).

## Evidence from previous experiments

Trial 017 proved that learnable frequencies adjust to physical periods, improving all 10 cases simultaneously. Unlike Trial 007 (where 14 fixed frequencies failed because fixed high frequencies added noise), learnable frequencies can freely adjust their values or contract toward relevant physical modes.

## Observed results

All 10 cases completed (87.0 s each, ~23.7k steps, 79,502 parameters). Mean validation loss was 0.001498 (Trial 017: 0.001181), worst 0.002714 (dev_07; Trial 017: 0.002819), std 0.00111, mean IC 7.52e-10.
Per case comparison with Trial 017 (8 learnable frequencies):
- dev_01: 7.57e-05 (Trial 017: 7.12e-05) - practically tied
- dev_02: 0.002560 (Trial 017: 0.001400) - higher
- dev_03: 0.001640 (Trial 017: 0.001060) - higher
- dev_04: 0.000205 (Trial 017: 0.000286) - 28% improvement
- dev_05: 1.06e-05 (Trial 017: 5.18e-06) - both in 10^-5/10^-6 range
- dev_06: 0.000887 (Trial 017: 0.000269) - higher
- dev_07: 0.002714 (Trial 017: 0.002210) - slightly higher
- dev_08: 0.001890 (Trial 017: 0.001860) - practically tied
- dev_09: 0.002550 (Trial 017: 0.002819) - improved (new best on dev_09!)
- dev_10: 0.002450 (Trial 017: 0.001820) - slightly higher

The worst-case validation error improved to 0.002714 (dev_09 reached 0.00255), and dev_04 improved. However, the overall mean loss was higher than Trial 017 (0.001498 vs 0.001181) because the 12-frequency input layer (25 features) dispersed the gradient across more spectral dimensions, slightly slowing convergence on intermediate cases.

## Agent decision

Reject 12 learnable frequencies as the default. Retain 8 learnable frequencies (Trial 017) as the champion spectral basis.

## Reason for decision

8 learnable frequencies achieved a substantially lower mean validation loss (0.001181 vs 0.001498, a 21% advantage) with virtually identical worst-case performance (0.002819 vs 0.002714). The 8-frequency bank provides the optimal balance between spectral expressivity and optimization compactness.

## Next experiment

Trial 019: Self-Adaptive Loss Weighting (Dynamic IC Loss Weighting). In all successful trials so far (Trials 004–018), the IC weight in the training loss was fixed at 100.0 (loss = physics + 100.0 * ic). At convergence, IC loss reaches ~1e-10, meaning 100.0 * ic ≈ 1e-8, which is 5 orders of magnitude smaller than the physics residual (~1e-3). Early in training, however, IC errors are O(1), dominating the physics loss. We will test an annealed IC weight schedule: starting at lambda_ic = 1000.0 to rapidly lock the initial condition trajectory in the first 10% of training, then annealing down to lambda_ic = 100.0 to maximize gradient focus on the physics residual across the rest of the domain.
