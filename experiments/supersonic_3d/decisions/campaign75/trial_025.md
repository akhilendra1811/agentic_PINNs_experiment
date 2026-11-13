# Trial 025

Research metadata (locked on preparation): parents=trial:17,trial:18,trial:19; kind=refinement; mechanism_id=staged_ic_pretraining.

## Parent methods and evidence

Parents Trials 017, 018 and 019 use the same B architecture and smooth IC-to-physics ramp after 20% IC-only fitting, with final IC weights 16, 32 and 24 respectively. Their IC L2 values were 0.26769212, 0.24650130 and 0.25407001, while weighted physics was 0.05710781, 0.15019682 and 0.11327072. Only Trial 018 met IC eligibility, at substantial physics cost.

## Novelty claim

Refinement of the known staged IC-pretraining mechanism, not a new method. The campaign evidence suggests a threshold crossing between final IC weights 24 and 32; this tests one intermediate value without changing the training process or architecture.

## Hypothesis and proposed change

Hypothesis: a final IC coefficient of 28 will meet IC L2 <=0.25 while giving lower weighted physics and L_val than Trial 018's coefficient 32. Starting from Trial 019 source, change only the ramp endpoint from 24 to 28, i.e. loss IC coefficient from 1+23*blend to 1+27*blend.

## Training objective and setup

B ResPINN, 256 width, ten sine residual blocks, three spatial harmonics, 664325 parameters, density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh weights. First 20% of 750 seconds: IC relative MSE only. From 20% to 40%, blend rises linearly 0 to 1; loss is blend*(3.5 continuity+7.5 momentum+2.5 Poisson)+(1+27*blend)*IC relative MSE. Same formula at full blend afterward. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5, fresh batches of 1024 IC and 1024 PDE points.

## Expected outcome

Expect IC L2 <=0.25 and weighted physics <0.15019682, yielding L_val <0.21095971 relative to Trial 018. Inspect early/middle/late residuals, mass drift, density spread, physical checks, parameter count, steps and runtime. If it misses eligibility or has no physics gain, reject this refinement.

## Observed results

L_val 0.19754017; weighted physics 0.13543805; IC relative L2 0.24920297 and MSE 0.06210212, eligible true. Early/middle/late physics totals 0.17388229/0.08342687/0.15126707; late Poisson 0.10972013. Physical checks passed, rho0 error 0, periodic error 3.22e-6. At t=0.8 mean density 0.97137713, mass drift -0.02862287, density std 0.57740957, p99 2.95601916. 664325 parameters, 23399 steps, 748.0443 training seconds.

## Decision and interpretation

The intermediate IC weight achieved the predicted threshold crossing: IC L2 0.24920 versus 0.25407 at weight 24 and 0.24650 at weight 32. It also reduced weighted physics from Trial 018's 0.15020 to 0.13544 and L_val from 0.21096 to 0.19754, making it the best eligible candidate so far. The margin to IC threshold is small, and late Poisson remains high (0.10972), so the result needs matched-time finalist testing before any winner claim. Retain as a finalist candidate.
