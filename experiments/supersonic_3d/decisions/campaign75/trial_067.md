# Trial 067

Research metadata (locked on preparation): parents=trial:66; kind=refinement; mechanism_id=stronger_poisson_coupled_curriculum.

## Parent methods and evidence

Trial 066 raised Poisson coefficient from 5 to 6 in Trial 057's high-sine, accelerated-Poisson method and became the best eligible candidate: L_val 0.14634504, weighted physics 0.08557238, IC L2 0.24652110, late Poisson 0.01017608. The continued slope beyond coefficient 6 is unknown.

## Novelty claim

Refinement of the stronger-Poisson coupled curriculum: raise the final Poisson coefficient to 7. This scalar tuning is campaign-specific; equation weighting is established PINN practice and no publication novelty is claimed.

## Hypothesis and proposed change

Hypothesis: coefficient 7 lowers late Poisson and weighted physics further without losing IC eligibility. Starting from Trial 066, change only the multiplier of p['poisson'] from 6.0 to 7.0; ramp and other terms stay fixed.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+7*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE; b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clip norm 0.5.

## Expected outcome

Expect late Poisson <0.01017608, IC L2 <=0.25 and L_val <0.14634504. Inspect all window residuals, mass drift, density spread, physical checks, steps and runtime. A worse eligible score rejects the higher coefficient, even if Poisson alone improves.

## Observed results

L_val 0.14728625; weighted physics 0.08643481; IC relative L2 0.24668084 and MSE 0.06085144, eligible true. Early/middle/late physics totals 0.18879099/0.08637937/0.04552561; late Poisson 0.01049678. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97831023, mass drift -0.02168977, density std 0.64529490, p99 3.30152082. 664325 parameters, 21830 steps, 748.0067 training seconds.

## Decision and interpretation

Poisson coefficient 7 did not improve Trial 066's late Poisson: 0.01049678 versus 0.01017608. Weighted physics rose from 0.08557238 to 0.08643481 and IC L2 slightly worsened. The eligible L_val 0.14728625 is above Trial 066's 0.14634504. Reject the higher coefficient as a leader; Trial 066 remains best. The difference is small relative to potential optimization variability and is not a claim of global optimum.
