# Experiment 003: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

The plateaued cases in Trial 002 (dev_06, dev_08, dev_02, dev_10) converged to physics-inconsistent smooth solutions (e.g. dev_06 "escapes" to z≈4.3 although the IC implies a fall towards the plane) because full-domain training lets the late-time residual be minimised by a weak-force trajectory before the IC information has propagated forward. Enforcing temporal causality with a time-marching curriculum (train on an expanding prefix of the time domain) should prevent these minima and reduce both mean and worst-case validation loss.

## Proposed method change

Architecture unchanged (3×48 tanh MLP, input t/(3π)−1, soft IC). Training changes:
- The 500 sorted training points are used as an expanding prefix window train_t[:k]. k starts at 50 (t ≲ 1.9) and increases by 25 points whenever the windowed loss at a check step (every 25 steps) is below TOL = 2e-4.
- Wall-clock floor: k ≥ 50 + 450·min(1, f/0.6), where f is elapsed fraction of the 87 s budget, so the whole domain is used by f = 0.6 at the latest.
- Adam lr = 1e-3 constant while marching; after the full window is reached at f_full, lr decays exponentially from 1e-3 to 1e-5 over the remaining wall-clock time.
- 11 time-spaced snapshots + final snapshot (final reported loss is on all 500 points).

## Training objective used

At each step: L_k(θ) = R_k(θ) + 100 · I(θ), where
- R_k(θ) = (1/k) Σ_{i=1..k} [(dz/dt(t_i) − v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2+ρ(t_i)^2)^{3/2})^2], over the first k (time-sorted) training points, via `context.physics_components(model, train_t[:k], case)`;
- I(θ) = (z(0)−z0)^2 + (v(0)−v0)^2.
Coefficients constant (physics 1, IC 100). Scheduled element: the window size k (adaptive on TOL with a linear wall-clock floor reaching k=500 at f=0.6) and the LR (constant 1e-3, then exponential decay to 1e-5 after k=500). No case-specific weighting; the curriculum is the same rule for every case (its realised speed depends on each case's loss).

## Expected effect

Elimination (or strong reduction) of the escaping / wrong-branch solutions in dev_06 and dev_08, so the worst case should drop well below 0.12. Mean may improve; cases that already trained well might lose a little because less time is spent on the full domain.

## Evidence from previous experiments

Trial 002 (full-budget Adam): mean 0.0365, worst 0.122. dev_06 plateaued at ~0.10 from 10% of training onward, with an escaping z trajectory inconsistent with v0<0; dev_02/dev_10 also plateaued early. Cases with steadily decreasing loss (dev_09: 0.0037) show the architecture can represent some solutions well, so the failure appears to be optimisation-path related rather than pure capacity.

## Observed results

All 10 cases completed (87.0 s each, ~23k steps). Mean validation 0.0412 (Trial 002: 0.0365), worst 0.123 (dev_08; Trial 002: 0.122), std 0.043, mean IC 3.7e-7. Per case vs Trial 002: dev_01 0.0057 (0.0086), dev_02 0.0249 (0.025), dev_03 0.028 (0.027), dev_04 0.071 (0.021, much worse), dev_05 0.0051 (0.0064), dev_06 0.103 (0.103, unchanged), dev_07 0.0088 (0.0089), dev_08 0.123 (0.122), dev_09 0.0042 (0.0037), dev_10 0.039 (0.039). Final = best snapshot in all cases; no train/validation gap. Snapshot notes show the window followed exactly the wall-clock floor (55, 118, 186, … 500 at f=0.6) in every inspected case: the adaptive TOL=2e-4 criterion was never met. Even on the first ~2 time units (window 55) the reported loss was 0.38 for dev_06 after ~1900 steps. dev_06 and dev_08 converged to the same plateau values (0.102, 0.122) as without curriculum.

## Agent decision

Reject the time-marching curriculum (in this form) and revert to full-domain training for the next trial.

## Reason for decision

No improvement in mean or worst case; one case (dev_04) was clearly hurt, and the problem cases ended at the same plateau values. The fact that the small network could not reduce the loss on a short prefix window below ~0.1–0.4 within thousands of steps suggests the bottleneck is the representation/optimisation capability of the 3×48 tanh MLP on raw scaled time (it also maps the early window to a tiny input interval), rather than only causality. This is an interpretation; the curriculum may be worth revisiting once the base model fits short windows well.

## Next experiment

Trial 004: architecture change with the Trial 002 training schedule (full domain, Adam 1e-3→1e-5 over 87 s). Replace the input with Fourier time features [t/(3π)−1, sin(ω_k t), cos(ω_k t)], ω_k = k/2, k = 1..8, and widen the MLP to 3 hidden tanh layers of 128 units, to test whether representation capacity/spectral bias is limiting.
