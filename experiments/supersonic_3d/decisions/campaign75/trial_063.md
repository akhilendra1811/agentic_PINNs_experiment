# Trial 063

Research metadata (locked on preparation): parents=trial:61; kind=refinement; mechanism_id=early_window_collocation_rebalance.

## Parent methods and evidence

Trial 061 rebalance of physics collocation (37.5/25/37.5 early/middle/late) has weighted physics 0.08840250, better than Trial 057's 0.09003139, but IC L2 0.24954768 is near the 0.25 cutoff and L_val 0.15067655 narrowly above Trial 057's 0.15052786. The parent uses final IC coefficient 33.

## Novelty claim

Refinement of early-window collocation rebalance: raise final IC coefficient from 33 to 34 to recover IC margin while keeping its physics gain. This is campaign scalar tuning of an established multi-loss PINN, not a publication novelty claim.

## Hypothesis and proposed change

Hypothesis: final IC weight 34 reduces Trial 061's IC L2 enough to lower eligible L_val below Trial 057. Starting from the exact Trial 061 candidate, change only IC coefficient 1+32*blend to 1+33*blend; architecture, collocation and Poisson ramp remain fixed.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial Fourier harmonics, 664325 parameters, positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+33*b(f))*IC relative MSE, with b full by f=0.40 and b_P full by f=0.25. Physics batch 1024 split 384 early/256 middle/384 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect IC L2 below 0.24954768, weighted physics near 0.08840250, and eligible L_val below 0.15052786. Check each window's residual, late Poisson, density mass drift and contrast, physical checks, steps and wall time. A worse eligible score rejects the refinement even if IC improves alone.

## Observed results

L_val 0.16983133; weighted physics 0.10783663; IC relative L2 0.24898735 and MSE 0.06199470, eligible true. Early/middle/late physics totals 0.13325748/0.10351687/0.10026015; late Poisson 0.04844668. Physical checks passed, rho0 error 0, periodic error 2.86e-6. At t=0.8 mean density 0.97445285, mass drift -0.02554715, density std 0.59661680, p99 3.06045651. 664325 parameters, 23351 steps, 748.0578 training seconds.

## Decision and interpretation

Raising final IC weight from 33 to 34 modestly improves IC L2 from Trial 061's 0.24954768 to 0.24898735, but weighted physics worsens from 0.08840250 to 0.10783663 and L_val rises from 0.15067655 to 0.16983133. Late Poisson is the largest deterioration. The IC prediction held; the score prediction failed. Reject this refinement as a leader and retain the measured tradeoff.
