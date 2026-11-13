# Experiment 011: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

Trial 009 demonstrated that widening the 2-block ResNet Fourier-PINN to width 192 gave our best performance (mean 0.003390, worst 0.01020), while Trial 010 showed that adding depth was inferior to widening. On modern GPU/MPS hardware, width 256 aligns with hardware memory-coalescing and tensor core tile dimensions (power of 2), enabling high compute efficiency. Expanding the hidden width to 256 will increase representation capacity to 136,706 parameters without sacrificing throughput (~680 steps/s on MPS), facilitating further residual reduction on the challenging large-amplitude cases.

## Proposed method change

Architecture modification to widen hidden layers to 256:
- Retain 2 residual blocks with 8 Fourier frequencies:
  - Input: 17 Fourier features [t/(3pi)-1, sin(w_k t), cos(w_k t)] with w_k = k/2, k=1..8.
  - Input projection: Linear(17, 256) + Tanh.
  - Two residual blocks:
    h = h + Tanh(Linear(256, 256)(h))
    h = h + Tanh(Linear(256, 256)(h))
  - Output projection: Linear(256, 2).
  - Total parameters: 136,706 (< 250k budget).
- Optimization and objective unchanged: Adam with lr decaying exponentially from 1e-3 to 1e-5 over 87.0 s, full batch on all 500 coordinates, soft IC weight 100.0.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Lower mean validation loss than Trial 009 (0.003390) and potential reduction of the worst case (dev_09) below 0.010, leveraging the increased parallel capacity of width 256.

## Evidence from previous experiments

Progressive width scaling has consistently improved validation accuracy: width 48 (Trial 002: 0.0365) -> width 128 (Trial 004: 0.00410) -> width 128 ResNet (Trial 008: 0.00378) -> width 192 ResNet (Trial 009: 0.00339). Across all these trials, the generalization gap remained zero (val/train = 1.00), demonstrating that higher capacity PINNs remain well-regularized by continuous physics collocation.

## Observed results

All 10 cases completed (87.0 s each, ~22.4k steps, 136,706 parameters). Mean validation loss was 0.003530 (Trial 009: 0.003390), worst 0.01027 (dev_09; Trial 009: 0.01020), std 0.00303, mean IC 7.04e-08.
Per case comparison with Trial 009 (width 192):
- dev_01: 0.000466 (Trial 009: 0.000496) - slightly improved
- dev_02: 0.00328 (Trial 009: 0.00324) - practically tied
- dev_03: 0.00269 (Trial 009: 0.00260) - practically tied
- dev_04: 0.00131 (Trial 009: 0.00152) - improved
- dev_05: 0.000240 (Trial 009: 0.000232) - practically tied
- dev_06: 0.00244 (Trial 009: 0.000649) - worse (fell short of Trial 009's breakthrough)
- dev_07: 0.00658 (Trial 009: 0.00631) - practically tied
- dev_08: 0.00425 (Trial 009: 0.00404) - practically tied
- dev_09: 0.01027 (Trial 009: 0.01020) - practically tied
- dev_10: 0.00378 (Trial 009: 0.00462) - improved

Val/train ratio was 1.00 everywhere (no overfitting). However, increasing width from 192 to 256 did not yield an overall improvement (mean 0.00353 vs 0.00339), as the extra parameters slightly slowed per-step optimization without adding necessary physical capacity.

## Agent decision

Reject width 256 as default; retain width 192 (Trial 009) as our champion architecture topology.

## Reason for decision

Width 192 achieves a slightly lower mean validation loss (0.00339 vs 0.00353) with half the parameters (78k vs 137k), providing a cleaner and more parameter-efficient model.

## Next experiment

Trial 012: Activation function investigation. In all previous trials, Tanh activation was used. Tanh has the property that its second derivative tanh''(x) = -2*tanh(x)*(1 - tanh^2(x)) rapidly decays toward zero for |x| > 2, which can cause second-order gradient vanishing during physics residual computation (where dv/dt is differentiated). We will test replacing Tanh with SiLU (Swish: x * sigmoid(x)), which is smooth, non-saturating on the positive domain, and maintains active second derivatives across a wider dynamic range, while keeping the 2-block ResNet (width 192) architecture.
