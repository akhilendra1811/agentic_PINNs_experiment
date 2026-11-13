# Experiment 004: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

The 3×48 tanh MLP on a single scaled time input cannot represent/optimise the multi-oscillation Sitnikov trajectories well over 0..6π (Trial 003 could not even fit short prefix windows below ~0.1). Adding a fixed bank of Fourier time features and widening the network will reduce the residual and break the plateaus seen in dev_06/dev_08/dev_02/dev_10.

## Proposed method change

Architecture only (training schedule reverts to Trial 002's):
- Input features γ(t) = [t/(3π)−1, sin(ω_k t), cos(ω_k t)] with ω_k = k/2, k=1..8 (frequencies 0.5–4 rad per time unit, covering the forcing frequency 1 and the expected vertical oscillation frequencies ~1–3). 17 input features.
- MLP: 3 hidden tanh layers of width 128 (35,586 parameters, < 250k).
- Soft IC, full-domain Adam, lr 1e-3 → 1e-5 exponential in wall-clock fraction over 87 s; 11 time-spaced snapshots + final.

## Training objective used

L(θ) = R(θ) + 100 · I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) − v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2+ρ(t_i)^2)^{3/2})^2] over all 500 training points (`context.physics_components`);
- I(θ) = (z(0)−z0)^2 + (v(0)−v0)^2.
Coefficients constant (physics 1, IC 100). Full batch every step; no curriculum, sampling or case-specific weighting. Only the LR is scheduled: lr(f) = 1e-3·(1e-2)^f, f = elapsed/87 s.

## Expected effect

Lower mean validation loss than Trial 002 (0.0365), particularly reductions for the plateaued cases. Risk: periodic features could encourage spurious periodic structure or high-frequency residual fitting between training points (would show as validation/train ratio > 1).

## Evidence from previous experiments

Trial 002: mean 0.0365, worst 0.122; dev_06, dev_02, dev_10 plateau early. Trial 003: time-marching did not help, and the window loss stayed high (~0.1–0.4) even on short windows, suggesting limited representation/optimisation ability of the base network. Both trials showed no train/val gap, so more capacity is not expected to overfit at this level.

## Observed results

All 10 cases completed (87.0 s, ~29k steps each, 35,586 params). Mean validation 0.00410 (Trial 002: 0.0365, ≈9× lower), worst 0.0110 (dev_09; Trial 002 worst 0.122), std 0.0036, mean IC 1.7e-8 (weighted ≈1.7e-6, negligible). Per case (Trial 002 in brackets): dev_01 0.00040 (0.0086), dev_02 0.0042 (0.025), dev_03 0.0034 (0.027), dev_04 0.0015 (0.021), dev_05 0.00022 (0.0064), dev_06 0.0022 (0.103), dev_07 0.0093 (0.0089, ≈unchanged), dev_08 0.0041 (0.122), dev_09 0.0110 (0.0037, worse), dev_10 0.0048 (0.039). 8 of 10 cases improved, by up to 50×. Final snapshot is best in every case; val/train ratio 1.00–1.01, so Fourier features did not cause between-point overfitting. All curves still decreasing at the end (e.g. dev_09 0.012 → 0.011 over the last two snapshots). The dev_06 prediction plot now shows sustained oscillation about z=0 consistent with the IC (z0 = 0.72, v0 < 0), replacing Trial 002's escaping solution. dev_09 (large z0=1.25, v0=0.70) and dev_07 (z0=1.50) remain the hardest; dev_09's prediction shows a large initial excursion followed by much smaller oscillations, which I cannot verify without reference data — I only note it has the largest residual.

## Agent decision

Retain: Fourier-feature input + 3×128 tanh MLP becomes the new working architecture.

## Reason for decision

Very large, broad improvement in mean and worst-case validation loss, the dev_06/dev_08 plateaus vanished, no generalisation gap. Trade-off: dev_09 got worse (0.0037 → 0.011), and dev_07 did not improve; these high-amplitude cases are the new bottleneck. Since all curves are still decreasing, optimisation efficiency is the next lever.

## Next experiment

Trial 005: same architecture; Adam for the first 60% of the budget (lr 1e-3 → 1e-4 exponential), then L-BFGS (strong-Wolfe line search) full-batch refinement for the remaining time. Keep a copy of the lowest-training-loss state as a safeguard against L-BFGS divergence.
