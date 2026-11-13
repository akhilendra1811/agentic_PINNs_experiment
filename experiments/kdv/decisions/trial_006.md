# Trial 006 Decision Record: Snake Periodic Activation Function

## Hypothesis
Replacing the hidden layer activations with the Snake activation function $\sigma(z) = z + \sin^2(z)$ (Ziyin et al., 2020) will provide an inductive bias towards periodic waveforms while maintaining unobstructed linear gradient flow, accelerating convergence and potentially improving upon Trial 004's pure sinusoidal baseline.

## Proposed method change
Modify `KdVPINN` in `candidate.py`:
1. Define the `Snake` activation:
$$\text{Snake}(z) = z + \sin^2(z)$$
2. Use `Snake()` in `in_proj` and across all 7 residual blocks:
$$h_{l+1} = h_l + 0.5 \cdot \text{Snake}(W_l h_l + b_l)$$
3. Retain the standard `AdamW` optimizer (learning rate $1.08\times 10^{-3}$, $\beta=(0.9, 0.99)$, weight decay $5\times 10^{-5}$) with cosine decay and linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
The first derivative of Snake is $1 + \sin(2z) \ge 0$, which guarantees monotonic non-negative gradient propagation across deep layers. The third derivative is $-4\sin(2z)$, which oscillates with doubled frequency without vanishing. This combination could offer the periodic advantages observed in Trial 004 while avoiding optimization instabilities associated with pure unconstrained sinusoidal networks.

## Evidence from previous experiments
Trial 004 demonstrated that periodic activations drastically outperform monotonic tanh (mean loss reduced from 0.003040 to 0.001260). However, pure $\sin(z)$ can exhibit sensitivity to weight initialization. Snake was specifically proposed by Ziyin et al. to cure this dilemma by hybridizing an identity slope with a periodic $\sin^2$ term.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: snake_periodic_activation
- Source: Ziyin, Hartwig, Ueda (NeurIPS 2020), "Neural Networks Fail to Learn Periodic Functions and How to Fix It", arXiv:2006.08195.
- Distinctness: Genuinely novel activation function that blends identity forward mapping with periodic inductive bias. It is $C^\infty$ smooth with non-vanishing third derivatives, mathematically tailored for periodic boundary value problems and dispersive wave equations.

## Observed results
Trial 006 completed all three cases in 891.07 seconds total.
- Mean validation loss: 0.0062124 (worse than Trial 004's 0.0012602)
- Case dev_01 validation: 1.0382e-06 (nearly 3x lower than baseline 001's 3.0361e-06)
- Case dev_02 validation: 0.0160910
- Case dev_03 validation: 0.0025453
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.69\times 10^{-6} \le 10^{-3}$).
- Throughput: Completed ~5,250 optimizer steps per case compared to ~8,450 in Trial 004 (~37% slower per step). Evaluating the composite function $z + \sin^2(z)$ through 3rd-order spatial autograd produces a substantially deeper symbolic computation graph than pure $\sin(z)$.

## Agent decision
Do not promote Trial 006. Retain Trial 004 (SIREN pure $\sin(x)$) as the active validation incumbent. Mark `snake_periodic_activation` as credited novelty in the activation category.

## Reason for decision
While Snake verified the power of periodic inductive bias on the single-harmonic soliton case dev_01 (1.04e-06), the compounding polynomial-trigonometric terms in $\frac{\partial^3}{\partial x^3}[z + \sin^2(z)]$ significantly increased backward autograd overhead per step. Under the strict 300-second wall-clock budget, this ~37% drop in optimizer throughput penalized convergence on multi-frequency cases. Pure sinusoidal activations from Trial 004 remain the optimal balance of spectral representation and computational efficiency.
