# Trial 038

Research metadata (locked on preparation): parents=trial:2,trial:30; kind=mechanism; mechanism_id=moving_time_strata_curriculum.

## Parent methods and evidence

Parents Trial 002 and Trial 030. Trial 002 tested a causal time curriculum on B, yielding L_val 0.15086197 but IC L2 0.29229149, ineligible. Trial 030 is the best eligible model at L_val 0.15077613 and IC L2 0.24972807 using fixed 25/25/50 early/middle/late collocation. Its early physics total 0.18229144 remains larger than its late total 0.05426590. This trial uses a moving sampling distribution rather than Trial 002's loss-time curriculum.

## Novelty claim

Campaign mechanism: staged time-stratified collocation, shifting from early-biased to late-biased physics batches during training. Earlier Trial 002 used causal loss weighting and Trial 030 used fixed stratification; this sampling curriculum has not been tested. Time curricula are known in PINN research, so this is only campaign novelty.

## Hypothesis and proposed change

Hypothesis: 37.5/25/37.5 early/middle/late batches during f=0.2–0.6 improve early physics, while switching to 25/25/50 for f>=0.6 recovers late Poisson accuracy. Starting from Trial 030, change only the per-window physics sample counts as a function of cumulative training fraction.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. During f<0.6 the 1024-point physics batch is 384 early/256 middle/384 late; afterward it is 256/256/512. IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect early physics below Trial 030's 0.18229144, late Poisson near 0.01984955, IC L2 <=0.25 and L_val <0.15077613. Check all validation windows, mass drift, density spread, physical validity, runtime and steps. If the late switch cannot recover late accuracy or IC eligibility, reject the curriculum.

## Observed results

L_val 0.16753170; weighted physics 0.10531319; IC relative L2 0.24943638 and MSE 0.06221851, eligible true. Early/middle/late physics totals 0.17911878/0.10389160/0.07664391. Early improved only slightly from Trial 030's 0.18229144; late Poisson worsened to 0.03692668 from 0.01984955. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97133976, mass drift -0.02866024, density std 0.57259369, p99 2.95909524. 664325 parameters, 23386 steps, 748.0798 training seconds.

## Decision and interpretation

The early-biased first stage reduced early physics only slightly but worsened middle and late windows; switching late did not recover Trial 030's low late Poisson. IC remained barely eligible. L_val rose from 0.15078 to 0.16753, so the curriculum hypothesis is rejected for this schedule. Trial 030 remains the stronger finalist candidate.
