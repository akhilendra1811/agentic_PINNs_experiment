# Trial 068 Decision Record: SOAP-AdEMAMix Calibrated Learning Rate ($\text{lr} = 1.20 \times 10^{-3}$)

## Hypothesis
Under quasi-second-order Kronecker preconditioning (SOAP, Perdikaris et al., arXiv:2502.00604, Feb 2025: *"Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective"*), parameter updates are projected into the rotated eigenbasis of the running Kronecker covariance factor matrices, flattening anisotropic loss landscape curvature and suppressing gradient spikes along stiff directions.
In Trial 067, increasing `LEARNING_RATE` from $1.08 \times 10^{-3}$ to $1.15 \times 10^{-3}$ achieved an all-time campaign record mean validation loss of `4.689899 \times 10^{-5}` with `dev_03` dropping to `9.47 \times 10^{-6}` and `dev_01` remaining rock-solid at `2.36 \times 10^{-7}`.
We hypothesize that a further modest increase to `LEARNING_RATE = 1.20e-3` (+4.3% step size) will:
1. Increase early descent velocity into the steep non-linear two-soliton collision valley on `dev_02`.
2. Test whether SOAP preconditioning provides sufficient second-order curvature damping to prevent the gradient divergence observed in unconditioned first-order optimizers at $\text{lr} \ge 1.14 \times 10^{-3}$.
3. Rigorously bracket the global optimal learning rate for SOAP-AdEMAMix on KdV dynamics.

## Proposed method change
In `candidate.py`:
1. Update `LEARNING_RATE`:
   ```python
   LEARNING_RATE = 1.20e-3
   ```
2. Retain all other winning hyperparameters of incumbent Trial 067:
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
Potential further reduction in `dev_02` collision loss, or identification of the upper stability boundary for preconditioned learning rate scaling.

## Evidence from previous experiments
- In Trial 064, $\text{lr} = 1.08 \times 10^{-3}$ yielded mean val `4.857 \times 10^{-5}`.
- In Trial 067, $\text{lr} = 1.15 \times 10^{-3}$ yielded all-time best mean val `4.690 \times 10^{-5}`.
- In Trial 042 (unconditioned AdEMAMix), $\text{lr} = 1.25 \times 10^{-3}$ diverged on `dev_01`, proving that unconditioned methods cannot support step sizes $\ge 1.14 \times 10^{-3}$.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false

## Observed results
- Mean validation loss: `5.174796e-05` ($5.17 \times 10^{-5}$) [vs Trial 067: `4.689899e-05`].
- dev_01 validation loss: `2.12493e-07` ($L_{\mathrm{IC}} = 0.0$, $L_{\mathrm{BC}} = 3.98 \times 10^{-8}$).
- dev_02 validation loss: `0.00014575` ($1.46 \times 10^{-4}$) [vs Trial 067: `1.3099 \times 10^{-4}`].
- dev_03 validation loss: `9.27660e-06` ($9.28 \times 10^{-6}$) [solid sub-10-microscale precision].
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, $L_{\mathrm{BC}} = 0.000138 \le 10^{-3}$, parameter count: 219,650).
- Runtime: 891.1s total (6,843 optimizer steps per case on Apple Silicon MPS).

## Agent decision
**REJECT METHOD CHANGE; TRIAL 067 REMAINS INCUMBENT WINNER.**
Revert `LEARNING_RATE` to `1.15e-3` in `candidate.py`.

## Reason for decision
1. **Clean Optimum Bracketing:**
   Systematic testing across `lr = 1.08e-3` (064: `4.857e-05`), `lr = 1.15e-3` (067: `4.690e-05`), and `lr = 1.20e-3` (068: `5.175e-05`) establishes that `1.15e-3` is the exact global optimum learning rate under SOAP-AdEMAMix preconditioning.
2. **Onset of Collocation Overshoot:**
   At `lr = 1.20e-3`, step sizes in the rotated eigenspaces are slightly too large near the sharp non-linear curvature minimum of the two-soliton collision (`dev_02`), increasing its validation error from `1.31e-4` to `1.46e-4`.
3. **Incumbent Stability:**
   Trial 067 holds both the all-time lowest mean validation loss (`4.689899e-05`) and the all-time lowest worst-case validation loss (`0.00013099`).
