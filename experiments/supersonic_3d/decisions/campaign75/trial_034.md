# Trial 034

Research metadata (locked on preparation): parents=trial:31; kind=mechanism; mechanism_id=stochastic_mass_conservation_penalty.

## Parent methods and evidence

Parent Trial 031 is eligible with IC L2 0.24664535, L_val 0.16011182 and weighted physics 0.09927789. Its mean density at t=0.8 is 0.97285688, a relative mass drift of -0.02714312 on the diagnostic grid. The periodic Euler continuity equation should conserve total mass; the stochastic pointwise residual need not fully enforce that integral at finite training budget.

## Novelty claim

New campaign mechanism: add a stochastic global mass penalty at several fixed times while retaining the canonical pointwise Euler-Poisson residual. No earlier trial explicitly constrained the spatial density mean. Conservation penalties are known physics-informed training tools; this is not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: penalizing departures of mean density from rho0 at t=0.2,0.5,0.8 will reduce mass drift and improve continuity consistency without losing IC eligibility. Starting from Trial 031, keep the model and all other training terms fixed. At each physics step, reuse 512 fresh spatial points to estimate mean density at those times, and add 20*blend times the average squared relative mass error.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+31*blend)*IC relative MSE+20*blend*mean_{t in {.2,.5,.8}}(mean_x rho(x,t)/rho0-1)^2, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Mass estimates reuse 512 spatial points. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect t=0.8 mass drift magnitude below 0.02714312, weighted physics <=0.09927789, IC L2 <=0.25 and L_val <=0.16011182. Check all time-window residuals and density diagnostics, including p99 and spread, to detect an overly flat density solution. If mass improves but the locked score worsens materially, treat the penalty as a physical diagnostic tradeoff rather than a better candidate.

## Observed results

L_val 0.16893565; weighted physics 0.10612698; IC relative L2 0.25061658 and MSE 0.06280867, eligible false. Early/middle/late physics totals 0.20669068/0.09927629/0.07001192. Physical checks passed, rho0 error 0, periodic error 2.86e-6. Mean density at t=0.8 improved to 0.99028957, mass drift -0.00971043; density std 0.59115458 and p99 3.05533242. 664325 parameters, 23509 steps, 748.0245 training seconds.

## Decision and interpretation

The penalty reduced t=0.8 mass drift magnitude from Trial 031's 0.02714312 to 0.00971043, showing the stochastic integral constraint has the intended physical effect. However weighted physics worsened from 0.09928 to 0.10613, L_val from 0.16011 to 0.16894, and IC L2 from 0.24665 to 0.25062, losing eligibility. The hypothesis of simultaneous score and conservation improvement is rejected. Preserve the mass result as a possible later ingredient, but do not promote this trial.
