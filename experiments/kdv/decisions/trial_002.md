# Trial 002 Decision Record: Layer-wise Adaptive Activation Functions (L-LAAF)

## Hypothesis
Introducing trainable layer-wise scaling parameters $a_l$ to the residual tanh activations (Locally Adaptive Activation Functions, L-LAAF) will dynamically optimize activation slope and local gradient flow, accelerating convergence on stiff nonlinear KdV advection and dispersive terms compared to the static baseline.

## Proposed method change
Modify `KdVPINN` in `candidate.py` to instantiate a list of scalar learnable slope parameters $a_l$, initialized to 1.0, for each of the 7 residual hidden layers:
$$h_{l+1} = h_l + \tanh(a_l \cdot W_l h_l + b_l)$$
All other architectural dimensions, optimizer settings (AdamW, lr=1.08e-3, cosine decay), loss definitions, and curriculum schedules remain identical to baseline Trial 001.

## Training objective used
Identical to Trial 001:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled each optimizer step, alongside 512 spatial IC points at $t=0$.

## Expected effect
The trainable slope parameters allow the network to autonomously steepen or flatten activations layer-by-layer. This is expected to improve the worst-case development validation loss (dev_02) below 0.00717 while maintaining exact initial condition adherence ($L_{\mathrm{IC}} \le 10^{-3}$) and periodic boundary continuity.

## Evidence from previous experiments
Baseline Trial 001 converged to a mean validation loss of 0.003040, but case dev_02 was significantly worse (0.007173) than dev_01 (3.04e-6) and dev_03 (0.001943). The higher frequency / amplitude interaction in dev_02 indicates a need for increased gradient responsiveness without destabilizing the deep 8-layer backbone.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: laaf_layerwise_slope_tanh
- Source: Jagtap, Kawaguchi, Karniadakis (2019), "Adaptive activation functions accelerate convergence in deep and physics-informed neural networks", JCP / arXiv:1906.01170.
- Distinctness: Unlike the fixed static tanh activation of Trial 001, L-LAAF alters the optimization landscape dynamically through learnable activation scaling. It is $C^\infty$ smooth, preserving clean autograd computation of the 3rd spatial derivative $u_{xxx}$.

## Observed results
Trial 002 completed all three cases in 891.09 seconds total training time (~7,900 optimizer steps per case).
- Mean validation loss: 0.0044307 (higher than Trial 001's 0.0030397)
- Case dev_01 validation: 4.2742e-06 (vs 3.0361e-06 in 001)
- Case dev_02 validation: 0.0099672 (vs 0.0071730 in 001)
- Case dev_03 validation: 0.0033206 (vs 0.0019431 in 001)
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.88\times 10^{-6} \le 10^{-3}$).
- Throughput: Averaged 26.6 steps/second compared to 28.7 steps/second in Trial 001, yielding ~700 fewer optimization steps within the 300-second budget due to autograd graph overhead over the learnable slope tensor leaves.

## Agent decision
Do not promote Trial 002 to incumbent. Retain Trial 001 as the active validation incumbent. Mark `laaf_layerwise_slope_tanh` as credited novelty in the activation category.

## Reason for decision
While L-LAAF maintains numerical stability and strict boundary eligibility, dynamically adapting the activation slope slightly degraded empirical PDE residual minimization under the fixed 300-second wall-clock budget. The additional autograd graph depth decreased step throughput by ~7%, and free slope scaling without regularization allowed slight deviation from the optimal residual highway. Next, explore an optimizer-focused innovation or a fundamentally different activation family (e.g. Snake periodic activation).
