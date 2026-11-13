# Trial 036

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=delayed_poisson_weight_curriculum.

## Parent methods and evidence

Parent Trial 030 is the best eligible score to date: L_val 0.15077613, weighted physics 0.08841202, late Poisson 0.01984955, IC L2 0.24972807. Its IC margin to threshold is only 0.00027193. Trial 029 had nearly identical low Poisson with IC L2 0.25263432, while Trial 031 increased IC pressure to widen the margin at a score cost.

## Novelty claim

Campaign mechanism: delay the full Poisson loss weight during the IC-to-physics transition, then reach the same final objective as Trial 030. This is a curriculum on PDE-component emphasis rather than a fixed coefficient change. Curriculum and loss annealing are known approaches; no publication novelty claim.

## Hypothesis and proposed change

Hypothesis: easing Poisson pressure during the early physics stage will reduce its conflict with IC fitting, widening the IC margin, while later full weight preserves Trial 030's low late Poisson. Starting from Trial 030, change Poisson coefficient from constant 5 to 2.5+2.5*min(1,(f-0.2)/0.4) for f>=0.2; all else fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+w_P(f) Poisson)+(1+29*blend)*IC relative MSE, then full blend; w_P rises linearly 2.5 at f=0.2 to 5 at f=0.6. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below Trial 030's 0.24972807, late Poisson near 0.01984955 and L_val <=0.15077613. Inspect all PDE windows, density spread, mass drift, physical checks, runtime and steps. If delayed weighting increases Poisson error or fails to widen eligibility, keep Trial 030 as leader.

## Observed results

L_val 0.16332689; weighted physics 0.10147225; IC relative L2 0.24870594 and MSE 0.06185464, eligible true. Early/middle/late physics totals 0.19628024/0.09749443/0.06593574; late Poisson 0.02998678. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97218609, mass drift -0.02781391, density std 0.59456211, p99 3.06943464. 664325 parameters, 24047 steps, 748.0966 training seconds.

## Decision and interpretation

The delayed Poisson emphasis improved IC L2 from Trial 030's 0.24972807 to 0.24870594, modestly widening eligibility. It also raised late Poisson from 0.01984955 to 0.02998678, weighted physics from 0.08841 to 0.10147, and L_val from 0.15078 to 0.16333. The joint improvement hypothesis is rejected. Trial 030 remains best by eligible score; retain Trial 036 only as an eligible comparison.
