# Trial 049 Decision Record: Two-Stage Active Cosine with Terminal Cooldown Quench

## Hypothesis
Our campaign has revealed a fundamental dichotomy between simple travelling waves (`dev_01`) and stiff two-soliton collisions (`dev_02`):
- In Trial 045, maintaining an active learning rate floor ($\eta_{\min} = 3.5 \times 10^{-5}$) allowed continuous active gradient descent on the stiff two-soliton collision, achieving our all-time eligible record on `dev_02` (`0.0015287`). However, holding $3.5 \times 10^{-5}$ up to the final step prevented asymptotic microscale settling on `dev_01` ($5.07 \times 10^{-6}$).
- In Trial 033, decaying all the way to $10^{-7}$ enabled sub-microscale precision on `dev_01` ($1.76 \times 10^{-7}$), but prematurely stalled convergence on `dev_02` (`0.0015491`).
Following modern Warmup-Stable-Decay / mini-cooldown optimization theory (Hägele et al., 2024, arXiv:2405.18392), we decouple active representation learning from terminal convergence using a two-stage decay schedule:
1. **Phase 2 (Active Descent Phase, $\text{fraction} \in [0.35, 0.85]$):**
   The learning rate decays smoothly from $1.08 \times 10^{-3}$ down to $\eta_{\text{active}} = 3.5 \times 10^{-5}$ via cosine annealing:
   $$\eta(t) = 3.5 \times 10^{-5} + \frac{1}{2}(1.08 \times 10^{-3} - 3.5 \times 10^{-5})(1 + \cos(\pi \cdot p_2)), \quad p_2 = \frac{\text{fraction} - 0.35}{0.50}$$
2. **Phase 3 (Terminal Mini-Cooldown Quench, $\text{fraction} \in [0.85, 1.0]$):**
   Over the final 15% of steps (steps ~5,900 to 6,950), the learning rate quenches smoothly from $3.5 \times 10^{-5}$ down to $10^{-7}$:
   $$\eta(t) = 10^{-7} + \frac{1}{2}(3.5 \times 10^{-5} - 10^{-7})(1 + \cos(\pi \cdot p_3)), \quad p_3 = \frac{\text{fraction} - 0.85}{0.15}$$
This two-stage schedule combines the active descent depth of Trial 045 on two-soliton collisions with the terminal asymptotic micro-settling of Trial 033 on simple waves, driving overall mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. In `train_model`, update the post-curriculum learning rate schedule:
   ```python
        if fraction < CURRICULUM_FRAC:
            lr_curr = LEARNING_RATE
            alpha_curr = 2.0 * (fraction / CURRICULUM_FRAC)
        elif fraction < 0.85:
            alpha_curr = 2.0
            p2 = (fraction - CURRICULUM_FRAC) / (0.85 - CURRICULUM_FRAC)
            lr_active = 3.5e-5
            lr_curr = lr_active + 0.5 * (LEARNING_RATE - lr_active) * (
                1.0 + math.cos(math.pi * p2)
            )
        else:
            alpha_curr = 2.0
            p3 = (fraction - 0.85) / 0.15
            lr_active = 3.5e-5
            lr_curr = 1e-7 + 0.5 * (lr_active - 1e-7) * (
                1.0 + math.cos(math.pi * p3)
            )
   ```
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
Phase 2 provides 50% of the entire budget with active learning rates ($\ge 3.5 \times 10^{-5}$), resolving complex multi-soliton collisions on `dev_02` down to $\approx 0.0015$. Phase 3 then applies a gentle terminal quench, freezing the trajectory inside the narrow minimum on `dev_01` and `dev_03` without disturbing `dev_02`.

## Evidence from previous experiments
- In Trial 045, maintaining $\ge 3.5 \times 10^{-5}$ drove `dev_02` to our all-time record 0.0015287.
- In Trial 033, decaying to $10^{-7}$ drove `dev_01` to our all-time record $1.76 \times 10^{-7}$.
- Combining active descent with a terminal cooldown matches modern WSD optimization best practices.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: twostage_active_cosine_with_terminal_cooldown_quench
- Source: Hägele et al. (arXiv:2405.18392, 2024), "Scaling Laws and Compute-Optimal Training via Two-Stage Learning Rate Schedules".
- Distinctness: Formulates a two-stage active cosine decay with terminal mini-cooldown quench to simultaneously optimize complex soliton collision depth and simple wave asymptotic settling.

## Observed results
- Validation loss:
  - Mean: 0.00077445 (Higher than incumbent Trial 033: 0.0005464)
  - dev_01: 3.53e-07 (Sub-microscale precision successfully preserved)
  - dev_02: 0.00222735
  - dev_03: 9.57e-05
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.39e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (6,945 steps/case, 23.38 steps/sec).
- Comparison: The two-stage schedule successfully confirmed that the terminal quench down to $10^{-7}$ locks in sub-microscale precision on `dev_01` ($3.53 \times 10^{-7}$). However, confining the terminal quench to the final 15% (fraction 0.85 to 1.0) was too abrupt for `dev_02`: the continuous single-stage cosine decay of Trial 033 gives `dev_02` a longer and smoother cooling window across the entire post-curriculum phase.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert `candidate.py` back to single-stage continuous cosine decay down to $10^{-7}$. Mark Trial 049 as completed and eligible.

## Reason for decision
Trial 033 retains significantly lower mean validation loss (0.0005464 vs 0.0007745) and superior worst-case error (0.0015491 vs 0.0022274). Single-stage continuous cosine decay across the entire 65% post-curriculum window provides the optimal cooling duration.
