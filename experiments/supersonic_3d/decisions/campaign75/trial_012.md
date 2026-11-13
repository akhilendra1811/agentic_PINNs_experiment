# Trial 012

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=multiscale_time_features.

## Parent methods and evidence

Parent B alone. B weighted physics 0.04541517, L_val 0.12733444 and IC L2 0.28621542. Trials 001 and 010 modified spatial encodings without IC benefit. Trial 002 time curriculum worsened late physics. Trial 011 separate heads modestly improved B but remained ineligible. This trial changes temporal representation rather than sampling or heads.

## Novelty claim

Distinct campaign mechanism: multiscale temporal Fourier input features. No numbered trial used a richer differentiable time encoding. Wang, Wang and Perdikaris discuss spatio-temporal Fourier features for multiscale PINNs (https://arxiv.org/abs/2012.10047). This trial adapts that broad idea using four deterministic time frequencies and is not a reproduction of their architecture or a global novelty claim.

## Hypothesis and proposed change

Hypothesis: explicit smooth time frequencies improve representation of rapidly changing early and late Euler-Poisson dynamics without sacrificing the turbulent IC fit. Keep B spatial harmonics and raw t, append sin/cos of pi*k*t/tmax for k=1,2,4,8, scaled 1/sqrt(k), increasing input size 19 to 27. All other model and training settings stay B.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, alpha 0.5, density exp(t*raw_rho), three spatial harmonics plus eight temporal features, fresh weights. Parameter count <=750000. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE/IC batches 1024. Adam warmup 1e-4 to 1e-3 for 5% of 750 s then cosine to 1e-5; clip gradient 0.5. Locked validation.

## Expected outcome

Expect weighted physics below B 0.04541517 with early and late temporal totals improved, while IC L2 stays <=0.28621542; ideally reaches 0.25. Compare L_val to B 0.12733444. Check time-feature derivative cost via steps, and density spread, mass drift, positivity and periodicity. If high-frequency time derivatives worsen PDE residuals, reject.

## Observed results

L_val 0.12367696; weighted physics 0.04262899; IC relative L2 0.28468925 (ineligible). Early/middle/late totals 0.07680976/0.03176358/0.03547593. Early continuity/momentum/Poisson 0.02951577/0.03613337/0.01116062; middle 0.00918789/0.01680927/0.00576643; late 0.01073253/0.01548154/0.00926187. Physical checks passed, rho0 error 0, periodic max error 2.26e-6. At t=0.8 mean rho 0.98835409, mass drift -0.01164591, density std 0.68475378, p99 3.51354980. 666373 parameters, 6273 steps, 748.062 s. Recorded training loss 2.4511 at 187.5 s to 1.4288 at 748.1 s.

## Decision and interpretation

Partially supports temporal-feature hypothesis: versus B, weighted physics improved 0.04542 to 0.04263 and L_val 0.12733 to 0.12368; middle and late windows improved, but early total slightly worsened 0.07511 to 0.07681. IC L2 improved only marginally 0.28622 to 0.28469 and remains ineligible. Retain as a secondary physics-improving parent for combinations, with no claim of numerical-reference accuracy. The result does not prove whether individual time frequencies are all useful.
