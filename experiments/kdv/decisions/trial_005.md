# Trial 005 Decision Record: Adan (Adaptive Nesterov Momentum) Optimizer

## Hypothesis
Replacing standard AdamW with the Adan optimizer (Xie et al., 2022) will accelerate optimization along the steep, curved valleys of the third-order KdV residual manifold by integrating Nesterov momentum estimation and tracking gradient differences as a directional curvature proxy.

## Proposed method change
Preserve the top-performing sinusoidal PINN architecture from Trial 004. In `train_model`, replace `torch.optim.AdamW` with `Adan`:
$$m_k = (1 - \beta_1) m_{k-1} + \beta_1 g_k$$
$$v_k = (1 - \beta_2) v_{k-1} + \beta_2 (g_k - g_{k-1})$$
$$n_k = (1 - \beta_3) n_{k-1} + \beta_3 [g_k + (1 - \beta_2)(g_k - g_{k-1})]^2$$
$$\theta_k = \frac{\theta_{k-1} - \eta_k (m_k + (1 - \beta_2) v_k) / (\sqrt{n_k} + \epsilon)}{1 + \lambda \eta_k}$$
with standard hyperparameters $\beta_1 = 0.02, \beta_2 = 0.08, \beta_3 = 0.01$, learning rate $\eta = 1.0\times 10^{-3}$, weight decay $\lambda = 10^{-4}$, preserving the cosine decay schedule and temporal warm-up curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
Adan's explicit momentum on the gradient difference $(g_k - g_{k-1})$ acts as an extrapolation operator, dampening high-frequency oscillations perpendicular to the valley while speeding progression along the solution trajectory. We expect this to improve convergence speed and lower validation loss further below Trial 004's 0.001260.

## Evidence from previous experiments
Trial 004 proved that sinusoidal activations unlock higher derivative fidelity, reducing mean validation error from 0.003040 to 0.001260. In Trial 003, Lion showed that pure sign momentum lacked the fine adaptive scaling needed for multi-frequency waves. Adan provides the missing bridge: full adaptive coordinate scaling combined with Nesterov curvature anticipation.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: adan_adaptive_nesterov_optimizer
- Source: Xie et al. (NeurIPS 2022), "Adan: Adaptive Nesterov Momentum Algorithm for Faster Optimizing Deep Models", arXiv:2208.06677.
- Distinctness: Unlike AdamW (which tracks only gradient mean and uncentered variance), Adan estimates three distinct moment sequences $(m, v, n)$, uniquely tracking the gradient difference to incorporate Nesterov acceleration without requiring additional gradient evaluations per step.

## Observed results
Trial 005 completed all three cases in 891.06 seconds total (~8,380-8,460 steps per case).
- Mean validation loss: 0.0058116 (worse than Trial 004's 0.0012602)
- Case dev_01 validation: 4.4906e-06
- Case dev_02 validation: 0.0142171
- Case dev_03 validation: 0.0032134
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.95\times 10^{-6} \le 10^{-3}$).

## Agent decision
Do not promote Trial 005. Retain Trial 004 as the active validation incumbent. Mark `adan_adaptive_nesterov_optimizer` as credited novelty in the optimizer category.

## Reason for decision
While Adan maintained numerical stability and strict boundary eligibility, its gradient-difference momentum term $(g_k - g_{k-1})$ suffered from substantial Monte Carlo variance. Because 4,096 fresh uniform collocation points are resampled every optimizer step, the difference between consecutive gradients reflects sample collocation noise rather than deterministic Riemannian curvature along the loss landscape. AdamW's exponential second-moment averaging smooths this stochastic noise significantly better. Next, explore another distinct candidate family (e.g. Snake periodic activation or multi-scale Fourier representations).
