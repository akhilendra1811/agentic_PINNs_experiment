# Trial 011

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=separate_physics_readout_heads.

## Parent methods and evidence

Parent B alone. B L_val 0.12733444, IC L2 0.28621542, weighted physics 0.04541517, ineligible. Trial 006 added a separate spatial velocity branch and worsened IC; Trial 007 anchored that branch and lowered physics but harmed IC. Neither tested separation only at the final mapping from shared features to the three physical fields. Trial 003 has best IC L2 0.27059138; Trial 008 best L_val 0.12092633.

## Novelty claim

Distinct campaign mechanism: field-specific readout heads from a shared residual trunk. Unlike Trial 006 spatial velocity branch, these heads all receive the same learned time-dependent trunk and use separate nonlinear mappings for density, velocity and potential. This is an independently reasoned multi-task architecture hypothesis, not a claim of global originality or a reproduction of a particular paper.

## Hypothesis and proposed change

Hypothesis: separate nonlinear heads allow the turbulent velocity IC and coupled density/potential dynamics to occupy different final feature maps, reducing output-gradient interference. Replace B single 256-to-5 output layer with rho 256-64-1, velocity 256-64-3, potential 256-64-1 SiLU heads. Retain all earlier B trunk layers and training.

## Training objective and setup

B width-256 ten sine residual block trunk, three spatial harmonics, alpha 0.5, plus three width-64 SiLU readout heads, fresh weights. Density exp(t*raw_rho), velocity and potential direct. Parameter cap <=750000. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and IC batches 1024. Adam warmup 1e-4 to 1e-3 over 5% of 750 s then cosine to 1e-5; gradient clipping 0.5. Locked evaluator.

## Expected outcome

Expect IC L2 below B 0.28621542 and total L_val below 0.12733444 without exceeding parameter cap. Check whether Poisson or continuity worsens from head separation, and inspect early/middle/late scores, mass drift, density spread, physical checks, steps and time. Eligibility needs IC L2 <=0.25.

## Observed results

L_val 0.12489542; weighted physics 0.04414146; IC relative L2 0.28417242 (ineligible). Early/middle/late totals 0.07089098/0.03356020/0.03979040. Early continuity/momentum/Poisson 0.02707315/0.03467509/0.00914273; middle 0.00981354/0.01638408/0.00736258; late 0.01174195/0.01649139/0.01155706. Physical checks passed, rho0 error 0, periodic max error 2.62e-6. At t=0.8 mean rho 0.98748529, mass drift -0.01251471, density std 0.68011445, p99 3.51433516. 712709 parameters, 5631 steps, 748.114 s. Training loss 2.1921 at 187.6 s and 1.4876 at 748.1 s.

## Decision and interpretation

Modestly supports the head-separation hypothesis: versus B, IC L2 improved 0.28622 to 0.28417, weighted physics 0.04542 to 0.04414, and L_val 0.12733 to 0.12490. However, IC remains well above 0.25, and Trial 003 achieved better IC 0.27059 while Trial 008 achieved lower L_val 0.12093. Retain as a secondary branch for potential IC-focused combinations, not a finalist yet. A single matched-time seed cannot prove the improvement is robust. No numerical-reference accuracy claim follows.
