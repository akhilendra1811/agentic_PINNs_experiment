# Trial 069

Research metadata (locked on preparation): parents=trial:62,trial:66; kind=mechanism; mechanism_id=poisson_early_strata_integration.

## Parent methods and evidence

Trial 066 is the current best eligible candidate (L_val 0.14634504, physics 0.08557238, IC L2 0.24652110), with Poisson weight 6 and 25/25/50 early/middle/late collocation. Trial 062 changed its predecessor's time split to 31.25/25/43.75, lowering early residual but yielding a weaker score. This trial combines Trial 066's stronger Poisson coupling with the intermediate time allocation.

## Novelty claim

New campaign integration of stronger-Poisson training with moderate early-window collocation rebalancing. Both components have been tested separately; their interaction has not. Equation weighting and time stratification are known techniques; no publication novelty is claimed.

## Hypothesis and proposed change

Hypothesis: Poisson weight 6 protects the late window while the 31.25/25/43.75 split reduces early residual, yielding eligible score below Trial 066. Starting from Trial 066, change only the physics point quotas and availability checks to 5n/16 early, n/4 middle, 7n/16 late.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+6*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 320 early/256 middle/448 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect early physics below Trial 066's 0.18880641, late Poisson near 0.01017608, IC L2 <=0.25 and L_val <0.14634504. Inspect all residual windows, mass drift, density spread, physical checks, steps and runtime. A score increase or eligibility loss rejects the integration.

## Observed results

L_val 0.14105955; weighted physics 0.07881428; IC relative L2 0.24949001 and MSE 0.06224526, eligible true with a narrow 0.00050999 margin. Early/middle/late physics totals 0.14354923/0.07937580/0.05258339; late Poisson 0.01053077. Physical checks passed, rho0 error 0, periodic error 1.71e-6. At t=0.8 mean density 0.97827423, mass drift -0.02172577, density std 0.66430610, p99 3.43837547. 664325 parameters, 21179 steps, 748.0706 training seconds.

## Decision and interpretation

The integration reduced early physics from Trial 066's 0.18880641 to 0.14354923 and weighted physics from 0.08557238 to 0.07881428. Late Poisson stayed near the parent (0.01053077 versus 0.01017608), though the late total worsened (0.05258339 versus 0.04539964). IC L2 rose from 0.24652110 to 0.24949001 but remained strictly eligible. L_val 0.14105955 is a new eligible leader, 0.00528549 below Trial 066. Retain for finalist consideration; the very narrow IC margin makes matched-time stability especially important. This reference-free score does not establish numerical-solution accuracy.
