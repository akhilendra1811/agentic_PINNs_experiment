# Trial 048

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=accelerated_poisson_curriculum.

## Parent methods and evidence

Parent Trial 030 is the best eligible model: L_val 0.15077613, IC L2 0.24972807, weighted physics 0.08841202. Its late Poisson residual 0.01984955 is much lower than earlier eligible trials but still contributes to late physics. Trial 036 delayed Poisson emphasis and worsened late Poisson, suggesting that earlier emphasis might help further.

## Novelty claim

New campaign mechanism: component-specific curriculum with a faster Poisson ramp than continuity and momentum after IC pretraining. Trial 036 tested a delayed Poisson coefficient, but not an accelerated ramp. Curriculum weighting is known; this is a campaign-specific timing hypothesis, not publication novelty.

## Hypothesis and proposed change

Hypothesis: bringing Poisson loss to full weight by f=0.25, rather than f=0.40, will improve potential and late Poisson accuracy while retaining IC eligibility. Starting from Trial 030, multiply Poisson by a separate ramp min(1,(f-0.20)/0.05); keep continuity and momentum on the original 0.20-to-0.40 ramp, and keep the IC coefficient, model, optimizer and sampling unchanged.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From f=0.20 onward, loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+29*b(f))*IC relative MSE, where b rises to 1 by f=0.40 and b_P rises to 1 by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect late Poisson below Trial 030's 0.01984955, IC L2 <=0.25 and L_val <0.15077613. Check early continuity/momentum, all temporal windows, mass drift, density spread, physical checks, steps and runtime. If early Poisson pressure harms IC or other physics components, reject the schedule.

## Observed results

L_val 0.14355815; weighted physics 0.08044155; IC relative L2 0.25123018 and MSE 0.06311660, eligible false. Early/middle/late physics totals 0.17200769/0.07662895/0.04610265; late Poisson 0.01210435. Physical checks passed, rho0 error 0, periodic error 2.15e-6. At t=0.8 mean density 0.97810441, mass drift -0.02189559, density std 0.65888661, p99 3.37910318. 664325 parameters, 23991 steps, 748.0558 training seconds.

## Decision and interpretation

The faster Poisson ramp improved late Poisson from Trial 030's 0.01984955 to 0.01210435, weighted physics from 0.08841 to 0.08044, and L_val from 0.15078 to 0.14356. IC L2 increased from 0.24973 to 0.25123, narrowly losing eligibility. The physics hypothesis is supported but the candidate is ineligible. A separate stronger-IC integration is justified; do not select Trial 048 itself.
