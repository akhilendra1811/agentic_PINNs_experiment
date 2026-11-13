# Trial 074

Research metadata (locked on preparation): parents=trial:66,trial:69; kind=mechanism; mechanism_id=early_to_late_strata_curriculum.

## Parent methods and evidence

Trial 069 uses constant 31.25/25/43.75 early/middle/late physics sampling and Poisson weight 6, reaching the best eligible score L_val 0.14105955 but IC L2 0.24949001 and late physics 0.05258339. Trial 066 uses 25/25/50 sampling with the same Poisson weight, giving higher score 0.14634504 but better late physics 0.04539964 and IC L2 0.24652110. Their strengths suggest a time-varying allocation.

## Novelty claim

Campaign mechanism: begin PDE training with Trial 069's early-emphasized split, then shift to Trial 066's late-emphasized split for the final 40% of training. This differs from earlier moving strata Trial 038 by using fixed two-stage quotas on the current Poisson-weight-6 method. Time curricula are known in PINNs; no publication novelty is claimed.

## Hypothesis and proposed change

Hypothesis: early emphasis during f=0.20 to 0.60 captures Trial 069's early residual gain, while returning to 25/25/50 for f>=0.60 reduces late residual and widens IC margin, yielding eligible score below 0.14105955. Starting from Trial 069, make early and late quotas conditional on f=.60; leave all other code fixed.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full at f=0.40 and b_P full at f=0.25. Physics batch 1024: 320 early/256 middle/448 late through f<0.60, then 256/256/512. IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect early physics below Trial 066's 0.18880641, late physics below Trial 069's 0.05258339, IC L2 <=0.25 and eligible L_val <0.14105955. Examine late Poisson, density drift and spread, physical checks, steps and runtime. A score increase or eligibility failure rejects the moving allocation as a leader.

## Observed results

L_val 0.14672486; weighted physics 0.08612557; IC relative L2 0.24616922 and MSE 0.06059929, eligible true with a wider margin than Trial 069. Early/middle/late physics totals 0.17887244/0.08745386/0.04822985; late Poisson 0.01243926. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.97756284, mass drift -0.02243716, density std 0.64659137, p99 3.29678297. 664325 parameters, 23140 steps, 748.0230 training seconds.

## Decision and interpretation

The two-stage shift improved late physics versus Trial 069 (0.04822985 versus 0.05258339) and widened IC margin (L2 0.24616922 versus 0.24949001). Early physics worsened to 0.17887244 but remained below Trial 066's 0.18880641. Overall score 0.14672486 is above Trial 069's 0.14105955, so the score hypothesis failed. Retain as an eligible, more robust-margin finalist alternative; the validation remains reference-free.
