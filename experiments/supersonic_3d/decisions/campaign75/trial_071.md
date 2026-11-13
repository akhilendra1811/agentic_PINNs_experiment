# Trial 071

Research metadata (locked on preparation): parents=trial:67,trial:69; kind=refinement; mechanism_id=poisson_early_strata_integration.

## Parent methods and evidence

Trial 069 is the best eligible candidate: L_val 0.14105955, weighted physics 0.07881428, IC L2 0.24949001. It combines Poisson coefficient 6 with 31.25/25/43.75 early/middle/late sampling. Trial 067 tested coefficient 7 with the older 25/25/50 split and had L_val 0.14728625, slightly worse than coefficient 6 without rebalance. The interaction between coefficient 7 and early rebalancing is untested.

## Novelty claim

Refinement of Poisson/early-strata integration: raise Poisson coefficient to 7 with Trial 069's intermediate collocation split. This is an interaction test of known equation weighting and time-stratified sampling, not publication novelty.

## Hypothesis and proposed change

Hypothesis: stronger Poisson weight can offset any late-window cost of early rebalancing and lower Trial 069's score while preserving IC eligibility. Starting from Trial 069, change only p['poisson'] multiplier from 6.0 to 7.0.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+7*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 320 early/256 middle/448 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect late Poisson below Trial 069's 0.01053077, IC L2 <=0.25 and L_val <0.14105955. Inspect all window residuals, density mass drift and contrast, physical checks, steps and runtime. A score increase or eligibility loss rejects this coefficient within the integrated method.

## Observed results

L_val 0.15946220; weighted physics 0.09712258; IC relative L2 0.24967904 and MSE 0.06233962, eligible true with very narrow margin. Early/middle/late physics totals 0.15809146/0.10131026/0.07022242; late Poisson 0.02506491. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97567862, mass drift -0.02432138, density std 0.59771115, p99 3.08933234. 664325 parameters, 22044 steps, 748.0114 training seconds.

## Decision and interpretation

Poisson coefficient 7 did not protect the late window under early-rebalanced collocation: late Poisson rose from Trial 069's 0.01053077 to 0.02506491. Weighted physics rose from 0.07881428 to 0.09712258, IC L2 worsened slightly, and eligible L_val rose from 0.14105955 to 0.15946220. Reject the higher coefficient in this integration. Trial 069 remains the best eligible score.
