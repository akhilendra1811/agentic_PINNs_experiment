# Trial 070 Decision Record: SOAP-AdEMAMix Covariance Smoothing ($\beta_2 = 0.995$)

## Hypothesis
In physics-informed neural networks with stochastic collocation sampling (4,096 fresh uniform points drawn at every step), the empirical gradient outer products $G_t G_t^T$ and $G_t^T G_t$ fluctuate due to Monte Carlo sampling variance.
In our winning SOAP-AdEMAMix configuration (Trial 067), the running Kronecker covariance factor matrices are updated with $\beta_2 = 0.99$:
$$L_t = \beta_2 L_{t-1} + (1 - \beta_2) G_t G_t^T$$
$$R_t = \beta_2 R_{t-1} + (1 - \beta_2) G_t^T G_t$$
Under $\beta_2 = 0.99$, the effective averaging window is $1 / (1 - \beta_2) = 100$ steps (half-life $\approx 69$ steps). Over an 80-step preconditioning interval (`precondition_frequency = 80`), the covariance matrices lose 55% of their prior weight, allowing transient batch-to-batch collocation noise to perturb the eigenvectors $Q_L, Q_R$ and rotated variance $v$.
By increasing $\beta_2$ from $0.99$ to $0.995$:
1. The effective averaging window doubles from 100 to 200 steps (half-life extended to 138 steps).
2. High-frequency Monte Carlo noise in the outer product estimates is substantially smoothed out, yielding more stable and consistent principal curvature axes in $Q_L$ and $Q_R$.
3. The diagonal variance $v$ in rotated coordinates exhibits less step-to-step variance, preventing localized step spikes near narrow minima.
4. Tests whether covariance smoothing improves upon Trial 067's all-time record mean validation loss of `4.689899 \times 10^{-5}`.

## Proposed method change
In `candidate.py`:
1. In `train_model()`, instantiate `SOAPAdEMAMix` with $\beta_2 = 0.995$:
   ```python
   betas = (0.9, 0.995, 0.999)
   ```
2. Retain all other winning hyperparameters of incumbent Trial 067:
   - $\text{WIDTH} = 176, \text{HIDDEN\_LAYERS} = 8$ (219,650 params).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - $\text{LEARNING\_RATE} = 1.15 \times 10^{-3}$, `precondition_frequency = 80`.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Smoother Kronecker factor eigenspaces, reduced collocation gradient noise in rotated coordinate scaling, and deeper convergence on `dev_02`.

## Evidence from previous experiments
- In Trial 064 and 067, $\beta_2 = 0.99$ achieved mean validation losses of $4.857 \times 10^{-5}$ and $4.690 \times 10^{-5}$.
- In first-order AdEMAMix (Trial 029), higher $\beta_2 = 0.999$ was key to stabilizing multi-soliton interaction gradients.
- Perdikaris et al. (2025) noted that accurate Kronecker covariance tracking is critical when loss terms have disparate gradient magnitudes.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false

## Observed results
- Mean validation loss: `8.329886e-05` ($8.33 \times 10^{-5}$) [vs Trial 067: `4.689899e-05`].
- dev_01 validation loss: `7.07071e-07` ($L_{\mathrm{IC}} = 0.0$, $L_{\mathrm{BC}} = 7.18 \times 10^{-10}$).
- dev_02 validation loss: `0.00023066` ($2.31 \times 10^{-4}$) [vs Trial 067: `1.3099 \times 10^{-4}`].
- dev_03 validation loss: `1.85256e-05` ($1.85 \times 10^{-5}$).
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, $L_{\mathrm{BC}} = 2.73 \times 10^{-6} \le 10^{-3}$, parameter count: 219,650).
- Runtime: 891.1s total.

## Agent decision
**REJECT METHOD CHANGE; TRIAL 067 REMAINS INCUMBENT WINNER.**
Revert $\beta_2$ to `0.99` in `candidate.py`.

## Reason for decision
1. **Curvature Inertia under Non-Stationary Curriculum Expansion:**
   During the first 35% of training, the temporal domain expands dynamically from $t \in [0, 0.05]$ to $[0, 1.0]$. A higher $\beta_2 = 0.995$ creates excessive curvature memory (half-life 138 steps), causing the Kronecker covariance factors $L$ and $R$ to lag behind the evolving PDE dynamics.
2. **Superiority of $\beta_2 = 0.99$:**
   $\beta_2 = 0.99$ (half-life 69 steps) closely matches the 80-step eigenspace persistence interval (`precondition_frequency = 80`), adapting briskly to newly exposed domain regions without lag.
3. **Firm Incumbent Position:**
   Trial 067 maintains the lowest recorded mean validation loss (`4.689899e-05`) and worst-case loss (`0.00013099`).
