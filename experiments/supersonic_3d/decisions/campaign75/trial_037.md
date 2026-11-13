# Trial 037

Research metadata (locked on preparation): parents=trial:30; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parent Trial 030 is the best eligible candidate so far: L_val 0.15077613, weighted physics 0.08841202, IC L2 0.24972807. Its 25/25/50 early/middle/late physics allocation produced window totals 0.18229144/0.08273595/0.05426590. The middle window is 30% of validation physics and remains larger than late despite receiving half as many training points as late.

## Novelty claim

Refinement of time-stratified collocation. Reallocate one eighth of the physics batch from late to middle. Stratified sampling is known; this is a campaign-specific allocation test, not a new mechanism or publication claim.

## Hypothesis and proposed change

Hypothesis: a 25/37.5/37.5 allocation will reduce the middle residual enough to lower L_val while Poisson weight 5 keeps the late residual small. Starting from Trial 030, change only the selected physics sample counts from 256/256/512 to 256/384/384 per 1024-point batch.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/384 middle/384 late from fresh candidates; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect middle physics below Trial 030's 0.08273595, late physics near 0.05426590, IC L2 <=0.25 and L_val <0.15077613. Check early residuals, late Poisson, mass drift, density spread, physical checks, runtime and steps. If reduced late coverage loses the late gain, retain Trial 030.

## Observed results

L_val 0.15260755; weighted physics 0.08996397; IC relative L2 0.25028700 and MSE 0.06264358, eligible false. Early/middle/late physics totals 0.17498101/0.06439662/0.07129756. Middle improved from Trial 030's 0.08273595, but late worsened from 0.05426590; late Poisson 0.02811887. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97781932, mass drift -0.02218068, density std 0.64036590, p99 3.29835105. 664325 parameters, 23620 steps, 748.0856 training seconds.

## Decision and interpretation

The redistribution improved the intended middle window, but the late physics cost and IC L2 increase outweighed it. L_val 0.15261 is slightly worse than Trial 030's 0.15078, and IC L2 0.250287 exceeds the threshold. The hypothesis of a better eligible total score is rejected. Trial 030's 25/25/50 allocation remains the stronger option.
