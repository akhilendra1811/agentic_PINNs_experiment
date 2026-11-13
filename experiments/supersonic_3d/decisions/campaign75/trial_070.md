# Trial 070

Research metadata (locked on preparation): parents=trial:69; kind=refinement; mechanism_id=poisson_early_strata_integration.

## Parent methods and evidence

Trial 069 is the best eligible candidate: L_val 0.14105955, weighted physics 0.07881428, IC L2 0.24949001. It combines Poisson coefficient 6 with 31.25/25/43.75 time sampling, but its IC margin is only 0.00050999 against the 0.25 threshold. Its final IC loss coefficient is 33.

## Novelty claim

Refinement of Trial 069's integrated method: increase final IC coefficient from 33 to 34 to widen eligibility margin. This is campaign scalar tuning of established multi-objective PINN training, not publication novelty. A similar increase on Trial 061 worsened physics, so this is an uncertain interaction test rather than an assumed improvement.

## Hypothesis and proposed change

Hypothesis: stronger IC emphasis on Trial 069 lowers IC L2 enough to improve the combined validation score or at least produce a more robust eligible alternative without large physics cost. Starting from Trial 069, change only 1+32*blend to 1+33*blend.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+33*b(f))*IC relative MSE, with b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 320 early/256 middle/448 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect IC L2 <0.24949001 and eligible L_val <=0.14105955, with weighted physics near 0.07881428. Inspect temporal residuals, late Poisson, mass drift, density spread, physical checks, steps and runtime. A substantially higher score or loss of eligibility rejects this refinement as a leader; a wider IC margin can still make it a finalist alternative.

## Observed results

L_val 0.15160604; weighted physics 0.08970255; IC relative L2 0.24880412 and MSE 0.06190349, eligible true. Early/middle/late physics totals 0.15188193/0.09135750/0.06383782; late Poisson 0.02127506. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97758961, mass drift -0.02241039, density std 0.63918275, p99 3.29665899. 664325 parameters, 22915 steps, 748.0965 training seconds.

## Decision and interpretation

Raising final IC coefficient to 34 improved IC L2 from Trial 069's 0.24949001 to 0.24880412, widening the threshold margin. Weighted physics worsened from 0.07881428 to 0.08970255, especially late Poisson (0.01053077 to 0.02127506). L_val rose from 0.14105955 to 0.15160604. The score hypothesis failed; reject as a leader, retaining it as a measured IC-margin alternative. Trial 069 remains the best eligible 750-second score.
