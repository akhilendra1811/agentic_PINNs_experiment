# Experiment 027: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

Trial 026 proved that tuning Adam's moment timescales to the non-stationary physics of the Sitnikov problem yielded a 17% breakthrough in validation loss (mean 0.0007266) by shortening the second-moment window (beta2 = 0.99). Standard Adam pairs this with beta1 = 0.9 (momentum memory window of ~10 steps). In second-order conservative dynamical systems where the restoring force has steep curvature (e.g. z / (z^2 + rho^2)^{3/2}), a 10-step momentum buffer can induce inertia that causes parameter vectors to overshoot narrow curvature troughs. Reducing beta1 from 0.9 to 0.8 shortens momentum memory to ~5 steps, increasing gradient responsiveness and reducing overshooting along high-curvature directions.

## Proposed method change

Optimizer momentum modification:
- In `train_model`, configure Adam with `betas=(0.8, 0.99)` (was `(0.9, 0.99)` in Trial 026).
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 learnable Fourier frequencies, Tanh activations (84,490 parameters, identical to Trial 026).
- Learning rate schedule: Cosine Annealing from lr0 = 1.0e-3 to lr1 = 1.0e-6 over the 87.0 s budget.
- Gradient norm clipping: max_norm = 1.0.
- Annealed IC loss weight: lambda_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10).
- Objective: L(θ) = physics + lambda_ic * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10). Adam optimizer configured with betas=(0.8, 0.99). Learning rate follows Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)) over 87.0 s budget. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against Trial 026 (betas=(0.9, 0.99), mean 0.0007266, worst 0.001393). If reducing momentum inertia dampens overshooting in steep potential regions, mean validation loss will decrease below 0.00070. If 0.9 is needed to smooth directional noise, validation error will increase.

## Evidence from previous experiments

Trial 026 demonstrated that Adam's moment hyperparameters directly interact with the physical timescales of the ODE. Systematically evaluating the first-moment parameter beta1 completes the optimization timescale analysis.

## Observed results

All 10 cases completed (87.0 s each, ~24.5k steps, 84,490 parameters). Mean validation loss degraded substantially to 0.001837 (Trial 026: 0.0007266, a 2.5x increase), worst case surged to 0.009150 (dev_09; Trial 026: 0.001393), std widened to 0.00268, mean IC 4.51e-10.
Per case comparison with Trial 026 (beta1 = 0.9):
- dev_01: 3.10e-05 (Trial 026: 1.13e-05) - worse
- dev_02: 0.001910 (Trial 026: 0.001393) - worse
- dev_03: 0.001160 (Trial 026: 0.000540) - 2x worse
- dev_04: 0.000225 (Trial 026: 0.000128) - worse
- dev_05: 4.30e-06 (Trial 026: 5.06e-07) - worse
- dev_06: 0.000788 (Trial 026: 0.000618) - worse
- dev_07: 0.001930 (Trial 026: 0.001120) - worse
- dev_08: 0.001660 (Trial 026: 0.001370) - worse
- dev_09: 0.009150 (Trial 026: 0.001100) - 8x worse, late-stage instability (val/train 5.87)
- dev_10: 0.001500 (Trial 026: 0.000986) - worse

All 10 out of 10 cases performed worse with beta1 = 0.8. On dev_09, the reduced momentum buffer failed to filter high-frequency gradient jitter across the narrow potential valley, causing severe late-stage divergence (v/t = 5.87).

## Agent decision

Decisively reject beta1 = 0.8. Firmly retain beta1 = 0.9 (momentum memory ~10 steps) alongside beta2 = 0.99.

## Reason for decision

First-moment momentum (beta1 = 0.9) provides essential directional inertia that averages out gradient oscillations along orthogonal directions in steep potential ravines. Lowering momentum directly destabilizes convergence on high-velocity cases.

## Next experiment

Trial 028: Multi-Layer Residual Blocks (True 2-Layer Residual Branches). In our champion Highway Input Injection architecture (Trial 026), each residual block consists of a single linear layer: h = h + tanh(W[h, feats]). A single-layer residual branch can only execute rank-preserving affine shifts. By upgrading each block to a true 2-layer residual branch:
delta = W2 * tanh(W1 * [h, feats] + b1) + b2
h = h + tanh(delta)
at width 160 (111,690 parameters), the residual branch gains the universal approximation capability of a full hidden layer. This enables the network to compute complex nonlinear orbital perturbations in each block before adding them back to the identity stream. All optimization hyperparameters match champion Trial 026 (Adam betas=(0.9, 0.99), Cosine Annealing, grad clip 1.0, annealed IC).
