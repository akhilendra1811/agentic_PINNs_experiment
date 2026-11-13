# Trial 041 Decision Record: PirateNet Trainable Adaptive Residual Scaling

## Hypothesis
In standard deep ResNet PINNs, computing the third-order spatial derivative $u_{xxx} = \partial^3 u / \partial x^3$ through 8 uncalibrated non-linear sinusoidal layers at initialization creates large variance in the PDE residual loss, forcing early optimization steps to spend substantial compute damping out initial derivative shocks.
Following the PirateNet architecture (Wang, Li, Chen, Perdikaris, JMLR 2024 / arXiv:2402.01928), we replace fixed unit residual skips with trainable scalar multipliers $\alpha_l$ initialized to zero:
$$h_{l+1} = h_l + \alpha_l \cdot \sin(W_l h_l + b_l), \quad \alpha_l \big|_{t=0} = 0.0$$
At step 0, because all $\alpha_l = 0.0$, the entire hidden network collapses mathematically into an identity mapping:
$$h_L = h_1 = \sin(W_{\text{in}} x + b_{\text{in}})$$
The network behaves as a shallow, perfectly conditioned single-layer model with well-bounded third derivatives at initialization. As AdEMAMix minimizes the conservative physics loss, $\alpha_l$ adapts dynamically via gradient descent, allowing the architecture to progressively deepen without derivative explosion. This will stabilize early curriculum optimization and accelerate convergence on complex multi-soliton interactions (`dev_02`), lowering mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. In `KdVPINN`:
   - Keep `WIDTH = 176`, `HIDDEN_LAYERS = 8`, `in_dim = 7` (targeted dual harmonics $k \in \{1, 2\}$).
   - Add `self.res_alphas = nn.ParameterList([nn.Parameter(torch.zeros(1)) for _ in range(HIDDEN_LAYERS - 1)])` (7 parameters, total 219,657 $\le 250,000$).
   - In `forward`:
     ```python
     h = torch.sin(self.in_linear(features))
     for layer, alpha in zip(self.hidden, self.res_alphas):
         h = h + alpha * torch.sin(layer(h))
     net_out = self.out_proj(h)
     ```
2. In `train_model`:
   - Retain the incumbent AdEMAMix optimizer configuration from Trial 033: static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$, cosine decay to $10^{-7}$.
   - Retain linear $\alpha$-warmup from $0.0$ to $2.0$ over first 35% of steps.
   - Retain ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - Retain 35% domain expansion temporal curriculum.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Derivative explosion at $t=0$ is completely eliminated by construction. The network starts in a shallow, globally stable configuration, matching initial boundary conditions and basic harmonic wave motion instantly. As $\alpha_l$ grows smoothly under gradient guidance, the network recruits deep capacity specifically where required by non-linear soliton steepening and dispersion balance.

## Evidence from previous experiments
- In Trial 004, SIREN activations demonstrated dramatic improvements over tanh, but higher layers required careful conditioning.
- In Trial 028, scaling early layer parameters unguided disrupted downstream stability.
- In Trial 033, scaling width to 176 achieved our best performance, showing that capacity helps if derivative conditioning is preserved.
- Wang et al. (JMLR 2024) proved that zero-initialized residual scaling resolves the fundamental derivative trainability pathology in deep PINNs.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: piratenet_adaptive_residual_scaling
- Source: Wang, Li, Chen, Perdikaris (JMLR 2024, arXiv:2402.01928), "PirateNets: Physics-informed Deep Learning with Residual Adaptive Networks".
- Distinctness: Introduces trainable zero-initialized residual scaling multipliers ($\alpha_l = 0$ at $t=0$) for progressive deepening and higher-order derivative stabilization in periodic KdV PINNs.

## Observed results
- Validation loss:
  - Mean: 0.0162065 (Substantially higher than incumbent Trial 033: 0.0005464)
  - dev_01: 9.925e-06
  - dev_02: 0.0366087
  - dev_03: 0.0120009
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 1.64e-06 <= 1e-3, params = 219,657 <= 250,000).
- Optimizer step throughput: Reduced from ~6,950 to ~6,280 steps/case (-9.6%) due to per-layer scalar autograd graph tracking.
- Comparison: While zero-initialization ($\alpha_l = 0$) mathematically prevents initial derivative explosion, it introduces a severe "dead start" pathology: because $\nabla_{W_l} \mathcal{L} \propto \alpha_l$, all hidden layer weights receive near-zero gradients at initialization. In a compute-bounded setting (300 seconds), $\alpha_l$ took hundreds of steps to drift upward, preventing the deep layers from adapting before the curriculum expanded to the full domain. Fixed unitary residual skips ($h + \sin(Wh)$) allow simultaneous end-to-end gradient flow through all layers from step 1.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert `candidate.py` back to fixed unitary residual skips without scalar multipliers. Mark Trial 041 as completed and eligible.

## Reason for decision
Trial 033 retains vastly superior mean validation loss (0.0005464 vs 0.0162065, a ~30x advantage) and 10% higher step throughput. Unitary residual skips enable immediate multi-layer gradient propagation that is essential under fixed time budgets.
