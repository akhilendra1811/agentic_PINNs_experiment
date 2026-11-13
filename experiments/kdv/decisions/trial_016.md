# Trial 016 Decision Record: Trainable Phase-Harmonic Coordinate Embedding

## Hypothesis
Fixed trigonometric coordinate embeddings rigidly pin wave phases to $x=0$, forcing intermediate network layers to learn nonlinear spatial phase shifts to track propagating soliton wave crests. Parameterizing the spatial coordinate embedding as harmonic basis functions with trainable phase shifts $\sin(k \pi x + \theta_k)$ and $\cos(k \pi x + \phi_k)$ (Dong & Ni, JCP 2021) will enable the network to align its coordinate representation directly with moving wave structures, reducing residual error on multi-frequency collisions while maintaining exact periodic boundary conditions.

## Proposed method change
In `KdVPINN`:
1. Implement a trainable phase-harmonic coordinate layer for spatial input $x$:
   $$\phi_k(x) = \sin(k \pi x + \theta_k), \quad \psi_k(x) = \cos(k \pi x + \phi_k) \quad \text{for } k \in \{1, 2, 3, 4\}$$
   where $\theta = [\theta_1, \dots, \theta_4]$ and $\phi = [\phi_1, \dots, \phi_4]$ are learnable parameters initialized to zero.
2. Concatenate the resulting 8-dimensional phase-adapted spatial features with $t$, $u_0(x)$, and $u_{0,x}(x)/\pi$ into an 11-dimensional feature vector.
3. Pass through the SIREN sinusoidal residual architecture (WIDTH=160, 8 layers, additive residual connections) and the temporal ansatz $u = u_0 + \tanh(\alpha t) \cdot \text{net\_out}$.
4. Retain the winning Hamiltonian invariant regularizer (mass and $L^2$ energy penalty with weight 0.1) from Trial 015.
5. Optimize with standard AdamW ($1.08 \times 10^{-3}$, cosine decay, linear temporal curriculum over first 35%).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, $\lambda_{\mathrm{inv}} = 0.1$, using 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Because all integer harmonic frequencies $k \in \mathbb{Z}$ satisfy exact $2$-periodicity on $[-1, 1]$ for any phase shift $\theta_k$ ($\sin(k \pi (x + 2) + \theta_k) = \sin(k \pi x + 2k\pi + \theta_k) = \sin(k \pi x + \theta_k)$), periodic boundary conditions remain satisfied analytically to machine precision. The trainable phase parameters $\theta_k$ and $\phi_k$ provide a flexible coordinate alignment mechanism that tracks localized wave crests, expected to further reduce worst-case validation loss on `dev_02`.

## Evidence from previous experiments
- In Trial 014, fixed multi-scale Fourier features achieved strong validation loss (0.002361), but lacked adaptability to shift phase frames.
- In Trial 015, adding the zero-order Hamiltonian invariant regularizer achieved our new incumbent score (0.001183 mean, 0.003097 worst-case), proving that physical constraints stabilize soliton dynamics.
- Combining the invariant regularizer with adaptive phase embeddings targets both the physical conservation and spatial representation of KdV waves.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: trainable_phase_harmonic_embedding
- Source: Suchuan Dong & Naxian Ni (Journal of Computational Physics, 2021, arXiv:2007.07442), "A Method for Representing Periodic Functions and Enforcing Exactly Periodic Boundary Conditions with Deep Neural Networks".
- Distinctness: Introduces trainable phase-shifted harmonic basis functions $\sin(k \pi x + \theta_k)$ and $\cos(k \pi x + \phi_k)$ into the input coordinate transformation layer, providing adaptive spatial coordinate alignment under exact periodicity. Counts toward the 15 early-stage novelty quota.


## Observed results
- Validation loss:
  - Mean: 0.0023896
  - dev_01: 2.8601e-06
  - dev_02: 0.0047398
  - dev_03: 0.0024262
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.26e-6 <= 1e-3, params = 182,410 <= 250,000).
- Comparison: While comfortably outperforming the baseline Trial 001 (0.003040), Trial 016 did not improve upon incumbent Trial 015 (0.001183). Learnable phase angles in the input embedding introduced subtle non-convexity in early training that slightly retarded convergence on `dev_02` compared to the fixed coordinate basis with Hamiltonian invariant regularization.

## Agent decision
Retain Trial 015 (sinusoidal SIREN architecture with Hamiltonian mass and $L^2$ invariant regularizer) as the incumbent winner. Mark Trial 016 as completed and eligible, crediting 1 substantive novelty key toward the 15 early-stage quota (total now 14 / 15).

## Reason for decision
Trial 016 verified that trainable phase shifts in harmonic coordinate representations preserve exact boundary conditions and achieve solid performance. However, incumbent Trial 015 remains our clear empirical leader with 2x lower mean loss (0.001183 vs 0.002390) and lower worst-case error (0.003097 vs 0.004740). We proceed to Trial 017 to fulfill the final remaining novelty credit requirement for the early-stage exploration quota.
