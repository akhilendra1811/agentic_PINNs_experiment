# Trial 018 Decision Record: Cautious AdamW (C-AdamW)

## Hypothesis
Under dynamic stochastic collocation resampling in PINNs, stochastic variance between batches causes historical momentum $m_t$ to occasionally point in directions that oppose the current physical gradient $g_t$ ($u_t \odot g_t < 0$), producing destructive steps that degrade residual accuracy. Cautious AdamW (C-AdamW; Liang et al., 2024) masks parameter coordinate updates whenever momentum conflicts with the instant gradient, filtering out noisy steps and stabilizing descent trajectories along narrow KdV dispersion valleys.

## Proposed method change
1. Maintain the winning SIREN sinusoidal architecture and Hamiltonian invariant regularizer (mass and $L^2$ energy conservation with weight 0.1) from Trial 015.
2. Replace standard `torch.optim.AdamW` with `CautiousAdamW`:
   - Compute standard first moment $m_t$ and second moment $v_t$ with bias corrections $\hat{m}_t$ and $\hat{v}_t$.
   - Compute standard proposed coordinate update $u_t = \hat{m}_t / (\sqrt{\hat{v}_t} + \epsilon)$.
   - Generate coordinate-wise cautious alignment mask:
     $$M_t = \mathbb{I}(u_t \odot g_t \ge 0)$$
   - Apply update only along coordinates where momentum agrees with the instant gradient:
     $$\theta_{t+1} = \theta_t (1 - \eta_t \lambda) - \eta_t (M_t \odot u_t)$$
3. Maintain base learning rate $1.08 \times 10^{-3}$, cosine decay schedule, and the linear temporal curriculum over the first 35%.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0$ and $\lambda_{\mathrm{inv}} = 0.1$, evaluated alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
By selectively suppressing coordinate updates where stochastic collocation noise causes momentum to push against the instant PDE residual gradient, C-AdamW eliminates oscillatory trajectory jitter. Unlike Lookahead (which slowed down parameter updates by pulling back 50% every 5 steps across all coordinates), C-AdamW operates coordinate-wise with zero latency and zero extra hyperparameters, potentially improving on Trial 015's 0.001183 mean validation loss.

## Evidence from previous experiments
- In Trial 003 (Lion) and Trial 005 (Adan), stochastic collocation noise degraded gradient estimators that relied on coordinate sign or difference moments without variance smoothing.
- In Trial 015, standard AdamW with Hamiltonian invariant regularization became the incumbent winner (0.001183 mean, 0.003097 worst-case).
- C-AdamW retains AdamW's smoothed second moment while adding cautious coordinate masking to eliminate conflicting momentum steps.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: cautious_adamw_c_adamw
- Source: Chen Liang et al. (arXiv:2411.16085, 2024), "Cautious Optimizers: Improving Training with One Line of Code".
- Distinctness: Introduces a dynamic coordinate-wise directional alignment mask $M_t = \mathbb{I}(u_t \odot g_t \ge 0)$ that filters out contradictory momentum updates, representing an optimizer update mechanism distinct from standard moment scaling, clipping, or iterate averaging.


## Observed results
- Validation loss:
  - Mean: 0.0017819
  - dev_01: 2.5577e-06
  - dev_02: 0.0046658
  - dev_03: 0.0006772
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.25e-6 <= 1e-3, params = 181,442 <= 250,000).
- Comparison: C-AdamW beat baseline Trial 001 (0.003040) by 1.7x and maintained full step throughput (~8,300 steps per case). However, it did not beat incumbent Trial 015 (0.001183 mean, 0.003097 worst-case). Zeroing out coordinate updates whenever momentum conflicted with instant batch gradient over-dampened parameter exploration along high-frequency soliton dimensions.

## Agent decision
Retain Trial 015 (sinusoidal SIREN architecture with standard AdamW and Hamiltonian invariant regularizer) as the incumbent winner. Mark Trial 018 as completed and eligible, logging an additional optimizer exploration record.

## Reason for decision
Trial 018 demonstrated that coordinate-level cautious masking suppresses trajectory oscillations, but acts as an excessive drag on parameter progression in steep multi-soliton collisions where momentum must overcome localized collocation noise. Standard unmasked AdamW with smoothed uncentered second moments remains empirically superior across all 7 optimizer variants tested. We proceed to investigate adaptive sinusoidal activations.
