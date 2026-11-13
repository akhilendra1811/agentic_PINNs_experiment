# Trial 044

Research metadata (locked on preparation): parents=trial:11,trial:30; kind=mechanism; mechanism_id=field_heads_stratified_ic.

## Parent methods and evidence

Parents Trial 011 and Trial 030. Trial 011 used separate field heads on B, producing L_val 0.12489542 and IC L2 0.28417242, a modest B score improvement but still ineligible. Trial 030 uses a shared five-output linear head with the best eligible training result, L_val 0.15077613, IC L2 0.24972807, weighted physics 0.08841202. This trial combines Trial 011's architecture with Trial 030's curriculum and sampling.

## Novelty claim

Campaign integration mechanism: field-specific nonlinear readout heads under the eligible staged IC and balanced collocation training method. Separate heads were tested in Trial 011 only with B training. Multi-head networks are known; this is a campaign combination, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: separating density, velocity and potential outputs reduces competition among their gradients and improves Trial 030's physics score without losing IC eligibility. Replace the shared linear five-channel head by three 64-wide SiLU heads matching Trial 011; keep all upstream blocks and training unchanged.

## Training objective and setup

ResPINN width 256, ten sine residual blocks, three spatial harmonics, separate 64-wide SiLU heads for rho, three velocity components and phi, 712709 parameters. Positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect L_val below Trial 030's 0.15077613 and IC L2 <=0.25, with at least one PDE component improved without offsetting degradation. Check all temporal windows, mass drift, density contrast, physical checks, runtime and steps. If extra heads consume budget without score gain or lose IC eligibility, reject the integration.

## Observed results

L_val 0.16052826; weighted physics 0.09793281; IC relative L2 0.25019082 and MSE 0.06259545, eligible false. Early/middle/late physics totals 0.18059053/0.09760209/0.06506817. Early Poisson 0.01377505 improved from Trial 030's 0.01668559, but late Poisson rose to 0.02983340. Physical checks passed, rho0 error 0, periodic error 3.10e-6. At t=0.8 mean density 0.97559786, mass drift -0.02440214, density std 0.59488326, p99 3.10085297. 712709 parameters, 21559 steps, 748.0685 training seconds.

## Decision and interpretation

The separate heads did not improve the total locked score or preserve eligibility. Relative to Trial 030, weighted physics rose from 0.08841 to 0.09793 and IC L2 from 0.24973 to 0.25019. The extra parameters and lower step throughput did not yield a sufficient field-specific gain. Reject this integration as a finalist.
