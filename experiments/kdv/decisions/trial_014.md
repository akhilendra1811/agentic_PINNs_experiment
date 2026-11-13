# Trial 014 Decision Record: Multi-scale Fourier Feature Input Projection

## Hypothesis
Standard PINNs suffer from eigenvector/spectral bias (Wang, Wang, Perdikaris, CMAME 2021), prioritizing low-frequency modes and struggling to resolve steep multi-harmonic wave structures. Augmenting the coordinate input representation with a deterministic multi-scale Fourier feature basis $[\sin(k \pi x), \cos(k \pi x)]$ for $k \in \{1, 2, 3, 4\}$ will tune the Neural Tangent Kernel eigenspectrum, enabling the network to learn higher-frequency soliton interactions directly while preserving exact periodic boundary compliance analytically.

## Proposed method change
In `KdVPINN`:
1. Expand the spatial coordinate features from the single fundamental mode $k=1$ to four integer harmonics $k \in \{1, 2, 3, 4\}$:
   $$\phi_x(x) = [\sin(\pi x), \cos(\pi x), \sin(2\pi x), \cos(2\pi x), \sin(3\pi x), \cos(3\pi x), \sin(4\pi x), \cos(4\pi x)] \in \mathbb{R}^8$$
2. Concatenate with temporal coordinate $t$, initial profile $u_0(x)$, and normalized initial derivative $u_{0,x}(x)/\pi$, yielding an 11-dimensional input feature vector.
3. Pass through input projection `Linear(11, 160)` and 7 residual sinusoidal layers:
   $$h_{l+1} = h_l + \sin(W_l h_l + b_l)$$
4. Final scalar output through `Linear(160, 1)` with temporal ansatz:
   $$u(t, x) = u_0(x) + \tanh(\alpha t) \cdot \text{net\_out}(t, x)$$
5. Train with standard AdamW (lr=$1.08 \times 10^{-3}$, cosine decay, linear temporal curriculum over first 35%).

## Training objective used
Standard composite KdV physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Because all harmonic basis functions $\sin(k \pi x)$ and $\cos(k \pi x)$ are $2$-periodic on $[-1, 1]$ for integer $k$, periodic boundary conditions remain satisfied analytically to machine precision ($L_{\mathrm{BC}} \approx 0$). Providing explicit higher spatial harmonics directly counteracts spectral bias, expected to significantly improve accuracy on `dev_02` (which superimposes frequencies 1 and 2 and previously exhibited the highest error: 0.003337 in Trial 004). Moreover, preserving the additive residual architecture restores maximum step throughput (~8,500 steps per case).

## Evidence from previous experiments
- In Trial 004 (SIREN), mean validation loss dropped to 0.001260, but `dev_02` remained the dominant error source (0.003337) due to high-frequency wave steepening.
- In Trial 013, multiplicative coordinate gating halved optimizer throughput to 12.5 steps/sec due to 3rd-order autograd graph bloat, showing that coordinate enhancements must be introduced at the input projection level rather than through deep layer-wise gating.
- Multi-scale Fourier features provide rich coordinate representations with zero autograd branching overhead in intermediate layers.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: multiscale_fourier_feature_projection
- Source: Sifan Wang, Hanwen Wang, Paris Perdikaris (CMAME 2021, arXiv:2012.10047), "On the eigenvector bias of Fourier feature networks: From regression to solving multi-scale PDEs with physics-informed neural networks".
- Distinctness: Substantively changes the input coordinate embedding from single-frequency cartesian trigonometric features to a multi-harmonic Fourier feature map $[\sin(k \pi x), \cos(k \pi x)]_{k=1}^4$. This directly modifies the NTK spectrum, satisfying the early exploration novelty requirements.


## Observed results
- Validation loss:
  - Mean: 0.0023608
  - dev_01: 1.8122e-06
  - dev_02: 0.0041603
  - dev_03: 0.0029202
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.11e-6 <= 1e-3, params = 182,402 <= 250,000).
- Comparison: Substantially outperforms baseline Trial 001 (mean 0.003040, dev_01: 1.05e-5, dev_02: 0.007173), achieving exceptional residual precision on dev_01 (1.81e-06). Full optimizer throughput was restored (~8,250 steps per case, 27.8 steps/sec). However, Trial 004's single-mode sine trunk remains ahead on dev_02 (0.003337) and dev_03 (0.000442), suggesting that four input harmonics slightly diffused attention across redundant feature dimensions without sufficient regularizing bias.

## Agent decision
Retain Trial 004 (SIREN sinusoidal activation with fundamental coordinate embedding and AdamW) as the incumbent winner. Mark Trial 014 as completed and eligible, logging 1 substantive input representation novelty toward the 15 early-stage quota (total now 12 / 15).

## Reason for decision
Trial 014 confirmed that multi-scale Fourier feature input mapping successfully avoids autograd bottlenecks while achieving low PDE residual (0.002361), comfortably beating the baseline. However, unaugmented SIREN (Trial 004) continues to hold the best mean loss (0.001260) and worst-case loss (0.003337). The multi-harmonic projection remains a strong modular candidate for subsequent combination phases. We advance to the next novel idea.
