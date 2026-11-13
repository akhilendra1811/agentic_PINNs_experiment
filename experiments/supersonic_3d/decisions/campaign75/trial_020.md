# Trial 020

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=pcgrad_ic_physics.

## Parent methods and evidence

Parent B alone to isolate optimisation geometry. B L_val 0.12733444, weighted physics 0.04541517, IC L2 0.28621542 (ineligible). Trials 017–019 varied IC pressure: IC L2 improved from 0.26769 to 0.24650, but weighted physics increased from 0.05711 to 0.15020. This steep tradeoff motivates testing whether PDE and IC gradients conflict, rather than changing weights again.

## Novelty claim

Distinct campaign mechanism: PCGrad-style projection between the weighted PDE task and weighted IC task. Yu et al., “Gradient Surgery for Multi-Task Learning” (https://papers.neurips.cc/paper_files/paper/2020/file/3fe78a8acf5fda99de95303940a2420c-Paper.pdf) proposes projecting conflicting task gradients. Here the two tasks are B physics and IC. This is an adaptation to the fixed PINN, not a claim of exact paper reproduction or global novelty. No previous campaign trial projected gradients.

## Hypothesis and proposed change

Hypothesis: when PDE and IC gradients oppose, symmetric projection reduces destructive interference and improves IC/physics balance. On each B batch, calculate separate parameter gradients g_p of 3.5 continuity+7.5 momentum+2.5 Poisson and g_i of 16 IC relative MSE. If dot(g_p,g_i)<0, use g_p+g_i-dot/norm_i*g_i-dot/norm_p*g_p; otherwise use their sum. Retain B model and sample distribution.

## Training objective and setup

Exact B ResPINN 664325 parameters, fresh weights. B task losses as above, separate gradients, symmetric conflict projection only for negative dot product, then total gradient clipping at 0.5. Fresh PDE and IC batches 1024. Adam warmup 1e-4 to 1e-3 over first 5% of 750 s, cosine to 1e-5. Extra gradient computations count within the locked budget; locked validation remains unchanged.

## Expected outcome

Expect lower IC L2 than B 0.28621542 with weighted physics no worse than 0.04541517, or a better L_val than 0.12733444; eligibility target <=0.25. The extra backward pass may reduce steps, so inspect steps/time. Check all PDE temporal terms, mass drift, density spread, positivity and periodicity. If both tasks worsen, reject this projection design.

## Observed results

L_val 0.12734962; weighted physics 0.04496663; IC relative L2 0.28702438 (ineligible). Early/middle/late totals 0.07466194/0.03261869/0.04049727. Early continuity/momentum/Poisson 0.02848652/0.03471616/0.01145926; middle 0.00900764/0.01645607/0.00715498; late 0.01118640/0.01754064/0.01177023. Physical checks passed, rho0 error 0, periodic max error 1.97e-6. At t=0.8 mean rho 0.98740125, mass drift -0.01259875, density std 0.67008764, p99 3.48706818. 664325 parameters, 6732 steps, 748.100 s. Training loss 2.3069 at 187.6 s to 1.5492 at 748.1 s.

## Decision and interpretation

Hypothesis not supported by this outcome. Versus B, L_val is essentially unchanged (0.12734962 vs 0.12733444), IC L2 is slightly worse (0.28702 vs 0.28622), and weighted physics is only marginally lower (0.04497 vs 0.04542). The method remained computationally feasible, 6732 steps versus B 6852. Conflict frequency and gradient angles were not logged, so this trial cannot establish whether gradients rarely conflicted or the projection was simply ineffective. Do not promote this implementation. No reference-solution accuracy claim follows.
