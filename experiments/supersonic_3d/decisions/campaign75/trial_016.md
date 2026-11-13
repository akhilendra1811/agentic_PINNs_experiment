# Trial 016

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=high_speed_ic_sampling.

## Parent methods and evidence

Parent B alone. B IC relative L2 0.28621542 misses eligibility <=0.25. Trial 003 IC-first optimisation reached 0.27059138, the best so far, but hurt physics. Trial 015 adaptive PDE balancing reached IC 0.27280518 but worsened aggregate physics. No numbered trial has sampled IC training targets by velocity magnitude. Trial 014 sampled PDE points by predicted density and did not help.

## Novelty claim

Distinct campaign mechanism: velocity-magnitude-aware IC sampling with random coverage. This changes which authorised initial-condition examples enter updates, not the model or scalar loss weights. It is motivated by the turbulent high-speed tails and the IC eligibility failure. It is a campaign hypothesis, not a claim of global scientific originality or a reproduction of a paper.

## Hypothesis and proposed change

Hypothesis: presenting more high-speed IC examples will improve the difficult turbulent velocity fit enough to lower validation IC relative L2 without excessive physics tradeoff. Every other step draw 2048 authorised training IC examples; choose 512 with largest target speed squared and 512 random, while intervening steps use 1024 uniformly sampled IC examples. PDE sampling remains B fresh uniform.

## Training objective and setup

Exact B ResPINN 664325 parameters, fresh weights. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE batch 1024 each step. IC batch 1024; every other step selected from 2048 targets as stated. Adam warmup 1e-4 to 1e-3 over first 5% of 750 s, cosine to 1e-5; clip gradient 0.5. Locked validation and parameter cap.

## Expected outcome

Expect IC L2 below B 0.28621542 and preferably <=0.25; compare L_val to B 0.12733444 and Trial 003 0.12452034. Target-biased sampling may sacrifice average IC fit or PDE consistency, so inspect all temporal residuals, mass drift, density spread, positivity, periodicity, steps and training time. If validation IC does not improve, reject this sampling rule.

## Observed results

L_val 0.12766574; weighted physics 0.04006413; IC relative L2 0.29597569 (ineligible). Early/middle/late totals 0.06506739/0.02889592/0.03676376. Early continuity/momentum/Poisson 0.02438991/0.03035114/0.01032634; middle 0.00790890/0.01441595/0.00657107; late 0.01096905/0.01543125/0.01036346. Physical checks passed, rho0 error 0, periodic max error 2.38e-6. At t=0.8 mean rho 0.98753762, mass drift -0.01246238, density std 0.68381560, p99 3.53398061. 664325 parameters, 6569 steps, 748.002 s. Recorded training loss 1.7115 at 187.5 s to 1.0387 at 748.0 s.

## Decision and interpretation

Hypothesis rejected for validation IC fit: IC L2 worsened versus B 0.28622 to 0.29598 and remains ineligible. Weighted physics improved 0.04542 to 0.04006, with all temporal totals lower, but IC penalty pushed L_val slightly above B (0.12767 vs 0.12733). Biased targets may improve selected high-speed samples while neglecting average points; per-speed-bin validation was not provided, so that remains an interpretation. Do not promote this IC sampling rule as-is. No numerical-reference accuracy claim follows.
