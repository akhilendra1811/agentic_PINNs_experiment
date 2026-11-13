# Trial 052

Research metadata (locked on preparation): parents=trial:49; kind=refinement; mechanism_id=accelerated_poisson_curriculum.

## Parent methods and evidence

Parent Trial 049 has the accelerated Poisson ramp, final IC weight 32, L_val 0.14756965 and IC L2 0.25001004. It misses eligibility by only 0.00001004. Trial 050 raised IC weight to 33 and crossed the threshold but L_val rose to 0.15160360. A small extra IC-only period might cross without as much physics cost.

## Novelty claim

Refinement of the accelerated-Poisson staged-training method: extend IC-only pretraining from 20% to 22% and shift both later ramps by the same two percentage points. Stage-duration tuning is known and not a new mechanism or publication claim.

## Hypothesis and proposed change

Hypothesis: two more percent of IC-only fitting will move Trial 049's IC L2 below 0.25 while retaining its L_val advantage over Trial 030. Starting from Trial 049, change the IC-only cutoff from f=0.20 to 0.22, the continuity/momentum/IC blend origin to 0.22 with width 0.20, and Poisson ramp origin to 0.22 with width 0.05. Final weights and all other settings stay fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 22% IC relative MSE only. From f=0.22 onward, loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+31*b(f))*IC relative MSE, where b reaches 1 by f=0.42 and b_P by f=0.27. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25 and L_val below Trial 030's 0.15077613. Check whether shorter full-physics duration worsens all temporal residuals, particularly late Poisson, plus mass drift, density spread, physical checks, steps and runtime. If it still misses eligibility or loses the score gain, stop this stage-duration refinement.

## Observed results

L_val 0.15057274; weighted physics 0.08805106; IC relative L2 0.25004336 and MSE 0.06252168, eligible false by 0.00004336. Early/middle/late physics totals 0.18926683/0.08280735/0.05071098; late Poisson 0.01478949. Physical checks passed, rho0 error 0, periodic error 2.26e-6. At t=0.8 mean density 0.97726339, mass drift -0.02273661, density std 0.64816135, p99 3.34874582. 664325 parameters, 25660 steps, 748.0842 training seconds.

## Decision and interpretation

The extra IC-only period did not improve IC fit relative to Trial 049 (0.25004336 versus 0.25001004); both are ineligible. Weighted physics worsened from 0.08506 to 0.08805 and L_val from 0.14757 to 0.15057. The stage-duration hypothesis is rejected, and this narrow threshold search should stop. Trial 050 remains the eligible accelerated-Poisson alternative.
