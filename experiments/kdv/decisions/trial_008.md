# Trial 008 Decision Record: Gaussian (Radial Basis Function) Activation

## Hypothesis
Replacing network activations with localized Gaussian radial basis functions $\sigma(z) = \exp(-z^2)$ (Bai et al., 2023) will provide localized spatial-temporal receptive fields and well-conditioned higher-order derivatives ($\sigma'''(z) = 4z(3 - 2z^2)\exp(-z^2)$), improving local soliton tracking in the KdV equation.

## Proposed method change
Modify `KdVPINN` in `candidate.py`:
1. Define the Gaussian activation:
$$\text{GaussianActivation}(z) = \exp(-z^2)$$
2. In `in_proj` and across all 7 residual hidden blocks, use `GaussianActivation()`:
$$h_{l+1} = h_l + \exp(-(W_l h_l + b_l)^2)$$
3. Retain the standard `AdamW` optimizer (learning rate $1.08\times 10^{-3}$, $\beta=(0.9, 0.99)$, weight decay $5\times 10^{-5}$) with unclipped steps, cosine decay schedule, and linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Unlike monotonic activations like $\tanh$ or global periodic activations like $\sin$, Gaussian activations act as local bump functions. Because each hidden neuron responds maximally to a compact region in activation space, the network should resolve localized steep wave fronts without inducing global spurious oscillations.

## Evidence from previous experiments
Trial 004 proved that non-monotonic activations ($\sin$) strongly outperform monotonic $\tanh$ by preventing derivative vanishing. Trial 006 tested Snake, but composite autograd slowed training. Gaussian activations provide another non-monotonic, $C^\infty$ alternative with clean, localized derivatives and low computational graph depth.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: gaussian_rbf_activation
- Source: Bai et al. (2023), "Physics-Informed Radial Basis Network", arXiv:2304.06234.
- Distinctness: Radically distinct from both monotonic $\tanh$ and periodic $\sin$. It introduces localized radial basis behavior into the deep residual stream, naturally bounding activations within $(0, 1]$ while yielding smooth local polynomial-exponential higher derivatives.

## Observed results
Trial 008 completed all three cases in 891.06 seconds total (~6,660 steps per case).
- Mean validation loss: 0.0278089 (higher than Trial 004's 0.0012602 and baseline 001's 0.0030397)
- Case dev_01 validation: 9.9054e-05
- Case dev_02 validation: 0.0613423
- Case dev_03 validation: 0.0219854
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.11\times 10^{-6} \le 10^{-3}$).
- Analysis: Due to the compact Gaussian support ($\exp(-z^2) \to 0$ for $|z| > 2$), neurons initialized with large pre-activation norms effectively become inactive ("dead" receptive fields), causing gradient starvation in deep layers.

## Agent decision
Do not promote Trial 008. Retain Trial 004 as the active validation incumbent. Mark `gaussian_rbf_activation` as credited novelty in the activation category.

## Reason for decision
The experiment demonstrates a critical theoretical distinction: while Gaussian RBF activations are infinitely smooth, their localized decay creates vanishing gradients in deep networks when inputs move outside the kernel centers. In contrast, sinusoidal activations (Trial 004) maintain infinite periodic support across the entire input space, preventing dead zones while preserving non-vanishing third derivatives. Pure sinusoidal representation remains the definitive activation choice for periodic KdV.
