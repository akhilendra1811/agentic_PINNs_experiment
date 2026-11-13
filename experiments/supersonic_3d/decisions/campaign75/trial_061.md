# Trial 061

Research metadata (locked on preparation): parents=trial:57; kind=mechanism; mechanism_id=early_window_collocation_rebalance.

## Parent methods and evidence

Parent Trial 057 is the best eligible candidate at L_val 0.15052786, physics 0.09003139, IC L2 0.24596031. Its early/middle/late physics totals are 0.19259569/0.08685857/0.05090936. The early window is much harder than late, while training uses 25% early, 25% middle, and 50% late physics points.

## Novelty claim

Campaign mechanism: rebalance the fixed physics batch toward the early temporal window where Trial 057 has its largest residual. Earlier Trial 037 tested a 25/37.5/37.5 split on Trial 030; this tests a distinct 37.5/25/37.5 allocation on the combined Trial 057 method. Time-stratified collocation is established practice; no publication novelty is claimed.

## Hypothesis and proposed change

Hypothesis: allocating 37.5% early, 25% middle and 37.5% late physics samples reduces early residual enough to lower eligible L_val without harming late Poisson excessively. Starting from Trial 057, change only the early and late sample counts and availability checks from 25/50% to 37.5/37.5%.

## Training objective and setup

Trial 057 ResPINN: width 256, ten 1.5-scaled sine residual blocks, three spatial Fourier harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. Afterward loss b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE; b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 384 early/256 middle/384 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect early physics total below 0.19259569, IC L2 <=0.25, and L_val <0.15052786. Examine all windows, late Poisson, mass drift, density contrast, physical checks, steps and runtime. Rejection if score worsens or eligibility is lost, even if early residual alone improves.

## Observed results

L_val 0.15067655; weighted physics 0.08840250; IC relative L2 0.24954768 and MSE 0.06227404, eligible true. Early/middle/late physics totals 0.11798767/0.08690182/0.07746884; late Poisson 0.02805561. Physical checks passed, rho0 error 0, periodic error 3.34e-6. At t=0.8 mean density 0.97896868, mass drift -0.02103132, density std 0.64855844, p99 3.31100631. 664325 parameters, 22776 steps, 748.0397 training seconds.

## Decision and interpretation

The 37.5/25/37.5 sampling split cut early physics total from Trial 057's 0.19259569 to 0.11798767, but late total rose from 0.05090936 to 0.07746884 and late Poisson from 0.01507682 to 0.02805561. Weighted physics improved to 0.08840250, yet IC L2 worsened to 0.24954768 and L_val is 0.15067655, slightly above Trial 057's 0.15052786. The early-residual prediction was supported; the overall-score prediction failed. Retain as a near-leader but with narrow IC margin, and test an intermediate allocation next.
