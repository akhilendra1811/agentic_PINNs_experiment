# Trial 003

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=staged_ic_pretraining.

## Parent methods and evidence

Parent B alone. B is the best reference-free method so far (L_val 0.12733444, IC L2 0.28621542, ineligible). Trials 001 and 002 worsened IC L2 to 0.29519 and 0.29229. Both baselines and both trials missed the 0.25 threshold. This trial returns to B architecture and targets IC optimisation directly.

## Novelty claim

Distinct campaign mechanism: staged initial-condition pretraining. No numbered trial has isolated IC fit before physics optimisation. This is a curriculum of objectives, not a scalar-weight tweak. The Cornell SciML hard-constraint overview and recent PINN IC-stability literature motivate paying special attention to ICs, but this experiment uses soft IC pretraining because only sampled training IC targets are available. No global originality claim.

## Hypothesis and proposed change

Hypothesis: fitting the turbulent IC first gives the shared representation a better starting point, reducing final IC relative L2 and perhaps crossing eligibility without unacceptable physics degradation. For first 20% of budget, optimise IC relative MSE alone on authorised training IC samples; for remaining 80%, use exact B joint loss and fresh PDE samples. Keep model and optimiser unchanged.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, three periodic harmonics, 664325 parameters, fresh weights. First 20%: mean squared IC velocity error / mean squared IC target velocity. Remaining 80%: 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Batch 1024. Adam 1e-4 to 1e-3 warmup for first 5% of 750 s, then cosine to 1e-5; gradient clip 0.5. Locked validation and budget.

## Expected outcome

Expect IC L2 below B 0.28621542, ideally <=0.25. Compare L_val to B 0.12733444 and early/middle/late physics totals 0.07511238/0.03290586/0.04104188. Physics may worsen because fewer seconds are spent on PDE losses; check the magnitude. Physical checks, mass drift and density spread must also be inspected.

## Observed results

L_val 0.12452034; weighted physics 0.05130065; IC relative L2 0.27059138 (ineligible). Early/middle/late physics totals 0.08318412/0.03337046/0.04930537. Early continuity/momentum/Poisson 0.03509940/0.03329251/0.01479221; middle 0.01026841/0.01595849/0.00714357; late 0.01032622/0.01547166/0.02350749. Positivity/periodicity passed, rho0 error 0, periodic error 3.10e-6. At t=0.8 mean rho 0.98537076, mass drift -0.01462924, density std 0.68394524, p99 3.50677109. 664325 parameters, 21535 steps, 748.033 s. Recorded joint-loss values 2.5078 at 187.6 s, 1.7023 at 375.1 s, 1.3659 at 562.5 s and 1.4219 at 748.0 s; the first 20% IC-only phase yielded many cheap steps before these records.

## Decision and interpretation

Partially supports the IC hypothesis: IC L2 improved from B 0.28622 to 0.27059 and L_val improved from 0.12733 to 0.12452, the best so far. It remains ineligible because IC L2 > 0.25. Physics weighted score worsened (0.05130 vs 0.04542), including early and late totals; late Poisson rose from 0.01179 to 0.02351. Retain as a promising parent for an IC-focused refinement or combination, but account for physics tradeoff. No numerical-reference accuracy claim is justified.
