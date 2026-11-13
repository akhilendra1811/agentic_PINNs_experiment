# Trial 050

Research metadata (locked on preparation): parents=trial:48,trial:49; kind=refinement; mechanism_id=accelerated_poisson_curriculum.

## Parent methods and evidence

Parents Trials 048 and 049 use the same accelerated Poisson curriculum. Final IC weight 30 gave IC L2 0.25123018, L_val 0.14355815; final IC weight 32 gave IC L2 0.25001004, L_val 0.14756965, missing eligibility by only 0.00001004. The expected threshold crossing lies just above weight 32, subject to nonlinear optimizer effects.

## Novelty claim

Refinement of the accelerated Poisson curriculum mechanism: raise the final IC coefficient from 32 to 33. This is a scalar threshold test, not a new mechanism or publication novelty.

## Hypothesis and proposed change

Hypothesis: final IC weight 33 will cross IC L2 <=0.25 and retain L_val below Trial 030's best eligible 0.15077613. Starting from Trial 049, change only 1+31*blend to 1+32*blend.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From f=0.20 onward, loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, where b reaches 1 by f=0.40 and b_P by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25 and L_val <0.15077613 with late Poisson near Trial 049's 0.01313104. Check all temporal residuals, mass drift, density spread, physical checks, steps and runtime. If this still misses eligibility or physics cost exceeds the score margin, stop the scalar search and pursue another mechanism.

## Observed results

L_val 0.15160360; weighted physics 0.08964395; IC relative L2 0.24891695 and MSE 0.06195965, eligible true. Early/middle/late physics totals 0.19546326/0.08554811/0.04977373; late Poisson 0.01416380. Physical checks passed, rho0 error 0, periodic error 3.34e-6. At t=0.8 mean density 0.97714669, mass drift -0.02285331, density std 0.64987600, p99 3.31948709. 664325 parameters, 23712 steps, 748.0086 training seconds.

## Decision and interpretation

Final IC weight 33 crossed the threshold: IC L2 fell from Trial 049's 0.25001004 to 0.24891695. L_val rose from 0.14757 to 0.15160 and is slightly above Trial 030's 0.15078, so the strict score-improvement part of the hypothesis failed. The wider IC margin and lower late Poisson than Trial 030 make this a credible finalist alternative. Keep it for matched-time comparison, but Trial 030 remains the lowest eligible 750-second score.
