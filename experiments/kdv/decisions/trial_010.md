# Trial 010 Decision Record: Centered RMSprop with Momentum

## Hypothesis
Replacing uncentered AdamW with Centered RMSprop with momentum (Graves, 2013) will provide superior noise normalization under stochastic collocation sampling by scaling updates by true centered variance $\sigma^2 = \mathbb{E}[g^2] - (\mathbb{E}[g])^2$ rather than the uncentered raw second moment $\mathbb{E}[g^2]$.

## Proposed method change
Retain the winning SIREN sinusoidal architecture from Trial 004. In `train_model`, replace `torch.optim.AdamW` with `torch.optim.RMSprop`:
$$m_t = \alpha m_{t-1} + (1 - \alpha) g_t$$
$$v_t = \alpha v_{t-1} + (1 - \alpha) g_t^2$$
$$\sigma_t^2 = v_t - m_t^2$$
$$\Delta \theta_t = \mu \Delta \theta_{t-1} + \frac{\eta_t}{\sqrt{\sigma_t^2 + \epsilon}} g_t$$
$$\theta_t = \theta_{t-1} - \Delta \theta_t$$
with learning rate $\eta_0 = 8.0\times 10^{-4}$, smoothing constant $\alpha = 0.99$, momentum $\mu = 0.9$, $\epsilon = 10^{-8}$, weight decay $5\times 10^{-5}$, cosine decay schedule, and the linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
In standard Adam/RMSprop, when gradients have a consistent non-zero directional drift, the uncentered second moment $v_t$ is dominated by the square of the mean drift, which throttles the effective step size. Centered RMSprop isolates the stochastic collocation variance $\sigma_t^2$, allowing parameters in steady descent trajectories to move freely while dampening noisy coordinates.

## Evidence from previous experiments
Trial 004 established sinusoidal activation as the strongest representation (mean loss 0.001260). Trial 003 (Lion) showed that uniform coordinate updates struggled with multi-frequency waves. Trial 005 (Adan) showed that gradient differences were too sensitive to collocation noise. Centered RMSprop provides an exact statistical variance filter suited for stochastic mini-batching.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: centered_rmsprop_momentum
- Source: Alex Graves (2013), "Generating Sequences With Recurrent Neural Networks", arXiv:1308.0850.
- Distinctness: Radically different normalization mechanism compared to AdamW: computes centered variance $\mathbb{E}[g^2] - \mathbb{E}[g]^2$ rather than raw second moments, preventing steady non-zero gradients from artificially inflating the denominator.

## Observed results
Trial 010 encountered a numerical failure on case dev_01 during step execution (`ValueError: Model returned invalid output`).
- Status: failed (non-finite outputs encountered).
- Root Cause: In Centered RMSprop, when the exponential moving average of the squared gradient $v_t$ closely matches the square of the mean gradient $m_t^2$, the centered variance difference $\sigma_t^2 = v_t - m_t^2$ drops below zero or approaches machine epsilon due to finite floating point precision. Under high momentum ($\mu = 0.9$), dividing by near-zero centered variance caused an explosive parameter update that blew network activations to NaN/Inf.
- Eligibility: Failed (did not complete all three development cases).
- Quota: Uncompleted trials do not earn quota credit under locked runner rules.

## Agent decision
Mark Trial 010 as failed. Retain Trial 004 as the active validation incumbent. Reject centered RMSprop due to numerical instability in third-order PINN optimization.

## Reason for decision
This empirical failure provides valuable negative scientific evidence: while centered variance estimation is theoretically appealing for isolating noise variance from deterministic drift, numerical subtraction $v_t - m_t^2$ is inherently ill-conditioned when gradient drift dominates variance. AdamW's uncentered second moment $v_t$ is strictly monotonic and non-negative, preventing near-zero denominator catastrophes. Next, test an uncentered alternative such as Schedule-Free AdamW.
