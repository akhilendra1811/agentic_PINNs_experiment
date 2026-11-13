# Trial 001

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=multiscale_periodic_encoding.

## Parent methods and evidence

Parent B alone. At 750 s, B had IC relative L2 0.2862 (ineligible), early/middle/late physics 0.07511/0.03291/0.04104 and L_val 0.12733. The velocity IC fit may be limited by the three-harmonic coordinate encoding.

## Novelty claim

First numbered campaign trial; no prior mechanism trial. Expand the periodic spatial encoding from three to eight harmonics on each axis. This is a multiscale representation mechanism, adapted from Fourier-feature PINN literature, not a global originality claim. Baselines both used three harmonics.

## Hypothesis and proposed change

Hypothesis: higher periodic harmonics allow better initial turbulent velocity fitting, reducing IC L2 enough to offset any higher-frequency PDE derivative cost. Change only the input layer dimension from 19 to 49 and the feature loop from k=1..3 to k=1..8 in candidate.py.

## Training objective and setup

Retain B ResPINN width 256, ten residual sine blocks, alpha 0.5, rho=exp(t*raw_rho), and fresh weights. Loss = 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and sampled IC batches of 1024. Adam warmup 1e-4 to 1e-3 over 5% time then cosine to 1e-5, gradient clip 0.5. Locked budget 750 s, parameter cap 750000.

## Expected outcome

Expect IC relative L2 below B 0.2862, ideally <=0.25, and lower total L_val than 0.12733. Monitor early continuity and momentum for degradation from stronger derivatives; positive density, periodicity and mass drift should remain valid.

## Observed results

L_val 0.14317630, weighted physics 0.05603784, IC relative L2 0.29519224 (ineligible); early/middle/late physics 0.08592707/0.03930101/0.05412425. Early continuity/momentum/Poisson 0.03169713/0.04044319/0.01378674; middle 0.01105357/0.01860858/0.00963886; late 0.01390968/0.01946729/0.02074728. Positivity and periodicity checks passed, rho0 error 0. At t=0.8 mean rho 0.98331088, mass drift -0.01668912, density std 0.63329160, p99 3.25474072. 672005 parameters; 4682 steps and 748.109 s training. Recorded loss 2.4551 at 187.6 s, 1.9342 at 375.1 s, 1.6861 at 562.6 s, 1.6851 at 748.1 s.

## Decision and interpretation

Hypothesis not supported at the matched budget: IC L2 worsened versus B (0.29519 vs 0.28622), as did L_val (0.14318 vs 0.12733) and every temporal physics total. The larger encoding reduced completed steps (4682 vs 6852), a plausible compute/optimisation cost, but this single run cannot isolate representation from optimiser effects. Do not retain as a leading parent. Explore a different mechanism, such as IC-prioritised training or causal sampling. Reference-free diagnostics cannot establish reference trajectory accuracy.
