# Experiment 028: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In our champion Highway Input Injection architecture (Trial 026), each residual block contains only a single linear transformation: h = h + tanh(Linear([h, feats])). By linear algebra, a single linear layer plus activation cannot model complex cross-feature interactions or multi-modal residual corrections. In standard deep ResNet design (He et al.), residual blocks contain two sequential linear layers separated by an activation:
delta = W2 * tanh(W1 * [h, feats] + b1) + b2
h = h + tanh(delta)
This two-layer residual branch forms a universal nonlinear approximator, enabling each block to learn sophisticated nonlinear orbital perturbations against the identity stream. At width 160, this architecture has 111,690 parameters (< 250k budget), combining deep residual expressivity with compact execution.

## Proposed method change

Architecture modification for two-layer residual branches:
- In `TwoLayerBlockHighwayResNet`:
  - 8 learnable Fourier frequencies (initialized on uniform grid 0.5*k).
  - Initial projection: Linear(17, 160) + Tanh.
  - Residual Block 1 (2-layer branch):
    d1 = Linear(160, 160)(Tanh(Linear(160 + 17, 160)([h, feats])))
    h = h + Tanh(d1)
  - Residual Block 2 (2-layer branch):
    d2 = Linear(160, 160)(Tanh(Linear(160 + 17, 160)([h, feats])))
    h = h + Tanh(d2)
  - Output projection: Linear(160, 2).
  - Total parameters: 111,690.
- Optimization and schedule identical to champion Trial 026: Adam with betas=(0.9, 0.99), Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6), gradient norm clipping (max_norm = 1.0), annealed IC loss weight (1000 -> 100 over first 10% of budget), full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10). Adam optimizer configured with betas=(0.9, 0.99). Learning rate follows Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)) over 87.0 s budget. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against Trial 026 (1-layer branches, mean 0.0007266, worst 0.001393). Two-layer residual branches should enhance the nonlinear approximation capacity of each block, driving mean validation loss below 0.00065.

## Evidence from previous experiments

Trial 026 established our champion score (0.0007266). All previous trials scaled width and depth uniformly; upgrading the internal functional depth of the residual branches themselves directly targets representation bottlenecks.

## Observed results

All 10 cases completed (87.0 s each, ~19.3k steps, 111,690 parameters). Mean validation loss degraded to 0.003057 (Trial 026: 0.0007266, a 4x increase), worst case surged to 0.02001 (dev_03; Trial 026: 0.001393), std 0.00603, mean IC 6.08e-10.
Per case comparison with Trial 026 (1-layer residual branches):
- dev_01: 6.39e-05 (Trial 026: 1.13e-05) - higher
- dev_02: 0.001070 (Trial 026: 0.001393) - 23% improvement
- dev_03: 0.020010 (Trial 026: 0.000540) - 37x worse, late-stage divergence (v/t = 26.57)
- dev_04: 0.000191 (Trial 026: 0.000128) - higher
- dev_05: 8.90e-06 (Trial 026: 5.06e-07) - higher
- dev_06: 0.000860 (Trial 026: 0.000618) - higher
- dev_07: 0.001760 (Trial 026: 0.001120) - higher
- dev_08: 0.002570 (Trial 026: 0.001370) - higher
- dev_09: 0.002390 (Trial 026: 0.001100) - higher
- dev_10: 0.001650 (Trial 026: 0.000986) - higher

The two-layer residual branches suffered a 20% step throughput penalty (~19.3k steps vs ~23.9k steps in Trial 026) and introduced higher-order autograd instability. Because the Sitnikov ODE loss evaluates second-order derivatives (dv/dt), differentiating through two sequential linear layers and activations inside each residual branch compounded Hessian products across four layers, triggering late-stage divergence in dev_03.

## Agent decision

Reject two-layer residual branches. Firmly retain single-layer residual branches in the Highway Input Injection architecture from Trial 026.

## Reason for decision

Single-layer residual branches provide a clean, shallow derivative graph that stabilizes higher-order automatic differentiation, preserves high step throughput, and prevents Hessian gradient explosion.

## Next experiment

Trial 029: Asymmetric IC Annealing Schedule (Initial Anchor 2000 -> Terminal Floor 50). In Trial 026, the IC loss weight annealed from 1000 to 100 over the first 10% of training. We will test strengthening early trajectory pinning by increasing initial IC weight to IC_W_INIT = 2000 over the first 15% (frac <= 0.15), and relaxing the terminal IC weight to IC_W_BASE = 50.0:
lambda_ic(f) = 50.0 + 1950.0 * max(0.0, 1.0 - f / 0.15)
This reinforces initial phase space locking during the critical early orbital formation phase while freeing an extra 50% of late-stage gradient capacity to minimize interior physics residuals. All architecture and optimizer settings match champion Trial 026.
