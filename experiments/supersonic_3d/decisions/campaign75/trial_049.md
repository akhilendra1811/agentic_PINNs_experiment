# Trial 049

Research metadata (locked on preparation): parents=trial:31,trial:48; kind=refinement; mechanism_id=accelerated_poisson_curriculum.

## Parent methods and evidence

Parents Trial 048 and Trial 031. Trial 048 accelerated the Poisson ramp and improved L_val to 0.14355815, weighted physics to 0.08044155 and late Poisson to 0.01210435, but IC L2 0.25123018 was ineligible. Trial 031 used final IC weight 32 in the standard ramp, producing eligible IC L2 0.24664535 at L_val 0.16011182. This trial tests the higher IC weight with Trial 048's faster Poisson schedule.

## Novelty claim

Refinement of the accelerated Poisson curriculum mechanism. Increase final IC coefficient from 30 to 32 while holding Poisson timing and every other method component fixed. Loss coefficient tuning is known, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: final IC weight 32 will recover IC L2 <=0.25 while retaining most of Trial 048's physics benefit, possibly yielding a lower eligible L_val than Trial 030's 0.15077613. Starting from Trial 048, change only IC coefficient 1+29*blend to 1+31*blend.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From f=0.20 onward, loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+31*b(f))*IC relative MSE, where b reaches 1 by f=0.40 and b_P by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25 and L_val <Trial 030's 0.15077613, with late Poisson below 0.01984955. Inspect all temporal windows, mass drift, density spread, physical checks, steps and runtime. If higher IC pressure erases the physics benefit, retain Trial 030.

## Observed results

L_val 0.14756965; weighted physics 0.08506462; IC relative L2 0.25001004 and MSE 0.06250502, eligible false by 0.00001004. Early/middle/late physics totals 0.18305833/0.08173003/0.04786790; late Poisson 0.01313104. Physical checks passed, rho0 error 0, periodic error 1.91e-6. At t=0.8 mean density 0.97805637, mass drift -0.02194363, density std 0.65590763, p99 3.35995269. 664325 parameters, 24075 steps, 748.0961 training seconds.

## Decision and interpretation

Increasing final IC weight from 30 to 32 improved IC L2 from Trial 048's 0.25123018 to 0.25001004, but missed the exact <=0.25 threshold by 1.0e-5. L_val 0.14757 remains below eligible Trial 030's 0.15078, yet this trial cannot be selected because it is ineligible. The near-threshold response motivates one intermediate stronger weight test; do not round this result to eligible.
