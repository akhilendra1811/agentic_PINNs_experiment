# Trial 066

Research metadata (locked on preparation): parents=trial:57; kind=mechanism; mechanism_id=stronger_poisson_coupled_curriculum.

## Parent methods and evidence

Trial 057 is the best eligible candidate: L_val 0.15052786, weighted physics 0.09003139, IC L2 0.24596031. Its accelerated Poisson curriculum reaches full coefficient 5 by 25% of training and yields late Poisson residual 0.01507682. Recent equation reweighting toward momentum improved that component but hurt the overall score; Poisson reweighting on the leader remains untested.

## Novelty claim

Campaign mechanism: strengthen the accelerated Poisson loss in the high-sine coupled method from 5 to 6. Poisson equation weighting is established PINN practice, so this is a campaign-specific test, not publication novelty.

## Hypothesis and proposed change

Hypothesis: Poisson coefficient 6 lowers late Poisson and total physics enough to improve eligible L_val without eroding IC fit. Starting from Trial 057, change only the Poisson term multiplier from 5.0 to 6.0; its ramp still reaches full weight at f=0.25.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. Afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect late Poisson below 0.01507682, IC L2 <=0.25 and L_val <0.15052786. Examine all time-window residual components, density mass drift and spread, physical checks, steps and runtime. A higher eligible score rejects the approach even if late Poisson alone improves.

## Observed results

L_val 0.14634504; weighted physics 0.08557238; IC relative L2 0.24652110 and MSE 0.06077265, eligible true. Early/middle/late physics totals 0.18880641/0.08370427/0.04539964; late Poisson 0.01017608. Physical checks passed, rho0 error 0, periodic error 2.29e-6. At t=0.8 mean density 0.97970039, mass drift -0.02029961, density std 0.65685588, p99 3.36948323. 664325 parameters, 22486 steps, 748.0517 training seconds.

## Decision and interpretation

Raising Poisson weight from 5 to 6 reduced late Poisson from Trial 057's 0.01507682 to 0.01017608 and weighted physics from 0.09003139 to 0.08557238. IC L2 rose slightly from 0.24596031 to 0.24652110 but remained eligible. L_val fell from 0.15052786 to 0.14634504, a new eligible campaign leader. The hypothesis is supported for this reference-free 750-second validation; retain for finalist consideration and test nearby Poisson weights.
