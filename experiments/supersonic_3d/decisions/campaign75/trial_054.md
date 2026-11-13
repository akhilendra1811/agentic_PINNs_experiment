# Trial 054

Research metadata (locked on preparation): parents=trial:22; kind=refinement; mechanism_id=frozen_ic_branch_evolution.

## Parent methods and evidence

Parent Trial 022 trained a separate spatial IC branch for 20% of the budget, froze it and trained a time-dependent B-style branch. It achieved excellent IC L2 0.23181394 but poor weighted physics 0.71570144, early total 1.69052203 and t=0.8 mass drift -0.18965745. Its fixed spatial IC field contributed unchanged at all later times, potentially constraining the dynamic branch too strongly.

## Novelty claim

Refinement of the frozen-IC-branch mechanism: apply a linear temporal fade to the pretrained IC field. Trial 022 used v=v_IC+t*v_dynamic; this trial uses v=(1-t/T)*v_IC+t*v_dynamic, preserving the exact learned t=0 field but freeing later times. Temporal ansatz factors are known PINN tools, not publication novelty.

## Hypothesis and proposed change

Hypothesis: fading the fixed IC field toward zero by t=0.8 will reduce the severe physics error of Trial 022 while retaining its eligible IC fit. Starting from Trial 022 source, add tmax from the case and change only the coefficient on the frozen spatial velocity branch from 1 to 1-t/tmax. Keep model size and training stages fixed.

## Training objective and setup

733192-parameter model with four-block 128-wide periodic IC branch and ten-block 256-wide dynamic branch, v=(1-t/0.8)*v_IC(x)+t*v_dynamic(x,t), rho=rho0*exp(clamp(t*raw_rho,-4,4)). First 20% of 750 seconds: IC relative MSE only, Adam 1e-3, 1024 IC samples. Remaining 80% freezes the IC branch and minimizes 3.5 continuity+7.5 momentum+2.5 Poisson+16 IC relative MSE on fresh 1024 physics and 1024 IC samples; dynamic Adam cosine 1e-3 to 1e-5, clipping 0.5. Fresh weights.

## Expected outcome

Expect IC L2 close to Trial 022's 0.23181394 and still <=0.25, while weighted physics falls far below 0.71570144 and mass drift magnitude below 0.18965745. Inspect early/middle/late residuals, especially early continuity and momentum, density contrast, physical checks, runtime and steps. If the temporal derivative from the fade worsens early physics, reject the ansatz.

## Observed results

L_val 0.59935722; weighted physics 0.54569082; IC relative L2 0.23166010 and MSE 0.05366640, eligible true. Early/middle/late physics totals 1.52631136/0.38605634/0.24922330. Early continuity/momentum 0.75179790/0.73551434; late Poisson 0.10364807. Physical checks passed, rho0 error 0, periodic error 3.81e-6. At t=0.8 mean density 0.88281655, mass drift -0.11718345, density std 0.50891668, p99 2.60785794. 733192 parameters, 22188 steps, 748.0475 training seconds.

## Decision and interpretation

Fading the frozen IC field reduced weighted physics from Trial 022's 0.71570 to 0.54569 and mass drift magnitude from 0.18966 to 0.11718 while preserving excellent IC L2. However early physics remains 1.52631 and L_val 0.59936, far above leading eligible trials near 0.15. The temporal fade helps the frozen-branch limitation but does not solve it at this budget. Do not promote this candidate.
