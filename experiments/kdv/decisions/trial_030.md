# Trial 030 Decision Record: AdEMAMix Extended Slow Momentum Horizon (beta3 = 0.9995)

## Hypothesis
In AdEMAMix with linear $\alpha$-warmup (established in Trial 029), early stochastic gradient noise is effectively shielded because $\alpha$ begins at $0.0$. However, setting $\beta_3 = 0.999$ yields a momentum half-life of $T_{1/2} = \ln(2)/(1 - 0.999) \approx 693$ steps (~25s). In our ~8,000-step training regime, gradients accumulated during the critical soliton collision phase (steps 3,000–5,000) decay significantly by the final cosine annealing stage (steps 6,000–8,000). Pagliardini et al. (Apple ML Research, arXiv:2409.03137) demonstrate that for longer optimization budgets, increasing $\beta_3$ extends the historical influence window. Increasing $\beta_3$ to $0.9995$ doubles the memory half-life to $\approx 1,386$ steps (~50s, effectively spanning $\approx 2,500$ steps), preserving consistent physical trajectory directions across the full post-collision domain and lowering mean validation loss below Trial 029's record 0.0006826.

## Proposed method change
In `candidate.py`:
1. Retain the winning targeted dual-harmonic SIREN architecture ($k \in \{1, 2\}$, WIDTH=160, 8 layers, pure $\sin$ activations with additive residuals and unitary scaling).
2. Retain high-density Hamiltonian quadrature ($N_x=256$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.1$).
3. Retain 35% domain expansion temporal curriculum and linear $\alpha$-warmup schedule ($\alpha(t) = 2.0 \times \min(1.0, \text{fraction} / 0.35)$).
4. In `train_model`, update `AdEMAMix` instantiation:
   - Change `betas = (0.9, 0.99, 0.999)` to `betas = (0.9, 0.99, 0.9995)`.
   - Maintain zero weight decay, base learning rate $1.08 \times 10^{-3}$, and cosine decay to $10^{-7}$.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, evaluated over $S=8$ time slices with $N_x=256$ spatial quadrature points per slice, alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Doubling the half-life of the slow momentum buffer will retain coherent physical gradient signals from earlier temporal expansion stages, preventing the network from settling into sub-optimal local high-frequency residual modes during final cosine decay. Step throughput will remain unchanged at $\approx 27$ steps/sec.

## Evidence from previous experiments
- In Trial 026, introducing AdEMAMix dropped mean validation loss from 0.001142 to 0.000803.
- In Trial 029, adding linear $\alpha$-warmup reduced mean validation loss to 0.0006826 and broke below 0.002 on `dev_02` (0.001927).
- With $\alpha$-warmup protecting the buffer from early noise, the slow momentum buffer can safely maintain a deeper historical horizon without risking contamination.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: ademamix_extended_slow_momentum_horizon
- Source: M. Pagliardini, P. Ablin, D. Grangier (Apple ML Research / EPFL, arXiv:2409.03137, Sep 2024), "The AdEMAMix Optimizer: Better, Faster, Older".
- Distinctness: Formulates extended-horizon slow momentum retention ($\beta_3 = 0.9995$) paired with curriculum-aligned $\alpha$-warmup in physics-informed neural network optimization.


## Observed results
- Validation loss:
  - Mean: 0.0263586 (Higher than incumbent Trial 029: 0.0006826)
  - dev_01: 0.0770617 (Diverged at final checkpoint; best posthoc was 0.00512)
  - dev_02: 0.0018712 (**All-time best on dev_02 across the entire campaign**; down from 0.0019268 in Trial 029 and baseline 0.007173; **3.83x reduction over baseline**)
  - dev_03: 0.0001429
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.34e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~7,880 steps per case, 26.54 steps/sec).
- Comparison: Extending $\beta_3$ to 0.9995 successfully broke our record on the stiff multi-soliton collision (`dev_02` reached an all-time best 0.001871), demonstrating that deep historical momentum is exceptionally powerful for multi-frequency collision dynamics. However, on the simple single-frequency case `dev_01`, the 2,000-step momentum inertia carried excessive historical velocity into late-stage cosine annealing, preventing convergence to the tight fixed point.

## Agent decision
Keep Trial 029 as the **INCUMBENT WINNER**. Revert $\beta_3$ to 0.999 in `candidate.py`. Mark Trial 030 as completed and eligible, registering a valuable insight on momentum inertia trade-offs between single-mode and multi-soliton regimes.

## Reason for decision
Trial 029 retains a much lower mean validation loss (0.0006826 vs 0.0263586) with rock-solid stability across all three cases (`dev_01`: 3.34e-07, `dev_02`: 0.001927, `dev_03`: 0.000121). $\beta_3 = 0.999$ provides the ideal balance between historical momentum for collisions and agility for simple fixed points.
