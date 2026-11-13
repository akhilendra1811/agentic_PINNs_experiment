# Trial 041

Research metadata (locked on preparation): parents=trial:30,trial:40; kind=refinement; mechanism_id=local_velocity_increment_ic_loss.

## Parent methods and evidence

Parents Trial 030 and Trial 040. Trial 030 has the best eligible score, L_val 0.15077613, with narrow IC L2 0.24972807. Trial 040 replaced 5% of its pointwise IC loss by local velocity-increment loss and widened IC fit to 0.24537270, but L_val rose to 0.17498952. This trial tests whether a smaller structural share improves that tradeoff.

## Novelty claim

Refinement of the local velocity-increment IC mechanism. Reduce its mixture fraction from 5% to 2% while keeping the total IC coefficient and every other method component fixed. This is a parameter refinement within a campaign mechanism, not publication novelty.

## Hypothesis and proposed change

Hypothesis: 2% local-increment loss will retain IC L2 below Trial 030's 0.24972807 while lowering weighted physics and L_val relative to Trial 040. Starting from Trial 040, change the mixture from 0.95 pointwise+0.05 increment to 0.98 pointwise+0.02 increment in both stages.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. For each IC batch, match the first 128 samples to their nearest other sample in periodic distance. IC objective is 0.98 pointwise relative MSE+0.02 relative velocity-increment MSE. First 20% IC-only; from 20% to 40%, blend 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC objective, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <0.24972807 and L_val <Trial 040's 0.17498952, ideally close to or below Trial 030's 0.15077613. Inspect each physics window, mass drift, density spread, physical checks, runtime and steps. If the small increment term gives no IC benefit or still costs too much physics, stop this refinement line.

## Observed results

L_val 0.16591852; weighted physics 0.10460245; IC relative L2 0.24762082 and MSE 0.06131607, eligible true. Early/middle/late physics totals 0.20613703/0.10030573/0.06656664; late Poisson 0.02794384. Physical checks passed, rho0 error 0, periodic error 2.03e-6. At t=0.8 mean density 0.97307158, mass drift -0.02692842, density std 0.59728277, p99 3.08163714. 664325 parameters, 22218 steps, 748.0346 training seconds.

## Decision and interpretation

The 2% increment share retained a modest IC gain over Trial 030 (0.24762 versus 0.24973) and improved L_val relative to Trial 040 (0.16592 versus 0.17499). It still worsened weighted physics and L_val versus Trial 030 (0.10460 versus 0.08841; 0.16592 versus 0.15078). This is a predictable tradeoff, not a new leader. Stop tuning this mixture for now; Trial 030 remains the best eligible score and Trial 031 offers a simpler wider-margin alternative.
