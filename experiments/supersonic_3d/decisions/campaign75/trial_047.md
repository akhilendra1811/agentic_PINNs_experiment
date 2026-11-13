# Trial 047

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=antithetic_periodic_collocation.

## Parent methods and evidence

Parent Trial 030 remains the best eligible candidate: L_val 0.15077613, weighted physics 0.08841202, IC L2 0.24972807. It selects independent fresh physics points in a 25/25/50 early/middle/late mix. At finite batch size, random spatial and temporal coverage may fluctuate even with fixed window counts.

## Novelty claim

New campaign mechanism: antithetic periodic collocation within each time window. A sampled point (x,y,z,t) is paired with (L-x,L-y,L-z,t_min+t_max-t) in the same window. This is a sampling variance hypothesis, not a claim that the physical solution is reflection symmetric. Antithetic sampling is a known numerical idea; its use here is campaign-specific.

## Hypothesis and proposed change

Hypothesis: mirrored pairs improve coverage and reduce stochastic physics-gradient variance, lowering validation physics and L_val without changing IC fit. Starting from Trial 030, select half as many independent physics points per time window (128 early,128 middle,256 late), create one reflected partner for each, and evaluate the same 1024-point physics loss. Keep all other settings fixed.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 consists of 512 fresh selected points and their periodic/window-reflected partners, preserving 256 early/256 middle/512 late counts; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect weighted physics <0.08841202, IC L2 <=0.25 and L_val <0.15077613. Inspect all temporal residuals, late Poisson, mass drift, density spread, physical checks, steps and runtime. If paired sampling correlates gradients unhelpfully or loses eligibility, reject it.

## Observed results

L_val 0.15238619; weighted physics 0.08975301; IC relative L2 0.25026622 and MSE 0.06263318, eligible false. Early/middle/late physics totals 0.18395449/0.08548996/0.05463024; late Poisson 0.01986328. Physical checks passed, rho0 error 0, periodic error 2.58e-6. At t=0.8 mean density 0.97593606, mass drift -0.02406394, density std 0.63496739, p99 3.25735402. 664325 parameters, 24070 steps, 748.0995 training seconds.

## Decision and interpretation

Antithetic sampling produced physics very close to Trial 030 but slightly worse (weighted 0.08975 versus 0.08841), and IC L2 rose from 0.24973 to 0.25027, losing eligibility. The reflected pairing did not improve the locked score in this run. Reject as a finalist; preserve the negative result.
