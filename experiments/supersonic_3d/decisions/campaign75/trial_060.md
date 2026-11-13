# Trial 060

Research metadata (locked on preparation): parents=trial:57; kind=refinement; mechanism_id=high_sine_accelerated_poisson_integration.

## Parent methods and evidence

Trial 057 is the best eligible 750-second candidate: L_val 0.15052786, weighted physics 0.09003139, IC L2 0.24596031. Its final IC loss coefficient is 33, leaving about 0.00404 IC L2 margin below the 0.25 eligibility limit. Trial 050 needed 33 with unscaled sine blocks, but the improved IC fit of Trial 057 may allow a smaller coefficient.

## Novelty claim

Refinement of the Trial 057 combined mechanism: lower final IC coefficient from 33 to 32 while keeping the 1.5 hidden sine and accelerated Poisson schedule. This is campaign scalar optimization, not a new mechanism or publication novelty.

## Hypothesis and proposed change

Hypothesis: Trial 057's wider IC margin permits final IC weight 32, freeing optimization capacity for physics and lowering eligible L_val. Starting from Trial 057, change only 1+32*blend to 1+31*blend in the IC loss coefficient.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial Fourier harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. Afterward loss b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+31*b(f))*IC relative MSE, with b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, gradient clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25, weighted physics <0.09003139 and L_val <0.15052786. Examine temporal residual components, late Poisson, density mass drift and contrast, physical checks, steps, and runtime. Loss of IC eligibility or score gain below the margin will reject the hypothesis.

## Observed results

L_val 0.15613592; weighted physics 0.09538102; IC relative L2 0.24648508 and MSE 0.06075490, eligible true. Early/middle/late physics totals 0.19126542/0.09150557/0.05935253; late Poisson 0.02198308. Physical checks passed, rho0 error 0, periodic error 2.38e-6. At t=0.8 mean density 0.97741872, mass drift -0.02258128, density std 0.62665504, p99 3.22854590. 664325 parameters, 22753 steps, 748.0685 training seconds.

## Decision and interpretation

Reducing final IC weight from 33 to 32 retained eligibility but did not improve physics: weighted physics rose from Trial 057's 0.09003139 to 0.09538102, and L_val rose from 0.15052786 to 0.15613592. IC L2 also rose slightly from 0.24596031 to 0.24648508. Reject this scalar refinement as a leader. The result shows that freeing nominal IC weight did not reliably improve the coupled optimization at this budget.
