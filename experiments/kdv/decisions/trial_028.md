# Trial 028 Decision Record: First-Layer Frequency Scaling in SIREN

## Hypothesis
Under standard linear layer initialization, the first-layer pre-activations $z = W x + b$ have variance $\sigma^2 \approx 1/3$, confining initial outputs to $|z| < 0.5$ where $\sin(z) \approx z$ behaves almost purely linearly (Sitzmann et al., NeurIPS 2020). Consequently, the network begins training in an essentially linear subspace, requiring extensive optimization iterations simply to expand weight magnitudes into the non-linear oscillatory regime required to model sharp dispersive wave fronts. Introducing Sitzmann's first-layer frequency scaling factor $\omega_0 = 3.0$ ($\mathbf{h}_1 = \sin(\omega_0 (W \mathbf{x} + \mathbf{b}))$) maps the input coordinates across multiple periodic wave cycles $[-3\pi, 3\pi]$ from initialization. This immediately expands the network's spectral bandwidth, accelerating convergence on steep multi-soliton wave crests and improving upon Trial 027's record 0.0007327 mean validation loss.

## Proposed method change
In `candidate.py`:
1. Retain the winning targeted dual-harmonic input coordinates ($k \in \{1, 2\}$, $u_0, u_{0,x}/\pi$).
2. Retain the winning AdEMAMix optimizer ($\beta_1=0.9, \beta_2=0.99, \beta_3=0.999, \alpha=2.0$, zero weight decay, peak lr $1.08 \times 10^{-3}$).
3. Retain high-density Hamiltonian quadrature ($N_x=256$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.1$).
4. Retain 35% domain curriculum pacing.
5. In `KdVPINN`:
   - Define `OMEGA_0 = 3.0`.
   - Update `self.in_proj` forward pass to apply `torch.sin(OMEGA_0 * self.in_proj_linear(features))`.
   - Keep hidden residual layers with unitary scale $\sin(\mathbf{h} + \text{layer}(\mathbf{h}))$.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, evaluated over $S=8$ time slices with $N_x=256$ spatial quadrature points per slice, alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Multiplying first-layer pre-activations by $\omega_0 = 3.0$ shifts the initial activation values from the small-angle linear regime into the full sinusoidal domain $[-1, 1]$ with non-vanishing 3rd derivatives ($\frac{d^3}{dz^3}\sin(\omega_0 z) = -\omega_0^3 \cos(\omega_0 z)$). This expands the early dynamic range of the PDE residual loss and prevents low-frequency spectral bias, particularly during the early curriculum expansion phase.

## Evidence from previous experiments
- In Trial 004, introducing pure sinusoidal activations produced our first 2.4x leap over baseline.
- In Trial 024, eliminating weight decay allowed weights to grow, highlighting that weight magnitude constraints restrict spectral capacity.
- In Trial 027, resolving narrow soliton peaks via fine spatial quadrature unlocked record validation performance, showing that the physical system is limited by high-frequency spatial resolution.

## Literature and novelty assessment
- Category: activation
- Novelty credit: true
- Novelty key: siren_first_layer_omega_scaling
- Source: V. Sitzmann, J. Martel, A. Bergman, D. Lindell, G. Wetzstein (Stanford University, NeurIPS 2020), "Implicit Neural Representations with Periodic Activation Functions", arXiv:2006.09661.
- Distinctness: Formulates explicit first-layer $\omega_0 = 3.0$ sinusoidal frequency scaling in combination with targeted dual-harmonic projections and AdEMAMix for dispersive PDE solving.


## Observed results
- Validation loss:
  - Mean: 0.0264297 (Higher than incumbent Trial 027: 0.0007327)
  - dev_01: 0.0769939 (Diverged at final checkpoint; best posthoc was 0.001638)
  - dev_02: 0.0022035 (Strong, competitive with Trial 027's 0.0021435)
  - dev_03: 0.0000916
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.50e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~8,110 steps per case, 27.30 steps/sec).
- Comparison: While $\omega_0 = 3.0$ provided strong representation for multi-soliton collisions on `dev_02` (0.002203), applying $\omega_0 = 3.0$ without inverse initialization re-scaling inflated downstream activation variance by a factor of 9, inducing late-training gradient instability on single-mode case `dev_01`.

## Agent decision
Keep Trial 027 as the **INCUMBENT WINNER**. Revert first-layer frequency scaling back to unitary scale ($\omega_0 = 1.0$) in `candidate.py`. Mark Trial 028 as completed and eligible.

## Reason for decision
Trial 027 remains vastly superior on mean validation loss (0.0007327 vs 0.0264297) and worst-case stability. The hypothesis that first-layer frequency scaling alone would accelerate convergence is refuted in the absence of explicit variance-preserving weight initialization.
