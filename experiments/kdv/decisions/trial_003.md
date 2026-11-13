# Trial 003 Decision Record: Lion (EvoLved Sign Momentum) Optimizer

## Hypothesis
Replacing AdamW with the Lion optimizer (Chen et al., 2023) will improve optimization stability and reduce empirical KdV PDE residual loss by bounding parameter update magnitudes uniformly through the sign operation, preventing gradient variance spikes caused by dynamic Monte Carlo collocation sampling under third-order differentiation.

## Proposed method change
Revert the network architecture to the clean baseline 8-layer residual MLP (width 160, static tanh activations, no learnable slope parameters). Replace the optimizer in `train_model` from `torch.optim.AdamW` to `Lion`:
$$\theta_t = \theta_{t-1} - \eta_t (\text{sign}(\beta_1 m_{t-1} + (1 - \beta_1) g_t) + \lambda \theta_{t-1})$$
$$m_t = \beta_2 m_{t-1} + (1 - \beta_2) g_t$$
with $\beta_1 = 0.9, \beta_2 = 0.99, \lambda = 10^{-4}$, base learning rate $\eta_0 = 3.2\times 10^{-4}$ (scaled down from AdamW due to unit magnitude sign updates), and preserve the identical cosine decay schedule and linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Because Lion updates each coordinate by $\pm \eta_t$ rather than scaling by $1/\sqrt{v_t + \epsilon}$, it should resist sudden gradient magnitude explosions when collocation points land in steep dispersive wave fronts. We anticipate faster per-step execution (only one momentum state buffer) and potential reduction in dev_02 validation loss.

## Evidence from previous experiments
Trial 001 demonstrated that AdamW achieves mean validation loss 0.003040, but suffers in the multi-harmonic case dev_02 (loss 0.007173). Trial 002 showed that activation slope adaptation added computational overhead without improving residual convergence. Testing an alternative optimizer algorithm addresses the optimization dynamics directly without touching the backbone architecture.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: lion_sign_momentum_optimizer
- Source: Chen et al. (Google Brain 2023), "Symbolic Discovery of Optimization Algorithms", arXiv:2302.06675.
- Distinctness: Radically different optimization paradigm compared to AdamW. It eliminates second-moment variance division entirely, relying instead on sign-based momentum interpolation discovered via symbolic evolutionary program synthesis.

## Observed results
Trial 003 completed all three development cases in 891.07 seconds total (~8,650-8,770 optimizer steps per case, confirming ~2% higher step throughput than AdamW).
- Mean validation loss: 0.0079624
- Case dev_01 validation: 6.5261e-07 (achieved a remarkable ~4.6x improvement over Trial 001's 3.0361e-06)
- Case dev_02 validation: 0.0158848 (worse than 001's 0.0071730)
- Case dev_03 validation: 0.0080016 (worse than 001's 0.0019431)
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.45\times 10^{-6} \le 10^{-3}$).

## Agent decision
Do not promote Trial 003 to incumbent. Retain Trial 001 as the active validation incumbent. Mark `lion_sign_momentum_optimizer` as credited novelty in the optimizer category.

## Reason for decision
Lion demonstrated exceptional precision on the single-harmonic soliton case dev_01 (reaching 6.53e-07), verifying that sign-bounded momentum provides clean descent on smooth solitary waves. However, for multi-harmonic cases with high spatial frequencies (dev_02 and dev_03), coordinate-wise uniform magnitude updates without adaptive variance scaling required more steps than available in the 300-second budget to resolve intricate wave packet interactions. The hypothesis is validated regarding step throughput and smooth wave precision, but AdamW remains superior in aggregate. Next, explore another distinct candidate family (e.g. Snake periodic activation).
