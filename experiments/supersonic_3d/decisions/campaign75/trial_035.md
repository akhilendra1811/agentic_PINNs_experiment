# Trial 035

Research metadata (locked on preparation): parents=trial:31,trial:34; kind=mechanism; mechanism_id=control_volume_continuity_balance.

## Parent methods and evidence

Parents Trial 031 and Trial 034. Trial 031 is eligible (IC L2 0.24664535, L_val 0.16011182) but has t=0.8 mass drift -0.02714312. Trial 034 added a global mass-mean penalty, reducing drift to -0.00971043 but worsening L_val to 0.16893565 and losing IC eligibility at 0.25061658. This trial tests a local conservative continuity balance rather than a global mean constraint.

## Novelty claim

New campaign mechanism: auxiliary coarse control-volume mass balance based on density time differences and flux differences across cell faces. The locked pointwise Euler-Poisson residual and validation remain unchanged. This is motivated by weak/control-volume PINN literature, including the primary sources logged in internet_use.md, but is an adaptation to this benchmark rather than a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: a coarse conservative continuity objective will improve mass behavior and reduce early continuity error without the IC tradeoff seen with the global mean penalty. Starting from Trial 031, evaluate 64 fresh cell centers per physics step at t±0.05 and spatial face positions ±0.20, calculate the centered density time difference plus face mass-flux differences, and add 3.5*blend times its squared mean to the existing loss.

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From 20% to 40%, blend rises linearly; loss is blend*(3.5 pointwise continuity+7.5 momentum+5.0 Poisson+3.5 coarse mass balance)+(1+31*blend)*IC relative MSE, then full blend. Coarse mass balance uses 64 centers and eight model evaluations per center in one batch; center times lie in [0.05,0.75]. Pointwise physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect t=0.8 mass drift magnitude below Trial 031's 0.02714312, early continuity below 0.09544032, IC L2 <=0.25 and L_val <=0.16011182. Inspect all PDE windows, density spread, positivity, periodicity, runtime and steps. If the auxiliary conservative loss raises the locked score or loses eligibility, reject it as a candidate despite any local conservation improvement.

## Observed results

L_val 0.16806624; weighted physics 0.09892041; IC relative L2 0.26295593 and MSE 0.06914582, eligible false. Early/middle/late physics totals 0.17454186/0.07760538/0.08146085. Early continuity 0.06346171, middle continuity 0.01549425, late continuity 0.01125006. Late Poisson 0.04649445. Physical checks passed, rho0 error 0, periodic error 2.15e-6. At t=0.8 mean density 0.98068684, mass drift -0.01931316, density std 0.59375983, p99 3.02943611. 664325 parameters, 23877 steps, 748.0288 training seconds.

## Decision and interpretation

The auxiliary coarse balance reduced Trial 031's early continuity from 0.09544032 to 0.06346171 and t=0.8 mass drift magnitude from 0.02714312 to 0.01931316. Overall weighted physics remained similar (0.09928 to 0.09892), but IC L2 rose from 0.24665 to 0.26296, losing eligibility and increasing L_val from 0.16011 to 0.16807. The local conservation effect is real in these diagnostics, but the candidate fails the main hypothesis. Do not promote it; a future test would need to protect IC accuracy while using weak-form training.
