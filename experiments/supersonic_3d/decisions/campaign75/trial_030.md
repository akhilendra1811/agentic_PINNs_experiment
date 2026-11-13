# Trial 030

Research metadata (locked on preparation): parents=trial:28,trial:29; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parents Trial 028 and Trial 029 share balanced 25/25/50 time-stratified collocation. Trial 028 used final IC weight 30 and Poisson weight 2.5, yielding eligible IC L2 0.24756718 but L_val 0.18099374. Trial 029 used final IC weight 28 and Poisson weight 5, yielding much lower L_val 0.14587287 and late Poisson 0.01812841, but ineligible IC L2 0.25263432. This trial integrates their respective strengths.

## Novelty claim

Refinement of the established time-stratified staged-training mechanism: combine the higher Poisson coefficient from Trial 029 with the stronger IC term from Trial 028. The integration is new within the campaign but uses known loss weighting, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: with Poisson weight 5 held fixed, raising the final IC coefficient from 28 to 30 will recover IC eligibility while preserving most of Trial 029's late Poisson and L_val gains. Starting from Trial 029 source, change only 1+27*blend to 1+29*blend.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Each physics batch has 256 early, 256 middle and 512 late points from fresh domain candidates; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25, late Poisson below Trial 027's 0.06188309, and L_val below Trial 027's 0.17473586. Inspect all residual windows, density diagnostics, mass drift and physical checks. If the added IC pressure erases the physics gain or still misses eligibility, reject the integration.

## Observed results

L_val 0.15077613; weighted physics 0.08841202; IC relative L2 0.24972807 and MSE 0.06236411, eligible true. Early/middle/late physics totals 0.18229144/0.08273595/0.05426590; late Poisson 0.01984955. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97567320, mass drift -0.02432680, density std 0.63375694, p99 3.25030398. 664325 parameters, 23648 steps, 748.0161 training seconds.

## Decision and interpretation

The stronger IC term recovered eligibility relative to Trial 029 (IC L2 0.25263 to 0.24973) while retaining most of its physics gain: weighted physics 0.08205 to 0.08841 and late Poisson 0.01813 to 0.01985. L_val 0.15078 is the best eligible score so far, improving on Trial 027's 0.17474. The IC threshold margin is only 0.000272, so matched-time finalist training must test robustness. Retain as a high-priority finalist candidate; do not claim a winner yet.
