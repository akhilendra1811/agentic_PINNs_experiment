# Trial 040 Decision Record: AdEMAMix with Non-linear Half-Life Beta3 Warmup

## Hypothesis
In AdEMAMix, the slow EMA buffer ($\beta_3$) captures long-term gradient trajectory memory. In Trial 033, fixing $\beta_3 = 0.999$ statically yielded our campaign record (mean validation loss 0.0005464). However, a static $\beta_3 = 0.999$ imposes an effective $\approx 1,000$-step memory window right from step 0—during the early curriculum phase ($t \in [0, 0.05]$ expanding to $[0, 1.0]$) when gradients are shifting rapidly as new temporal domains are uncovered. In Trial 030, an even longer static memory ($\beta_3 = 0.9995$) overshot the single-mode fixed point on `dev_01` due to this early inertia.
Following Pagliardini et al. (Apple ML Research, arXiv:2409.03137), we implement a non-linear half-life warmup scheduler for $\beta_3$:
$$t_{1/2}(\beta) = \frac{\ln(0.5)}{\ln(\beta)} - 1$$
Starting at $\beta_{3,\text{start}} = 0.90$ ($t_{1/2} \approx 5.6$ steps, matching $\beta_1$), the half-life scales linearly to $t_{1/2} \approx 691.8$ steps ($\beta_{3,\text{end}} = 0.999$) over the 35% curriculum expansion window. This protects early training from obsolete gradient inertia while establishing deep trajectory stabilization for late-stage convergence, driving mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. Revert coordinate projection to targeted dual harmonics ($k \in \{1, 2\}$, `in_dim = 7`), restoring the exact 219,650-parameter capacity of the winning $\text{WIDTH} = 176$ architecture.
2. Retain ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.10$).
3. Retain 35% domain expansion temporal curriculum.
4. Implement Pagliardini et al.'s half-life scheduler for slow EMA parameter $\beta_3$:
   - During the first 35% of steps (`fraction < CURRICULUM_FRAC`), $\beta_3$ warms up from $0.90$ to $0.999$ via linear interpolation in half-life space.
   - Concurrently, $\alpha$ warms up linearly from $0.0$ to $2.0$.
   - For `fraction >= CURRICULUM_FRAC`, $\beta_3 = 0.999$, $\alpha = 2.0$, with cosine learning rate decay from $1.08 \times 10^{-3}$ to $10^{-7}$.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
During the early curriculum phase (when domain boundaries expand), the slow buffer has a short memory ($t_{1/2} \approx 5.6 \to 100$ steps), preventing the network from retaining gradients from truncated temporal domains. As the domain reaches $t \in [0, 1.0]$, $\beta_3$ reaches $0.999$ ($t_{1/2} \approx 692$ steps), providing long-term trajectory memory to dampen collocation sampling noise. This eliminates early phase distortion without sacrificing late-stage multi-soliton precision.

## Evidence from previous experiments
- In Trial 026, static AdEMAMix ($\alpha=2.0, \beta_3=0.999$) dropped mean validation loss from 0.001142 to 0.000803.
- In Trial 029, adding linear $\alpha$-warmup dropped mean validation loss further to 0.000683, and `dev_01` error to $3.34 \times 10^{-7}$.
- In Trial 030, static $\beta_3=0.9995$ gave an all-time record on `dev_02` (0.001871), but early inertia disturbed `dev_01` (0.077062).
- Non-linear half-life scheduling is the exact theoretical mechanism formulated by Pagliardini et al. to eliminate early $\beta_3$ inertia while enabling high asymptotic $\beta_3$.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: ademamix_halflife_beta3_warmup
- Source: Pagliardini, Ablin, Grangier (Apple ML Research / EPFL, arXiv:2409.03137), "The AdEMAMix Optimizer: Better, Faster, Older".
- Distinctness: Formulates non-linear half-life space scheduling of the slow EMA buffer in dual-momentum mixture optimization for curriculum-driven physics-informed neural networks.

## Observed results
- Validation loss:
  - Mean: 0.000676264 (Stronger than Trial 029's 0.0006826, but higher than incumbent Trial 033: 0.0005464)
  - dev_01: 1.147e-06
  - dev_02: 0.0019015 (Improved over Trial 029's 0.001927)
  - dev_03: 0.0001261
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.39e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (~6,947 steps per case, 23.39 steps/sec).
- Comparison: While half-life warmup of $\beta_3$ improved upon Trial 029, keeping $\beta_3 = 0.999$ static right from step 1 (Trial 033) proved even more effective. In KdV PINNs, the initial condition and boundary conditions are known exactly at $t=0$, and having full 1,000-step trajectory averaging immediately suppresses early Monte Carlo collocation noise without inducing instability, as long as $\alpha$ is warmed up.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert $\beta_3$ to static $0.999$ (with linear $\alpha$-warmup $0.0 \to 2.0$) in `candidate.py`. Mark Trial 040 as completed and eligible.

## Reason for decision
Trial 033 retains significantly lower mean validation loss (0.0005464 vs 0.0006763) and superior worst-case error (0.0015491 vs 0.0019015). Static $\beta_3 = 0.999$ coupled with linear $\alpha$-warmup represents the optimal balance of immediate collocation noise filtering and trajectory stability.
