# Trial 009 Decision Record: Mish Non-Monotonic Smooth Activation

## Hypothesis
Replacing network activations with Mish $\sigma(z) = z \tanh(\ln(1 + e^z))$ (Misra, 2020) will provide smooth $C^\infty$ derivatives without the positive saturation ceiling of $\tanh$, improving gradient propagation through deep residual layers on nonlinear advection and dispersion.

## Proposed method change
Modify `KdVPINN` in `candidate.py`:
1. Use `nn.Mish()` in `in_proj` and across all 7 residual hidden blocks:
$$h_{l+1} = h_l + 0.5 \cdot \text{Mish}(W_l h_l + b_l)$$
2. Retain standard unclipped `AdamW` optimizer (learning rate $1.08\times 10^{-3}$, $\beta=(0.9, 0.99)$, weight decay $5\times 10^{-5}$) with cosine decay and linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Unlike $\tanh$, which asymptotically bounds outputs to $\pm 1$ and suffers severe derivative vanishing in the third spatial derivative $\tanh'''(z)$, Mish is unbounded above ($z \to \infty \implies \text{Mish}(z) \to z$). This allows large wave amplitudes to pass without saturation while preserving a smooth negative dip that self-regularizes small negative values.

## Evidence from previous experiments
Trial 004 established that breaking away from $\tanh$ saturation is essential for 3rd-order KdV (reducing mean loss by 2.4x). Trial 008 showed that compact radial basis kernels suffer from dead zones. Mish offers a non-saturating, non-periodic smooth activation that preserves continuous gradient flow across deep networks.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: mish_smooth_activation
- Source: Misra (BMVC 2020), "Mish: A Self Regularized Non-Monotonic Neural Activation Function", arXiv:1908.08681.
- Distinctness: Represents a distinct class of smooth non-monotonic activations that are unbounded above and bounded below ($\approx -0.31$). This completes the 5 required activation novelty tests in the first 35 trials.

## Observed results
Trial 009 completed all three cases in 891.15 seconds total (~3,415 steps per case).
- Mean validation loss: 0.0296361 (worse than Trial 004's 0.0012602)
- Case dev_01 validation: 0.0001342
- Case dev_02 validation: 0.0598113
- Case dev_03 validation: 0.0289628
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.21\times 10^{-6} \le 10^{-3}$).
- Autograd Profiling: Step throughput dropped to ~11.5 steps/sec (vs ~28.5 steps/sec in Trial 004), resulting in less than half the total optimizer steps (~3,415 vs ~8,450). Third-order differentiation through $z \tanh(\ln(1+e^z))$ generates an exponentially branching computation graph.

## Agent decision
Do not promote Trial 009. Retain Trial 004 as the active validation incumbent. Mark `mish_smooth_activation` as credited novelty in the activation category.

## Reason for decision
While Mish avoids the positive saturation ceiling of $\tanh$, its algebraic composition ($\text{softplus}$ inside $\tanh$) creates massive symbolic autograd expansion under 3rd spatial derivatives $u_{xxx}$. This halved the available training steps within the 300-second budget. Combined with the absence of periodic inductive bias, convergence on dispersive wave dynamics was substantially degraded. Sinusoidal activation (Trial 004) remains unchallenged as the superior activation mechanism.
