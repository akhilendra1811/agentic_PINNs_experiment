# Trial 042

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=optimizer_reset_at_physics_transition.

## Parent methods and evidence

Parent Trial 030 is the best eligible model so far: L_val 0.15077613, weighted physics 0.08841202, IC L2 0.24972807. It trains on IC alone for 20% of the budget, then ramps in PDE residuals while continuing to use Adam moments accumulated from the IC-only objective. Those moments may bias early physics updates toward the previous task.

## Novelty claim

New campaign mechanism: reset optimizer state at the IC-to-physics stage boundary while retaining learned network weights. Earlier trials changed stage duration and loss ramps, but did not isolate Adam-moment carryover. Optimizer restarts are a known technique, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: reinitializing Adam at cumulative fraction 0.20 will improve physics convergence by removing IC-only moment history without sacrificing the fitted IC field. Starting from Trial 030, create a fresh Adam optimizer once at the first physics step with the same scheduled learning rate; all model parameters, losses, data sampling and schedules remain fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5. Adam moments reset at f=0.20, with LR schedule continuing unchanged.

## Expected outcome

Expect weighted physics below Trial 030's 0.08841202 and L_val below 0.15077613 while IC L2 remains <=0.25. Inspect early and late residuals, mass drift, density spread, physical checks, steps and runtime. If reset destabilizes IC fitting or physics, reject it.

## Observed results

L_val 0.15307667; weighted physics 0.08610868; IC relative L2 0.25878173 and MSE 0.06696798, eligible false. Early/middle/late physics totals 0.17720854/0.08287667/0.05160795; late Poisson 0.01475685. Physical checks passed, rho0 error 0, periodic error 3.10e-6. At t=0.8 mean density 0.97672170, mass drift -0.02327830, density std 0.63212037, p99 3.24759245. 664325 parameters, 23945 steps, 748.0838 training seconds.

## Decision and interpretation

The optimizer reset modestly improved weighted physics from Trial 030's 0.08841 to 0.08611 and late Poisson from 0.01985 to 0.01476, but IC L2 deteriorated from 0.24973 to 0.25878. L_val also rose slightly. The hypothesis of a better eligible solution is rejected; carryover of IC moments appears useful for retaining IC fit in this schedule. Do not promote the ineligible trial.
