# Trial 027

Research metadata (locked on preparation): parents=trial:25,trial:26; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parents Trials 025 and 026 share the same architecture and smooth IC-to-physics ramp. Trial 025's uniform sampling gave L_val 0.19754017, IC L2 0.24920297, early physics 0.17388229 and late Poisson 0.10972013. Trial 026's late-biased sampling improved late Poisson to 0.03588615 and IC L2 to 0.24084945 but worsened early physics to 0.44715198, raising L_val to 0.21293513.

## Novelty claim

Refinement of Trial 026's time-stratified collocation mechanism. Explicitly allocate physics points across the three locked validation windows rather than drawing half late and half uniformly. Stratification is a known sampling method; this is a campaign-specific allocation test.

## Hypothesis and proposed change

Hypothesis: 25% early, 25% middle and 50% late collocation will retain much of Trial 026's late Poisson improvement while reducing its early residual enough to beat Trial 025's L_val. Change only the selection of fresh physics points; keep model, loss, IC sampling and optimiser fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+2.5 Poisson)+(1+27*blend)*IC relative MSE, then full blend. Each 1024-point physics batch has 256 early t<=0.2, 256 middle 0.2<t<=0.5 and 512 late t>0.5, selected from fresh candidates. IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect early physics below Trial 026's 0.44715198 and late Poisson below Trial 025's 0.10972013, with IC L2 <=0.25 and L_val <0.19754017. Inspect all residual windows, mass drift, density spread and physical checks. If the balanced allocation still underperforms uniform sampling overall, reject it.

## Observed results

L_val 0.17473586; weighted physics 0.11269733; IC relative L2 0.24907537 and MSE 0.06203854, eligible true. Early/middle/late physics totals 0.18585699/0.09348071/0.09496343. Late Poisson 0.06188309. Physical checks passed, rho0 error 0, periodic error 4.05e-6. At t=0.8 mean density 0.97045749, mass drift -0.02954251, density std 0.59931302, p99 3.07966518. 664325 parameters, 24072 steps, 748.0734 training seconds.

## Decision and interpretation

The balanced allocation reduced L_val below both parents: 0.17474 versus 0.19754 (Trial 025) and 0.21294 (Trial 026). It kept IC eligibility at 0.24908 and lowered late Poisson from Trial 025's 0.10972 to 0.06188, while early physics 0.18586 was close to Trial 025's 0.17388 rather than Trial 026's 0.44715. This supports the sampling hypothesis and makes Trial 027 the best eligible candidate so far. The IC margin is narrow, so matched-time finalist training remains necessary.
