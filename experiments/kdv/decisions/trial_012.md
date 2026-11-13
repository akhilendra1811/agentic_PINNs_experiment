# Trial 012 Decision Record: Lookahead AdamW Meta-Optimizer

## Hypothesis
Wrapping AdamW in the Lookahead optimizer (Zhang et al., NeurIPS 2019) will dampen stochastic trajectory jitter caused by random collocation sampling without stalling parameter progress, pulling fast-weight exploration back toward a stable descent consensus.

## Proposed method change
Retain the winning SIREN sinusoidal architecture from Trial 004. In `train_model`, wrap `torch.optim.AdamW` in `Lookahead`:
$$\theta_{t, i} = \text{AdamWStep}(\theta_{t, i-1}) \quad \text{for } i = 1, \dots, k$$
$$\phi_t = \phi_{t-1} + \alpha (\theta_{t, k} - \phi_{t-1})$$
$$\theta_{t+1, 0} = \phi_t$$
with lookahead period $k = 5$, slow step size $\alpha = 0.5$, base learning rate $1.08\times 10^{-3}$, cosine decay schedule, and the linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Unlike Trial 011's global iterate averaging (which averaged all weights since step 1, contaminating later stages with early curriculum states), Lookahead updates its slow anchor every $k=5$ steps. This provides local variance reduction while allowing the slow weights to advance along the dynamic curriculum, potentially improving upon Trial 004's 0.001260 loss.

## Evidence from previous experiments
Trial 004 demonstrated that the sinusoidal network is our strongest representation. However, random collocation sampling injects stochastic variance into the gradient at every step. Trials 003 (Lion) and 005 (Adan) showed that modifying inner coordinate scaling was vulnerable to collocation noise. Lookahead operates on outer weight trajectories, smoothing the trajectory without distorting inner Adam dynamics.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: lookahead_adamw
- Source: Zhang, Lucas, Ba, Hinton (NeurIPS 2019), "Lookahead Optimizer: k steps forward, 1 step back", arXiv:1907.08610.
- Distinctness: Genuinely distinct optimization mechanism employing dual-timescale slow and fast weights with periodic linear interpolation, orthogonal to standard inner gradient moments. This completes the 5 required optimizer tests in the first 35 trials.


## Observed results
- Validation loss:
  - Mean: 0.0048087
  - dev_01: 5.3420e-06
  - dev_02: 0.0106920
  - dev_03: 0.0037290
- Eligibility: Eligible (IC = 0.0 <= 1e-3, BC total = 1.99e-6 <= 1e-3 on all 3 cases).
- Comparison: While dev_01 achieved an impressive 5.34e-06, dev_02 (0.010692) and dev_03 (0.003729) underperformed Trial 004's base AdamW (dev_02: 0.003337, dev_03: 0.000442, mean: 0.001260). Interpolating back 50% toward slow weights every 5 steps acted as a damping drag on the parameters, preventing the network from navigating the steep loss ravines associated with high-frequency interaction cases within the 300s budget.

## Agent decision
Retain Trial 004 (SIREN sinusoidal activation with standard AdamW) as the current incumbent winning configuration. Mark Trial 012 as completed and eligible, successfully satisfying the 5th and final required optimizer novelty trial for the early exploration quota. Advance to structural and architectural inductive biases for Trial 013.

## Reason for decision
Lookahead effectively suppressed divergence and ensured high stability (dev_01 reached near machine precision for PDE residuals), but the conservative slow-weight interpolation restricted effective traversal speed across complex multi-soliton phases. Standard AdamW with cosine decay remains the most effective optimizer for the SIREN sinusoidal network among all 6 optimizer variants tested (Lion, Adan, AGC AdamW, Centered RMSprop, Schedule-Free AdamW, Lookahead AdamW). Completing this test fulfills the requirement of at least 5 optimizer-focused novelty trials (Trials 003, 005, 007, 011, 012).
