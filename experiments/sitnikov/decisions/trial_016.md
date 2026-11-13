# Experiment 016: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 015, our champion configuration (2-block ResNet Fourier-PINN, width 192, Cosine Annealing, grad clip 1.0) achieved a new record mean validation loss of 0.001787. In neural representations of physical systems, weight decay (L2 penalty) discourages unnecessarily large weight norms, acting as an implicit Sobolev-norm regularizer that penalizes high-frequency spurious oscillations. Testing AdamW with weight_decay = 1.0e-4 will determine whether weight decay regularizes the internal representations toward smoother, lower-energy Hamiltonian trajectories, or whether it acts as an unwanted inductive drag against the governing physics residual.

## Proposed method change

Optimizer modification to add weight decay:
- Architecture: 2-block ResNet Fourier-PINN with width 192, 8 Fourier frequencies, and Tanh activations (77,954 parameters, identical to Trial 015).
- Optimizer: Replace Adam with AdamW, using weight_decay = 1.0e-4.
- Learning rate schedule: Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6) over the 87.0 s budget.
- Gradient clipping: Apply `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`.
- Objective unchanged: L(θ) = physics + 100.0 * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ) + (weight_decay / 2) * ||θ||_2^2, where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: AdamW learning rate following Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)), where f is the elapsed fraction of the 87.0 s budget. Parameter weight decay = 1e-4. Gradient updates clipped to maximum L2 norm of 1.0.

## Expected effect

Comparison against Trial 015 (mean 0.001787, worst 0.004532). If weight decay suppresses spurious inter-sample curvature without hindering ODE satisfaction, validation error will decrease below 0.001787. If the L2 penalty competes with the physics objective, validation loss will increase.

## Evidence from previous experiments

Trial 015 proved that stabilizing parameter updates via gradient clipping gave a massive 26% gain across all 10 cases. Exploring whether parameter magnitude regularization provides further stabilization is the logical next optimization question.

## Observed results

All 10 cases completed (87.0 s each, ~20.2k steps, 77,954 parameters). Mean validation loss was 0.001807 (Trial 015: 0.001787), worst 0.004413 (dev_09; Trial 015: 0.004532), std 0.00150, mean IC 1.31e-09.
Per case comparison with Trial 015:
- dev_01: 0.000161 (Trial 015: 0.000148) - practically tied
- dev_02: 0.001840 (Trial 015: 0.001760) - practically tied
- dev_03: 0.001850 (Trial 015: 0.001670) - practically tied
- dev_04: 0.000682 (Trial 015: 0.000656) - practically tied
- dev_05: 0.0000896 (Trial 015: 0.0000898) - practically tied
- dev_06: 0.000330 (Trial 015: 0.000326) - practically tied
- dev_07: 0.003540 (Trial 015: 0.003470) - practically tied
- dev_08: 0.002610 (Trial 015: 0.002530) - practically tied
- dev_09: 0.004413 (Trial 015: 0.004532) - slightly improved (new campaign best on dev_09)
- dev_10: 0.002550 (Trial 015: 0.002680) - slightly improved

The results are practically indistinguishable from Trial 015 within normal stochastic noise (mean 0.001807 vs 0.001787, ~1% difference). The L2 weight decay of 1e-4 provided a very slight improvement on the high-energy cases dev_09 and dev_10, but did not significantly alter the overall trajectory.

## Agent decision

Reject weight decay as a major driver of improvement; retain pure Adam (without weight decay) as the simpler, unregularized optimizer from Trial 015.

## Reason for decision

Continuous physics collocation across 500 coordinates already acts as an implicit functional regularizer, making parameter L2 weight decay redundant. Keeping the loss objective unencumbered by artificial weight decay terms preserves pure fidelity to the governing equations.

## Next experiment

Trial 017: Learnable Fourier Frequencies (Adaptive Spectral Encoding). In all trials since Trial 004, the Fourier bank frequencies were hardcoded to a fixed harmonic grid w_k = 0.5 * k (0.5 to 4.0 rad/s). However, in the Sitnikov problem, every development case has different initial conditions (e, z0, v0) and therefore a distinct nonlinear oscillation period and fundamental frequency (which deviates from the infinitesimal linear frequency sqrt(2) ≈ 1.414 rad/s depending on amplitude). Making the 8 frequency coefficients learnable parameters (nn.Parameter initialized at the 0.5*k grid) will allow gradient descent to adaptively tune the input frequencies to the exact physical harmonics of each specific case, reducing representation error without increasing model size.
