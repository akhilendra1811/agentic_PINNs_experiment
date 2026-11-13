# Trial 005

Research metadata (locked on preparation): parents=trial:3; kind=refinement; mechanism_id=staged_ic_pretraining.

## Parent methods and evidence

Parent Trial 003, which used B architecture with 20% IC-only pretraining. It produced the campaign-best L_val 0.12452034 and IC L2 0.27059138, improving B IC L2 0.28621542 but missing eligibility <=0.25. Its weighted physics worsened from B 0.04541517 to 0.05130065. Trial 004 adaptive sampling failed without metrics due excessive runtime.

## Novelty claim

Refinement of staged_ic_pretraining, not a fifth distinct mechanism. Change only IC-only duration from 20% to 40% of fixed budget. Trial 003 established a partial benefit; this tests whether the dose-response reaches IC eligibility or overfits the initial field at the expense of physics.

## Hypothesis and proposed change

Hypothesis: extending the IC-only stage to 40% lowers validation IC relative L2 below 0.25, with a measurable but tolerable PDE residual penalty. Replace the f < .20 stage boundary with f < .40 in Trial 003 candidate.py; all other architecture, optimiser, sampling and losses remain fixed.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, three harmonics, 664325 parameters, fresh weights. First 40%: relative IC velocity MSE only. Final 60%: 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 relative IC MSE. Authorised IC and fresh PDE batches of 1024. Adam warmup from 1e-4 to 1e-3 for first 5% of 750 s, then cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Expect IC L2 below Trial 003 0.27059138 and ideally <=0.25. Compare L_val against 0.12452034 and weighted physics against 0.05130065; inspect early and late Poisson for degradation. Record steps, mass drift, density spread, positivity and periodicity. If IC improves but physics outweighs it, the schedule is not a leading finalist.

## Observed results

L_val 0.16037011; weighted physics 0.08062024; IC relative L2 0.28240019 (ineligible). Early/middle/late physics totals 0.10286166/0.04724068/0.09175141. Early continuity/momentum/Poisson 0.04229809/0.03803269/0.02253088; middle 0.01410326/0.01830678/0.01483064; late 0.01228436/0.01781294/0.06165410. Positivity and periodicity passed, rho0 error 0, periodic max error 2.50e-6. At t=0.8 mean rho 0.98155713, relative mass drift -0.01844287, density std 0.61206472, p99 3.15918517. 664325 parameters, 39349 steps, 748.017 s. Recorded loss 0.00998 during IC-only stage at 187.5 s, 2.03691 shortly after joint-stage transition at 375.1 s, 1.68163 at 562.5 s and 1.46674 at 748.0 s.

## Decision and interpretation

Hypothesis rejected for this duration: compared with Trial 003, IC L2 worsened 0.27059 to 0.28240 and L_val worsened 0.12452 to 0.16037. Physics weighted loss increased 0.05130 to 0.08062, driven particularly by late Poisson 0.02351 to 0.06165. The 40% IC stage gave less time to reconcile the field with PDE constraints and did not reach IC eligibility. Trial 003 remains the better staged-IC parent. A shorter or smoother transition may be studied later, but this schedule should not be retained. No numerical-reference accuracy claim follows.
