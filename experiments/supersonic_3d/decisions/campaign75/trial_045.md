# Trial 045

Research metadata (locked on preparation): parents=trial:30; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parent Trial 030 is the best eligible candidate: L_val 0.15077613, IC L2 0.24972807, weighted physics 0.08841202. It uses 1024 physics and 1024 IC samples per physics step, with 23648 total steps in 748 seconds. Physics residual evaluation is relatively costly; more, smaller stochastic updates may improve convergence within the fixed wall time.

## Novelty claim

Refinement of Trial 030's optimizer throughput within the established time-stratified training mechanism. Halve only the physics batch, preserving the IC batch and temporal proportions. Batch-size tuning is standard, not a new mechanism or publication novelty.

## Hypothesis and proposed change

Hypothesis: 512-point physics batches will allow more optimizer steps and lower weighted physics or L_val without compromising IC eligibility. Starting from Trial 030, keep the IC batch at 1024, but use 512 physics points per step: 128 early, 128 middle and 256 late. No loss or architecture changes.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only, 1024 IC samples. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 512 split 128 early/128 middle/256 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect more than Trial 030's 23648 total steps, weighted physics below 0.08841202, IC L2 <=0.25 and L_val <0.15077613. Inspect gradient-noise effects by temporal residuals, mass drift, density spread, physical checks and runtime. If smaller batches destabilize training or miss eligibility, retain Trial 030.

## Observed results

L_val 0.16153656; weighted physics 0.09997192; IC relative L2 0.24812223 and MSE 0.06156464, eligible true. Early/middle/late physics totals 0.18983273/0.09546971/0.06672892; late Poisson 0.03069707. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97304517, mass drift -0.02695483, density std 0.59736347, p99 3.07670283. 664325 parameters, 26451 steps, 748.0047 training seconds.

## Decision and interpretation

Halving the physics batch increased completed steps from Trial 030's 23648 to 26451 and widened the IC margin (0.24812 versus 0.24973). Weighted physics worsened from 0.08841 to 0.09997 and L_val from 0.15078 to 0.16154, so more noisy updates did not improve the locked score. Retain as an eligible comparison, not a new leader.
