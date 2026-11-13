# Experiment 036: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In all trials so far, the output projection layer `self.out_proj = nn.Linear(WIDTH, 2)` was initialized with standard PyTorch default uniform initialization ($\mathcal{U}(-1/\sqrt{192}, 1/\sqrt{192}) \approx [-0.072, 0.072]$). Consequently, at step 0 before any training, the network's predicted state $[z(0), v(0)]$ is near $[0, 0]$.

However, the physical initial conditions $[z_0, v_0]$ for our development cases have substantial offsets, ranging up to $z_0 = 1.5$ (dev_08) and $v_0 = 1.1$ (dev_09). Under our strong initial IC weight ($\lambda_{ic} = 2000.0$), the initial forward pass produces a massive IC loss ($I(\theta) \approx z_0^2 + v_0^2 \approx 2.5 \implies \lambda_{ic} I(\theta) \approx 5000.0$). This delivers an enormous, unbalanced gradient shock during the first few hundred steps whose sole purpose is shifting the output layer's bias from $\approx 0$ to $[z_0, v_0]$. This transient shock detunes the early weight distributions across all hidden layers.

Because `build_model(case)` is explicitly provided with the physical parameters and initial conditions for each case, we hypothesize that initializing `self.out_proj.bias` directly to $[z_0, v_0]$:
$\text{bias}_\text{out} = [z_0, v_0]$
will center the initial trajectory envelope at the true physical scale from step 0. This reduces the initial IC loss from $\approx 2.5$ to $\approx 0.005$, eliminating the transient initialization shock and allowing early gradients to focus immediately on learning smooth orbital curvature.

## Proposed method change

Architecture initialization modification:
- In `build_model(case)`:
  Pass `case` to `HighwayInputInjectionResNet(case)`.
  Initialize `self.out_proj.bias.data = torch.tensor([case['z0'], case['v0']], dtype=torch.float32)`.
  The weights of `self.out_proj` remain normally initialized.
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 domain-orthogonal learnable Fourier frequencies (ω_k = k / 3.0), single-layer unscaled residual branches, Tanh activations (84,490 parameters, identical to Trial 034).
- Loss weighting: Asymmetric IC annealing from Trial 034 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99) (reverting Trial 035 back to champion 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 034 (mean 0.0003971, worst 0.0008162). Eliminating the initial 5000-magnitude IC gradient shock should protect hidden layer weights and learnable Fourier frequencies from early distortion, accelerating early convergence on high-amplitude cases (dev_07, dev_08) and targeting mean validation loss below 0.00035.

## Evidence from previous experiments

Trial 006 previously attempted rigid algebraic IC conditioning ($z = z_0 + v_0 t + t^2 N(t)$) which blew up because of the polynomial $t^2$ factor at late times. In contrast, initializing the linear output bias to $[z_0, v_0]$ introduces zero algebraic distortion or gradient artifacts while providing the exact physical origin anchor.

## Observed results

All 10 development cases completed (87.0 s each, ~22.9k steps, 84,490 parameters). The hypothesis was decisively refuted by a spectacular failure mode:
- Mean validation loss exploded from 0.0003971 (Trial 034) to 0.9062 (a ~2300x catastrophe!).
- Worst-case validation loss blew up to 4.956 on dev_08.
- 7 out of 10 cases completely diverged with massive val/train generalization ratios (v/t > 1,000,000!):
  - dev_02: val = 0.289, v/t = 6,247,842
  - dev_03: val = 1.120, v/t = 32,047,011
  - dev_04: val = 0.630, v/t = 401,255
  - dev_07: val = 0.329, v/t = 36,732,549
  - dev_08: val = 4.956, v/t = 145,812,742
  - dev_09: val = 0.144, v/t = 4,207,480
  - dev_10: val = 1.600, v/t = 47,693,596
- In contrast, the IC loss for these diverged cases was nearly zero (e.g. 6.1e-12 on dev_08, 1.8e-13 on dev_09!).

Physical and optimization explanation: This is a classic manifestation of "boundary shortcut collapse" in PINNs. By hard-initializing bias = [z0, v0], the output projection y(t) = W h(t) + [z0, v0] satisfies the initial condition at t=0 simply by driving W h(0) -> 0. Under the large initial IC weight (lambda_ic = 2000), any gradient that moves W away from the kernel of h(0) is heavily penalized. The optimizer discovers a trivial spurious attractor: collapse W toward 0, leaving y(t) ≈ [z0, v0] as a flat, static trajectory! While the IC error is literally 1e-13, the interior physics loss across 0..6π is completely violated (val = 4.96). When bias is initialized randomly near 0 (as in Trial 034), the network cannot take this shortcut: the weights W MUST actively learn dynamic oscillatory representations to balance both the ODE residual and the boundary loss simultaneously, enforcing true global trajectory synthesis.

## Agent decision

Reject: Initializing output bias to [z0, v0] causes catastrophic boundary shortcut collapse. Revert immediately to default unbiased output initialization from champion Trial 034.

## Reason for decision

Validation error exploded from 0.0003971 to 0.9062 due to optimizer collapse into static boundary attractors. Default unbiased output initialization forces true global trajectory learning.

## Next experiment

Trial 037: Terminal Learning Rate Floor Decaying to 1e-7 (Cosine Annealing lr0=1e-3, lr1=1e-7).
In all trials since Trial 014, the terminal learning rate floor has been lr1 = 1.0e-6. In Trial 034 (mean 0.0003971), we saw that validation loss was still monotonically decreasing in the final seconds of training. However, with Adam beta2 = 0.99, an lr of 1.0e-6 yields parameter step increments on the order of 1e-5 to 1e-6 (since step = lr / sqrt(v_t) * m_t). In the deep asymptotic convergence regime, reducing the learning rate floor by one order of magnitude to lr1 = 1.0e-7 allows the optimizer to perform ultra-fine gradient descent along the narrow bottom of the ODE loss basin during the final 10% of training, without triggering boundary or curvature instability. All other settings match champion Trial 034.
