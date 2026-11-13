# Trial 058

Research metadata (locked on preparation): parents=trial:57; kind=refinement; mechanism_id=high_sine_accelerated_poisson_integration.

## Parent methods and evidence

Parent Trial 057 combined 1.5-scaled hidden sine blocks with accelerated Poisson training and became the best eligible candidate: L_val 0.15052786, weighted physics 0.09003139, IC L2 0.24596031. Its IC margin is good, but physics is slightly worse than Trial 050's 0.08964395 with unscaled sine blocks.

## Novelty claim

Refinement of Trial 057's integrated representation and curriculum. Test intermediate hidden sine frequency 1.25 between Trial 050's 1.0 and Trial 057's 1.5. This scalar interpolation is a campaign tuning test, not a new mechanism or publication novelty.

## Hypothesis and proposed change

Hypothesis: hidden sine argument scale 1.25 retains Trial 057's IC margin while reducing its physics cost. Starting from Trial 057, change only 0.5*sin(1.5*layer(h)) to 0.5*sin(1.25*layer(h)) in all ten residual blocks.

## Training objective and setup

ResPINN width 256, ten 1.25-scaled sine residual blocks, three spatial Fourier harmonics, 664325 parameters. Positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, with b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 with 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; gradient clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25, weighted physics below 0.09003139, and L_val below 0.15052786. Inspect each temporal residual, late Poisson, mass drift, density spread, physical checks, steps and wall time. A loss of eligibility or higher score rejects this interpolation.

## Observed results

L_val 0.15359408; weighted physics 0.09219490; IC relative L2 0.24778858 and MSE 0.06139918, eligible true. Early/middle/late physics totals 0.19640698/0.08952734/0.05211061; late Poisson 0.01631066. Physical checks passed, rho0 error 0, periodic error 2.74e-6. At t=0.8 mean density 0.97522187, mass drift -0.02477813, density std 0.63884121, p99 3.29738188. 664325 parameters, 22575 steps, 748.0324 training seconds.

## Decision and interpretation

Scale 1.25 is eligible, but its IC L2 rises from Trial 057's 0.24596031 to 0.24778858, weighted physics rises from 0.09003139 to 0.09219490, and L_val rises from 0.15052786 to 0.15359408. The interpolation did not improve either target; reject it as a leader while retaining the recorded result. The comparison is for this fixed training budget and seed policy.
