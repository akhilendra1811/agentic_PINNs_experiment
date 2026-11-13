# Trial 059

Research metadata (locked on preparation): parents=trial:57; kind=refinement; mechanism_id=high_sine_accelerated_poisson_integration.

## Parent methods and evidence

Trial 057 is the best eligible candidate at L_val 0.15052786, weighted physics 0.09003139, IC L2 0.24596031, with 1.5-scaled hidden sine and accelerated Poisson curriculum. Trial 058 reduced that scale to 1.25, worsening both physics and IC. The direction above 1.5 remains untested.

## Novelty claim

Refinement of hidden sine frequency in the integrated Trial 057 mechanism: test 1.75. Periodic activation networks are established; this is campaign parameter tuning, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: a modest increase above Trial 057's scale 1.5 captures sharper spatial evolution while preserving its IC margin and lowers eligible L_val. Starting from the exact Trial 057 source, change only 0.5*sin(1.5*layer(h)) to 0.5*sin(1.75*layer(h)) in all ten hidden blocks.

## Training objective and setup

ResPINN width 256, ten 1.75-scaled sine residual blocks, three spatial Fourier harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clip norm 0.5.

## Expected outcome

Expect IC L2 below 0.25, weighted physics <=0.09003139, and L_val <0.15052786. Examine all time-window residuals, late Poisson, mass drift, density contrast, physical checks, steps and runtime. If score or eligibility worsens, reject the higher frequency.

## Observed results

L_val 0.15909936; weighted physics 0.09961074; IC relative L2 0.24390288 and MSE 0.05948861, eligible true. Early/middle/late physics totals 0.20285918/0.09673084/0.06003932; late Poisson 0.02462740. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97349322, mass drift -0.02650678, density std 0.61953378, p99 3.19010091. 664325 parameters, 22860 steps, 748.1066 training seconds.

## Decision and interpretation

The higher 1.75 sine scale improves IC L2 from Trial 057's 0.24596031 to 0.24390288, but weighted physics worsens from 0.09003139 to 0.09961074 and score rises from 0.15052786 to 0.15909936. Late Poisson especially worsens. The candidate is eligible and offers a wider IC margin, but it is not a score leader; reject the primary hypothesis for the fixed budget.
