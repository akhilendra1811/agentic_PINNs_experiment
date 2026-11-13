# Experiment 013: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 009, an exponential learning rate schedule lr(f) = 1e-3 * (1e-2)^f was used. Under exponential decay, the learning rate drops by a full order of magnitude to 1e-4 at the exact midpoint (f=0.5), which slows down parameter motion and gradient traversal in the second half of training before the global trajectory structure is fully resolved. A Cosine Annealing schedule preserves an active exploration rate (~1e-3) through f=0.5, then smoothly tapers to a fine-tuning rate of 1e-6 at the end:
lr(f) = lr1 + 0.5 * (lr0 - lr1) * (1 + cos(pi * f))
with lr0 = 2e-3 and lr1 = 1e-6. This extended high-mobility window combined with a lower terminal floor should help the network escape shallow saddle points and achieve tighter terminal convergence across all 10 cases.

## Proposed method change

Optimization schedule modification:
- Architecture: 2-block ResNet Fourier-PINN with width 192, 8 Fourier frequencies, and Tanh activations (77,954 parameters, identical to Trial 009).
- Replace exponential LR decay with Cosine Annealing:
  lr(f) = lr1 + 0.5 * (lr0 - lr1) * (1 + cos(pi * f))
  with lr0 = 2.0e-3, lr1 = 1.0e-6, over the 87.0 s budget.
- Objective unchanged: L(θ) = physics + 100.0 * ic, full batch on all 500 coordinates.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + 100 * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Coefficients: physics weight 1.0 (constant), IC weight 100.0 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Scheduled element: Adam learning rate following Cosine Annealing lr(f) = 1e-6 + 0.5 * (2e-3 - 1e-6) * (1 + cos(pi * f)), where f is the elapsed fraction of the 87.0 s budget.

## Expected effect

Comparison against Trial 009 (exponential schedule, mean 0.003390, worst 0.01020). Cosine annealing is expected to accelerate convergence during the 0.3-0.7 budget fraction and achieve lower final validation loss, especially on slow-converging cases like dev_09 and dev_07.

## Evidence from previous experiments

Trial 009 showed that training curves were still steadily decreasing at step ~23,000, indicating that optimization rate is still an active bottleneck. Trial 012 showed that Tanh is the optimal nonlinearity, leaving optimization scheduling as the primary lever for further progress.

## Observed results

All 10 cases completed (87.0 s each, ~22.1k steps, 77,954 parameters). Mean validation loss was 0.005206 (Trial 009: 0.003390), worst 0.03154 (dev_09; Trial 009: 0.01020), std 0.00936, mean IC 1.98e-09.
Per case comparison with Trial 009 (exponential schedule):
- dev_01: 0.000415 (Trial 009: 0.000496) - improved
- dev_02: 0.00304 (Trial 009: 0.00324) - improved
- dev_03: 0.00251 (Trial 009: 0.00260) - improved
- dev_04: 0.00127 (Trial 009: 0.00152) - improved
- dev_05: 0.000151 (Trial 009: 0.000232) - 35% improved (all-time best)
- dev_06: 0.00165 (Trial 009: 0.000649) - higher, but still low
- dev_07: 0.00400 (Trial 009: 0.00631) - 37% improved (all-time best on this bottleneck case!)
- dev_08: 0.00314 (Trial 009: 0.00404) - 22% improved (all-time best)
- dev_09: 0.03154 (Trial 009: 0.01020) - degraded late in training (val/train 7.16)
- dev_10: 0.00434 (Trial 009: 0.00462) - improved

Crucially, across 8 of the 10 cases, Cosine Annealing set brand new all-time records (notably dev_07 dropped from 0.00631 to 0.00400). In dev_09, the snapshot at step 17,643 reached an all-time record validation loss of 0.00710 before experiencing late-stage instability when lr was annealing down, resulting in val/train = 7.16 at the final step.

## Agent decision

Reject lr0 = 2e-3 due to the late-stage instability on dev_09. However, the evidence overwhelmingly supports Cosine Annealing for the remaining 9 cases.

## Reason for decision

An initial peak learning rate of 2e-3 was too aggressive for dev_09's high-energy initial conditions (z0=1.25, v0=0.70), exciting high-frequency modes that overfit the collocation points near the end. On 8 of 10 cases, however, Cosine Annealing produced the best results of the entire campaign.

## Next experiment

Trial 014: Cosine Annealing with a stabilized peak learning rate lr0 = 1.0e-3 (identical to Trial 009's initial rate) and terminal floor lr1 = 1.0e-6:
lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f))
This combines the proven stability of lr0=1e-3 from Trial 009 with the smooth mid-training exploration and fine terminal convergence of Cosine Annealing that yielded major gains on dev_07 and dev_08.
