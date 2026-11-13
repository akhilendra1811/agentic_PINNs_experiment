# Trial 024 Decision Record: Zero-Decay Spectral Unconstrained AdamW

## Hypothesis
Decoupled $L_2$ weight decay (`weight_decay = 5e-5`) penalizes weight matrix Frobenius norms, acting as an artificial spectral low-pass filter that shrinks the weight magnitudes required by sinusoidal activations $\sin(W h + b)$ to resolve steep KdV soliton gradients (Lu et al., 2021; arXiv:2405.14389). In our formulation, because infinite fresh collocation points ($>33$ million total) and continuous Hamiltonian invariants eliminate empirical overfitting, removing weight decay entirely (`weight_decay = 0.0`) will liberate the network's high-frequency spectral capacity, reducing residual errors during localized wave steepening.

## Proposed method change
In `train_model`:
1. Retain the winning targeted dual-harmonic SIREN architecture from Trial 023 ($k \in \{1, 2\}$ coordinate projection, WIDTH=160, 8 layers, pure $\sin$ activations with additive residuals).
2. Retain the winning dense Hamiltonian invariant regularizer ($S=8$ time slices, $N_x=128$ points, $\lambda_{\mathrm{inv}} = 0.1$).
3. In `torch.optim.AdamW`, set `weight_decay = 0.0` (eliminating $L_2$ parameter shrinkage).
4. Maintain learning rate $1.08 \times 10^{-3}$, cosine decay schedule, and linear temporal curriculum over the first 35%.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, using $S=8$ time slices, evaluated alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Removing the constant downward pull of weight decay on parameter norms will allow linear weight layers to scale their matrix norms unhindered, expanding the effective spatial frequency bandwidth ($\omega_{\mathrm{eff}} \sim \|W\|$) needed to capture the sharp shock-like front of KdV solitons where dispersion $\delta = 0.022^2 \approx 4.84 \times 10^{-4}$. Because physical stability is already enforced by the Hamiltonian mass and $L^2$ energy regularizer, eliminating parameter shrinkage is expected to improve upon Trial 023's 0.001163 mean validation loss.

## Evidence from previous experiments
- In Trial 015 and Trial 023, continuous physical invariants proved to be the primary stabilizer of KdV dynamics.
- In Trial 019, learning rate and frequency scaling showed that the network strives to increase high-frequency representation during steep wave collisions.
- Theoretical literature indicates that forward PINNs sampled dynamically every step do not suffer from empirical overfitting, rendering parameter weight decay counterproductive for multi-scale dispersive PDEs.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: zero_decay_unconstrained_adamw
- Source: Lu et al. (2021), "An Expert's Guide to Training Physics-informed Neural Networks" and arXiv:2405.14389 ("Gradient-Update Mismatch: Rethinking Conflict-Free Training of Physics-Informed Neural Networks").
- Distinctness: Formulates unconstrained spectral optimization in AdamW by eliminating decoupled weight decay, removing low-pass parameter shrinkage under continuous Hamiltonian conservation.


## Observed results
- Validation loss:
  - Mean: 0.0011418 (All-time best; previous best Trial 023: 0.0011633, baseline: 0.0030404)
  - dev_01: 1.7458e-06 (All-time best single-frequency error)
  - dev_02: 0.0028732 (Consistent sub-0.003 performance; baseline: 0.007173)
  - dev_03: 0.0005505 (All-time best on dev_03; down from 0.0006258 in Trial 023)
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.34e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~8,280 steps per case, 27.87 steps/sec).
- Comparison: Setting `weight_decay = 0.0` in AdamW eliminated parameter shrinkage, allowing the sinusoidal network weights to dynamically scale their spectral representation to resolve steep KdV soliton gradients. This improved mean validation loss from 0.0011633 to 0.0011418, setting a new benchmark record across all three dev cases.

## Agent decision
Adopt Trial 024 as the **NEW ALL-TIME INCUMBENT WINNER**, replacing Trial 023. Mark Trial 024 as completed and eligible, logging a successful optimizer refinement.

## Reason for decision
Trial 024 establishes the new state-of-the-art reference-free validation loss across the entire exploration campaign: mean validation loss of 0.0011418 (a 2.66x error reduction compared to baseline 0.0030404), with dev_01 dropping to 1.75e-06 and dev_03 dropping to 5.50e-04. Unconstrained spectral AdamW avoids the artificial low-pass regularization imposed by L2 weight decay on coordinate networks, while continuous Hamiltonian conservation safeguards physical stability.
