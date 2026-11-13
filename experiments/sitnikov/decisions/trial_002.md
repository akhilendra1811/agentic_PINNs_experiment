# Experiment 002: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

Trial 001 was severely under-trained (loss still falling at step 1000, only ~4.7 s of 90 s used). Using the full time budget with Adam and a decaying learning rate will substantially lower the validation PINN loss for the same architecture and loss.

## Proposed method change

Only the training schedule changes. Architecture (3×48 tanh MLP, input t/(3π)−1) and loss unchanged. Adam runs for ~87 s of wall-clock time (stopping earlier if fewer than 1.5 s remain). Learning rate decays exponentially in wall-clock fraction f∈[0,1]: lr(f) = 1e-3 · (1e-2)^f, i.e. 1e-3 → 1e-5. 11 snapshots at evenly spaced wall-clock fractions plus one final snapshot (12 total).

## Training objective used

L(θ) = R(θ) + 100 · I(θ), with
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) − v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2+ρ(t_i)^2)^{3/2})^2] over all 500 training points (from `context.physics_components`);
- I(θ) = (z(0)−z0)^2 + (v(0)−v0)^2.
Coefficients constant: physics 1, IC 100. Full batch every step, no curriculum, no sampling, no case-specific weighting. Only the LR is scheduled (exponential in wall-clock time, 1e-3 → 1e-5).

## Expected effect

Large reduction in mean validation loss (probably by one order of magnitude or more), training time ≈ 87 s per case. Some cases may still be trapped in a low-frequency / wrong-branch solution, so the worst case may remain high.

## Evidence from previous experiments

Trial 001: mean 0.164, worst 0.366 (dev_08); all curves still monotonically decreasing at the last step; best snapshot = final in every case; train ≈ validation full loss (no overfitting); IC loss negligible (1.8e-5). Hence more optimisation is the most direct lever.

## Observed results

All 10 cases completed, 87.0 s training each (~27k Adam steps). Mean validation 0.0365 (vs 0.164 in Trial 001, 4.5× lower), worst 0.122 (dev_08, vs 0.366), std 0.042. Mean IC loss 3.2e-7, so residual dominates. Per case: dev_01 0.0086, dev_02 0.025, dev_03 0.027, dev_04 0.021, dev_05 0.0064, dev_06 0.103, dev_07 0.0089, dev_08 0.122, dev_09 0.0037, dev_10 0.039. Final snapshot was best in all cases; val/train ratio ≈1.00–1.01 (no overfitting). Curves: dev_01/04/05/09 still decreasing at the end; dev_02, dev_06, dev_10 plateaued after ~10–20% of training (e.g. dev_06 stuck at 0.10–0.11 from snapshot 2 onward). The dev_06 prediction plot shows z rising monotonically from 0.72 to ≈4.3 with a very steep initial transient although v0 = −0.11: the network found a smooth "escaping" function for which the residual is small far from the origin (weak force), and the IC is reached only via a sharp kink near t=0. This is a physics-inconsistent local minimum, not an under-training issue.

## Agent decision

Retain the full-budget time-based schedule as the new reference training length. Do not consider the plain MLP+Adam method adequate.

## Reason for decision

Using the budget gave a clear improvement on every single case (all 10 lower than Trial 001), so it is retained. However, the plateaued cases and the escaping-solution plot indicate the dominant remaining failure is that information from the initial condition does not propagate forward in time during optimisation (a known PINN causality failure). This is my interpretation of the evidence, to be tested by a curriculum that enforces temporal ordering.

## Next experiment

Trial 003: adaptive time-marching curriculum. Train on an expanding prefix window of the 500 training points (start with the first 50, extend by 25 points whenever the windowed loss falls below a tolerance, with a wall-clock floor so the full domain is reached by 60% of the budget), then train on all points with decaying LR. Architecture and loss formula unchanged otherwise.
