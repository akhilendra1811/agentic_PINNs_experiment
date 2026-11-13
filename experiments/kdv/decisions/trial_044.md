# Trial 044 Decision Record: Stratified Midpoint Temporal Invariant Quadrature

## Hypothesis
In Trial 033 (incumbent winner), the Hamiltonian conservation regularizer evaluated mass and $L_2$ energy across $S=8$ random temporal slices drawn uniformly via Monte Carlo:
$$t_{\text{slices}} \sim \mathcal{U}(0, t_{\text{scale}})$$
Pseudo-random Monte Carlo sampling suffers from slow $O(S^{-1/2})$ convergence, and on any given step, random draws leave substantial temporal intervals with zero invariant enforcement while clustering multiple slices redundantly into small windows. This adds stochastic gradient variance to the AdEMAMix momentum buffers.
Following Taylor & Pardo (Computers & Mathematics with Applications 2026, arXiv:2504.11976), we replace random temporal sampling with deterministic stratified midpoint quadrature:
$$t_s = \frac{s + 0.5}{S} \cdot t_{\text{scale}}, \quad s \in \{0, 1, \dots, S-1\}$$
Stratified midpoint quadrature provides mathematically uniform temporal coverage across the entire active domain $[0, t_{\text{scale}}]$, reducing integration error to $O(S^{-2})$ and completely eliminating temporal slice variance. This ensures that physical conservation of mass and energy is enforced uniformly along the wave packet's propagation trajectory at every optimizer step, stabilizing late-stage multi-soliton phase alignment and driving mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. Precompute static normalized midpoint coordinates before the training loop:
   `t_midpoints = ((torch.arange(INV_SLICES, device=device, dtype=torch.float32) + 0.5) / float(INV_SLICES)).unsqueeze(1)`
2. In the training loop, replace `t_slices = torch.rand((INV_SLICES, 1), device=device) * t_scale` with:
   `t_slices = t_midpoints * t_scale`
3. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$, linear $\alpha$-warmup from $0.0$ to $2.0$ over first 35% of steps, cosine decay to $10^{-7}$.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stratified midpoint temporal slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Stratified midpoint sampling provides deterministic, perfectly spaced temporal coverage. The network receives a consistent conservation signal at 8 distinct propagation milestones at every step, preventing local energy drift between random slices and eliminating gradient variance in the slow momentum buffer.

## Evidence from previous experiments
- In Trial 015, adding conservative Hamiltonian invariants reduced mean validation loss by 2.57x.
- In Trial 027 and Trial 033, refining spatial quadrature $N_x \to 256 \to 512$ consistently produced major performance records by eliminating spatial discretization error.
- In Trial 031, attempting to increase random temporal slices to $S=16$ increased stochastic noise on `dev_01`, demonstrating that random temporal slice variance is a real impediment. Replacing random slicing with deterministic stratified quadrature resolves this fundamentally.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: stratified_midpoint_temporal_invariant_quadrature
- Source: Taylor & Pardo (Computers & Mathematics with Applications 2026, arXiv:2504.11976), "Stochastic Quadrature Rules for Solving PDEs using Neural Networks".
- Distinctness: Introduces deterministic stratified midpoint temporal quadrature to replace pseudo-random Monte Carlo slicing in Hamiltonian invariant PINN regularization.

## Observed results
- Validation loss:
  - Mean: 55,510.8 (Substantially worse than Trial 033: 0.0005464)
  - dev_01: 166,532.5 (Severe aliased mode divergence)
  - dev_02: 0.00180462
  - dev_03: 0.00010348
- Eligibility: Fully eligible on boundaries (IC = 0.0 <= 1e-3, BC total = 2.61e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Full speed maintained (6,920 steps/case, 23.30 steps/sec).
- Comparison: Evaluating invariants at deterministic static midpoints ($t_s = (s + 0.5)/8 \cdot t_{\text{scale}}$) creates temporal aliasing: the network satisfies mass and energy conservation at the 8 fixed temporal nodes while developing unpenalized spurious high-frequency oscillations in between. Stochastic Monte Carlo temporal sampling (`torch.rand`) sweeps across the continuous temporal interval $[0, t_{\text{scale}}]$ over training steps, completely suppressing inter-node aliasing.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert temporal invariant sampling to stochastic uniform draws (`torch.rand((INV_SLICES, 1), device=device) * t_scale`) in `candidate.py`. Mark Trial 044 as completed and eligible.

## Reason for decision
Trial 033 retains vastly superior mean validation loss (0.0005464 vs 55,510.8). Stochastic temporal sampling is essential for continuous invariant enforcement and prevents temporal collocation aliasing.
