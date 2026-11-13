# Trial 010

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=oblique_periodic_modes.

## Parent methods and evidence

Parent B alone. B IC L2 0.28621542 and L_val 0.12733444. Trial 001 added axis-aligned harmonics up to eight and worsened IC L2 to 0.29519224 and L_val to 0.14317630. That result discourages merely higher frequency on each coordinate, but does not test mixed spatial directions. Trial 003 has best IC L2 0.27059138; Trial 008 best L_val 0.12092633, both ineligible.

## Novelty claim

Distinct campaign mechanism: oblique periodic Fourier modes coupling coordinate pairs. Trial 001 added univariate high harmonics, whereas this trial adds sin/cos of k(x_i±x_j) for pairs xy, yz and zx at k=1,2. This is motivated by the Fourier-feature approach to multiscale PINNs in Wang, Wang and Perdikaris (https://arxiv.org/abs/2012.10047), but the exact selected oblique modes are a campaign design, not a claimed paper reproduction or global novelty.

## Hypothesis and proposed change

Hypothesis: directly supplying low-order oblique modes makes non-axis-aligned turbulent velocity structures easier to fit than increasing only axis harmonics. Retain B three-axis harmonics and add 24 pairwise sin/cos features: for 3 coordinate pairs, k=1,2, signs ±, and sine/cosine. Increase input layer 19 to 43; all else remains B.

## Training objective and setup

B ResPINN width 256, ten residual sine blocks, alpha 0.5, density exp(t*raw_rho), plus oblique periodic features; fresh weights and <=750000 parameters. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and IC batches 1024. Adam warmup 1e-4 to 1e-3 for 5% of 750 s then cosine to 1e-5; gradient clipping 0.5. Locked validation.

## Expected outcome

Expect IC L2 below B 0.28621542 and Trial 001 0.29519224; eligibility target <=0.25. Compare L_val to B 0.12733444 and each physics window. Oblique derivatives could increase PDE cost or residual; inspect steps, density spread, mass drift, physical checks and parameter count. If representation fails to improve IC, do not promote.

## Observed results

L_val 0.12919127; weighted physics 0.04673262; IC relative L2 0.28715613 (ineligible). Early/middle/late totals 0.07557789/0.03447187/0.04255096. Early continuity/momentum/Poisson 0.02851974/0.03556454/0.01149360; middle 0.00940283/0.01701810/0.00805094; late 0.01225421/0.01754866/0.01274809. Physical checks passed, rho0 error 0, periodic max error 2.38e-6. At t=0.8 mean rho 0.98758107, mass drift -0.01241893, density std 0.66945219, p99 3.45362139. 670469 parameters, 5520 steps, 748.127 s. Recorded training loss 2.2140 at 187.6 s and 1.5053 at 748.1 s.

## Decision and interpretation

Hypothesis not supported: IC L2 0.28716 is slightly worse than B 0.28622, and L_val 0.12919 exceeds B 0.12733. Weighted physics also slightly worsened 0.04673 versus 0.04542. All temporal totals are similar but no meaningful benefit appears at this budget. The feature set remained periodic and physically valid; the negative result does not exclude other mixed-frequency schemes. Do not promote. No numerical-reference accuracy claim follows.
