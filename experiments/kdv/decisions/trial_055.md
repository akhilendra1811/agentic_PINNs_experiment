# Trial 055 Decision Record: Real Gabor Wavelet Activation (WIRE) for KdV PINNs

## Hypothesis
In pure SIREN (Trial 033), the activation $\sigma(z) = \sin(z)$ is globally periodic and non-local.
However, solutions to the periodic Korteweg-de Vries (KdV) equation are composed of localized solitary wave packets with steep gradients and exponentially decaying spatial tails:
$$u(x, t) \sim 12 \kappa^2 \operatorname{sech}^2(\kappa(x - 4\kappa^2 t))$$
Pure sinusoidal activations are prone to global Gibbs-like high-frequency ringing artifacts, where the network introduces small spurious oscillations across the flat background domain $x \in [-1, 1]$ in an attempt to fit steep localized peaks.
Following the **WIRE (Wavelet Implicit Neural Representations)** framework (Saragadam et al., CVPR 2023, arXiv:2301.05187), we replace pure sine activations with real Gabor wavelets:
$$\sigma(z) = \sin(z) \exp\left(-\frac{z^2}{2 s_0^2}\right)$$
with scale factor $s_0 = 5.0$.
Gabor wavelets achieve the optimal Heisenberg-Gabor space-frequency concentration bound:
1. Inside the active operational range ($|z| \le 2$), the Gaussian envelope is $\approx 0.92 \to 1.0$, preserving the full derivative expressiveness and spectral fidelity of SIREN.
2. For large activations ($|z| > 5$), the Gaussian envelope smoothly suppresses extreme pre-activation excursions, eliminating non-physical spatial ringing artifacts across the quiescent domain.
3. Because $\sigma(z) \in C^\infty$, all 3rd-order spatial derivatives $u_{xxx}$ remain continuous, infinitely differentiable, and well-conditioned for backward automatic differentiation.
This tests whether Gabor wavelet localization improves resolution of the steep two-soliton collision on `dev_02` while preserving sub-microscale precision on `dev_01` and `dev_03`.

## Proposed method change
In `candidate.py`:
1. Define the real Gabor wavelet activation function:
   ```python
   GABOR_SCALE = 5.0


   def gabor_activation(z, scale=GABOR_SCALE):
     return torch.sin(z) * torch.exp(-0.5 * (z / scale).square())
```
2. In `KdVPINN.forward`:
   ```python
   h = gabor_activation(self.in_linear(features))
   for layer in self.hidden:
     h = h + gabor_activation(layer(h))
```
3. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$, linear $\alpha$-warmup from $0 \to 2.0$ over first 35% of steps, continuous cosine decay down to $10^{-7}$ over remaining 65%.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Gabor wavelets localize neural activations in space-frequency domain, reducing global spatial ringing artifacts around solitary wave peaks and providing smoother resolution of the two-soliton collision in `dev_02`.

## Evidence from previous experiments
- In Trial 006: Pure SIREN $\sin(z)$ drastically reduced error from 0.00304 to 0.00162.
- In CVPR 2023, WIRE demonstrated substantial reductions in reconstruction artifacts compared to SIREN on signals with sharp localized features.
- Testing Gabor wavelets on the periodic KdV PINN explores whether space-frequency compactness improves upon pure sinusoidal representations.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: wire_gabor_wavelet_activation
- Source: Saragadam et al. (Rice University, CVPR 2023, arXiv:2301.05187), "WIRE: Wavelet Implicit Neural Representations".
- Distinctness: Introduces continuous Gabor wavelet activation functions combining sinusoidal oscillations with Gaussian envelopes to achieve optimal space-frequency concentration and suppress spatial ringing.


## Observed results
- Validation loss:
  - Mean: 0.00503427 (Higher than incumbent Trial 033: 0.00054644)
  - dev_01: 5.73105e-06
  - dev_02: 0.01195401
  - dev_03: 0.00314306
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 1.98e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Severe computational bottleneck — throughput dropped from 23.4 steps/sec (6,950 steps) down to 9.68 steps/sec (2,877 steps).
- Comparison: While Gabor wavelets theoretically offer optimal space-frequency concentration, composing the Gaussian envelope $\exp(-0.5 (z/s)^2)$ with $\sin(z)$ creates an acute combinatorial explosion in PyTorch's automatic differentiation graph when computing 3rd-order spatial derivatives $u_{xxx}$. For pure sine activations, $\frac{d}{dz}\sin(z) = \cos(z)$ and $\frac{d^3}{dz^3}\sin(z) = -\cos(z)$, which keeps autograd graphs linear in depth without product-rule expansion. In contrast, differentiating Gabor wavelets 3 times generates Hermite polynomial expansions with cross-terms, increasing per-step backward time by 2.4x and causing the model to receive less than half the training iterations within the 300s budget.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert `candidate.py` back to pure SIREN $\sin(z)$. Mark Trial 055 as completed and eligible.

## Reason for decision
Trial 033 achieves 9.2x lower validation loss (0.0005464 vs 0.005034) and provides 2.4x higher step throughput (6,950 vs 2,877 steps). Pure sinusoidal activations are mathematically uniquely suited for 3rd-order PDEs due to closed-form derivative compactness.
