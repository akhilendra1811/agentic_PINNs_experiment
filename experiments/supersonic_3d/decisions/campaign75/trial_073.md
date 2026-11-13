# Trial 073

Research metadata (locked on preparation): parents=trial:66,trial:69; kind=refinement; mechanism_id=poisson_early_strata_integration.

## Parent methods and evidence

Trial 066 with 25/25/50 early/middle/late samples has eligible L_val 0.14634504, weighted physics 0.08557238, IC L2 0.24652110. Trial 069 with 31.25/25/43.75 split is the best eligible score at L_val 0.14105955 and physics 0.07881428, but IC L2 0.24949001 has a narrow threshold margin. Both use Poisson weight 6 and otherwise identical training. An intermediate split may trade some physics gain for IC robustness.

## Novelty claim

Refinement of Poisson/early-strata integration: interpolate physics sampling to 28.125% early, 25% middle, 46.875% late. This is campaign tuning of established stratified collocation, not publication novelty.

## Hypothesis and proposed change

Hypothesis: the intermediate allocation retains much of Trial 069's early-physics gain while restoring IC margin and yields eligible L_val below 0.14105955. Starting from Trial 069, change only early and late quotas and availability checks to 9n/32 and 15n/32, respectively.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 288 early/256 middle/480 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect IC L2 below Trial 069's 0.24949001, early physics below Trial 066's 0.18880641, and eligible L_val <0.14105955. Inspect all window residuals, late Poisson, density drift and spread, physical checks, steps and runtime. A worse eligible score does not disqualify it as a robustness alternative if the IC margin is materially wider, but rejects the score hypothesis.

## Observed results

L_val 0.15755662; weighted physics 0.09545851; IC relative L2 0.24919493 and MSE 0.06209812, eligible true but still close to threshold. Early/middle/late physics totals 0.17446269/0.09637466/0.06330714; late Poisson 0.02321192. Physical checks passed, rho0 error 0, periodic error 4.05e-6. At t=0.8 mean density 0.97864997, mass drift -0.02135003, density std 0.62201667, p99 3.19818187. 664325 parameters, 22880 steps, 748.0492 training seconds.

## Decision and interpretation

The intermediate split improved IC L2 only slightly from Trial 069's 0.24949001 to 0.24919493, leaving a still-narrow margin. Early physics 0.17446269 is below Trial 066's 0.18880641 but above Trial 069's 0.14354923; late Poisson worsened to 0.02321192. Weighted physics and score both worsened sharply, with L_val 0.15755662. Reject as a leader and robustness alternative; Trial 066 offers a materially wider IC margin and lower score.
