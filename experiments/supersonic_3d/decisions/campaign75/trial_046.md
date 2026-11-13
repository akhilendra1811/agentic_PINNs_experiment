# Trial 046

Research metadata (locked on preparation): parents=trial:10,trial:30; kind=mechanism; mechanism_id=oblique_modes_stratified_ic.

## Parent methods and evidence

Parents Trial 010 and Trial 030. Trial 010 added diagonal periodic Fourier modes to the B architecture, yielding L_val 0.12919127 and IC L2 0.28715613, slightly worse than B but with different spatial representation. Trial 030 is the best eligible method, L_val 0.15077613 and IC L2 0.24972807, with axis-aligned modes only. This trial combines the oblique representation with the stronger IC and physics schedule.

## Novelty claim

Campaign integration mechanism: oblique periodic spatial modes under staged IC pretraining and balanced time-stratified collocation. Oblique modes alone were tested in Trial 010, but not with the eligible training method. Fourier features and directional modes are known tools; no publication novelty claim.

## Hypothesis and proposed change

Hypothesis: diagonal spatial modes can represent turbulent velocity structure more efficiently when paired with IC-first training, improving IC margin or physics over Trial 030. Starting from Trial 030, add sine/cosine modes for each coordinate pair, k=1,2 and both diagonal signs exactly as in Trial 010, increasing input width from 19 to 43. Keep all training settings fixed.

## Training objective and setup

ResPINN width 256, ten sine residual blocks, three axis harmonics plus 24 oblique feature channels, 670469 parameters. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below Trial 030's 0.24972807 while staying eligible, and L_val below 0.15077613 or at least better density contrast. Inspect time-window residuals, late Poisson, mass drift, density p99, physical checks, step throughput and runtime. If extra modes increase derivative cost without quality gain, reject the integration.

## Observed results

L_val 0.18966314; weighted physics 0.12753159; IC relative L2 0.24926202 and MSE 0.06213155, eligible true. Early/middle/late physics totals 0.21895677/0.12051174/0.09517343, all worse than Trial 030; late Poisson 0.05410881. Physical checks passed, rho0 error 0, periodic error 1.55e-6. At t=0.8 mean density 0.96600580, mass drift -0.03399420, density std 0.50911659, p99 2.65528846. 670469 parameters, 22340 steps, 748.1169 training seconds.

## Decision and interpretation

The extra oblique modes slightly improved IC L2 versus Trial 030 (0.24926 versus 0.24973), but worsened weighted physics from 0.08841 to 0.12753 and L_val from 0.15078 to 0.18966. The lower density p99 and standard deviation do not support better compressive structure. Reject this integration as a finalist.
