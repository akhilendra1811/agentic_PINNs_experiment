# Trial 053

Research metadata (locked on preparation): parents=trial:14,trial:30; kind=mechanism; mechanism_id=stratified_density_aware_collocation.

## Parent methods and evidence

Parents Trial 014 and Trial 030. Trial 014 occasionally selected high predicted density points under B training and obtained L_val 0.12882566, IC L2 0.28935596, without clear gain. Trial 030 is the best eligible model at L_val 0.15077613 and IC L2 0.24972807, using fixed 25/25/50 temporal stratification but random points within each window. Its t=0.8 density p99 is 3.25030398, and the broader research problem seeks better compressive structures.

## Novelty claim

Campaign integration mechanism: density-aware collocation separately within each time window. Trial 014 used global density-focused selection without temporal stratification; Trial 030 used temporal stratification without density focus. This combines both while keeping most points random. Adaptive collocation is known in PINN research, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: focusing one quarter of each window's physics points on the highest predicted densities will better train compressive regions, improving density spread or late residuals without losing IC eligibility. Starting from Trial 030, draw the same fresh candidate pool, evaluate predicted density without gradients, choose 25% top density and 75% random non-top points separately in early, middle and late windows. Keep batch counts and all other training settings fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late, each window 25% top-density and 75% random non-top candidates from fresh context sampling; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect t=0.8 density p99 above Trial 030's 3.25030398 or lower late physics, with IC L2 <=0.25 and ideally L_val <0.15077613. Inspect all temporal residuals, mass drift, density std, physical checks, steps and runtime to detect sampling cost or overfitting to dense regions. If quality worsens, reject the integration.

## Observed results

L_val 0.15169059; weighted physics 0.08820404; IC relative L2 0.25196537 and MSE 0.06348655, eligible false. Early/middle/late physics totals 0.20043973/0.07688392/0.05010184. Middle and late improved relative to Trial 030, but early worsened; late Poisson 0.01903510. Physical checks passed, rho0 error 0, periodic error 3.34e-6. At t=0.8 mean density 0.97600371, mass drift -0.02399629, density std 0.63547361, p99 3.26322150. 664325 parameters, 23499 steps, 748.0596 training seconds.

## Decision and interpretation

Density-aware selection produced only a small late p99 increase from Trial 030's 3.25030 to 3.26322, while IC L2 worsened from 0.24973 to 0.25197 and lost eligibility. Weighted physics was nearly unchanged, and L_val rose slightly. This does not support a meaningful compressive-structure or score gain at the tested 25% focus. Reject as a finalist; the window stratification alone remains stronger.
