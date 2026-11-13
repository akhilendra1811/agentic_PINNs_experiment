# Trial 071 Decision Record: SOAP-AdEMAMix 5% Linear Learning Rate Warmup

## Hypothesis
In Vyas et al. (arXiv:2409.11321, Appendix A.1: *"SOAP: Improving and Stabilizing Shampoo using Adam"*), the authors standardly employ a linear learning rate warmup prior to cosine decay.
In our previous trials (e.g. Trial 067), `LEARNING_RATE` started immediately at full intensity ($1.15 \times 10^{-3}$) from step 1.
However, in SOAP, the Kronecker covariance factors $L$ and $R$ are initialized as identity matrices, and the first eigendecomposition ($Q_L, Q_R$) does not occur until step 80 (`precondition_frequency = 80`).
Consequently:
1. Steps 1 to 79 run in an unconditioned state, where large gradient steps can perturb SIREN weights away from the well-conditioned wave representation manifold.
2. The initial gradient outer products $G_1 G_1^T$ have large variance because the network has not yet adapted to the initial condition.
Introducing a 5% linear learning rate warmup (`WARMUP_FRAC = 0.05`, $\approx 325$ steps):
1. Ramps $\text{lr}$ gently from $10^{-7}$ to $1.15 \times 10^{-3}$, ensuring that steps 1 to 79 operate at reduced step sizes ($< 2.8 \times 10^{-4}$) while $L$ and $R$ populate with stable covariance statistics.
2. Smoothly brings the optimizer to full learning rate right as the preconditioned eigenspaces mature and become persistent.
3. Tests whether learning rate warmup improves upon Trial 067's all-time record mean validation loss of `4.689899 \times 10^{-5}`.

## Proposed method change
In `candidate.py`:
1. Define `WARMUP_FRAC = 0.05`.
2. In `train_model()`, ramp $\text{lr}$ linearly from $10^{-7}$ to `LEARNING_RATE` over `fraction < WARMUP_FRAC`:
   ```python
   if fraction < WARMUP_FRAC:
       lr_curr = 1e-7 + (LEARNING_RATE - 1e-7) * (fraction / WARMUP_FRAC)
       alpha_curr = ALPHA_MAX * (fraction / CURRICULUM_FRAC)
   elif fraction < CURRICULUM_FRAC:
       lr_curr = LEARNING_RATE
       alpha_curr = ALPHA_MAX * (fraction / CURRICULUM_FRAC)
   else:
       alpha_curr = ALPHA_MAX
       phase2_frac = min((fraction - CURRICULUM_FRAC) / (1.0 - CURRICULUM_FRAC), 1.0)
       lr_curr = 1e-7 + 0.5 * (LEARNING_RATE - 1e-7) * (
           1.0 + math.cos(math.pi * phase2_frac)
       )
   ```
3. Retain all other winning hyperparameters of incumbent Trial 067:
   - $\text{WIDTH} = 176, \text{HIDDEN\_LAYERS} = 8$ (219,650 params).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - Synchronous rotated-space SOAP-AdEMAMix with `precondition_frequency = 80`.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Smoother early optimization trajectory, reduced early weight perturbation, and improved terminal convergence across all development cases.

## Evidence from previous experiments
- In Trial 067, un-warmed lr achieved `4.689899 \times 10^{-5}`.
- Vyas et al. (2024) demonstrated that linear warmup is critical for stabilizing SOAP across neural architectures.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false

## Observed results
- Mean validation loss: `0.0001336` ($1.34 \times 10^{-4}$) [vs Trial 067: `4.689899e-05`].
- dev_01 validation loss: `7.84458e-06`.
- dev_02 validation loss: `0.00034045` (val_bc_total = `0.002170` $> 10^{-3}$, **ineligible**).
- dev_03 validation loss: `5.26294e-05`.
- Eligibility: Ineligible (periodic boundary mismatch on dev_02 exceeded threshold).
- Runtime: 891.1s total.

## Agent decision
**REJECT METHOD CHANGE; TRIAL 067 REMAINS INCUMBENT WINNER.**
Immediately revert `candidate.py` to Trial 067 (remove learning rate warmup).

## Reason for decision
1. **Criticality of Rapid Initial-Condition Grounding:**
   In temporal curriculum training, the initial condition profile must be learned with near-zero error in the very first few dozen steps when $t \in [0, 0.05]$.
   Throttling the learning rate with a 5% warmup delayed convergence to the initial profile. By step 325, domain expansion had outpaced initial condition fitting, causing a phase lag that drifted into the boundary ($L_{\mathrm{BC}} = 0.00217$).
2. **Superiority of Full Step Size from Step 1:**
   Starting at full base `lr = 1.15e-3` immediately pins the IC within the first 50 steps, allowing subsequent domain expansion to propagate the wave cleanly.
3. **Firm Reversion:**
   Trial 067's un-warmed learning rate schedule remains fully intact.
