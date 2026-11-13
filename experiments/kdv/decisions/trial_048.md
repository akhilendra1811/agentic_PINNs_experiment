# Trial 048 Decision Record: SIREN with 1/sqrt(2) DeepNorm Residual Scaling

## Hypothesis
In our incumbent architecture (Trial 033), the deep hidden layers use unscaled sinusoidal residual skips:
$$h_{l+1} = h_l + \sin(W_l h_l + b_l)$$
Because $\sin(z)$ does not saturate (its derivative $\cos(z)$ maintains peak magnitude 1.0 everywhere), compounding 7 residual sinusoidal branches across 8 layers causes the variance of the hidden representations and higher-order spatial derivatives ($u_{xxx} = \partial^3 u / \partial x^3$) to accumulate with depth. In deep networks, this creates high-frequency derivative stiffness that can destabilize early training on stiff multi-soliton collisions (`dev_02`).
Following DeepNorm / residual scaling principles (Wang et al., 2022, arXiv:2203.00555), scaling each non-linear residual branch by a fixed variance-preserving factor $\beta = \frac{1}{\sqrt{2}} \approx 0.7071$:
$$h_{l+1} = h_l + \frac{1}{\sqrt{2}} \sin(W_l h_l + b_l)$$
stems the variance accumulation across the 7 hidden layers. Unlike zero-initialized trainable gating (which suffered from a dead-start bottleneck in Trial 041), fixed $1/\sqrt{2}$ scaling ensures full, immediate gradient flow through all layers from step 1 while damping third-order derivative compounding by $(1/\sqrt{2})^7 \approx 0.088$ across the hidden depth. This will stabilize high-order spatial derivatives and accelerate two-soliton collision convergence, driving mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. In `KdVPINN.forward`, update the hidden layer loop:
   ```python
   inv_sqrt2 = 1.0 / math.sqrt(2.0)
   h = torch.sin(self.in_linear(features))
   for layer in self.hidden:
       h = h + inv_sqrt2 * torch.sin(layer(h))
   net_out = self.out_proj(h)
   ```
2. Retain all other winning hyperparameters of incumbent Trial 033:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$, linear $\alpha$-warmup from $0.0$ to $2.0$ over first 35% of steps, cosine decay to $10^{-7}$.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Damping derivative compounding by $1/\sqrt{2}$ at each residual stage provides a smoother, better-conditioned third-derivative field $u_{xxx}$, reducing the stiffness of the PDE residual loss landscape and enabling deeper convergence on the two-soliton collision cases (`dev_02` and `dev_03`).

## Evidence from previous experiments
- In Trial 004, sinusoidal activations established massive improvements over tanh.
- In Trial 032 and Trial 033, scaling width to 176 increased capacity, but revealed that derivative conditioning is essential to avoid Hessian ill-conditioning.
- In Trial 041, zero-initialized gating eliminated derivative explosion but caused a dead start; fixed $1/\sqrt{2}$ scaling avoids the dead start while preserving bounded derivative propagation.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: siren_deepnorm_residual_scaling_invsqrt2
- Source: Wang et al. (arXiv:2203.00555), "DeepNet: Scaling Transformers to 1,000 Layers".
- Distinctness: Formulates fixed $1/\sqrt{2}$ variance-preserving sinusoidal residual branch scaling to damp 3rd-order spatial derivative compounding in deep periodic KdV PINNs.

## Observed results
- Validation loss:
  - Mean: 0.001151 (Higher than incumbent Trial 033: 0.0005464)
  - dev_01: 4.80e-07 (Sub-microscale precision preserved)
  - dev_02: 0.00319349
  - dev_03: 0.00025913
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.34e-06 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: ~6,620 steps/case (22.28 steps/sec).
- Comparison: While $1/\sqrt{2}$ scaling successfully bounded derivative propagation and kept `dev_01` at sub-microscale error ($4.80 \times 10^{-7}$), damping each residual branch by $0.7071$ restricted the network's non-linear expressive capacity on the complex two-soliton collision (`dev_02`: 0.00319 vs 0.00155 in Trial 033). Unitary residual skips ($h + \sin(Wh)$) allow the network to recruit full non-linear amplitude to resolve sharp soliton collisions.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert hidden layers to unitary residual skips ($h = h + \sin(layer(h))$) in `candidate.py`. Mark Trial 048 as completed and eligible.

## Reason for decision
Trial 033 retains vastly superior mean validation loss (0.0005464 vs 0.001151) and 2x lower error on the hardest two-soliton collision case (`dev_02`). Full unitary residual additions provide the non-linear dynamic range necessary for multi-soliton collisions.
