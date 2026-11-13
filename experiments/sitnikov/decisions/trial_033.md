# Experiment 033: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In our champion architecture (Trial 031), each residual block adds the full-magnitude output of a Tanh-activated sub-network directly into the residual highway:
$h_{l+1} = h_l + f_l([h_l, \text{feats}])$.
Because $h_0 \in [-1, 1]$ from the initial projection and each $f_l$ outputs in $[-1, 1]$, the activation magnitude grows through depth: $h_1 \in [-2, 2]$ and $h_2 \in [-3, 3]$. In deep networks and continuous PINNs, unscaled residual addition increases activation variance along the network depth, driving downstream linear projections into the saturation regions of Tanh ($|x| > 2$), where first derivatives $\tanh'(x) = 1 - \tanh^2(x) \ll 1$ and second derivatives $\tanh''(x) = -2\tanh(x)(1 - \tanh^2(x)) \ll 1$ vanish.

Scaling each residual update by a damping factor $\alpha = 0.5$:
$h_{l+1} = h_l + 0.5 \times f_l([h_l, \text{feats}])$
prevents activation norm growth, preserving variance across layers and keeping the hidden representations within the active, non-saturated linear/sub-linear regime of Tanh. This maintains strong derivative flow during autograd calculation of $dz/dt$ and $dv/dt$.

## Proposed method change

Architecture modification:
- In `HighwayInputInjectionResNet.forward`:
  ```python
  h = self.in_proj(feats)
  h = h + 0.5 * self.res1(torch.cat([h, feats], dim=1))
  h = h + 0.5 * self.res2(torch.cat([h, feats], dim=1))
  return self.out_proj(h)
  ```
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$ (reverting Trial 032 back to Trial 031 champion basis).
- Width 192, single-layer residual branches, Tanh activations (84,490 parameters).
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

Comparison against champion Trial 031 (mean 0.0004918, worst 0.0009345). By preventing Tanh saturation in hidden layers, residual scaling should improve derivative gradient conditioning, helping the network settle more precisely into local curvature minima and potentially lowering mean validation loss below 0.00045.

## Evidence from previous experiments

Trial 031 established the optimal 8-frequency domain-orthogonal basis. Trial 028 demonstrated that deep bottlenecks within residual branches harmed autograd stability. Damping the residual skip addition by 0.5 is a standard variance-preserving technique in deep residual architectures (e.g. He et al., 2016; ReZero, 2020) that stabilizes gradient propagation.

## Observed results

All 10 cases completed (87.0 s each, ~22.3k steps, 84,490 parameters). Scaling the residual skip additions by 0.5 caused severe instability and overall degradation:
- Mean validation loss degraded to 0.01174 (Trial 031: 0.0004918, a 24x degradation).
- Worst-case validation loss suffered a catastrophic divergence on dev_09, reaching 0.1114 (v/t ratio = 176.13!). On dev_09, the validation loss was 0.0029 at snapshot 6 (step 12,294), but then diverged rapidly through 0.022 -> 0.045 -> 0.081 -> 0.111.
- Furthermore, 7 of the remaining 9 cases degraded compared to Trial 031:
  - dev_02: 0.000798 (Trial 031: 0.000380) - 2x worse
  - dev_03: 0.000762 (Trial 031: 0.000366) - 2x worse
  - dev_04: 6.30e-05 (Trial 031: 5.88e-05) - worse
  - dev_07: 0.001310 (Trial 031: 0.000813) - 61% worse
  - dev_08: 0.001610 (Trial 031: 0.000935) - 72% worse
  - dev_10: 0.001000 (Trial 031: 0.000932) - worse
- While benign low-eccentricity cases achieved fine precision (dev_01 reached 1.33e-06 and dev_05 reached 4.75e-08), all challenging cases were severely crippled.

Physical and optimization explanation: In a shallow 2-block ResNet, saturation is not a pathological issue. Rather, the residual branch must generate substantial non-linear amplitude to model the sharp acceleration pulses that occur when the primaries pass pericenter. Attenuating the residual addition by 0.5 effectively halves the nonlinear authority of each block, forcing the network into a linear regime that cannot synthesize the steep anharmonic curvature required in eccentric cases like dev_09. When the network under-predicts the acceleration peak, phase error compounds exponentially until autograd gradients destabilize into runaway divergence.

## Agent decision

Reject: Residual branch scaling (α = 0.5) degrades nonlinear expressive capacity and causes divergence on dev_09. Revert immediately to full-strength residual additions (α = 1.0) from Trial 031.

## Reason for decision

Mean validation error jumped from 0.0004918 to 0.01174, worst-case error blew up to 0.1114, and 7 of 10 cases degraded. Full-strength residual connections are essential for capturing sharp gravitational acceleration peaks.

## Next experiment

Trial 034: Modulated Fourier Feature Scale Initialization (Spectral Power Normalization).
In Trial 031, the Fourier frequencies are initialized as ω_k = k / 3.0 for k=1..8. The input features are [t_norm, sin(ω_k t), cos(ω_k t)]. Notice that all Fourier sinusoids are passed to the initial projection Linear(17, 192) with identical unit amplitudes. In physical systems, the energy spectrum of an oscillatory solution decays with frequency (typically as 1/k or 1/k^2 according to Fourier analysis of smooth dynamical trajectories). However, standard PyTorch uniform Xavier initialization weights all 17 input dimensions identically. If we initialize the initial linear projection weights corresponding to the k-th harmonic with an amplitude scaling factor proportional to 1/k (or 1/sqrt(k)), the network is physically biased toward low-frequency dominant modes early in training, avoiding high-frequency spectral bias. We will test spectral weighting in the input projection while keeping all other settings identical to champion Trial 031.
