# Trial 019 Decision Record: Adaptive Frequency SIREN (Learnable Frequency Scaling)

## Hypothesis
Standard SIREN uses a fixed unitary frequency scaling factor $\omega_0 = 1.0$ across all layers ($\sin(z)$). Because the periodic KdV equation features small dispersive regularization ($\delta = 0.022^2 \approx 4.84 \times 10^{-4}$), localized soliton pulses exhibit extremely sharp spatial gradients and high-frequency dispersive wave packets. Introducing learnable layer-wise frequency scaling parameters $\omega_l$ into each sinusoidal activation $\sin(\omega_l \cdot z)$ (Sitzmann et al., 2020; Jagtap et al., 2020) will allow the network to dynamically adapt its spectral representation bandwidth to match localized wave steepening, reducing residual loss on multi-frequency collisions (`dev_02` and `dev_03`).

## Proposed method change
In `KdVPINN`:
1. Define `AdaptiveSinActivation(init_omega=1.0)` with a trainable scalar parameter `omega`:
   $$\phi_l(z) = \sin(\omega_l \cdot z)$$
2. Equip each of the 8 hidden residual layers with an independent trainable frequency parameter $\omega_l$, initialized to 1.0.
3. Keep the winning SIREN additive residual architecture (WIDTH=160, 8 layers) and bounded hyperbolic tangent temporal ansatz:
   $$u(t, x) = u_0(x) + \tanh(\alpha t) \cdot \text{net\_out}(t, x)$$
4. Retain the winning Hamiltonian invariant regularizer (mass and $L^2$ energy penalty with weight 0.1) from Trial 015.
5. Train with standard AdamW (lr=$1.08 \times 10^{-3}$, cosine decay schedule, linear temporal curriculum over first 35%).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0$ and $\lambda_{\mathrm{inv}} = 0.1$, evaluated alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Because $\omega_l$ is a scalar multiplier inside each activation, it adds only 8 trainable parameters to the network ($181,450 \le 250,000$) and incurs virtually zero autograd computational overhead, preserving maximum step throughput (~8,400 steps per case). By enabling the network to learn higher effective frequencies $\omega_l > 1$ where steep solitons form, this is expected to improve resolution of localized dispersive gradients, potentially driving mean validation loss below Trial 015's 0.001183.

## Evidence from previous experiments
- In Trial 004, fixed sinusoidal activation $\sin(x)$ established the dramatic power of periodic representations for 3rd-order KdV derivatives ($u_{xxx}$), cutting validation loss by 2.4x.
- In Trial 015, adding the zero-order Hamiltonian invariant regularizer established our current incumbent winner (0.001183 mean, 0.003097 worst-case).
- In Trial 018, C-AdamW showed that AdamW remains the best optimizer, indicating that further progress lies in enhancing the network's spectral capacity without sacrificing throughput.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: adaptive_frequency_siren
- Source: Vincent Sitzmann et al. (NeurIPS 2020, arXiv:2006.09661), "Implicit Neural Representations with Periodic Activation Functions" and Ameya Jagtap et al. (2020), "Locally adaptive activation functions with slope recovery for deep and physics-informed neural networks".
- Distinctness: Introduces independent trainable frequency scaling parameters $\omega_l$ into each sinusoidal activation layer, providing dynamic spectral bandwidth modulation across depth.


## Observed results
- Validation loss:
  - Mean: 0.0013838
  - dev_01: 4.3313e-06
  - dev_02: 0.0035582
  - dev_03: 0.0005889
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.32e-6 <= 1e-3, params = 181,450 <= 250,000).
- Comparison: Adaptive frequency scaling achieved strong validation loss, outperforming baseline Trial 001 (0.003040) by 2.2x. However, the additional multiplication node inside each activation layer slightly increased autograd graph depth during 3rd-order spatial differentiation, reducing optimizer steps from ~8,400 to ~7,500. Fixed unitary frequency SIREN (Trial 015) retains a slight edge (0.001183 mean, 0.003097 worst-case).

## Agent decision
Retain Trial 015 (unitary frequency sinusoidal SIREN architecture with Hamiltonian invariant regularizer and AdamW) as the incumbent winner. Mark Trial 019 as completed and eligible, crediting an additional activation-focused exploration trial.

## Reason for decision
Trial 019 demonstrated that learnable frequency scaling provides a strong, flexible periodic representation, but fixed unitary frequency with additive residual connections provides optimal computational efficiency (~11% more optimizer steps within the 300s budget) and slightly superior numerical convergence on the KdV test cases. We proceed to investigate composite adaptive activations combining sine and hyperbolic tangent representations.
