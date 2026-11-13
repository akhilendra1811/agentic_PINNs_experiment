# Experiment 005: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

With the Fourier 3×128 architecture all training curves were still decreasing at 87 s, so the method is optimisation-limited. A quasi-Newton L-BFGS refinement after an Adam warm-up converges much faster near a minimum for smooth, full-batch PINN losses and should lower the residual, especially in the hardest cases (dev_09, dev_07).

## Proposed method change

Architecture unchanged from Trial 004 (Fourier features ω_k = k/2, k=1..8, plus t/(3π)−1; 3×128 tanh). Training:
- Phase 1 (first 60% of the 87 s budget): full-batch Adam, lr 1e-3 → 1e-4 exponential in wall-clock fraction.
- Phase 2 (remaining 40%): torch L-BFGS, lr 1.0, strong-Wolfe line search, history 50, 10 inner iterations per outer step, full batch, until time runs out.
- Safeguards based only on the training loss: the parameter state at the start of each L-BFGS outer step is saved with its training loss; if L-BFGS raises (e.g. non-finite predictions) or gives a non-finite loss, the best saved state is restored and training continues with Adam lr 1e-4. At the end, if the final training loss is worse than the best saved L-BFGS state, that state is restored.
- 11 time-spaced snapshots + final.

## Training objective used

L(θ) = R(θ) + 100 · I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) − v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2+ρ(t_i)^2)^{3/2})^2] over all 500 training points (`context.physics_components`);
- I(θ) = (z(0)−z0)^2 + (v(0)−v0)^2.
Coefficients constant (physics 1, IC 100) in both phases. Full batch; no curriculum, sampling or case-specific weighting. Scheduled: optimiser switch at f = 0.6 and Adam lr(f) = 1e-3·(0.1)^(f/0.6).

## Expected effect

Mean validation loss clearly below Trial 004's 0.0041 (I would guess 2–10× lower if L-BFGS works in float32 on MPS), with reduced worst case. Risks: float32 L-BFGS may stall on line-search precision, and L-BFGS could find sharper minima that generalise worse between training points (val/train ratio > 1).

## Evidence from previous experiments

Trial 004: mean 0.0041, worst 0.011 (dev_09), all curves still decreasing (final = best snapshot everywhere), val/train ≈1.00. Trial 002 → 004 showed the architecture/representation was the main limitation before; now the curves indicate optimisation speed.

## Observed results

All 10 cases completed (87.1 s per case). Mean validation loss 0.004511 (Trial 004: 0.004097), worst 0.01435 (dev_07; Trial 004 worst was 0.01097 dev_09), std 0.00428, mean IC 7.9e-09.
Per case comparison with Trial 004:
- dev_01: 0.000321 (was 0.000399) - improved
- dev_02: 0.00331 (was 0.00417) - improved
- dev_03: 0.00517 (was 0.00340) - worse (stalled during L-BFGS)
- dev_04: 0.00198 (was 0.00148) - worse (stalled during L-BFGS)
- dev_05: 0.000337 (was 0.000216) - worse (stalled during L-BFGS)
- dev_06: 0.00199 (was 0.00216) - improved
- dev_07: 0.01435 (was 0.00930) - worse (stalled during L-BFGS)
- dev_08: 0.00337 (was 0.00408) - improved
- dev_09: 0.00848 (was 0.01097) - improved
- dev_10: 0.00579 (was 0.00480) - worse (stalled during L-BFGS)

Examination of snapshot histories shows that for five cases (dev_03, dev_04, dev_05, dev_07, dev_10), L-BFGS stalled almost immediately upon entering Phase 2: loss values remained completely flat across snapshots 8 to 11. In single precision (float32) on MPS, L-BFGS line search frequently fails to find a step satisfying the strong-Wolfe curvature condition, terminating progress prematurely. Where it did not stall (dev_01, dev_02, dev_06, dev_08, dev_09), L-BFGS achieved meaningful reductions.

## Agent decision

Reject L-BFGS as the default second-phase optimiser. Retain pure Adam with learning rate scheduling as the more reliable optimisation strategy for float32.

## Reason for decision

L-BFGS produced a higher mean validation loss and worse maximum error due to premature line-search stagnation on 50% of the cases. While quasi-Newton methods are theoretically attractive for smooth PINN objectives, float32 precision limitations on MPS make standard strong-Wolfe L-BFGS fragile without extensive custom line-search tuning.

## Next experiment

Trial 006: Hard initial-condition enforcement. In Trial 004 and 005, soft IC loss was used with weight 100. While IC error was low (~1e-8), soft constraints still create gradient competition between the t=0 boundary and interior collocation points. We will implement an exact ansatz:
z(t) = z0 + (1 - exp(-t)) * N_z(t)
v(t) = v0 + (1 - exp(-t)) * N_v(t)
using the pure Adam schedule from Trial 004 to evaluate whether removing IC gradient conflict improves interior residual convergence.
