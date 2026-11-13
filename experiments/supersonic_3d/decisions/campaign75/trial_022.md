# Trial 022

Research metadata (locked on preparation): parents=trial:3,trial:7; kind=mechanism; mechanism_id=frozen_ic_branch_evolution.

## Parent methods and evidence

Parents are Trial 003 (20% IC-only pretraining, L_val 0.12452034, IC L2 0.27059138) and Trial 007 (spatial velocity branch plus time-dependent residual, L_val 0.15390302, IC L2 0.36665267). Trial 007 trained both branches jointly, so the IC representation could move while physics gradients acted on it. This trial combines spatial decomposition with staged training and explicitly freezes the spatial branch after fitting the IC.

## Novelty claim

Campaign novelty: staged, frozen IC branch feeding a time-dependent Euler-Poisson evolution branch. A separate spatial branch was tried in Trial 007, and IC-first optimisation in Trial 003, but freezing the fitted spatial field before physics training has not been evaluated here. This is a combination of known architectural and curriculum ideas, not a claim of publication novelty.

## Hypothesis and proposed change

Hypothesis: preserving a fitted periodic initial velocity field during physics optimisation will reduce IC degradation and approach the 0.25 eligibility threshold without forcing a large IC penalty throughout training. The model returns v(x,t)=v_IC(x)+t*v_dynamic(x,t), with a four-block 128-wide sine IC branch and the B 256-wide, ten-block dynamic branch. Fit only the IC branch during the first 20% of the budget, then freeze its parameters and train only the dynamic branch with the canonical physics and IC objective.

## Training objective and setup

733192 trainable parameters at initialization; spatial inputs use three periodic sine/cosine harmonics per axis. Density is rho0*exp(clamp(t*raw_rho,-4,4)); potential is the dynamic branch output. First 20% of 750 seconds minimises IC relative MSE with Adam 1e-3 and 1024 IC samples. Remaining 80% freezes the IC branch and minimises 3.5 continuity + 7.5 momentum + 2.5 Poisson + 16 IC relative MSE, with fresh 1024 physics and 1024 IC samples, separate Adam starting 1e-3 and cosine decay to 1e-5, gradient clipping 0.5. All weights start fresh.

## Expected outcome

Expect IC L2 below Trial 003's 0.27059138 and much below Trial 007's 0.36665267, ideally <=0.25. Physics weighted should remain near Trial 003's 0.05130065 and L_val below Trial 007's 0.15390302. Check early/middle/late residuals, late Poisson, physical checks, mass drift, density spread, runtime, step count and parameter cap. If a frozen IC field prevents physics optimisation or still misses the IC threshold, reject the mechanism.

## Observed results

L_val 0.76943914; weighted physics 0.71570144; IC relative L2 0.23181394 and MSE 0.05373770, eligible true. Early/middle/late physics totals 1.69052203/0.51171242/0.44816662. Early continuity 0.96175698 and momentum 0.70995833 dominate; late Poisson 0.16025361. Physical checks passed, rho0 error 0, periodic error 4.35e-6. At t=0.8 mean density 0.81034255, mass drift -0.18965745, density std 0.45153806, p99 2.27895451. 733192 parameters, 21718 steps, 748.1318 training seconds.

## Decision and interpretation

The frozen spatial branch reached the IC threshold, substantially improving IC fit over Trials 003 and 007. The physics score and mass conservation degraded severely, especially the early continuity and momentum residuals. The hypothesis that freezing would retain acceptable evolution accuracy is rejected. This is an eligible fallback only in the formal threshold sense, not a strong finalist. A later refinement could allow controlled updates to the IC branch during physics training, but must be evaluated separately.
