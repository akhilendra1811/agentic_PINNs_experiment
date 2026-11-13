# Trial 029

Research metadata (locked on preparation): parents=trial:27; kind=refinement; mechanism_id=late_time_collocation_stratification.

## Parent methods and evidence

Parent Trial 027 is the current best eligible candidate: L_val 0.17473586, weighted physics 0.11269733, IC L2 0.24907537. Late Poisson 0.06188309 remains the largest late component, compared with continuity 0.01446038 and momentum 0.01861996. The 25/25/50 time-stratified sampling already improved late Poisson relative to uniform Trial 025.

## Novelty claim

Refinement of Trial 027's training objective: double the Poisson coefficient while keeping the time allocation and IC curriculum unchanged. Trial 015 dynamically balanced PDE components on the B baseline and did not improve overall score; this is a fixed Poisson emphasis on the best eligible branch. This is a loss-weight test, not a new method.

## Hypothesis and proposed change

Hypothesis: raising the Poisson coefficient from 2.5 to 5.0 will reduce late Poisson below 0.06188309 without increasing continuity or momentum enough to lose the score gain. Change only that coefficient in the ramped physics loss.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+27*blend)*IC relative MSE, then full blend. Each physics batch has 256 early, 256 middle and 512 late points from fresh domain candidates; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect late Poisson <0.06188309, IC L2 <=0.25 and L_val <0.17473586. Inspect whether continuity, momentum or early-window error worsens, and check density spread, mass drift, physical validity, runtime and steps. If the stronger coefficient merely shifts error or loses eligibility, retain Trial 027.

## Observed results

L_val 0.14587287; weighted physics 0.08204877; IC relative L2 0.25263432 and MSE 0.06382410, eligible false. Early/middle/late physics totals 0.16675097/0.07787818/0.05067025. Late Poisson fell to 0.01812841. Physical checks passed, rho0 error 0, periodic error 3.34e-6. At t=0.8 mean density 0.97803473, mass drift -0.02196527, density std 0.64212704, p99 3.31496382. 664325 parameters, 23953 steps, 748.0838 training seconds.

## Decision and interpretation

Doubling Poisson weight improved late Poisson from Trial 027's 0.06188309 to 0.01812841 and reduced L_val from 0.17473586 to 0.14587287. It also raised IC L2 from 0.24907537 to 0.25263432, failing the 0.25 eligibility threshold. The physics hypothesis is supported, but this candidate is ineligible. A separate integration trial with a stronger IC term is justified; do not promote Trial 029 itself.
