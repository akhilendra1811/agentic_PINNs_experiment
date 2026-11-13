# Trial 017

Research metadata (locked on preparation): parents=trial:3; kind=refinement; mechanism_id=staged_ic_pretraining.

## Parent methods and evidence

Parent Trial 003 (B architecture with 20% IC-only pretraining). It achieved campaign-best IC L2 0.27059138 and L_val 0.12452034, but weighted physics 0.05130065 was worse than B 0.04541517. Trial 005 extended pure IC stage to 40% and worsened both IC (0.28240019) and physics (0.08062024). This trial tests transition shape rather than a longer pure IC phase.

## Novelty claim

Refinement of staged_ic_pretraining, not a newly counted mechanism. Trial 003 changed abruptly from IC-only to full B objective at 20% time; Trial 005 delayed that abrupt switch to 40%. This trial retains 20% pure IC training and ramps the joint objective smoothly until 40%. No global novelty claim.

## Hypothesis and proposed change

Hypothesis: a smooth handoff preserves the IC representation from pretraining while reducing the physics shock seen in Trial 003 and Trial 005. For f<0.2 use IC relative MSE only. For 0.2<=f<0.4 set b=(f-0.2)/0.2 and loss=b*(3.5 continuity+7.5 momentum+2.5 Poisson)+(1+15b)*IC relative MSE. For f>=0.4 use full B loss. Same B model and optimiser.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, three harmonics, 664325 parameters, fresh weights. Staged loss as above. During f>=0.2, fresh PDE and IC batches 1024; during initial IC phase, IC batch 1024. Adam warmup 1e-4 to 1e-3 over first 5% of 750 s, cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Expect IC L2 below Trial 003 0.27059138, ideally <=0.25, with weighted physics no worse than 0.05130065 and L_val below 0.12452034. Examine early and late Poisson because prior IC stages hurt physics there. Inspect density spread, mass drift, positivity, periodicity, steps and training time. If smoothing worsens score, reject this schedule.

## Observed results

L_val 0.12876688; weighted physics 0.05710781; IC relative L2 0.26769212 (best IC so far, still ineligible). Early/middle/late totals 0.08904326/0.03585831/0.05708333. Early continuity/momentum/Poisson 0.03703973/0.03468686/0.01731666; middle 0.01076304/0.01605860/0.00903667; late 0.01042430/0.01509641/0.03156262. Physical checks passed, rho0 error 0, periodic max error 3.34e-6. At t=0.8 mean rho 0.98668098, mass drift -0.01331902, density std 0.67635447, p99 3.48569298. 664325 parameters, 24370 steps, 748.055 s. Recorded loss 0.6719 during ramp at 187.5 s, 1.6660 at 375.0 s, 1.3676 at 562.5 s and 1.2791 at 748.1 s.

## Decision and interpretation

Partially supports the smooth-handoff hypothesis for IC alone: IC L2 improved from Trial 003 0.27059 to 0.26769, but remains above eligibility <=0.25. Weighted physics worsened 0.05130 to 0.05711 and L_val worsened 0.12452 to 0.12877. Late Poisson increased 0.02351 to 0.03156, offsetting the IC gain. Retain as the best IC-fitting branch for later combinations, but not as a leading overall score or eligible method. A single seed does not establish robustness and reference-free scores do not establish trajectory accuracy.
