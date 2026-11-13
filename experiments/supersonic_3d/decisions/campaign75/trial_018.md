# Trial 018

Research metadata (locked on preparation): parents=trial:17; kind=refinement; mechanism_id=staged_ic_pretraining.

## Parent methods and evidence

Parent Trial 017. It gave campaign-best IC L2 0.26769212 but remained above 0.25; its weighted physics 0.05710781 and L_val 0.12876688 were worse than Trial 003. Trial 009 feedback IC weighting modestly improved IC on a different anchored model but worsened physics. This trial tests a fixed stronger IC target on the best IC schedule.

## Novelty claim

Refinement of Trial 017 staged IC-to-physics handoff. The only change is final IC loss coefficient 32 instead of 16, ramped smoothly from 1 during the same transition. This is scalar loss-weight tuning, not a distinct research mechanism or global originality claim. Its rationale is the measured 0.26769 IC L2 remaining just above eligibility.

## Hypothesis and proposed change

Hypothesis: doubling final IC pressure from 16 to 32 reduces validation IC L2 to <=0.25, while physics cost remains small enough for a useful eligible candidate. Keep Trial 017 20% pure IC and 20%-40% smooth ramp. Replace loss IC factor 1+15*b with 1+31*b; all other code unchanged.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, 664325 parameters, fresh weights. For f<0.2, IC relative MSE. For 0.2<=f<0.4, b=(f-0.2)/0.2 and loss=b*(3.5 continuity+7.5 mean momentum+2.5 Poisson)+(1+31b)*IC relative MSE. For f>=0.4, full PDE weighted terms plus 32 IC relative MSE. Fresh PDE/IC batches 1024 where applicable. Adam warmup 1e-4 to 1e-3 for 5% of 750 s then cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Primary target IC L2 <=0.25 versus Trial 017 0.26769212. Expect weighted physics to worsen from 0.05710781; compare final L_val to Trial 017 0.12876688 and baseline B 0.12733444. Inspect early and late Poisson, density spread, mass drift, positivity, periodicity, steps and time. If IC stays ineligible and score worsens, reject the stronger weight.

## Observed results

L_val 0.21095971; weighted physics 0.15019682; IC relative L2 0.24650130 (eligible, first eligible numbered trial). Early/middle/late totals 0.20424397/0.09413435/0.16221545. Early continuity/momentum/Poisson 0.09872600/0.08112531/0.02439266; middle 0.02769065/0.03298494/0.03345875; late 0.01877198/0.02555795/0.11788551. Physical checks passed, rho0 error 0, periodic max error 2.03e-6. At t=0.8 mean rho 0.96817553, mass drift -0.03182447, density std 0.56592107, p99 2.92424965. 664325 parameters, 22582 steps, 748.031 s. Recorded loss 1.0952 at 187.6 s, 3.1936 at 375.1 s, 2.3902 at 562.6 s and 2.3111 at 748.0 s.

## Decision and interpretation

IC hypothesis supported narrowly: increasing the final IC weight from 16 to 32 lowered IC L2 from Trial 017 0.26769 to 0.24650, crossing the fixed eligibility threshold; physical validity also passed. However, weighted physics rose 0.05711 to 0.15020, L_val rose 0.12877 to 0.21096, and late Poisson rose 0.03156 to 0.11789. Density p99 and spread fell and mass drift worsened. Retain only as an eligible fallback, not a leading fidelity method. An intermediate IC weight or different physics-aware method should be investigated. Eligibility does not establish numerical-reference accuracy.
