# Trial 036 Decision Record: Invariant Loss Weight Scaling (lambda_inv = 0.15)

## Hypothesis
In Trial 033, doubling spatial quadrature to $N_x = 512$ points across $S=8$ temporal slices virtually eliminated Riemann sum discretization noise, reducing mean validation loss to an all-time low of $0.0005464$. However, the invariant loss weight $\lambda_{\mathrm{inv}}$ remained at $0.10$—a value chosen heuristically in Trial 015 when quadrature had only $N_x = 128$ points. Now that the spatial integral evaluation is noise-free, increasing the invariant loss weight from $\lambda_{\mathrm{inv}} = 0.10$ to $\lambda_{\mathrm{inv}} = 0.15$ will enforce continuous mass and Hamiltonian $L^2$ energy conservation $50\%$ more strictly throughout multi-soliton collisions on `dev_02`. This stronger physical prior will prevent secular wave-crest dissipation during collision intervals without injecting gradient noise on single-frequency case `dev_01`, lowering worst-case validation loss below Trial 033's record 0.0015491.

## Proposed method change
In `candidate.py`:
1. Retain the winning $\text{WIDTH} = 176$ architecture (219,650 parameters, 8 layers, pure $\sin$ activations with additive residuals and unitary scaling).
2. Retain ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ time slices).
3. Retain winning AdEMAMix optimizer with linear $\alpha$-warmup schedule ($\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, $\alpha$ warming from 0.0 to 2.0 over first 35%, zero weight decay, base lr $1.08 \times 10^{-3}$ with cosine decay).
4. Retain 35% domain expansion temporal curriculum.
5. In hyperparameter definitions, change `INV_WEIGHT = 0.1` to `INV_WEIGHT = 0.15`.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.15$, evaluated over $S=8$ time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Increasing $\lambda_{\mathrm{inv}}$ to $0.15$ places higher optimization priority on exact global energy conservation ($a_1^2 + a_2^2$). Because the $N_x = 512$ quadrature has high accuracy across narrow wave crests, the gradient contribution from $\mathcal{L}_{\mathrm{inv}}$ is pure physical signal that suppresses energy loss during multi-soliton interaction. Step throughput is unchanged.

## Evidence from previous experiments
- In Trial 015, introducing $\mathcal{L}_{\mathrm{inv}}$ dropped mean validation loss from 0.001260 to 0.001183.
- In Trial 027 and Trial 033, refining spatial quadrature from $N_x=128$ to 256 and then 512 unlocked dramatic improvements (0.000803 -> 0.000733 -> 0.000546).
- Now that spatial quadrature is pristine, tuning $\lambda_{\mathrm{inv}}$ is the natural next step.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: invariant_loss_weight_scaling_015
- Source: arXiv:2410.15582, "Structure-Preserving PINNs for Soliton Equations".
- Distinctness: Evaluates invariant loss weight scaling under pristine, low-noise spatial quadrature in multi-soliton PINN training.


## Observed results
- Validation loss:
  - Mean: 0.0008603 (Higher than incumbent Trial 033: 0.0005464)
  - dev_01: 2.8471e-07
  - dev_02: 0.0024763 (Higher than Trial 033's 0.0015491)
  - dev_03: 0.0001042
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.30e-6 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (~6,930 steps per case, 23.33 steps/sec).
- Comparison: Increasing the invariant loss weight from $\lambda_{\mathrm{inv}} = 0.10$ to $\lambda_{\mathrm{inv}} = 0.15$ caused the optimizer to over-prioritize the scalar energy integral $\int u^2 dx = a_1^2 + a_2^2$ relative to the 3rd-order spatial derivative dispersion term $u_{xxx}$. Because the global energy functional admits degenerate non-physical wave profiles that satisfy total energy without satisfying local dispersion, this competition degraded worst-case collision accuracy on `dev_02` from 0.001549 to 0.002476.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert `INV_WEIGHT` to 0.10 in `candidate.py`. Mark Trial 036 as completed and eligible, registering an empirical boundary on invariant constraint weighting.

## Reason for decision
Trial 033 retains vastly superior mean validation loss (0.0005464 vs 0.0008603) and worst-case performance (0.0015491 vs 0.0024763). $\lambda_{\mathrm{inv}} = 0.10$ provides the optimal trade-off: strong enough to prevent secular energy decay, yet light enough to allow PDE autograd gradients to govern local dispersion.
