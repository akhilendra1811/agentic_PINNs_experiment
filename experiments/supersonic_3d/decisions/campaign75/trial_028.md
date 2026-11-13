# Trial 028

Research metadata (locked on preparation): parents=trial:27; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parent Trial 027 combined a smooth IC-to-physics ramp with 25/25/50 early/middle/late physics sampling. It is the best eligible result so far at L_val 0.17473586, weighted physics 0.11269733 and IC L2 0.24907537. Its eligibility margin is only 0.00092463, which may not survive fresh matched-time training.

## Novelty claim

Refinement of Trial 027's time-stratified staged-training mechanism. Raise the final IC weight from 28 to 30 to test a wider eligibility margin. This is a loss-coefficient refinement, not a new mechanism or publication novelty.

## Hypothesis and proposed change

Hypothesis: final IC weight 30 will reduce IC L2 below Trial 027's 0.24907537 without raising L_val above Trial 025's 0.19754017. Change only the ramped IC coefficient from 1+27*blend to 1+29*blend; retain the architecture, sampling and optimizer.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+2.5 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Each physics batch has 256 early, 256 middle and 512 late points from fresh domain candidates; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <0.24907537 and eligible true, with L_val <0.19754017. Compare physics residuals in all windows, especially late Poisson, plus density spread, mass drift, physical checks, runtime and steps. If eligibility margin fails to widen or physics cost dominates, keep Trial 027 as the stronger candidate.

## Observed results

L_val 0.18099374; weighted physics 0.11970423; IC relative L2 0.24756718 and MSE 0.06128951, eligible true. Early/middle/late physics totals 0.20104993/0.09989602/0.09905087; late Poisson 0.06438857. Physical checks passed, rho0 error 0, periodic error 8.82e-6. At t=0.8 mean density 0.96997428, mass drift -0.03002572, density std 0.59712076, p99 3.08413911. 664325 parameters, 23616 steps, 748.0693 training seconds.

## Decision and interpretation

The higher IC coefficient widened the eligibility margin slightly: IC L2 0.24757 versus Trial 027's 0.24908. It also raised weighted physics from 0.11270 to 0.11970 and L_val from 0.17474 to 0.18099. The score remains below Trial 025's 0.19754, so the hypothesis was partly supported, but Trial 027 remains the best eligible score. Keep Trial 028 as a possible robust-IC finalist alternative, not the current leader.
