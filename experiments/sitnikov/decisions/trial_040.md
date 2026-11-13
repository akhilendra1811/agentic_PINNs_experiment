# Experiment 040: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 038, our champion Modified PINN used Tanh-activated feature encoder projections:
$U = \tanh(W_u x + b_u)$ and $V = \tanh(W_v x + b_v)$.
While Tanh bounds the encoder outputs within $[-1, 1]$, it compresses large harmonic oscillations into the flat saturation shoulders of the hyperbolic tangent function. Consequently, the first and second time-derivatives of the encoded features:
$dU/dt = (1 - U^2) \odot (W_u \cdot dx/dt)$
are suppressed whenever $|W_u x| > 1$.

In celestial mechanics, the true trajectory velocity and acceleration exhibit large dynamic ranges, particularly near primary pericenter passages. Removing the Tanh non-linearity from the encoders $U$ and $V$:
$U = W_u x + b_u$ and $V = W_v x + b_v$
allows $U(t)$ and $V(t)$ to act as uncompressed linear Fourier synthesis bases. The time-derivatives $dU/dt$ and $d^2U/dt^2$ then flow cleanly without activation damping, while the hidden gating units $z_l = \tanh(W_l h_{l-1} + b_l)$ provide all necessary non-linear phase modulation. We hypothesize that linear encoders will preserve full harmonic dynamic range and improve derivative propagation.

## Proposed method change

Architecture modification:
- In `ModifiedPINN`:
  - Change `self.u_proj = nn.Linear(n_feats, WIDTH)` (remove Tanh).
  - Change `self.v_proj = nn.Linear(n_feats, WIDTH)` (remove Tanh).
  - Keep `self.in_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())` so initial hidden state $h_0 \in [-1, 1]$.
  - Revert depth to 2 gating stages ($z_1, z_2$) with `WIDTH = 192` (84,874 parameters, identical to Trial 038).
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Loss weighting: Asymmetric IC annealing from Trial 034/038 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 038 (mean 0.0002937, worst 0.0008230). Eliminating Tanh compression on $U$ and $V$ should improve gradient flow through high-amplitude acceleration peaks, targeting worst-case reduction on dev_08 and dev_10 and aiming to lower mean validation loss toward 0.00024.

## Evidence from previous experiments

Trial 038 proved the superiority of the Modified PINN architecture. In the foundational literature (Wang et al., 2021), linear feature encoders are often employed when input features already consist of bounded Fourier sinusoids, avoiding redundant activation saturation.

## Observed results

All 10 development cases completed (87.0 s each, ~19.7k steps, 84,874 parameters). Linear feature encoders demonstrated a compelling trade-off:
- Worst-case validation loss dropped to an all-time campaign record of 0.0006257 (dev_08; Trial 038: 0.0008230, a 24.0% reduction in worst-case bottleneck error!).
- All 10 development cases now sit strictly below 0.00063:
  - dev_01: 4.94e-06
  - dev_02: 0.000426
  - dev_03: 0.000263
  - dev_04: 2.27e-05
  - dev_05: 1.01e-07
  - dev_06: 0.000353
  - dev_07: 0.000605
  - dev_08: 0.000626 (campaign best worst-case error!)
  - dev_09: 0.000271
  - dev_10: 0.000527
- Standard deviation across the 10 cases compressed to an ultra-compact 0.000241.
- Mean validation loss was 0.0003100, slightly above Trial 038's all-time record of 0.0002937 (+5.5%).
- Generalization was perfect: val/train ratio was 1.00 across all 10 cases; mean IC loss was 1.02e-08.

Physical and optimization explanation: Bounding the encoders with Tanh (Trial 038) provides stronger regularization on smooth low-amplitude orbits (dev_01, dev_03, dev_05), leading to marginally lower mean validation loss (0.0002937). Conversely, removing Tanh from U and V eliminates saturation on large-amplitude, high-eccentricity orbits (dev_08: z0=1.5, e=0.35), where uncompressed linear encoders allow the network to synthesize high-energy orbital crests without derivative attenuation, slashing the dev_08 bottleneck error from 0.000823 to 0.000626.

## Agent decision

Reject / Keep Trial 038 as reference champion: While linear encoders achieve our lowest worst-case error (0.000626) and tightest variance, Trial 038 retains the lowest mean validation loss (0.0002937). We revert to Trial 038's Tanh encoders as the primary baseline, while keeping this worst-case enhancement documented for candidate selection analysis.

## Reason for decision

Mean validation loss was marginally lower in Trial 038 (0.0002937 vs 0.0003100). Preserving bounded Tanh encoders provides slightly better global calibration across low-to-moderate eccentricity cases.

## Next experiment

Trial 041: Multiplicative Encoder Fusion (Hybrid Encoder: U with Tanh, V with Linear).
Trial 038 demonstrated that Tanh encoders optimize smooth orbits (dev_01, dev_03, dev_05), while Trial 040 demonstrated that linear encoders optimize high-amplitude turning points (dev_08). In the Sitnikov phase space, position z(t) is bounded and smooth, whereas velocity v(t) = dz/dt requires high dynamic range. What if we configure U as a Tanh-bounded encoder (representing bounded displacement features) and V as an uncompressed Linear encoder (representing high-dynamic-range velocity/acceleration features)?
U = tanh(Linear(feats)), V = Linear(feats).
This asymmetric hybrid encoder could theoretically combine the smooth calibration of Trial 038 with the uncompressed dynamic range of Trial 040.
