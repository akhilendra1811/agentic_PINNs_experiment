# Trial 033

Research metadata (locked on preparation): parents=trial:12,trial:31; kind=mechanism; mechanism_id=temporal_fourier_stratified_ic.

## Parent methods and evidence

Parents Trial 012 and Trial 031. Trial 012 added four temporal Fourier frequencies to B and improved some middle/late physics, reaching L_val 0.12367696 but IC L2 0.28468925, ineligible. Trial 031 combines IC-first training with balanced time sampling and stronger Poisson loss, yielding eligible IC L2 0.24664535 and L_val 0.16011182. This trial combines the architecture of 012 with the training method of 031.

## Novelty claim

Campaign integration mechanism: multiscale temporal Fourier features inside a time-stratified, IC-pretrained PINN. Temporal Fourier features were tried in Trial 012, and the eligible training method in Trial 031, but not together. Fourier features are known in neural PDE modelling; no publication novelty claim is made.

## Hypothesis and proposed change

Hypothesis: temporal frequencies will improve middle/late evolution while Trial 031's IC curriculum retains eligibility. Starting from Trial 031, add sine and cosine features at temporal k=1,2,4,8 scaled by 1/sqrt(k), and increase the input layer from 19 to 27. Keep training, sampling and loss unchanged.

## Training objective and setup

ResPINN width 256, ten sine residual blocks, 666373 parameters; three periodic spatial harmonics and four temporal Fourier frequencies. Positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 continuity+7.5 momentum+5.0 Poisson)+(1+31*blend)*IC relative MSE, then full blend. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect L_val below Trial 031's 0.16011182, with IC L2 <=0.25 and middle/late physics no worse than Trial 031's 0.09615792/0.06230808. Inspect early derivatives, late Poisson, mass drift, density spread and physical checks. If time features raise derivative cost or IC error, reject the integration.

## Observed results

L_val 0.16987397; weighted physics 0.10913527; IC relative L2 0.24645221 and MSE 0.06073869, eligible true. Early/middle/late physics totals 0.20989881/0.11054216/0.06798573, all worse than Trial 031. Late Poisson 0.03322977. Physical checks passed, rho0 error 0, periodic error 3.46e-6. At t=0.8 mean density 0.97089893, mass drift -0.02910107, density std 0.58626163, p99 3.03003192. 666373 parameters, 23685 steps, 748.1095 training seconds.

## Decision and interpretation

The temporal features preserved IC eligibility and slightly improved IC L2 relative to Trial 031 (0.24665 to 0.24645), but worsened weighted physics from 0.09928 to 0.10914 and L_val from 0.16011 to 0.16987. Middle and late windows did not improve, so the integration hypothesis is rejected for this budget. Keep as an eligible negative comparison, not a priority finalist.
