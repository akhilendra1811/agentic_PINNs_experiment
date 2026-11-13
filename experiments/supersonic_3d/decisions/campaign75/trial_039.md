# Trial 039

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=local_velocity_increment_ic_loss.

## Parent methods and evidence

Parent Trial 030 is the best eligible candidate: L_val 0.15077613, IC L2 0.24972807 and weighted physics 0.08841202. Its IC margin is narrow. It uses pointwise velocity relative MSE only; that loss does not explicitly distinguish local turbulent increments from a global offset. The development IC supplies positions and velocity targets, so local differences can be computed without external data.

## Novelty claim

New campaign mechanism: fit nearby periodic velocity increments as part of the IC objective. No earlier trial used pairwise IC structure. A web search for turbulence/structure-function PINN losses did not establish a directly comparable method; this is a heuristic test motivated by the spatial structure of turbulence, not a publication novelty claim. The search is logged in internet_use.md.

## Hypothesis and proposed change

Hypothesis: emphasizing local velocity differences will improve IC structure and cross the eligibility threshold with a wider margin while retaining Trial 030's physics score. For each IC batch, pair the first 128 points with their closest other sample under periodic distance; compute relative MSE of predicted versus target velocity increments. Replace 25% of the IC loss by this increment loss during both IC-only and physics stages; keep total nominal IC coefficient, architecture, physics loss, sampling and optimiser fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. IC objective is 0.75 pointwise relative MSE +0.25 nearest-neighbor increment relative MSE, each normalized by its corresponding target energy. First 20% uses IC objective alone. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC objective, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below Trial 030's 0.24972807 and L_val no worse than 0.15077613. Inspect whether local increment pressure changes early continuity, momentum, late Poisson, mass drift, density spread, physical checks and step throughput. If pointwise IC accuracy or physics worsens, reject the pairwise objective.

## Observed results

L_val 0.30669533; weighted physics 0.25381970; IC relative L2 0.22994703 and MSE 0.05287564, eligible true. Early/middle/late physics totals 0.59175543/0.20945538/0.14526399. Early continuity/momentum 0.33237347/0.24760825 and late Poisson 0.08263462. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.94391650, mass drift -0.05608350, density std 0.38083157, p99 2.11917901. 664325 parameters, 22590 steps, 748.0523 training seconds.

## Decision and interpretation

The local-increment term substantially improved IC L2 from Trial 030's 0.24972807 to 0.22994703, making eligibility much more robust. It also raised weighted physics from 0.08841 to 0.25382, worsened mass drift and flattened density contrast, so L_val rose to 0.30670. The joint improvement hypothesis is rejected. The strong IC response suggests a lower increment fraction may offer a better tradeoff, but Trial 039 itself is not a priority finalist.
