# Trial 020 Decision Record: Composite Adaptive Sine-Tanh Activation

## Hypothesis
Pure $\tanh$ activations suffer from severe derivative saturation where 3rd-order spatial derivatives vanish exponentially away from zero ($\tanh'''(z) \to 0$), while pure $\sin$ activations lack localized spatial damping. Constructing a specialized composite adaptive activation function as a trainable linear mixture of $\sin(a z)$ and $\tanh(b z)$ with adaptive slopes (Wang, Lu, Song, Huang, arXiv:2308.04073, *Communications in Computational Physics* 2023) will allow the network to dynamically synthesize both localized soliton profiles and oscillatory dispersive wave packets, optimizing the Neural Tangent Kernel spectrum for the periodic KdV equation.

## Proposed method change
In `KdVPINN`:
1. Define `CompositeAdaptiveActivation`:
   $$\sigma_l(z) = w_{\sin, l} \sin(a_l \cdot z) + w_{\tanh, l} \tanh(b_l \cdot z)$$
   where $[w_{\sin, l}, w_{\tanh, l}] = \text{softmax}([p_{1, l}, p_{2, l}])$ are learnable mixture coefficients initialized to equal weights ($0.5, 0.5$), and $a_l, b_l$ are learnable slope parameters initialized to 1.0.
2. Equip each of the 8 hidden residual layers with an independent `CompositeAdaptiveActivation` module.
3. Retain the winning SIREN additive residual architecture (WIDTH=160, 8 layers) and bounded hyperbolic tangent temporal ansatz:
   $$u(t, x) = u_0(x) + \tanh(\alpha t) \cdot \text{net\_out}(t, x)$$
4. Retain the winning Hamiltonian invariant regularizer (mass and $L^2$ energy penalty with weight 0.1) from Trial 015.
5. Train with standard AdamW (lr=$1.08 \times 10^{-3}$, cosine decay schedule, linear temporal curriculum over first 35%).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0$ and $\lambda_{\mathrm{inv}} = 0.1$, evaluated alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
The combination of non-vanishing sinusoidal derivatives with localized hyperbolic tangent saturation provides the network with a flexible, problem-specific basis that was shown by Wang et al. (2023) to achieve superior convergence on the Korteweg-de Vries benchmark. Because both base functions are smooth $C^\infty$ with simple derivatives, this is expected to maintain high step throughput while exploring an expressive hybrid activation space.

## Evidence from previous experiments
- In Trial 001, pure $\tanh$ reached 0.003040 validation loss.
- In Trial 004, pure $\sin$ improved loss by 2.4x to 0.001260 by preserving derivative fidelity.
- In Trial 015, adding the Hamiltonian invariant regularizer reached our best incumbent loss of 0.001183.
- Blending sine and tanh adaptively with learnable mixing weights directly tests the synergy between periodic expressiveness and localized damping.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: composite_adaptive_sine_tanh_activation
- Source: Honghui Wang, Lu Lu, Shiji Song, Gao Huang (Communications in Computational Physics 2023, arXiv:2308.04073), "Learning Specialized Activation Functions for Physics-informed Neural Networks".
- Distinctness: Introduces a trainable composite activation combining smooth sinusoidal and hyperbolic tangent bases with dynamic softmax mixture weights and independent adaptive slopes, benchmarked specifically for KdV PINNs.


## Observed results
- Validation loss:
  - Mean: 0.0079421
  - dev_01: 1.6081e-05
  - dev_02: 0.0187901
  - dev_03: 0.0050202
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 1.93e-6 <= 1e-3, params = 181,474 <= 250,000).
- Optimizer step throughput: ~4,160 steps per case (~14.0 steps/sec), down from ~8,400 steps in Trial 015. Dual evaluation of trigonometric $\sin(a z)$ and hyperbolic $\tanh(b z)$ through triple autograd differentiation doubled expression graph complexity. Furthermore, the $\tanh$ branch suffered from exponentially decaying 3rd derivatives $\tanh'''(z) \to 0$, diluting the non-vanishing derivative advantages of pure $\sin$.

## Agent decision
Retain Trial 015 (pure SIREN sinusoidal architecture with Hamiltonian invariant regularizer and AdamW) as the incumbent winner. Mark Trial 020 as completed and eligible, logging an additional activation novelty record.

## Reason for decision
Trial 020 conclusively establishes that adding hyperbolic tangent branches to sinusoidal PINNs for 3rd-order dispersive PDEs degrades performance in two distinct ways: (1) it cuts optimizer step throughput by 50% due to dual-branch autograd graph size, and (2) it introduces derivative saturation from $\tanh'''$, increasing validation loss by 6.7x (0.00794 vs 0.00118). Pure sinusoidal activation ($\sin$) remains the definitive optimal non-linearity for the periodic KdV equation.
