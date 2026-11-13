# Trial 002

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=causal_time_curriculum.

## Parent methods and evidence

Parent B alone. Its L_val 0.12733444, IC L2 0.28621542, early/middle/late physics 0.07511238/0.03290586/0.04104188. Trial 001 eight-harmonic encoding worsened IC and all windows, so revert architecture to B and investigate temporal optimisation. B early physics is higher than its middle and late physics.

## Novelty claim

Distinct campaign mechanism: causal time curriculum. No earlier numbered trial used time-dependent domain sampling. Adapted from Wang, Sankaran and Perdikaris, “Respecting causality is all you need for training physics-informed neural networks” (https://arxiv.org/abs/2203.07404). This is a staged sampling adaptation, not a claimed exact reproduction or global novelty.

## Hypothesis and proposed change

Hypothesis: resolving early-time Euler-Poisson residuals before exposing later times reduces early residuals and improves subsequent full-interval consistency. Change only B domain sampling: first 30% of budget sample t in [0,0.2], next 30% in [0,0.5], final 40% in [0,0.8]. Keep IC sampling throughout.

## Training objective and setup

Exact B architecture (ResPINN width 256, ten sine residual blocks, alpha 0.5, three periodic harmonics, rho=exp(t*raw_rho)); 664325 parameters. Loss = 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh domain and IC batches of 1024. Adam 1e-4 to 1e-3 warmup over 5% of 750 s, cosine decay to 1e-5; gradient clipping 0.5. Fresh weights; locked evaluator and validation.

## Expected outcome

Expect early physics total below B 0.07511238 and weighted physics below 0.04541517 without a larger late-time penalty that worsens L_val. IC relative L2 should remain comparable to B; eligibility needs <=0.25. Check density spread, mass drift, positivity and periodicity for tradeoffs.

## Observed results

L_val 0.15086197; weighted physics 0.06542765; IC relative L2 0.29229149 (ineligible). Early/middle/late physics 0.07933791/0.03904567/0.07569274. Early continuity/momentum/Poisson 0.03005061/0.03328246/0.01600485; middle 0.01206572/0.01755937/0.00942058; late 0.01703583/0.02256953/0.03608738. Physical checks passed (rho0 error 0, periodic max error 2.62e-6). At t=0.8 mean rho 0.98175555, mass drift -0.01824445, density std 0.62538844, p99 3.21842456. 664325 parameters, 5560 steps, 748.089 s. Training loss recorded 2.1068 at 187.6 s, 1.7336 at 375.0 s, 1.8469 at 562.6 s, and 1.6445 at 748.1 s.

## Decision and interpretation

Hypothesis not supported by this schedule. Early physics worsened versus B (0.07934 vs 0.07511), and late physics deteriorated markedly (0.07569 vs 0.04104), especially Poisson (0.03609 vs 0.01179). IC L2 also worsened (0.29229 vs 0.28622), and L_val rose (0.15086 vs 0.12733). The curriculum withheld late times for 60% of training, which may have been too aggressive; that is an interpretation rather than a measured causal attribution. Do not promote this schedule. A different causal loss design would be a distinct follow-up only with explicit rationale. Reference-free diagnostics cannot establish numerical trajectory accuracy.
