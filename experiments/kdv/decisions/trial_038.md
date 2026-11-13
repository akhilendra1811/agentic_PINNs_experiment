# Trial 038 Decision Record: AdEMAMix Second-Moment Beta2 Smoothing (beta2 = 0.995)

## Hypothesis
Under dynamic stochastic collocation resampling (where fresh batches of 4,096 points are generated every step), the squared gradient vector $\mathbf{g}_t^2$ is inherently noisy. With our current setting $\beta_2 = 0.990$, the second-moment exponential moving average $\mathbf{v}_t$ has an effective memory horizon of only $1 / (1 - 0.990) = 100$ steps ($\approx 3.7\text{s}$). This short window permits stochastic variance from random collocation coordinates to transmit into the preconditioning denominator $\sqrt{\hat{\mathbf{v}}_t} + \epsilon$, causing coordinate-wise step size chatter that impedes asymptotic convergence during the final cosine annealing stage. Increasing $\beta_2$ to $0.995$ doubles the second-moment averaging window to $200$ steps ($\approx 7.4\text{s}$), producing a smoother, more reliable curvature estimate. This will stabilize gradient descent around the narrow multi-soliton collision crests on `dev_02`, lowering mean validation loss below Trial 033's record 0.0005464.

## Proposed method change
In `candidate.py`:
1. Retain the winning $\text{WIDTH} = 176$ architecture (219,650 parameters, 8 layers, pure $\sin$ activations with additive residuals and unitary scaling).
2. Retain ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.10$).
3. Retain optimal 35% domain expansion temporal curriculum and linear $\alpha$-warmup (0.0 to 2.0 over first 35%).
4. In `train_model`, update `AdEMAMix` instantiation:
   - Change `betas = (0.9, 0.99, 0.999)` to `betas = (0.9, 0.995, 0.999)`.
   - Maintain zero weight decay, base lr $1.08 \times 10^{-3}$, and cosine decay to $10^{-7}$.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Doubling the temporal averaging window of the uncentered variance estimator suppresses high-frequency noise in the per-parameter learning rate scaling. This is particularly advantageous during the second training phase (post-curriculum), where parameters are fine-tuning on the order of $10^{-6}$ adjustments. Step throughput will remain unchanged at $\approx 23.5$ steps/sec.

## Evidence from previous experiments
- In Trial 026 and Trial 029, optimizer momentum improvements unlocked the largest performance breakthroughs in the entire research campaign.
- In Trial 033, the network achieved an unprecedented 0.0005464 with steady, smooth loss descent through step 7,000.
- Stabilizing the variance preconditioner without altering the first-moment momentum buffer preserves all existing trajectory stability.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: ademamix_second_moment_beta2_smoothing
- Source: M. Pagliardini, P. Ablin, D. Grangier (Apple ML Research / EPFL, arXiv:2409.03137, Sep 2024), "The AdEMAMix Optimizer: Better, Faster, Older".
- Distinctness: Evaluates second-moment variance smoothing ($\beta_2 = 0.995$) in AdEMAMix for stochastic collocation-sampled physics-informed neural networks.


## Observed results
- Validation loss:
  - Mean: 79,218,851,317.4 (FAILED / Ineligible due to catastrophic divergence on dev_01)
  - dev_01: 2.3766e+11 (Best posthoc was 0.005768, but late-stage variance lag caused gradient explosion)
  - dev_02: 0.0022054
  - dev_03: 0.0001269
- Eligibility: NOT ELIGIBLE on BC tolerance (`val_bc_total = 0.3876 > 1e-3` on dev_01).
- Optimizer step throughput: Full speed maintained (~6,910 steps per case, 23.26 steps/sec).
- Comparison: Increasing $\beta_2$ from 0.990 to 0.995 doubled the second-moment lag window. On `dev_01`, where gradient norms plunge rapidly by orders of magnitude as the wave fixed point is reached, the sluggish second-moment estimate failed to adapt to sudden curvature changes, causing an ill-conditioned division that diverged the network at the final checkpoint.

## Agent decision
Keep Trial 033 as the **ALL-TIME INCUMBENT WINNER**. Revert $\beta_2$ to 0.990 in `candidate.py`. Mark Trial 038 as completed and ineligible, logging a critical stability boundary on second-moment variance estimation.

## Reason for decision
Trial 033 remains fully eligible and vastly superior (mean validation loss 0.0005464, dev_01: 1.76e-07). $\beta_2 = 0.990$ is mathematically required to ensure the preconditioner responds rapidly enough to vanishing gradients without triggering numerical instability.
