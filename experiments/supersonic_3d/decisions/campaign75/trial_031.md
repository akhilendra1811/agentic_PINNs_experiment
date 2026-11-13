# Trial 031

Research metadata (locked on preparation): parents=trial:30; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parent Trial 030 is the current best eligible candidate: L_val 0.15077613, weighted physics 0.08841202, late Poisson 0.01984955 and IC L2 0.24972807. The IC margin to the 0.25 threshold is only 0.00027193. Trial 018 showed weight 32 can produce IC L2 0.24650130 under a different sampling and Poisson setup.

## Novelty claim

Refinement of Trial 030's staged training and time-stratified collocation method. Increase only the final IC loss weight from 30 to 32. Loss-coefficient tuning is known and is not a new research mechanism.

## Hypothesis and proposed change

Hypothesis: final IC weight 32 will widen the eligibility margin without raising L_val above the prior best eligible Trial 027's 0.17473586. Starting from Trial 030 source, change only 1+29*blend to 1+31*blend.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+31*blend)*IC relative MSE, then full blend. Each 1024-point physics batch has 256 early, 256 middle and 512 late samples; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below 0.24972807 and L_val below 0.17473586. Compare physics components in all windows, late Poisson, mass drift, density spread, physical checks, runtime and steps. If the margin does not widen or physics cost outweighs it, retain Trial 030.

## Observed results

L_val 0.16011182; weighted physics 0.09927789; IC relative L2 0.24664535 and MSE 0.06083393, eligible true. Early/middle/late physics totals 0.19638240/0.09615792/0.06230808; late Poisson 0.02436442. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97285688, mass drift -0.02714312, density std 0.61033839, p99 3.13224411. 664325 parameters, 23966 steps, 748.0506 training seconds.

## Decision and interpretation

IC L2 improved from Trial 030's 0.24972807 to 0.24664535, widening the eligibility margin. L_val rose from 0.15077613 to 0.16011182 as weighted physics rose from 0.08841202 to 0.09927789, but stayed below the prior Trial 027 score 0.17473586. The hypothesis is supported in its stated robustness-score tradeoff. Retain Trial 031 as a potentially more robust finalist alternative; Trial 030 remains the current lowest eligible L_val.
