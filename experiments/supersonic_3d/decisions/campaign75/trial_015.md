# Trial 015

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=adaptive_pde_component_balance.

## Parent methods and evidence

Parent B alone. B weighted physics 0.04541517, IC L2 0.28621542 and L_val 0.12733444. Early continuity 0.02862355, early momentum 0.03469443, early Poisson 0.01179440 show differing component scales. Trial 009 fed back IC error and modestly improved IC but worsened physics; no numbered trial has balanced PDE components dynamically.

## Novelty claim

Distinct campaign mechanism: clipped inverse-EMA balancing of continuity, mean momentum and Poisson losses. This is related to published PINN loss-balancing and NTK gradient-pathology work, including Wang, Yu and Perdikaris (https://www.sciencedirect.com/science/article/pii/S002199912100663X), but uses loss magnitudes rather than their NTK or gradient algorithm. It differs from Trial 009 because IC weight stays fixed. No global novelty or paper-reproduction claim.

## Hypothesis and proposed change

Hypothesis: reducing domination by the largest raw PDE component lets weaker physics terms converge without sacrificing IC fit. Maintain 0.99 EMA of each current PDE loss; compute their geometric mean g; multiply B weights 3.5, 7.5, 2.5 by clip(g/EMA_i, 0.5, 2). Keep IC weight 16 and B architecture, sampling, optimiser.

## Training objective and setup

Exact B ResPINN 664325 parameters, fresh weights. Loss = 3.5*s_cont*continuity + 7.5*s_mom*mean momentum + 2.5*s_poi*Poisson + 16 IC relative MSE, where s_i is inverse-EMA ratio clipped to [0.5,2]. Fresh PDE/IC batches 1024. Adam warmup 1e-4 to 1e-3 over first 5% of 750 s then cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Expect one or more weak PDE components, particularly Poisson, to improve enough for weighted physics below B 0.04541517 and L_val below 0.12733444; IC L2 should remain <=0.28621542. Inspect all temporal component losses, density spread, mass drift, positivity, periodicity, steps and actual time. If balancing worsens the weighted score or IC eligibility, reject this controller.

## Observed results

L_val 0.13912567; weighted physics 0.06470300; IC relative L2 0.27280518 (ineligible). Early/middle/late totals 0.12426255/0.05027583/0.04953548. Early continuity/momentum/Poisson 0.04484687/0.07482824/0.00458743; middle 0.01296292/0.03442232/0.00289058; late 0.01467757/0.03047527/0.00438264. Physical checks passed, rho0 error 0, periodic max error 4.29e-6. At t=0.8 mean rho 0.98836738, mass drift -0.01163262, density std 0.67226768, p99 3.48705077. 664325 parameters, 6592 steps, 748.058 s. Recorded training loss 2.0935 at 187.6 s to 1.4414 at 748.1 s.

## Decision and interpretation

The controller shifted emphasis as intended but did not improve the aggregate objective. Compared with B, early Poisson fell 0.01179 to 0.00459 and late Poisson 0.01179 to 0.00438, yet early momentum rose 0.03469 to 0.07483 and continuity rose 0.02862 to 0.04485. Weighted physics increased 0.04542 to 0.06470 and L_val 0.12733 to 0.13913. IC L2 improved to 0.27281 but remains ineligible. This inverse-loss rule likely overemphasized the initially smaller Poisson term; that is an interpretation, as weight trajectories were not logged. Do not promote as-is. No reference-solution accuracy claim follows.
