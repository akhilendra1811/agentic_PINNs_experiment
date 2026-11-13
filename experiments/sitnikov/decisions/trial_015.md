# Experiment 015: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 014, although the final validation loss set a major new campaign record of 0.002423, inspection of intermediate progress curves shows transient loss spikes in early and middle training (e.g. dev_07 spiked to 0.16 at snapshot 2, dev_09 spiked to 0.15 at snapshot 3). The Sitnikov restoring force z / (z^2 + rho^2)^{3/2} possesses steep nonlinear gradients when z passes through zero while primary masses are close (low barycentric radius rho). These geometric configurations generate occasional large gradient bursts that momentarily knock the optimizer out of smooth trajectories. Applying global gradient norm clipping (max_norm = 1.0) will dampen these transient shocks, yielding smoother optimization paths and potentially improving terminal convergence.

## Proposed method change

Optimization modification to add gradient norm clipping:
- Architecture: 2-block ResNet Fourier-PINN with width 192, 8 Fourier frequencies, and Tanh activations (77,954 parameters, identical to Trial 014).
- Optimization: Adam with Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6) over the 87.0 s budget.
- Gradient clipping: Apply `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)` before `optim.step()`.
- Objective unchanged: L(θ) = physics + 100.0 * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate following Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)), where f is the elapsed fraction of the 87.0 s budget. Gradient updates clipped to maximum L2 norm of 1.0.

## Expected effect

Comparison against Trial 014 (mean 0.002423, worst 0.005531). Gradient clipping should eliminate the early intermediate loss spikes seen in dev_07 and dev_09, leading to smoother monotonic descent and potentially lower final validation loss.

## Evidence from previous experiments

Trial 014 history curves displayed noticeable transient jumps in early snapshots before recovering. Because the ODE force has a strong singularity-like concentration near z=0 and rho=min, gradient clipping is standard practice to stabilize training dynamics in nonlinear celestial mechanics PINNs.

## Observed results

All 10 cases completed (87.0 s each, ~21k steps, 77,954 parameters). Mean validation loss achieved a major milestone, breaking the 0.002 barrier down to 0.001787 (Trial 014: 0.002423, a 26.2% reduction!). The worst-case error also broke below 0.005 to 0.004532 (dev_09; Trial 014: 0.005531, an 18% reduction!). Std dropped to 0.00152, mean IC 1.28e-09.
Per case comparison with Trial 014 (a clean 10/10 improvement across every single development case):
- dev_01: 0.000148 (Trial 014: 0.000299) - 50% improvement (halved the error!)
- dev_02: 0.001760 (Trial 014: 0.002510) - 30% improvement
- dev_03: 0.001670 (Trial 014: 0.002120) - 21% improvement
- dev_04: 0.000656 (Trial 014: 0.001050) - 37% improvement
- dev_05: 0.0000898 (Trial 014: 0.000151) - 40% improvement (broke below 1e-4!)
- dev_06: 0.000326 (Trial 014: 0.000515) - 37% improvement
- dev_07: 0.003470 (Trial 014: 0.004000) - 13% improvement
- dev_08: 0.002530 (Trial 014: 0.002960) - 15% improvement
- dev_09: 0.004532 (Trial 014: 0.005531) - 18% improvement (new campaign best worst case)
- dev_10: 0.002680 (Trial 014: 0.005090) - 47% improvement (almost halved the error!)

Every single case improved. Generalization remains near-perfect (val/train ~ 1.00–1.02). Examination of progress curves confirms that clipping the gradient norm to 1.0 completely suppressed intermediate gradient shocks, yielding smooth, steady monotonic convergence curves across all 10 cases.

## Agent decision

Retain: Gradient norm clipping (max_norm = 1.0) is decisively retained as a permanent component of our champion method.

## Reason for decision

A universal 10/10 improvement across all development cases, reducing mean validation loss by 26% (to 0.001787) and worst-case loss to 0.004532. Damping large gradient bursts near the potential singularity is demonstrably essential for stable PINN convergence in the Sitnikov problem.

## Next experiment

Trial 016: Weight decay / L2 regularization investigation. With width 192 and 77,954 parameters, the network has substantial capacity. While val/train is ~1.00, small parameter weight decay (e.g. AdamW with weight_decay = 1e-4) can penalize excessive curvature and unnecessary high-frequency weight oscillations, encouraging smoother solutions and potentially improving generalization on the continuous ODE trajectory. We will test AdamW with weight_decay = 1e-4 on our champion Trial 015 method.
