# Trial 047 Decision Record: Synchronized Smooth Cosine Domain and Alpha Curriculum

## Hypothesis
In Trial 033 (incumbent winner), both temporal domain expansion ($t_{\text{scale}}: 0.05 \to 1.0$) and AdEMAMix mixture weight warmup ($\alpha: 0.0 \to 2.0$) follow piecewise-linear schedules over the first 35% of steps (`CURRICULUM_FRAC = 0.35`). At the 35% boundary, the expansion velocity $d(t_{\text{scale}})/dt$ and mixture ramp $d\alpha/dt$ drop discontinuously from positive values to zero. This $C^0$ slope kink produces transient optimization shocks when the full domain and full slow momentum weight are suddenly engaged simultaneously.
Following Krishnapriyan et al. (NeurIPS 2021, arXiv:2109.01050), we replace the piecewise-linear schedules with synchronized $C^1$-smooth cosine pacing:
$$\tau = \frac{\text{fraction}}{\text{CURRICULUM\_FRAC}}, \quad \mu(\tau) = \frac{1 - \cos(\pi \tau)}{2}$$
$$t_{\text{scale}}(\tau) = 0.05 + 0.95 \cdot \mu(\tau), \quad \alpha(\tau) = 2.0 \cdot \mu(\tau)$$
This formulation provides two distinct mathematical advantages:
1. Zero expansion velocity at $\tau = 0$ ($t_{\text{scale}} \approx 0.05$ for longer) grants the network extended time to lock the fundamental solitary wave phase and spatial derivatives during the initial steepening interval.
2. Zero acceleration and zero velocity entering $\tau = 1.0$ smoothly transitions the network into the full domain $[0, 1.0]$ and full slow momentum regime ($\alpha = 2.0$) without boundary shocks, stabilizing late-stage convergence and driving mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. In `train_model`, update the curriculum expansion and $\alpha$-warmup logic during `fraction < CURRICULUM_FRAC`:
   ```python
   tau = fraction / CURRICULUM_FRAC
   smooth_ramp = 0.5 * (1.0 - math.cos(math.pi * tau))
   t_scale = 0.05 + 0.95 * smooth_ramp
   alpha_curr = 2.0 * smooth_ramp
   ```
2. For `fraction >= CURRICULUM_FRAC`:
   `t_scale = 1.0`, `alpha_curr = 2.0`, with standard cosine decay of learning rate down to $10^{-7}$.
3. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Smooth $C^1$ transition eliminates gradient shocks at the 35% mark, while the gentler start allows better early soliton formation on `dev_02` without compromising the proven stability on `dev_01`.

## Evidence from previous experiments
- In Trial 017, smooth cosine pacing on the baseline network achieved strong early convergence (0.001366).
- In Trial 033, the linear curriculum achieved the all-time record, but inspect logs showed transient residual jumps around the 35% transition.
- Cosine pacing provides a continuous velocity profile across domain and momentum schedules.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: smooth_cosine_domain_and_alpha_curriculum
- Source: Krishnapriyan et al. (NeurIPS 2021, arXiv:2109.01050), "Characterizing possible failure modes in physics-informed neural networks".
- Distinctness: Introduces synchronized $C^1$-smooth cosine pacing for both temporal domain expansion and AdEMAMix dual-momentum mixture warmup in periodic KdV PINNs.

## Observed results
- Validation loss:
  - Mean: 0.026350 (Higher than incumbent Trial 033: 0.0005464)
  - dev_01: 0.076998
  - dev_02: 0.00194911
  - dev_03: 0.00010357
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.32e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (6,943 steps/case, 23.37 steps/sec).
- Comparison: While cosine pacing smooths boundary entry and exit, it concentrates temporal expansion velocity into the middle window ($\tau \in [0.4, 0.7]$), where $d(t_{\text{scale}})/dt$ surges to nearly double the constant linear rate. On single traveling wave `dev_01`, this sudden expansion velocity spike outpaced the optimizer's tracking speed, causing phase lag. Constant-velocity linear expansion (`t_scale = 0.05 + 0.95 * fraction / 0.35`) provides steady, uniform optimization time per temporal interval.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert `candidate.py` back to constant-velocity linear curriculum expansion and linear $\alpha$-warmup. Mark Trial 047 as completed and eligible.

## Reason for decision
Trial 033 retains vastly superior mean validation loss (0.0005464 vs 0.026350). Linear domain expansion ensures uniform step density across temporal expansion without mid-phase velocity surges.
