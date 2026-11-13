# Trial 075

Research metadata (locked on preparation): parents=trial:69,trial:74; kind=refinement; mechanism_id=early_to_late_strata_curriculum.

## Parent methods and evidence

Trial 069 used constant early-emphasized sampling and reached the best eligible score L_val 0.14105955, physics 0.07881428, IC L2 0.24949001. Trial 074 shifted to late-emphasized sampling at 60% of training, widening IC margin to 0.24616922 and improving late physics, but raising L_val to 0.14672486. A later shift could preserve more of Trial 069's score gain and still recover late fit.

## Novelty claim

Refinement of the two-stage early-to-late strata curriculum: move the switch from f=0.60 to f=0.80. This is a campaign timing test of a known time-curriculum idea, not publication novelty.

## Hypothesis and proposed change

Hypothesis: retaining the early-emphasized split until 80% of training lowers early residual and eligible score versus Trial 074 while the final late phase maintains IC margin. Starting from Trial 074, change only switch condition f<0.60 to f<0.80.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, with b full at f=0.40 and b_P full at f=0.25. Physics batch 1024: 320 early/256 middle/448 late through f<0.80, then 256/256/512. IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect early physics below Trial 074's 0.17887244, IC L2 <=0.25, and eligible L_val <0.14672486; aspirational best score is <0.14105955. Inspect late physics and Poisson, mass drift, density spread, physical checks, steps and runtime. A score increase or eligibility failure rejects the later shift as leader.

## Observed results

L_val 0.15096258; weighted physics 0.08875323; IC relative L2 0.24941802 and MSE 0.06220935, eligible true with narrow margin. Early/middle/late physics totals 0.17228838/0.09069929/0.05417153; late Poisson 0.01589144. Physical checks passed, rho0 error 0, periodic error 3.10e-6. At t=0.8 mean density 0.97567952, mass drift -0.02432048, density std 0.63352990, p99 3.24094105. 664325 parameters, 22222 steps, 748.0989 training seconds.

## Decision and interpretation

Moving the switch from 60% to 80% reduced early physics versus Trial 074 (0.17228838 versus 0.17887244), but late physics worsened (0.05417153 versus 0.04822985) and IC L2 worsened (0.24941802 versus 0.24616922). The eligible score 0.15096258 is worse than Trial 074's 0.14672486 and Trial 069's 0.14105955. The early prediction held; the overall score and robustness predictions failed. Reject as a leader. Trial 069 remains the best eligible 750-second score, pending matched-time finalist comparison.
