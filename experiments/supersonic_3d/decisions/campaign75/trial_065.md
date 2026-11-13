# Trial 065

Research metadata (locked on preparation): parents=trial:57,trial:64; kind=refinement; mechanism_id=momentum_focused_balanced_curriculum.

## Parent methods and evidence

Trial 057 with momentum coefficient 7.5 is best eligible: L_val 0.15052786, physics 0.09003139, IC L2 0.24596031. Trial 064 raised momentum coefficient to 9.0, improving physics to 0.08957064 but worsening IC L2 to 0.24918790 and score to 0.15166525. An intermediate coefficient may retain the physics benefit with less IC cost.

## Novelty claim

Refinement of the momentum-focused physics weighting mechanism: interpolate momentum coefficient to 8.25. Fixed equation weighting is established practice; this is a campaign parameter test, not publication novelty.

## Hypothesis and proposed change

Hypothesis: coefficient 8.25 balances the parent scores and yields eligible L_val below Trial 057. Starting from Trial 057, change only momentum coefficient 7.5 to 8.25 in the physics loss. All other model and training settings remain fixed.

## Training objective and setup

Trial 057 ResPINN: width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+8.25 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE; b full by f=0.40, b_P full by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect validation momentum below Trial 057, IC L2 <=0.25 and L_val <0.15052786. Inspect all window components, late Poisson, density mass drift and spread, physical checks, steps and runtime. A worse eligible score rejects the interpolation.

## Observed results

L_val 0.15751998; weighted physics 0.09595489; IC relative L2 0.24812312 and MSE 0.06156508, eligible true. Early/middle/late physics totals 0.19019334/0.09296749/0.06005195; momentum residuals 0.07494675/0.04119870/0.01877447; late Poisson 0.02561028. Physical checks passed, rho0 error 0, periodic error 3.10e-6. At t=0.8 mean density 0.97455502, mass drift -0.02544498, density std 0.62219042, p99 3.21901011. 664325 parameters, 22685 steps, 748.0123 training seconds.

## Decision and interpretation

The 8.25 momentum coefficient improves momentum residual relative to Trial 057, but weighted physics worsens to 0.09595489 and IC L2 worsens to 0.24812312. L_val 0.15751998 is above both Trial 057's 0.15052786 and Trial 064's 0.15166525. The scalar interpolation is not monotonic in score and fails the primary hypothesis. Reject as a leader.
