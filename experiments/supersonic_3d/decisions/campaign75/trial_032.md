# Trial 032

Research metadata (locked on preparation): parents=trial:31; kind=mechanism; mechanism_id=conservative_momentum_parameterization.

## Parent methods and evidence

Parent Trial 031 is an eligible balanced-time, high-Poisson-weight model: L_val 0.16011182, weighted physics 0.09927789, IC L2 0.24664535. It predicts density and velocity independently in the output head, despite the governing equations involving momentum rho*v. Trial 030 has slightly lower L_val but a narrower IC margin; Trial 031 provides more room for this representation test.

## Novelty claim

New campaign mechanism: parameterize momentum as the raw neural output and recover velocity as m/rho. No earlier campaign trial did this. Conservative variables are standard in compressible flow, so this is a campaign novelty and not a publication originality claim. The locked evaluator still computes the canonical Euler-Poisson residual from the five physical outputs.

## Hypothesis and proposed change

Hypothesis: coupling velocity to the positive density through a momentum output will reduce continuity or momentum residuals, especially later in time, while preserving initial velocity fit because rho(t=0)=1. Starting from Trial 031, keep every training setting fixed; in forward(), interpret raw channels 1:4 as momentum and return velocity=momentum/rho.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. rho=rho0*exp(clamp(t*raw_rho,-4,4)), velocity=raw_momentum/rho, phi=raw_phi. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+31*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect weighted physics below Trial 031's 0.09927789 and L_val below 0.16011182 while IC L2 stays <=0.25. Inspect each PDE component, late Poisson, positivity, periodicity, density spread and mass drift. If the coupling destabilizes derivatives or loses eligibility, reject it.

## Observed results

L_val 0.19733943; weighted physics 0.13404581; IC relative L2 0.25158224 and MSE 0.06329362, eligible false. Early/middle/late physics totals 0.26696975/0.13010374/0.08324147. Early continuity/momentum 0.14384037/0.10598644; late Poisson 0.04148918. Physical checks passed, rho0 error 0, periodic error 2.21e-6. At t=0.8 mean density 0.95867038, mass drift -0.04132962, density std 0.46933097, p99 2.41496158. 664325 parameters, 23463 steps, 748.1022 training seconds.

## Decision and interpretation

The conservative-output parameterization worsened Trial 031's weighted physics from 0.09928 to 0.13405 and IC L2 from 0.24665 to 0.25158, losing eligibility. Continuity and momentum rose especially in the early window, and density spread diminished. The proposed coupling did not improve the locked evaluator at this budget. Reject this mechanism in its tested form; no finalist promotion.
