# Trial 062

Research metadata (locked on preparation): parents=trial:57,trial:61; kind=refinement; mechanism_id=early_window_collocation_rebalance.

## Parent methods and evidence

Trial 057's 25/25/50 physics time allocation has eligible L_val 0.15052786, physics 0.09003139 and IC L2 0.24596031. Trial 061's 37.5/25/37.5 allocation cut early residual and weighted physics to 0.08840250, but raised late Poisson and IC L2, yielding L_val 0.15067655. Both are near leaders; an intermediate split may balance their effects.

## Novelty claim

Refinement of the early-window collocation rebalance mechanism: interpolate training allocation to 31.25% early, 25% middle, 43.75% late. This is a fixed time-strata campaign tuning test; no publication novelty is claimed.

## Hypothesis and proposed change

Hypothesis: an intermediate early/late allocation retains Trial 061's early gain while recovering Trial 057's late and IC performance, producing a lower eligible L_val. Starting from Trial 057, change only quota and availability checks to 5n/16 early, n/4 middle, 7n/16 late.

## Training objective and setup

Trial 057 ResPINN: width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. Afterward loss b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 split 320 early/256 middle/448 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, gradient clip 0.5.

## Expected outcome

Expect early physics below Trial 057's 0.19259569, late physics below Trial 061's 0.07746884, IC L2 <=0.25, and L_val <0.15052786. Examine late Poisson, mass drift, density spread, physical checks, steps and runtime. A worse eligible score or failed IC check rejects the interpolation as a leader.

## Observed results

L_val 0.15245468; weighted physics 0.09055549; IC relative L2 0.24879546 and MSE 0.06189918, eligible true. Early/middle/late physics totals 0.15017409/0.09057503/0.06669633; late Poisson 0.02527715. Physical checks passed, rho0 error 0, periodic error 3.58e-6. At t=0.8 mean density 0.97691643, mass drift -0.02308357, density std 0.63765293, p99 3.26074886. 664325 parameters, 23068 steps, 748.0697 training seconds.

## Decision and interpretation

The intermediate allocation gave early physics 0.15017409, below Trial 057's 0.19259569, and late physics 0.06669633, below Trial 061's 0.07746884. However, its weighted physics 0.09055549 and L_val 0.15245468 are both worse than Trial 057; IC L2 0.24879546 also has a narrower margin. The window-balance predictions held, but the score prediction failed. Reject as a leader and retain the result as a controlled allocation comparison.
