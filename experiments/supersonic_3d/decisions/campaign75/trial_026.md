# Trial 026

Research metadata (locked on preparation): parents=trial:25; kind=mechanism; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parent Trial 025 is the strongest eligible candidate to date: IC L2 0.24920297, L_val 0.19754017, weighted physics 0.13543805. Its late Poisson residual 0.10972013 dominates the late window total 0.15126707, which carries half of L_val's physics weighting. It uses uniform fresh physics sampling during the ramped objective.

## Novelty claim

Campaign mechanism: late-time-stratified physics collocation integrated with the eligible staged IC-pretraining schedule. Prior Trial 014 biased collocation toward high predicted density, and Trial 002 used causal time curriculum. Neither explicitly oversampled the late validation window. Stratified sampling is a known general approach, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: drawing about 69% of each physics batch from t>0.5 will reduce Trial 025's late Poisson residual and overall L_val without losing IC eligibility. Keep the architecture, objective and IC sampling fixed. During physics training, draw 2n fresh domain candidates, take n/2 with t>0.5 and n/2 randomly, then evaluate the canonical physics components on the n selected points.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20%: IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+2.5 Poisson)+(1+27*blend)*IC relative MSE, then full blend. Physics batch 1024 selected as 512 late and 512 random from fresh candidates; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect late Poisson below 0.10972013 and L_val below 0.19754017, with IC L2 <=0.25. Check whether early and middle residuals worsen from reduced coverage, whether mass drift and density spread change, and whether parameter count, runtime and physical checks remain valid. If late improvement is outweighed by earlier errors or IC ineligibility, reject this sampling schedule.

## Observed results

L_val 0.21293513; weighted physics 0.15492667; IC relative L2 0.24084945 and MSE 0.05800846, eligible true. Early/middle/late physics totals 0.44715198/0.12272781/0.05735586. Late Poisson fell to 0.03588615, but early continuity/momentum rose to 0.20526400/0.18579220. Physical checks passed, rho0 error 0, periodic error 2.15e-6. At t=0.8 mean density 0.95987570, mass drift -0.04012430, density std 0.56101781, p99 2.89017200. 664325 parameters, 24009 steps, 748.0192 training seconds.

## Decision and interpretation

The late-time oversampling reduced late Poisson from Trial 025's 0.10972013 to 0.03588615 and improved IC L2 from 0.24920 to 0.24085. It also raised early physics from 0.17388 to 0.44715, so weighted physics and L_val worsened overall (0.13544 to 0.15493; 0.19754 to 0.21294). The result supports the expected local late-window gain but rejects the proposed overall score improvement. A more balanced time distribution is worth a separate test; this candidate may be considered for finalist diversity, though Trial 025 remains stronger by L_val.
