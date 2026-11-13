# Trial 007 Decision Record: Adaptive Gradient Clipping (AGC) with AdamW

## Hypothesis
Applying unit-wise Adaptive Gradient Clipping (AGC; Brock et al., 2021) to AdamW will bound parameter updates relative to layer parameter norms, preventing catastrophic gradient spikes caused by high-curvature collocation points in third-order KdV evaluation while preserving smooth convergence in well-conditioned regions.

## Proposed method change
Retain the incumbent SIREN sinusoidal architecture from Trial 004. In `train_model`, integrate unit-wise Adaptive Gradient Clipping before `context.optimizer_step(optimizer)`:
$$G_l \leftarrow G_l \cdot \min\left(1, \lambda_{\mathrm{AGC}} \frac{\|W_l\|_F^*}{\|G_l\|_F}\right)$$
where $\lambda_{\mathrm{AGC}} = 0.10$ and $\|W_l\|_F^* = \max(\|W_l\|_F, 10^{-3})$.
Use AdamW with base learning rate $1.08\times 10^{-3}$, $\beta=(0.9, 0.99)$, weight decay $5\times 10^{-5}$, and the standard cosine decay schedule.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
AGC prevents transient gradient spikes from perturbing the delicate phase alignment of sinusoidal features, especially during the temporal curriculum expansion phase. We anticipate improved stability in the multi-harmonic case dev_02, potentially pushing validation loss below Trial 004's 0.001260.

## Evidence from previous experiments
Trial 004 achieved the best performance (mean val 0.001260) using sinusoidal activations, but case dev_02 remained an order of magnitude higher (0.003337) than dev_03 (0.000442) and dev_01 (1.83e-6). Trials 003 and 005 demonstrated that global coordinate scaling algorithms (Lion, Adan) struggled with collocation noise. AGC provides targeted local stabilization per parameter tensor.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: adaptive_gradient_clipping_adamw
- Source: Brock et al. (DeepMind 2021), "High-Performance Large-Scale Image Recognition Without Normalization", ICML 2021 / arXiv:2102.06171.
- Distinctness: Genuinely distinct optimization enhancement that replaces unclipped or global-norm gradient clipping with unit-wise, layer-relative norm constraints, preventing destructive parameter steps without distorting gradient scale proportions across layers.

## Observed results
Trial 007 completed all three cases in 891.06 seconds (~7,240-7,400 steps per case).
- Mean validation loss: 0.0022808 (beats baseline Trial 001's 0.0030397, but higher than Trial 004's 0.0012602)
- Case dev_01 validation: 2.8588e-06
- Case dev_02 validation: 0.0050682 (improved over baseline 001's 0.0071730)
- Case dev_03 validation: 0.0017713
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $2.28\times 10^{-6} \le 10^{-3}$).
- Step throughput: Averaged ~24.6 steps/sec compared to ~28.5 steps/sec in unclipped Trial 004 (~14% reduction in steps due to per-tensor norm reductions).

## Agent decision
Do not promote Trial 007 over Trial 004. Retain Trial 004 as the active validation incumbent. Mark `adaptive_gradient_clipping_adamw` as credited novelty in the optimizer category.

## Reason for decision
While AGC proved effective at beating baseline Trial 001 on both mean loss (0.002281 vs 0.003040) and worst case dev_02 (0.005068 vs 0.007173), clipping gradient vectors at 10% of parameter norm slightly dampened productive parameter adjustments in deep residual layers compared to unclipped AdamW. Additionally, computing tensor-wise 2-norms added ~14% latency per step. Unclipped AdamW paired with sinusoidal activations (Trial 004) remains empirically superior. Next, continue broadening exploration into representation and activation methods.
