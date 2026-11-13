# Trial 040

Research metadata (locked on preparation): parents=trial:39; kind=refinement; mechanism_id=local_velocity_increment_ic_loss.

## Parent methods and evidence

Parent Trial 039 replaced 25% of pointwise IC loss with nearest-neighbor periodic velocity-increment error. It improved IC L2 to 0.22994703 from Trial 030's 0.24972807 but worsened weighted physics from 0.08841202 to 0.25381970 and L_val from 0.15077613 to 0.30669533. This trial tests a smaller share of the same local structure objective.

## Novelty claim

Refinement of the local velocity-increment IC mechanism. Change the mixture fraction, not the pair construction or total IC coefficient. This is a campaign-specific loss-mixing test, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: a 5% increment share will retain enough of Trial 039's IC benefit to make eligibility less fragile, while keeping physics near Trial 030. Starting from Trial 039, change the IC mixture from 0.75 pointwise+0.25 increment to 0.95 pointwise+0.05 increment at both training stages.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. For each IC batch, pair the first 128 samples with their closest other sample under periodic distance; normalize velocity-increment MSE by target-increment energy. IC objective is 0.95 pointwise relative MSE+0.05 increment relative MSE. First 20% uses IC objective alone. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC objective, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below Trial 030's 0.24972807 and weighted physics much below Trial 039's 0.25381970, ideally <=0.10, yielding an eligible score competitive with Trial 030. Inspect all physics windows, density contrast, mass drift, physical checks, runtime and steps. If even 5% harms physics significantly, abandon this local-increment loss.

## Observed results

L_val 0.17498952; weighted physics 0.11478176; IC relative L2 0.24537270 and MSE 0.06020776, eligible true. Early/middle/late physics totals 0.23261106/0.10781806/0.07182827; late Poisson 0.03064733. Physical checks passed, rho0 error 0, periodic error 2.62e-6. At t=0.8 mean density 0.96853006, mass drift -0.03146994, density std 0.57983005, p99 2.96978450. 664325 parameters, 22538 steps, 748.0878 training seconds.

## Decision and interpretation

Reducing the increment share from 25% to 5% recovered much of the physics loss: weighted physics fell from Trial 039's 0.25382 to 0.11478, while IC L2 stayed better than Trial 030 (0.24537 versus 0.24973). L_val 0.17499 remains above Trial 030's 0.15078, so this is a robustness tradeoff, not a new best score. Retain as an eligible alternative; a further smaller fraction may be tested if it can preserve the IC benefit with less physics cost.
