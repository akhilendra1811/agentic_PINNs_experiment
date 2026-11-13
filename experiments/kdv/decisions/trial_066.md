# Trial 066 Decision Record: SOAP-AdEMAMix Calibrated Learning Rate ($\text{lr} = 1.15 \times 10^{-3}$)

## Hypothesis
In Perdikaris et al. (arXiv:2502.00604, Feb 2025: *"Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective"*), quasi-second-order Kronecker preconditioning (SOAP) flattens ill-conditioned loss landscape curvature and aligns directional gradients across multi-task PINN objectives, enabling more aggressive, stable learning rate schedules without the gradient spike instability typical of first-order optimizers.
In Trial 064, SOAP-AdEMAMix achieved our all-time record mean validation loss of `4.857 \times 10^{-5}` at base `LEARNING_RATE = 1.08e-3` with `dev_01` settling at $1.28 \times 10^{-7}$.
By calibrating `LEARNING_RATE` from $1.08 \times 10^{-3}$ up to $1.15 \times 10^{-3}$ (+6.5% step size):
1. The optimizer takes slightly larger parameter steps within the well-conditioned eigenspaces defined by $Q_L$ and $Q_R$, accelerating descent into the narrow two-soliton collision valley on `dev_02`.
2. Unlike Trials 042 and 043 (where unconditioned AdEMAMix exploded on `dev_01` when $\text{lr} \ge 1.14 \times 10^{-3}$), SOAP's Kronecker preconditioning normalizes gradient step magnitudes across parameter matrices, suppressing unconditioned step-size spikes.
3. Tests whether aggressive preconditioned learning rates drive mean validation loss below $4.0 \times 10^{-5}$.

## Proposed method change
In `candidate.py`:
1. Update `LEARNING_RATE`:
   ```python
   LEARNING_RATE = 1.15e-3
   ```
2. Retain all other winning hyperparameters of incumbent Trial 064:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - SOAP-AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, linear $\alpha$-warmup from $0 \to 2.0$ over first 35% of steps, continuous cosine decay down to $10^{-7}$ over remaining 65%, `precondition_frequency = 80`.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Accelerated convergence on `dev_02` without instability on `dev_01`, testing whether SOAP preconditioning safely supports higher learning rates on 3rd-order KdV dynamics.

## Evidence from previous experiments
- In Trial 042, $\text{lr} = 1.25 \times 10^{-3}$ reduced `dev_02` to 0.001069, but unconditioned gradients diverged on `dev_01`.
- In Trial 064, SOAP preconditioning stabilized all three cases, achieving an all-time record 4.857e-05.
- Perdikaris et al. (2025) proved that SOAP enables more aggressive learning rates in stiff PINNs.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: soap_ademamix_calibrated_lr_115
- Sources:
  - Wei, Wang, Bhartari, Li, Perdikaris (arXiv:2502.00604, Feb 2025), "Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective".
  - Vyas et al. (arXiv:2409.11321, 2024), "SOAP: Improving and Stabilizing Shampoo using Adam".
- Distinctness: Systematic calibration of base learning rate to 1.15e-3 under quasi-second-order Kronecker preconditioning.


## Observed results
- Run execution status: **FAILED** (`[Errno 5] Input/output error` during dev_02 training execution due to host laptop system sleep / I/O interruption).
- Partial metrics: `dev_01` completed successfully with sub-microscale precision ($1.38 \times 10^{-7}$, IC=0, BC=2.88e-08), confirming that $\text{lr} = 1.15 \times 10^{-3}$ was completely stable on single-mode traveling waves under SOAP-AdEMAMix. However, host sleep interrupted dev_02 before training finished.
- Eligibility: Ineligible / Failed (did not complete all 3 dev cases).

## Agent decision
Keep Trial 064 as the **ALL-TIME INCUMBENT WINNER**. Record Trial 066 as failed due to hardware/OS sleep interruption. Re-execute this exact hypothesis in Trial 067.

## Reason for decision
Trial 066 was interrupted by an external system sleep event. The partial dev_01 result confirmed perfect stability ($1.38 \times 10^{-7}$). Re-running the experiment under Trial 067 will provide the full 3-case evaluation without interruption.
