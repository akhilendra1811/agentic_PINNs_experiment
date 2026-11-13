# Trial 045 Decision Record: Cosine Decay Terminal Floor Calibration (eta_min = 3.5e-5)

## Hypothesis
In Trial 033 (incumbent winner), the cosine learning rate schedule annealed the base learning rate $1.08 \times 10^{-3}$ down to $\eta_{\min} = 10^{-7}$ over the final 65% of steps:
$$\eta(t) = \eta_{\min} + \frac{1}{2}(\eta_{\max} - \eta_{\min}) \left(1 + \cos(\pi \tau)\right)$$
Decaying all the way to $10^{-7}$ causes parameter updates $\Delta \theta = -\eta \cdot m_{\text{mix}} / (\sqrt{v} + \epsilon)$ to vanish during the final 15–20% of training steps (steps ~5,500 to ~6,950), prematurely halting optimization and leaving late-stage residual minimization under-exploited.
Following standard modern cosine annealing practice (Loshchilov & Hutter; Touvron et al., 2023), establishing an asymptotic floor at $\eta_{\min} = 3.5 \times 10^{-5}$ (~3.2% of $\eta_{\max}$) maintains an active, stable descent velocity through the final phase of training. This will allow the optimizer to continue polishing the complex two-soliton collision waveform on `dev_02` down to the final step without risking high-learning-rate divergence on `dev_01`, driving mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. In `train_model`, replace:
   `lr_curr = 1e-7 + 0.5 * (LEARNING_RATE - 1e-7) * (1.0 + math.cos(math.pi * phase2_frac))`
   with:
   `lr_min = 3.5e-5`
   `lr_curr = lr_min + 0.5 * (LEARNING_RATE - lr_min) * (1.0 + math.cos(math.pi * phase2_frac))`
2. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$, linear $\alpha$-warmup from $0.0$ to $2.0$ over first 35% of steps.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
The non-zero learning rate floor ensures that the optimizer continues refining parameters during the final 1,000 steps rather than stalling at near-zero step size. Because $\eta_{\min} = 3.5 \times 10^{-5}$ is small and well-conditioned, it maintains absolute numerical stability on simple waves (`dev_01`) while enabling active fine-tuning on complex waves (`dev_02` and `dev_03`).

## Evidence from previous experiments
- In Trial 033, the model showed continuous improvement up to the final snapshot, suggesting convergence was cut short by vanishing learning rate.
- In Trial 042, higher update capacity achieved all-time records on `dev_02` (0.00107) and `dev_03` (6.89e-5). A non-zero terminal floor allows the network to benefit from non-vanishing updates specifically at the end of training when loss curvature is highest.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: cosine_decay_terminal_floor_calibration
- Source: Loshchilov & Hutter (ICLR 2017); Touvron et al. (arXiv:2302.13971).
- Distinctness: Calibrates the non-zero asymptotic learning rate floor for terminal convergence in curriculum-trained PINNs.

## Observed results
- Validation loss:
  - Mean: 0.00055965 (Close second to incumbent Trial 033: 0.0005464)
  - dev_01: 5.07e-06
  - dev_02: 0.00152872 (**NEW ALL-TIME ELIGIBLE RECORD on dev_02**, beats Trial 033's 0.0015491)
  - dev_03: 0.00014517
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.48e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (6,942 steps/case, 23.37 steps/sec).
- Comparison: Setting $\eta_{\min} = 3.5 \times 10^{-5}$ successfully prevented late-stage optimization freezing, driving `dev_02` to an all-time eligible record of 0.0015287. However, for simpler cases (`dev_01` and `dev_03`), maintaining $3.5 \times 10^{-5}$ prevented final asymptotic micro-settling into the narrowest loss valley (where $10^{-7}$ reached $1.76 \times 10^{-7}$ and $9.00 \times 10^{-5}$).

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER** for overall mean validation loss (0.0005464 vs 0.0005596), while recognizing Trial 045 as the new record-holder on the hardest two-soliton collision case (`dev_02`: 0.0015287). Mark Trial 045 as completed and eligible.

## Reason for decision
Trial 033 maintains slightly lower overall mean validation loss across all 3 cases (0.0005464). A slightly lower terminal floor (e.g. $\eta_{\min} = 1.0 \times 10^{-5}$) could capture the best of both worlds.
