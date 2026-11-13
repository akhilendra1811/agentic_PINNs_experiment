# Experiment 012: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trials 004, 008, 009, and 011, Tanh was used as the activation function throughout the network. The second derivative of Tanh, tanh''(x) = -2*tanh(x)*(1 - tanh^2(x)), decays exponentially toward zero as |x| exceeds 2. In PINN formulations where second-order derivatives are required (dv/dt), saturated hidden units produce zero second-order gradient curvature, potentially stalling optimization on high-acceleration regions. Replacing Tanh with SiLU (Swish: x * sigmoid(x)) provides continuous, non-saturating derivatives across a broader dynamic range, which should improve second-derivative sensitivity and accelerate residual convergence.

## Proposed method change

Activation function replacement:
- Architecture: 2-block ResNet Fourier-PINN with width 192 and 8 Fourier frequencies (77,954 parameters, identical to Trial 009).
- Replace all Tanh activations with SiLU (Swish).
- Optimization and objective unchanged: Adam with exponential lr decay from 1e-3 to 1e-5 over 87.0 s, full batch on all 500 coordinates, soft IC weight 100.0.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Comparison against Trial 009 (Tanh, mean 0.003390, worst 0.01020). If SiLU's smoother, non-saturating second derivative aids higher-order ODE gradient propagation, mean validation loss will decrease below 0.003390.

## Evidence from previous experiments

Trial 009 established width 192 ResNet with Tanh as our best model (0.003390). Trials 010 and 011 showed that depth and width variations around this operating point have reached diminishing returns, making the activation function nonlinearity the next high-leverage component to investigate.

## Observed results

All 10 cases completed (87.0 s each, ~21.2k steps, 77,954 parameters). Mean validation loss degraded to 0.004045 (Trial 009: 0.003390), worst 0.01165 (dev_09; Trial 009: 0.01020), std 0.00346, mean IC 1.90e-08.
Per case comparison with Trial 009 (Tanh):
- dev_01: 0.000557 (Trial 009: 0.000496) - slightly worse
- dev_02: 0.00420 (Trial 009: 0.00324) - worse
- dev_03: 0.00366 (Trial 009: 0.00260) - worse
- dev_04: 0.00148 (Trial 009: 0.00152) - practically tied
- dev_05: 0.000239 (Trial 009: 0.000232) - practically tied
- dev_06: 0.00216 (Trial 009: 0.000649) - 3.3x worse
- dev_07: 0.00752 (Trial 009: 0.00631) - worse
- dev_08: 0.00403 (Trial 009: 0.00404) - practically tied
- dev_09: 0.01165 (Trial 009: 0.01020) - worse
- dev_10: 0.00494 (Trial 009: 0.00462) - worse

Tanh outperformed SiLU on 8 out of 10 cases, with a particularly marked difference on dev_06 (0.00065 vs 0.00216).

## Agent decision

Reject SiLU. Retain Tanh as the standard activation function for the ResNet Fourier-PINN.

## Reason for decision

The Sitnikov potential V(z) = -1/sqrt(z^2 + rho^2) is symmetric under reflection z -> -z, producing an odd restoring force F(-z) = -F(z). Tanh is an odd symmetric function (tanh(-x) = -tanh(x)), naturally embedding this reflection symmetry into the network representation. SiLU is asymmetric, breaking this physical inductive bias and leading to higher residual errors across the board.

## Next experiment

Trial 013: Learning rate schedule optimization. In Trial 009, Adam used an exponential decay from lr0=1e-3 to lr1=1e-5. While effective, exponential decay drops the learning rate rapidly in the middle of training, reducing exploration. A Cosine Annealing schedule maintains higher learning rates during the exploratory middle phase and smoothly transitions to a fine-tuning rate:
lr(f) = lr1 + 0.5 * (lr0 - lr1) * (1 + cos(pi * f))
with lr0 = 2e-3 and lr1 = 1e-6 over the 87 s budget, using our champion Trial 009 architecture (width 192 ResNet Fourier-PINN with Tanh).
