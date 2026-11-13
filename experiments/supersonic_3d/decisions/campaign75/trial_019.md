# Trial 019

Research metadata (locked on preparation): parents=trial:17,trial:18; kind=refinement; mechanism_id=staged_ic_pretraining.

## Parent methods and evidence

Parents Trials 017 and 018, both B architecture with 20% IC-only training and smooth joint-loss ramp. Trial 017 final IC weight 16 achieved IC L2 0.26769212, physics weighted 0.05710781, L_val 0.12876688 (ineligible). Trial 018 final weight 32 achieved first eligibility, IC L2 0.24650130, but physics weighted 0.15019682, L_val 0.21095971 and t=0.8 mass drift -0.03182447. This trial probes the apparent tradeoff between them.

## Novelty claim

Refinement of staged_ic_pretraining. It changes the final IC coefficient to 24, midway between the tested 16 and 32, without changing architecture, duration, ramp shape, sampling or optimiser. This is parameter refinement, not a distinct mechanism or originality claim.

## Hypothesis and proposed change

Hypothesis: final IC weight 24 may cross IC relative L2 <=0.25 while avoiding much of the physics deterioration seen at weight 32. Starting from Trial 017 candidate, replace IC factor 1+15*b with 1+23*b during ramp and final joint training. All other code unchanged.

## Training objective and setup

B ResPINN 664325 parameters, fresh weights. First 20% of 750 s IC relative MSE alone. From 20% to 40%, b=(f-0.2)/0.2 and loss=b*(3.5 continuity+7.5 mean momentum+2.5 Poisson)+(1+23b)*IC relative MSE. Final 60% full PDE weighted terms plus 24 IC relative MSE. Fresh PDE/IC batches 1024 where applicable. Adam 1e-4 to 1e-3 warmup first 5%, then cosine to 1e-5; clip 0.5. Locked validation.

## Expected outcome

Primary target eligibility IC L2 <=0.25. Expect weighted physics between Trials 017 0.05711 and 018 0.15020, preferably near 017, and L_val below Trial 018 0.21096. Inspect early and late Poisson, mass drift, density spread, positivity, periodicity, steps and time. If IC remains ineligible or physics remains poor, it does not solve the tradeoff.

## Observed results

L_val 0.17782229; weighted physics 0.11327072; IC relative L2 0.25407001 (ineligible). Early/middle/late totals 0.15103878/0.07035834/0.12391091. Early continuity/momentum/Poisson 0.06889731/0.05667516/0.02546631; middle 0.02124412/0.02512649/0.02398773; late 0.01534977/0.02104916/0.08751199. Physical checks passed, rho0 error 0, periodic max error 2.26e-6. At t=0.8 mean rho 0.97546309, mass drift -0.02453691, density std 0.60030180, p99 3.08095217. 664325 parameters, 24348 steps, 748.033 s. Training loss 0.8934 at 187.6 s to 1.7962 at 748.0 s.

## Decision and interpretation

The intermediate weight produced intermediate outcomes but failed eligibility: IC L2 0.25407 lies between Trial 017 0.26769 and Trial 018 0.24650, still above 0.25. Weighted physics 0.11327 also lies between their 0.05711 and 0.15020, but is much worse than baseline B 0.04542; late Poisson 0.08751 remains high. L_val 0.17782 is worse than Trial 017. This fixed-weight path has a steep IC/physics tradeoff. Do not promote Trial 019; retain Trial 018 only as eligible fallback. Further research should seek structural or objective changes rather than merely splitting the coefficient again. No numerical-reference accuracy claim follows.
