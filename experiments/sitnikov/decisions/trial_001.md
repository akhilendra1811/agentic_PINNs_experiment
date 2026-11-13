# Experiment 001: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

Baseline reference point. The unchanged baseline (3 hidden tanh layers of width 48, Adam lr=1e-3, 1000 full-batch steps) is expected to under-fit the oscillatory Sitnikov dynamics over 0..6π, because 1000 Adam steps is a small fraction of the 90 s budget and a plain tanh MLP on a single scaled time input is known to have spectral bias. This trial establishes the reference validation loss against which all later changes are compared.

## Proposed method change

None. candidate.py is unchanged from the provided baseline, as required for Trial 001.

## Training objective used

L(θ) = R(θ) + 100 · I(θ), where
- R(θ) = mean over all 500 training points t_i of [(dz/dt − v)^2 + (dv/dt + z/(z^2+ρ(t)^2)^{3/2})^2], computed by `context.physics_components` with autograd;
- I(θ) = (z(0) − z0)^2 + (v(0) − v0)^2 (soft initial-condition penalty).
Coefficients: physics weight 1 (constant), IC weight 100 (constant). Full batch of all 500 training points every step, no sampling, no curriculum, no case-specific weighting. Optimiser Adam lr=1e-3 constant, max 1000 steps (or until time is exceeded). Snapshots recorded at step 1 and every 100 steps.

## Expected effect

Moderate to high validation loss with clear under-fitting, short training time (well under 90 s), relatively large IC errors due to soft constraint, and probably a trivially-damped or low-frequency solution for cases with larger z0.

## Evidence from previous experiments

None, this is the first trial. Prior knowledge only: vanilla PINNs on long time horizons often converge to trivial/smooth solutions; hard IC constraints, Fourier/time features, longer training and L-BFGS usually help. These are hypotheses to test in later trials.

## Observed results

All 10 cases completed. Mean validation loss 0.1642, worst 0.3657 (dev_08), std 0.121. Per case: dev_01 0.145, dev_02 0.0395, dev_03 0.328, dev_04 0.187, dev_05 0.0846, dev_06 0.117, dev_07 0.0416, dev_08 0.366, dev_09 0.280, dev_10 0.0538. Mean IC loss 1.8e-5 (weighted ~1.8e-3), so the loss is almost entirely ODE residual (mean physics 0.162). Training used only ~4.7 s per case of the 90 s budget (1000 Adam steps, ~4 ms/step on MPS). Training curves are still decreasing monotonically at step 1000 (e.g. dev_01: 0.92 → 0.14 between step 100 and 1000), the best post-hoc snapshot is the final one in every case, and train and validation full losses are nearly identical (no generalisation gap between the 500 training and 2000 validation points). The dev_08 z-plot shows a single slow hump rising from z0 even though v0 < 0, i.e. the network has converged towards a smooth, low-frequency function that does not represent oscillatory dynamics. Prediction-only plots are used here only for qualitative consistency with the ICs/ODE; no reference trajectory was consulted.

## Agent decision

Retain as the reference baseline only (not a candidate method of interest). The trial closes successfully.

## Reason for decision

The evidence clearly shows under-training: curves still falling, 95% of the time budget unused, residual dominated, no overfitting. The low-frequency hump in dev_08 is consistent with the known spectral bias / trivial-solution tendency of plain PINNs, but that interpretation is a hypothesis; the direct evidence is only the still-decreasing loss.

## Next experiment

Trial 002: keep the architecture and loss unchanged, but use (almost) the full 90 s budget with Adam and an exponential wall-clock LR decay from 1e-3 to 1e-5, with 12 evenly time-spaced snapshots. This isolates the effect of training length/schedule before changing architecture or constraints.
