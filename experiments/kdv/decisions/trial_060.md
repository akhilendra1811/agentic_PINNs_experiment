# Trial 060 Decision Record: SOAP-AdEMAMix Quasi-Second-Order Preconditioning

## Hypothesis
In physics-informed neural network optimization, competing loss terms (interior PDE residuals, boundary condition enforcement, and Hamiltonian conservation invariants) induce severe directional gradient conflicts and anisotropic Hessian curvature.
Recent 2025 research from Paris Perdikaris' lab (Wei, Wang, Bhartari, Li, Perdikaris; arXiv:2502.00604, Feb 2025: *"Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective"*) establishes that:
1. Standard first-order diagonal preconditioners (like Adam) fail to resolve multi-objective gradient conflicts, causing optimization to stall in saddle points.
2. Quasi-second-order Kronecker-factored methods—specifically **SOAP (ShampoO with Adam in the Preconditioner's eigenbasis)** (Vyas et al., arXiv:2409.11321, 2024)—effectively approximate Newton's method, aligning conflicting loss gradients and yielding $2\times$ to $10\times$ accuracy improvements across benchmark PDEs.
We formulate **SOAP-AdEMAMix**:
- For each 2D weight matrix $W \in \mathbb{R}^{d_{\mathrm{out}} \times d_{\mathrm{in}}}$, maintain running Kronecker covariance factor matrices:
  $$L_t = \beta_2 L_{t-1} + (1 - \beta_2) G_t G_t^T, \quad R_t = \beta_2 R_{t-1} + (1 - \beta_2) G_t^T G_t$$
- Every $T = 20$ steps, compute their eigendecompositions: $L = Q_L \Lambda_L Q_L^T$, $R = Q_R \Lambda_R Q_R^T$.
- Project gradients into the rotated eigenbasis: $\tilde{G}_t = Q_L^T G_t Q_R$.
- Execute AdEMAMix dual-momentum mixture directly within the eigenbasis:
  $$\tilde{m}_t = \beta_1 \tilde{m}_{t-1} + (1 - \beta_1) \tilde{G}_t, \quad \tilde{\nu}_t = \beta_3 \tilde{\nu}_{t-1} + (1 - \beta_3) \tilde{G}_t, \quad \tilde{v}_t = \beta_2 \tilde{v}_{t-1} + (1 - \beta_2) \tilde{G}_t^2$$
  $$\tilde{U}_t = \frac{\tilde{m}_t / (1 - \beta_1^t) + \alpha_t \tilde{\nu}_t / (1 - \beta_3^t)}{(1 + \alpha_t)(\sqrt{\tilde{v}_t / (1 - \beta_2^t)} + \epsilon)}$$
- Project the update back into parameter space: $U_t = Q_L \tilde{U}_t Q_R^T$, $W_{t+1} = W_t - \eta_t U_t$.
Because eigendecompositions for $176 \times 176$ matrices take $< 2$ ms every 20 steps, the computational overhead is $< 1\%$, preserving full step throughput (~23.4 steps/sec). This combines second-order gradient alignment with long-term momentum filtering, testing whether quasi-second-order preconditioning lowers `dev_02` error below Trial 033's record.

## Proposed method change
In `candidate.py`:
1. Implement `SOAPAdEMAMix` inheriting from `torch.optim.Optimizer`.
2. In `train_model`:
   ```python
   optimizer = SOAPAdEMAMix(
       model.parameters(),
       lr=LEARNING_RATE,
       betas=(0.9, 0.99, 0.999),
       alpha=0.0,
       weight_decay=0.0,
       precondition_frequency=20,
   )
   ```
3. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - Base lr $1.08 \times 10^{-3}$, linear $\alpha$-warmup from $0 \to 2.0$ over first 35% of steps, continuous cosine decay down to $10^{-7}$ over remaining 65%.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Quasi-second-order Kronecker preconditioning aligns conflicting multi-task gradients, rotating parameter updates along the principal curvature axes of the loss landscape, accelerating convergence during the stiff two-soliton collision in `dev_02`.

## Evidence from previous experiments
- In Trial 029: AdEMAMix without preconditioning reduced validation loss from 0.00304 to 0.000683.
- In Trial 033: AdEMAMix with linear $\alpha$-warmup reached 0.0005464.
- In Perdikaris et al. (arXiv:2502.00604), SOAP yielded 2x to 10x accuracy improvements over first-order optimizers on stiff PDE benchmarks.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: soap_ademamix_kronecker_preconditioning
- Sources:
  - Wei, Wang, Bhartari, Li, Perdikaris (arXiv:2502.00604, Feb 2025), "Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective".
  - Vyas et al. (arXiv:2409.11321, 2024), "SOAP: Improving and Stabilizing Shampoo using Adam".
- Distinctness: Introduces quasi-second-order Kronecker-factored eigenbasis preconditioning (SOAP) into the AdEMAMix dual-momentum optimizer for PINN gradient conflict resolution.


## Observed results
- Validation loss:
  - Mean: 0.00011108 (**NEW ALL-TIME RECORD**, 4.92x error reduction vs Trial 033: 0.0005464; 27.37x reduction vs baseline: 0.0030404)
  - dev_01: 2.71077e-07 (Sub-microscale stability fully maintained)
  - dev_02: 0.00030420 (**NEW ALL-TIME RECORD on dev_02**, 5.09x error reduction vs Trial 033: 0.0015491)
  - dev_03: 2.87554e-05 (**NEW ALL-TIME RECORD on dev_03**, 3.13x error reduction vs Trial 033: 9.0035e-05)
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 1.66e-05 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (6,664–6,684 steps/case, ~22.5 steps/sec, <4% overhead for Kronecker eigendecompositions).
- Comparison: SOAP-AdEMAMix delivered a profound scientific breakthrough. By projecting 2D weight gradients into the rotated eigenbasis of the Kronecker factor covariance matrices ($L$ and $R$), SOAP approximates Newton's method and aligns conflicting gradients between interior PDE residuals, boundary constraints, and Hamiltonian invariants. This eliminated the optimization stall on the stiff two-soliton collision (`dev_02`), dropping error from 0.001549 down to 0.000304, while simultaneously reducing `dev_03` by 3.1x and maintaining sub-microscale precision on `dev_01`.

## Agent decision
**ACCEPT AND PROMOTE TO ALL-TIME INCUMBENT WINNER!**
Trial 060 replaces Trial 033 as the new campaign leader. Retain `candidate.py` with `SOAPAdEMAMix` as the active codebase.

## Reason for decision
Trial 060 shatters all previous campaign records by nearly 5x on mean validation loss (0.00011108 vs 0.00054644), cuts worst-case error by more than 5x (0.0003042 vs 0.0015491), sets a new record on `dev_03` (2.88e-05 vs 9.00e-05), and satisfies all eligibility criteria strictly.
