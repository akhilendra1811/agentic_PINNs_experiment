# Trial 023

Research metadata (locked on preparation): parents=trial:22; kind=refinement; mechanism_id=frozen_ic_branch_evolution.

## Parent methods and evidence

Parent Trial 022 fitted a dedicated periodic IC branch and then froze it. It achieved IC L2 0.23181394 (eligible) but L_val 0.76943914, weighted physics 0.71570144, early physics 1.69052203 and mass drift -0.18965745. The frozen field likely constrained evolution optimisation too strongly. This is a direct refinement of the same two-branch model.

## Novelty claim

Refinement of the Trial 022 mechanism: allow the fitted IC branch to adapt during physics training at one tenth the dynamic branch learning rate. This tests the stability-plasticity tradeoff of a pretrained initial-condition representation. Differential learning rates and staged fine-tuning are known techniques, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: slow IC-branch updates after pretraining can reduce the severe physics residual of Trial 022 while retaining IC L2 <=0.25. Keep the architecture, initial 20% IC fitting, physics objective, batches, and cosine schedule fixed. Replace the hard freeze with an Adam group for the IC parameters at 0.1 times the dynamic group's learning rate throughout the remaining 80%.

## Training objective and setup

Trial 022 architecture: 733192 parameters, four-block 128-wide periodic IC branch plus B ten-block 256-wide dynamic branch, v=v_IC(x)+t*v_dynamic(x,t), rho=rho0*exp(clamp(t*raw_rho,-4,4)). Train IC relative MSE alone for the first 20% of 750 seconds, Adam 1e-3. Then train 3.5 continuity + 7.5 momentum + 2.5 Poisson + 16 IC relative MSE on 1024 fresh PDE and 1024 IC points. New Adam for both parameter groups, cosine dynamic LR 1e-3 to 1e-5 and IC LR one tenth of it, gradient clipping 0.5. Fresh model weights.

## Expected outcome

Expect weighted physics well below Trial 022's 0.71570144, particularly early continuity and momentum, while IC L2 remains <=0.25. A useful result would cut L_val substantially and reduce t=0.8 mass drift magnitude below 0.18965745. Inspect all validation windows, density spread and physical checks. If physics improves only by losing IC eligibility, the refinement does not resolve the tradeoff.

## Observed results

L_val 0.18341815; weighted physics 0.09237855; IC relative L2 0.30172768 and MSE 0.09103959, eligible false. Early/middle/late physics totals 0.14599204/0.06933385/0.08475997. Early continuity/momentum 0.06223345/0.06832849; late Poisson 0.03043481. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97213995, mass drift -0.02786005, density std 0.56423444, p99 2.87906313. 733192 parameters, 22104 steps, 748.0709 training seconds.

## Decision and interpretation

Slow IC-branch adaptation substantially restored physics consistency relative to Trial 022 (weighted physics 0.71570 to 0.09238) and reduced t=0.8 mass drift magnitude from 0.18966 to 0.02786. However IC L2 increased from 0.23181 to 0.30173, losing eligibility. The hypothesised joint improvement is rejected. The two trials expose a strong stability-plasticity tradeoff; further work would need a more principled constraint or projection, rather than merely assuming a small IC learning rate preserves the fitted field.
