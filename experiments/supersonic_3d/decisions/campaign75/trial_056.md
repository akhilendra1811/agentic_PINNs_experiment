# Trial 056

Research metadata (locked on preparation): parents=trial:30; kind=mechanism; mechanism_id=higher_frequency_sine_blocks.

## Parent methods and evidence

Parent Trial 030 is the best eligible candidate: L_val 0.15077613, weighted physics 0.08841202, IC L2 0.24972807. Its B ResPINN has ten residual blocks with sine activation sin(W h+b), which provides periodic nonlinear features but may limit internal frequency under a fixed 750-second budget.

## Novelty claim

New campaign mechanism: increase hidden residual-block sine argument frequency to 1.5 while retaining the input sine and network size. This is inspired by periodic-activation implicit networks; the SIREN primary source is logged in internet_use.md. It is not a reproduction of SIREN initialization and not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: moderately faster hidden sine oscillations will improve turbulent IC and evolution representation without the compute penalty of extra Fourier input channels. Starting from Trial 030, change only h +=0.5*sin(layer(h)) to h +=0.5*sin(1.5*layer(h)) in each residual block; keep Xavier initialization and all training settings fixed.

## Training objective and setup

ResPINN width 256, ten residual blocks with 1.5-scaled sine arguments, three spatial Fourier harmonics, 664325 parameters. Positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+29*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 below Trial 030's 0.24972807, weighted physics <=0.08841202 and eligible L_val <0.15077613. Inspect time-window residuals, late Poisson, mass drift, density contrast, physical checks, steps and runtime. If higher derivatives destabilize physics or slow throughput, reject the change.

## Observed results

L_val 0.15705195; weighted physics 0.09565500; IC relative L2 0.24778408 and MSE 0.06139695, eligible true. Early/middle/late physics totals 0.18520373/0.09244856/0.06175938; late Poisson 0.02713487. Physical checks passed, rho0 error 0, periodic error 3.81e-6. At t=0.8 mean density 0.97419119, mass drift -0.02580881, density std 0.61158639, p99 3.14009476. 664325 parameters, 22808 steps, 748.0464 training seconds.

## Decision and interpretation

The 1.5 hidden sine frequency improved IC L2 from Trial 030's 0.24972807 to 0.24778408, but raised weighted physics from 0.08841 to 0.09566 and L_val from 0.15078 to 0.15705. The result is eligible but not a new leader. The representation might combine with a stronger Poisson curriculum, but this trial alone does not support a joint improvement claim.
