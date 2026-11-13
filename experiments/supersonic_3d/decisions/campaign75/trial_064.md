# Trial 064

Research metadata (locked on preparation): parents=trial:57; kind=mechanism; mechanism_id=momentum_focused_balanced_curriculum.

## Parent methods and evidence

Parent Trial 057 is best eligible at L_val 0.15052786, weighted physics 0.09003139 and IC L2 0.24596031. Its early momentum residual 0.08448228 dominates the early continuity 0.09402261 and Poisson 0.01409080 in raw magnitude, and the late momentum 0.02077646 remains material. The parent training uses momentum coefficient 7.5.

## Novelty claim

Campaign mechanism: focus the accelerated-Poisson, high-sine curriculum more strongly on the momentum equation. Prior trials balanced PDE components in other methods, but this targeted fixed momentum increase on Trial 057 has not been tested. Equation weighting is known PINN practice; no publication novelty is claimed.

## Hypothesis and proposed change

Hypothesis: raising momentum loss coefficient from 7.5 to 9.0 lowers the validation momentum residual enough to improve eligible L_val without losing the IC margin. Starting from Trial 057, change only the momentum coefficient in the physics loss; collocation and architecture remain fixed.

## Training objective and setup

Trial 057 ResPINN: width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+9.0 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, with b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect validation momentum below Trial 057 in early and late windows, IC L2 <=0.25 and L_val <0.15052786. Examine continuity and Poisson tradeoffs, density mass drift and contrast, physical checks, steps and runtime. Any eligibility loss or higher score rejects the mechanism as a leader.

## Observed results

L_val 0.15166525; weighted physics 0.08957064; IC relative L2 0.24918790 and MSE 0.06209461, eligible true. Early/middle/late physics totals 0.18075468/0.08707480/0.05459454; momentum residuals 0.06861856/0.03787967/0.01740990; late Poisson 0.02138926. Physical checks passed, rho0 error 0, periodic error 3.34e-6. At t=0.8 mean density 0.97455466, mass drift -0.02544534, density std 0.63498574, p99 3.27652359. 664325 parameters, 23173 steps, 748.0386 training seconds.

## Decision and interpretation

Momentum residual improved against Trial 057 in all three windows (early 0.08448228 to 0.06861856, middle 0.04575405 to 0.03787967, late 0.02077646 to 0.01740990), and weighted physics fell slightly from 0.09003139 to 0.08957064. IC L2 worsened from 0.24596031 to 0.24918790; L_val rose from 0.15052786 to 0.15166525. The momentum prediction held but the eligible-score prediction failed. Retain as evidence for possible IC rebalancing, not as a leader.
