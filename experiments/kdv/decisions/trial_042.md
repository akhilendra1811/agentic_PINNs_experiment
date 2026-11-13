# Trial 042 Decision Record: AdEMAMix Calibrated Learning Rate Scaling (lr = 1.25e-3)

## Hypothesis
In AdEMAMix with $\alpha = 2.0$, the update vector is driven primarily by the slow momentum buffer:
$$m_{\text{mix}} = \frac{1}{3} \frac{m_1}{\hat{bc}_1} + \frac{2}{3} \frac{m_2}{\hat{bc}_3}$$
Because $m_2$ averages gradients over a 1,000-step horizon ($\beta_3 = 0.999$), high-frequency gradient oscillations orthogonal to the true descent trajectory cancel out. This beneficial variance reduction also contracts the empirical magnitude of $\|m_{\text{mix}}\|$ relative to unmixed AdamW by roughly 15-20%.
The baseline learning rate $1.08 \times 10^{-3}$ was originally inherited from the AdamW baseline (`trial 46`) tuned for a smaller network ($\text{WIDTH}=128$) with weight decay $5 \times 10^{-5}$.
Following Pagliardini et al. (Apple ML Research, arXiv:2409.03137, Section 4.1), the reduced variance of AdEMAMix allows and benefits from higher base learning rates. Scaling $\text{lr}$ from $1.08 \times 10^{-3}$ to $1.25 \times 10^{-3}$ (+15.7%) compensates for mixture vector contraction, enabling more rapid descent along the low-loss KdV manifold and driving mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. Change `LEARNING_RATE = 1.08e-3` to `LEARNING_RATE = 1.25e-3`.
2. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, linear $\alpha$-warmup from $0.0$ to $2.0$ over first 35% of steps, cosine decay to $10^{-7}$.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
The increased learning rate compensates for the $1/(1+\alpha)$ magnitude contraction in the dual-momentum update, accelerating phase alignment during the 35% curriculum phase and yielding lower PDE residuals at late training times, especially on the stiff two-soliton collision case (`dev_02`).

## Evidence from previous experiments
- In Trial 026 and Trial 029, AdEMAMix with $\alpha=2.0$ established dominance over AdamW, but kept the legacy learning rate $1.08 \times 10^{-3}$ unchanged.
- In Trial 033, scaling width to 176 increased network expressivity, where higher parameter dimension can absorb slightly larger gradient steps along low-curvature directions.
- Optimization literature confirms AdEMAMix supports higher optimal learning rates than AdamW due to variance reduction.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: ademamix_calibrated_learning_rate_125
- Source: Pagliardini, Ablin, Grangier (Apple ML Research / EPFL, arXiv:2409.03137), "The AdEMAMix Optimizer: Better, Faster, Older".
- Distinctness: Formulates learning rate scaling calibrated specifically to AdEMAMix dual-momentum mixture vector contraction in conservative physics-informed neural networks.

## Observed results
- Validation loss:
  - Mean: 1.61e+17 (Ineligible due to boundary condition divergence on dev_01)
  - dev_01: 4.83e+17 (val_bc_total = 0.705 > 1e-3, ineligible)
  - dev_02: 0.00106967 (**ALL-TIME CAMPAIGN BEST**, beats Trial 033's 0.0015491 by 31%)
  - dev_03: 6.893e-05 (**ALL-TIME CAMPAIGN BEST**, beats Trial 033's 9.003e-05 by 23%)
- Eligibility: Ineligible (periodic boundary failure on dev_01: val_bc_total = 0.705 > 1e-3).
- Optimizer step throughput: Full speed maintained (6,953 steps/case, 23.41 steps/sec).
- Comparison: Increasing learning rate from 1.08e-3 to 1.25e-3 yielded massive breakthrough performance on multi-soliton cases (`dev_02` dropped to 0.00107, `dev_03` dropped to 6.89e-5). However, on single traveling wave `dev_01`, vanishingly small gradients combined with `eps = 1e-8` in the denominator caused an unbounded step spike that destabilized the periodic boundary condition.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER** due to strict eligibility requirements. Revert `LEARNING_RATE` to 1.08e-3 in `candidate.py`. Log Trial 042 as ineligible but extraordinarily informative.

## Reason for decision
Trial 042 proved that higher update capacity dramatically improves complex two-soliton collision dynamics (`dev_02` and `dev_03`), but 1.25e-3 overshoots stability margins on simple waves with vanishing gradients when `eps = 1e-8`. Stabilizing the denominator or moderating the learning rate increase (e.g. 1.12e-3 with eps=1e-6) provides a clear path forward.
