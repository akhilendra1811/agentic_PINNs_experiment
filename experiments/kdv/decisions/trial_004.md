# Trial 004 Decision Record: Sinusoidal Periodic Activation (SIREN)

## Hypothesis
Replacing the hyperbolic tangent ($\tanh$) activation function with periodic sinusoidal ($\sin$) activations in all hidden layers (SIREN; Sitzmann et al., 2020) will prevent higher-order derivative vanishing, improving the resolution of high-frequency oscillatory KdV dispersive structures.

## Proposed method change
Modify `KdVPINN` in `candidate.py`:
1. In the input projection block, replace `nn.Tanh()` with `SinActivation()` ($\sin(x)$).
2. In all 7 residual hidden blocks, replace `torch.tanh(layer(h))` with `torch.sin(layer(h))`.
3. Restore the optimizer to standard `AdamW` (learning rate $1.08\times 10^{-3}$, $\beta=(0.9, 0.99)$, weight decay $5\times 10^{-5}$), identical to baseline Trial 001.
No other architectural or scheduling modifications are made.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Because the derivative of $\sin(x)$ is $\cos(x)$, and the third derivative is $-\cos(x)$, the network's higher-order spatial derivatives will maintain full amplitude and avoid the vanishing gradients typical of $\tanh$ when saturated. This is expected to directly assist multi-frequency dispersive wave interactions (dev_02 and dev_03).

## Evidence from previous experiments
In Trial 001, baseline $\tanh$ yielded dev_02 loss 0.007173 (much higher than dev_01 3.04e-6). In Trial 002, adapting the slope of $\tanh$ added autograd overhead without altering the underlying saturation envelope. In Trial 003, Lion showed that the backbone representation itself is the bottleneck for multi-frequency waves. Switching to periodic sinusoidal activations targets this representation directly.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: siren_sinusoidal_activation
- Source: Sitzmann et al. (NeurIPS 2020), "Implicit Neural Representations with Periodic Activation Functions", arXiv:2006.09661.
- Distinctness: Represents a fundamental shift from monotonic saturating functions ($\tanh$) to periodic non-monotonic activations ($\sin$). Because derivatives of sinusoidal networks are themselves sinusoidal networks, all higher derivatives retain non-zero spectral features without vanishing.

## Observed results
Trial 004 completed all three cases in 891.06 seconds total (~8,400 to 8,490 optimizer steps per case on MPS).
- Mean validation loss: 0.0012602 (a massive 58.5% reduction / 2.41x improvement relative to baseline Trial 001's 0.0030397)
- Case dev_01 validation: 1.8262e-06 (1.66x improvement over baseline 3.0361e-06)
- Case dev_02 validation: 0.0033373 (2.15x improvement over baseline 0.0071730 on the most challenging multi-harmonic case)
- Case dev_03 validation: 0.0004416 (4.40x improvement over baseline 0.0019431)
- Worst development case: 0.0033373 (reduced from baseline 0.0071730)
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $2.50\times 10^{-6} \le 10^{-3}$).

## Agent decision
Promote Trial 004 to the new active empirical incumbent. It soundly beats Trial 001 on reference-free validation across all development cases while maintaining identical parameter count (181,442) and full eligibility.

## Reason for decision
The experimental evidence decisively supports the hypothesis: replacing $\tanh$ with periodic sinusoidal ($\sin$) activations overcomes higher-order derivative attenuation. In the KdV equation, evaluating $0.022^2 u_{xxx}$ requires calculating the third spatial derivative. Under $\tanh$, the third derivative $\tanh'''(z) = 2 \text{sech}^2(z)(2 - 3\text{sech}^2(z))$ decays exponentially to zero outside the central origin. Under $\sin$, the third derivative is $-\cos(z)$, maintaining full derivative signal fidelity across all spatial frequencies. This directly slashed error on the multi-frequency test cases dev_02 and dev_03. Retain this architectural breakthrough while continuing broad methodological exploration in subsequent trials.
