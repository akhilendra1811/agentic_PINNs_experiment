# Trial 055

Research metadata (locked on preparation): parents=trial:15,trial:30; kind=mechanism; mechanism_id=balanced_pde_ema_stratified_ic.

## Parent methods and evidence

Parents Trial 015 and Trial 030. Trial 015 used inverse-EMA scaling of continuity, momentum and Poisson losses on B, improving IC L2 to 0.27280518 but yielding L_val 0.13912567 and worse momentum, still ineligible. Trial 030 uses fixed PDE coefficients with staged IC training and balanced time sampling, achieving the best eligible L_val 0.15077613 and IC L2 0.24972807. This trial tests the EMA balance within Trial 030's stronger base method.

## Novelty claim

Campaign integration mechanism: adaptive PDE component scaling combined with IC pretraining and time-stratified physics batches. Trial 015 tested scaling only on B. Adaptive loss balancing is known PINN methodology; no publication novelty claim.

## Hypothesis and proposed change

Hypothesis: equalizing slowly varying PDE component magnitudes will improve Trial 030's weighted physics while preserving IC eligibility. Starting from Trial 030, maintain EMA of the three PDE scalar losses with decay 0.99; multiply each base coefficient by the geometric-mean EMA divided by its own EMA, clipped to [0.5,2], as in Trial 015. Keep architecture, IC coefficient, sampling and optimizer unchanged.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5*s_C continuity+7.5*s_M momentum+5.0*s_P Poisson)+(1+29*blend)*IC relative MSE, then full blend. Each s is clipped geometric-mean EMA / component EMA. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect weighted physics <Trial 030's 0.08841202, IC L2 <=0.25 and L_val <0.15077613. Inspect whether momentum worsens as in Trial 015, late Poisson, mass drift, density contrast, physical checks, throughput and runtime. If component balancing shifts rather than reduces error, reject the integration.

## Observed results

L_val 0.20159039; weighted physics 0.14157233; IC relative L2 0.24498583 and MSE 0.06001806, eligible true. Early/middle/late physics totals 0.29049638/0.16516415/0.06784761. Poisson residuals improved to 0.01029790/0.00474576/0.01007164, but continuity rose to 0.19285115/0.11285692/0.03641234. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97637194, mass drift -0.02362806, density std 0.54875141, p99 2.88866496. 664325 parameters, 24016 steps, 748.0962 training seconds.

## Decision and interpretation

Adaptive scaling improved IC L2 from Trial 030's 0.24973 to 0.24499 and reduced Poisson residuals, but shifted error strongly into continuity. Weighted physics rose from 0.08841 to 0.14157 and L_val from 0.15078 to 0.20159. The total-score hypothesis is rejected; this variant is eligible but not competitive for finalist selection.
