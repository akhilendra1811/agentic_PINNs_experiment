# Trial 006

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=separate_spatial_velocity_branch.

## Parent methods and evidence

Parent B alone. B IC L2 0.28621542 misses the 0.25 eligibility limit. Trial 003 IC-only pretraining improved IC to 0.27059138 and L_val to 0.12452034 but hurt physics. A longer IC-only stage in Trial 005 worsened both. This trial tests representational separation while keeping B training intact.

## Novelty claim

Distinct campaign mechanism: dedicated spatial velocity branch added to a shared time-dependent backbone. No prior numbered trial separated a time-independent spatial velocity representation from the evolving fields. This is a campaign architecture hypothesis, not a global originality claim; generic multi-branch neural architectures are known. No external source is asserted as an exact design origin.

## Hypothesis and proposed change

Hypothesis: a separate spatial branch can encode turbulent initial velocity more accurately without spending training time on an IC-only stage. Add an 18-to-128-to-128-to-3 smooth SiLU branch of the periodic spatial features; predicted velocity is B raw velocity plus this branch. Density and potential heads, backbone and training remain B. The spatial branch is periodic by construction.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, three spatial harmonics, alpha 0.5, plus a 2-hidden-layer width-128 spatial velocity branch with SiLU. Fresh weights; <=750000 parameters required. Loss = 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and IC batches 1024. Adam warmup 1e-4 to 1e-3 for 5% of 750 s then cosine to 1e-5, gradient clip 0.5. Locked evaluator.

## Expected outcome

Expect IC L2 below B 0.28621542, ideally <=0.25, and L_val below 0.12733444. Additional spatial derivatives may raise momentum or continuity, especially early; inspect each temporal window. Verify parameter count, mass drift, density spread, positivity, periodicity, and actual steps. Retain only if the IC benefit is not outweighed by physics degradation.

## Observed results

L_val 0.13232787; weighted physics 0.04761745; IC relative L2 0.29105055 (ineligible). Early/middle/late totals 0.07804436/0.03467228/0.04321379. Early continuity/momentum/Poisson 0.02945883/0.03644503/0.01214050; middle 0.00941681/0.01750390/0.00775157; late 0.01226519/0.01774810/0.01320051. Physical checks passed, rho0 error 0, periodic max error 3.10e-6. At t=0.8 mean rho 0.98633349, mass drift -0.01366651, density std 0.65933436, p99 3.42922139. 683656 parameters, 5908 steps, 748.069 s. Recorded training loss 2.3463 at 187.6 s to 1.5712 at 748.1 s.

## Decision and interpretation

Hypothesis not supported at this budget: IC L2 worsened versus B (0.29105 vs 0.28622), and L_val worsened (0.13233 vs 0.12733). Weighted physics also worsened slightly (0.04762 vs 0.04542); all temporal totals were higher. The branch increased parameters and reduced steps versus B (5908 vs 6852), which may explain some loss of optimisation but cannot be isolated in one run. Periodicity and positivity remained valid. Do not promote this architecture. No numerical-reference accuracy claim is supported.
