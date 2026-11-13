# Trial 057

Research metadata (locked on preparation): parents=trial:50,trial:56; kind=mechanism; mechanism_id=high_sine_accelerated_poisson_integration.

## Parent methods and evidence

Trial 050's accelerated Poisson curriculum is eligible with L_val 0.15160360, weighted physics 0.08964395, IC L2 0.24891695, and late Poisson 0.01416380. Trial 056's 1.5-scaled hidden sine blocks are eligible with L_val 0.15705195, physics 0.09565500, and IC L2 0.24778408. This trial combines their architecture and curriculum. Trial 030 remains the best eligible score at 0.15077613.

## Novelty claim

New campaign integration: use the higher-frequency hidden sine representation of Trial 056 with the accelerated Poisson curriculum of Trial 050. Each component has been tested separately; their interaction has not. Periodic activations are established in the literature, so this is a campaign combination, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: faster hidden sine oscillations will improve the IC margin while the early full Poisson weight counteracts Trial 056's physics penalty, yielding an eligible score below Trial 030. Starting from the exact Trial 050 candidate, change only each residual block from 0.5*sin(layer(h)) to 0.5*sin(1.5*layer(h)).

## Training objective and setup

ResPINN width 256, ten residual blocks with 1.5-scaled sine, three spatial Fourier harmonics, 664325 parameters. Positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. From f=0.20 onward loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, where b reaches 1 by f=0.40 and b_P by f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below 0.24891695, weighted physics no worse than Trial 050's 0.08964395, and eligible L_val below 0.15077613. Inspect time-window residuals, late Poisson, mass drift, density contrast, physical checks, steps, and runtime. A score increase or loss of IC eligibility rejects the combined hypothesis.

## Observed results

L_val 0.15052786; weighted physics 0.09003139; IC relative L2 0.24596031 and MSE 0.06049647, eligible true. Early/middle/late physics totals 0.19259569/0.08685857/0.05090936; late Poisson 0.01507682. Physical checks passed, rho0 error 0, periodic error 3.10e-6. At t=0.8 mean density 0.97826159, mass drift -0.02173841, density std 0.64349246, p99 3.30007291. 664325 parameters, 22602 steps, 748.0323 training seconds.

## Decision and interpretation

The combination improves IC L2 against both parents and crosses the best eligible Trial 030 score by 0.00024827. Weighted physics 0.09003139 is slightly worse than Trial 050's 0.08964395, so the component-level physics prediction failed, though the overall score and IC eligibility improved. The result is a new eligible leader by a very small margin and a finalist candidate, subject to matched-time comparison. This residual score is reference-free and does not establish numerical-solution accuracy.
