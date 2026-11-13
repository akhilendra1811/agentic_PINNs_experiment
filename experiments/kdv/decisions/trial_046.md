# Trial 046 Decision Record: Cosine Decay Refined Floor Calibration (eta_min = 1.0e-5)

## Hypothesis
In Trial 045, establishing an asymptotic learning rate floor of $\eta_{\min} = 3.5 \times 10^{-5}$ achieved a new all-time eligible record on `dev_02` (`0.0015287` vs Trial 033's `0.0015491`). However, $3.5 \times 10^{-5}$ left `dev_01` at $5.07 \times 10^{-6}$, slightly above its microscale potential ($1.76 \times 10^{-7}$ in Trial 033). Conversely, Trial 033 decayed all the way down to $10^{-7}$, which enabled sub-microscale precision on `dev_01` but prematurely froze optimization on `dev_02`.
A refined terminal floor at $\eta_{\min} = 1.0 \times 10^{-5}$ (~0.93% of base lr) resolves this trade-off:
- It is small enough to suppress discrete stepping oscillations on simple waves (`dev_01` and `dev_03`), allowing parameters to settle deeply into the microscale loss minimum.
- It is 100x larger than $10^{-7}$, providing enough active descent velocity during the final 1,000 steps to polish the stiff two-soliton collision waveform on `dev_02`.
This synthesis is expected to simultaneously achieve record-low `dev_02` error alongside sub-microscale `dev_01` precision, driving overall mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. In `train_model`, update the cosine learning rate decay floor:
   ```python
   lr_min = 1.0e-5
   lr_curr = lr_min + 0.5 * (LEARNING_RATE - lr_min) * (
       1.0 + math.cos(math.pi * phase2_frac)
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
The $1.0 \times 10^{-5}$ floor eliminates late-stage optimization stagnation on `dev_02` while providing a sufficiently low terminal learning rate for asymptotic micro-settling on `dev_01` and `dev_03`.

## Evidence from previous experiments
- In Trial 033 ($\eta_{\min} = 10^{-7}$): `dev_01 = 1.76e-7`, `dev_02 = 0.001549`, `dev_03 = 9.00e-5`, mean = `0.0005464`.
- In Trial 045 ($\eta_{\min} = 3.5 \times 10^{-5}$): `dev_02 = 0.0015287` (record), but `dev_01 = 5.07e-6`.
- $1.0 \times 10^{-5}$ is the geometric sweet spot between $10^{-7}$ and $3.5 \times 10^{-5}$.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: cosine_decay_refined_floor_1e5
- Source: Loshchilov & Hutter (ICLR 2017); Touvron et al. (arXiv:2302.13971).
- Distinctness: Calibrates the 1% asymptotic learning rate floor to simultaneously optimize two-soliton collision polishing and single-mode microscale settling.

## Observed results
- Validation loss:
  - Mean: 5.25e+06 (Ineligible due to boundary condition divergence on dev_01)
  - dev_01: 1.58e+07 (val_bc_total = 0.4047 > 1e-3, ineligible)
  - dev_02: 0.00146348 (**ALL-TIME RECORD on dev_02**, breaking the 0.0015 barrier for the first time)
  - dev_03: 9.912e-05 (Solid convergence)
- Eligibility: Ineligible (periodic boundary failure on dev_01: val_bc_total = 0.4047 > 1e-3).
- Optimizer step throughput: Full speed maintained (6,950 steps/case, 23.40 steps/sec).
- Comparison: Setting $\eta_{\min} = 1.0 \times 10^{-5}$ enabled unprecedented descent depth on two-soliton collision case `dev_02` (0.00146348, an all-time record). However, on single traveling wave `dev_01`, the intermediate floor combined with late-stage stochastic collocation noise kicked the trajectory out of the narrow minimum, exploding the high-order derivative.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER** for overall mean validation loss and strict eligibility. Revert `candidate.py` back to full cosine decay down to $10^{-7}$. Mark Trial 046 as completed and ineligible.

## Reason for decision
Trial 033 retains guaranteed eligibility across all three cases with mean validation loss 0.0005464. Full decay down to $10^{-7}$ provides essential asymptotic damping that locks the solution into the narrow microscale basin on single-mode solutions.
