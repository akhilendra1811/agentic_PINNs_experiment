# Trial 043

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=exponential_weight_averaging.

## Parent methods and evidence

Parent Trial 030 is the best eligible result: L_val 0.15077613, weighted physics 0.08841202 and IC L2 0.24972807. Its IC margin is only 0.00027193, so small late-optimization fluctuations could matter. Trial 031 widened the margin by stronger IC weighting but raised the score. This trial changes only how the final learned weights are selected.

## Novelty claim

New campaign mechanism: exponential moving average of network parameters during training, evaluated instead of the last Adam iterate. No earlier trial used weight averaging. EMA is a known optimization technique; this is a campaign-specific robustness test, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: averaging the last roughly 1000 optimizer iterates will reduce validation noise and improve L_val or IC eligibility margin without modifying the training objective. Starting from Trial 030, maintain parameter EMA with decay 0.999 after each optimizer step, then copy averaged parameters into the model before the evaluator saves and validates it.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5. EMA decay 0.999; all architecture and loss coefficients fixed.

## Expected outcome

Expect IC L2 <=0.25 with a margin wider than Trial 030 and L_val <=0.15077613. Inspect physics windows, mass drift, density contrast, physical checks, steps and runtime. If averaging lags the final convergence and worsens score or IC eligibility, reject it.

## Observed results

L_val 0.16126161; weighted physics 0.09860942; IC relative L2 0.25030419 and MSE 0.06265219, eligible false. Early/middle/late physics totals 0.19505812/0.09485421/0.06228307; late Poisson 0.02728963. Physical checks passed, rho0 error 0, periodic error 3.34e-6. At t=0.8 mean density 0.97372729, mass drift -0.02627271, density std 0.59572363, p99 3.03473735. 664325 parameters, 22871 steps, 748.0117 training seconds.

## Decision and interpretation

EMA worsened Trial 030's weighted physics from 0.08841 to 0.09861 and IC L2 from 0.24973 to 0.25030, losing eligibility. L_val rose from 0.15078 to 0.16126. The averaging hypothesis is rejected for decay 0.999; late model improvement appears important enough that this EMA lag is harmful. Do not select this candidate.
