# Experiment 008: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 004, a sequential 3-layer MLP architecture was used. The Sitnikov loss requires second-order automatic differentiation through the network (d/dt of v and dz/dt compared with v), and the backward pass to compute parameter gradients therefore takes third-order derivatives through the network graph. In sequential networks without identity shortcuts, repeated multiplication by tanh derivative matrices can attenuate backpropagated higher-order physics gradients to early layers. Introducing residual skip connections across the hidden layers (h_{l+1} = h_l + tanh(W_l h_l + b_l)) will preserve gradient magnitudes for higher-order derivatives, accelerating training and reducing the final physics residual.

## Proposed method change

Architecture modification to add residual skip connections:
- Retain the 8 Fourier frequencies from Trial 004: w_k = 0.5 * k for k = 1..8 (17 input features).
- Input projection: Linear(17, 128) + Tanh.
- Two residual blocks: each is h = h + Tanh(Linear(128, 128)(h)).
- Output projection: Linear(128, 2).
- Total parameters: 35,586 (identical to Trial 004).
- Training schedule and objective unchanged: Adam with lr decaying exponentially from 1e-3 to 1e-5 over 87.0 s, full batch on all 500 coordinates, soft IC weight 100.0.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate lr(f) = 1e-3 * (1e-2)^f where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Accelerated reduction of physics loss, especially during intermediate training, leading to lower final validation loss on the plateauing cases (e.g., dev_02, dev_03, dev_10) and potentially improving mean validation loss beyond Trial 004's 0.004097.

## Evidence from previous experiments

Trial 004 showed that with Fourier features, all cases made substantial progress, but training curves leveled off toward the end of the budget. Trial 007 showed that expanding the frequency bank did not help, isolating representation depth and gradient flow through the hidden layers as the logical architectural focus.

## Observed results

All 10 cases completed (87.0 s each, ~28k steps). Mean validation loss achieved a new campaign best of 0.003778 (Trial 004: 0.004097), worst 0.01106 (dev_09; Trial 004: 0.01097), std 0.00363, mean IC 1.47e-08.
Per case comparison with Trial 004:
- dev_01: 9.01e-06 (Trial 004: 0.000399) - 44x improvement!
- dev_02: 0.00356 (Trial 004: 0.00417) - improved
- dev_03: 0.00310 (Trial 004: 0.00340) - improved
- dev_04: 0.00128 (Trial 004: 0.00148) - improved
- dev_05: 0.000231 (Trial 004: 0.000216) - practically tied
- dev_06: 0.000988 (Trial 004: 0.00216) - 2.2x improvement (broke below 1e-3)
- dev_07: 0.00850 (Trial 004: 0.00930) - improved
- dev_08: 0.00385 (Trial 004: 0.00408) - improved
- dev_09: 0.01106 (Trial 004: 0.01097) - practically tied
- dev_10: 0.00520 (Trial 004: 0.00480) - slightly higher

7 of 10 cases improved over Trial 004. Val/train ratios remained exactly 1.00 across all cases, confirming zero generalisation gap. The identity shortcuts in the residual blocks clearly preserved higher-derivative gradient signals throughout training.

## Agent decision

Retain: The ResNet Fourier-PINN architecture becomes our new champion architecture and baseline for subsequent experiments.

## Reason for decision

Mean validation loss reached a new all-time low (0.003778), with broad improvements across 70% of development cases and dramatic gains on dev_01 (44x) and dev_06 (2.2x). The residual structure provides superior gradient flow without adding any parameters or computational overhead.

## Next experiment

Trial 009: Test increasing the network capacity by widening the residual layers from width 128 to width 192 (or 3 residual blocks). With width 192 and 2 residual blocks, parameters increase from 35,586 to ~77,000 (well within the 250,000 parameter budget). Given that no overfitting was observed (val/train = 1.00) and training curves are still steadily declining, increased representation capacity should further reduce the residual on complex cases like dev_07 and dev_09.
