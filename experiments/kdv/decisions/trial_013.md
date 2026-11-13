# Trial 013 Decision Record: Modified MLP with Coordinate Gating

## Hypothesis
Standard deep feedforward PINNs suffer from gradient pathologies where backpropagated gradients from high-order physical derivatives become exponentially attenuated or unbalanced across layers. Introducing two coordinate-encoder sub-networks ($U$ and $V$) that multiplicatively gate each hidden layer (Wang, Teng, Perdikaris, SISC 2021) will bypass deep network attenuation, injecting direct coordinate gradient signals into every hidden representation layer and accelerating convergence on steep KdV soliton interactions.

## Proposed method change
Adopt the modified MLP architecture proposed by Wang et al. (2021) combined with sinusoidal activation (SIREN):
1. Compute input periodic coordinate representations $X \in \mathbb{R}^5$ containing $[t, \sin(\pi x), \cos(\pi x), u_0, u_{0,x}/\pi]$.
2. Pass $X$ through two coordinate projection layers:
   $$U = \sin(X W_u + b_u)$$
   $$V = \sin(X W_v + b_v)$$
3. Initialize the first hidden layer $H^{(1)} = \sin(X W_1 + b_1)$.
4. For each subsequent hidden layer $k = 1, \dots, L-1$:
   $$Z^{(k)} = \sin(H^{(k)} W_k + b_k)$$
   $$H^{(k+1)} = (1 - Z^{(k)}) \odot U + Z^{(k)} \odot V$$
5. Map to scalar output $u = u_0 + \tanh(\alpha t) \cdot (H^{(L)} W_{\mathrm{out}} + b_{\mathrm{out}})$.
6. Optimize using standard AdamW with cosine decay learning rate schedule ($1.08 \times 10^{-3} \to 10^{-7}$) under the linear temporal curriculum.

## Training objective used
Standard composite KdV physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
The direct multiplicative gating from $U$ and $V$ into every hidden layer ensures that spatial and temporal derivative operators maintain non-vanishing gradient paths directly back to the coordinate representations without decaying through deep weight compositions. This is expected to improve on Trial 004's mean validation loss (0.001260) and especially reduce the residual error on complex multi-soliton interaction cases like `dev_02`.

## Evidence from previous experiments
- In Trial 004, sinusoidal activations delivered our best baseline by preserving 3rd-order spatial derivative fidelity ($\sin''' = -\cos$).
- In Trial 012, slowing down weight trajectory updates hampered convergence on `dev_02` (0.01069) and `dev_03` (0.00373), showing that the bottleneck is not optimizer stability but architectural capacity to resolve sharp localized gradients in multi-frequency waves.
- Multiplicative coordinate gating provides skip-like inductive bias tailored specifically for coordinate-based physical networks.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: modified_mlp_coordinate_gating
- Source: Sifan Wang, Yujun Teng, Paris Perdikaris (SIAM J. Sci. Comput. 2021, arXiv:2001.04536), "Understanding and Mitigating Gradient Flow Pathologies in Physics-Informed Neural Networks".
- Distinctness: Radially distinct from prior MLP structures by introducing dual coordinate projection heads ($U, V$) that multiplicatively modulate intermediate representations at every layer, addressing gradient flow pathologies. Counted toward the overall 15 novelty quota.


## Observed results
- Validation loss:
  - Mean: 0.0112156
  - dev_01: 9.6906e-06
  - dev_02: 0.0237639
  - dev_03: 0.0098733
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 1.84e-6 <= 1e-3, params = 183,362 <= 250,000).
- Optimizer step throughput: ~3,710 steps executed in 297s per case (~12.5 steps/sec), compared to ~8,500 steps (~28.6 steps/sec) in Trial 004's additive residual architecture. Differentiating 3rd-order spatial derivatives ($u_{xxx}$) through 7 consecutive multiplicative gating operations $(1 - Z) \odot U + Z \odot V$ generated an autograd expression graph with high branching factor, more than doubling per-step autograd backward overhead.

## Agent decision
Retain Trial 004 (sinusoidal activation with additive residual skip connections and AdamW) as the current incumbent winning configuration. Mark Trial 013 as completed and eligible, crediting 1 substantive architectural novelty toward the 15 early-stage quota (total now 11 / 15).

## Reason for decision
While multiplicative coordinate gating is theoretically sound for 1st- and 2nd-order PDEs, for 3rd-order dispersive PDEs like KdV the Leibniz product rule expansions during autograd triple differentiation create an overwhelming graph size. This slowed step throughput by 56%, leaving the network with insufficient steps within the 300s budget to refine high-frequency wave interactions. Additive residual connections ($h + \sin(layer(h))$) allow linear gradient flow without product-rule expansion overhead, making them computationally superior under fixed time budgets.
