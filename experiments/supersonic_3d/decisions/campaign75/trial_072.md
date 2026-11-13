# Trial 072

Research metadata (locked on preparation): parents=trial:61,trial:66; kind=refinement; mechanism_id=poisson_early_strata_integration.

## Parent methods and evidence

Trial 061's 37.5/25/37.5 early/middle/late collocation improved early physics, but with Poisson weight 5 its late Poisson rose and L_val was 0.15067655. Trial 066 with Poisson weight 6 and 25/25/50 split became eligible at L_val 0.14634504. Trial 069 combined weight 6 with an intermediate 31.25/25/43.75 split and improved to L_val 0.14105955, albeit IC L2 0.24949001 near threshold. The stronger early split with weight 6 remains untested.

## Novelty claim

Refinement of the Poisson/early-strata integration: test the full 37.5/25/37.5 early allocation with Poisson weight 6. This is a campaign interaction test of established equation weighting and time-stratified sampling, not publication novelty.

## Hypothesis and proposed change

Hypothesis: Poisson weight 6 protects late residual while more early samples further reduce the high early residual and improve eligible score. Starting from Trial 066, change only physics time quotas and availability checks to 3n/8 early, n/4 middle, 3n/8 late.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE; b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 384 early/256 middle/384 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect early physics below Trial 069's 0.14354923, late Poisson near 0.01053077, IC L2 <=0.25 and L_val <0.14105955. Inspect all time-window residuals, mass drift, density spread, physical checks, steps and runtime. Narrow or lost IC eligibility and a worse score reject the stronger early allocation as leader.

## Observed results

L_val 0.15841287; weighted physics 0.09537751; IC relative L2 0.25106844 and MSE 0.06303536, ineligible because IC L2 exceeds 0.25. Early/middle/late physics totals 0.12219867/0.09544327/0.08460958; late Poisson 0.03277761. Physical checks passed, rho0 error 0, periodic error 4.29e-6. At t=0.8 mean density 0.97746575, mass drift -0.02253425, density std 0.61848575, p99 3.20775557. 664325 parameters, 22899 steps, 748.0037 training seconds.

## Decision and interpretation

The full early allocation reduced early physics from Trial 069's 0.14354923 to 0.12219867 but harmed late total (0.05258339 to 0.08460958) and late Poisson (0.01053077 to 0.03277761). IC L2 0.25106844 fails the strict threshold, and L_val is also worse. Reject the candidate as ineligible; the stronger Poisson coefficient did not protect the late window under this allocation. Trial 069 remains the eligible leader.
