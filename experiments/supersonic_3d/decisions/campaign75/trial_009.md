# Trial 009

Research metadata (locked on preparation): parents=trial:8; kind=mechanism; mechanism_id=feedback_ic_loss_weight.

## Parent methods and evidence

Parent Trial 008, which combined anchored velocity with 20% IC-only pretraining. It reached campaign-best L_val 0.12092633 and weighted physics 0.03162275, but IC L2 0.29883704 remained ineligible. Trial 003 achieved better IC L2 0.27059138 with worse physics. This trial targets the unresolved IC/physics balance.

## Novelty claim

Distinct campaign mechanism: error-feedback IC loss weighting during joint training. Previous trials used fixed weight 16 or an IC-only stage, never a feedback controller on IC error. Inspired by adaptive PINN loss weighting literature, including McClenny and Braga-Neto (https://arxiv.org/abs/2009.04544), but this is a simple EMA controller rather than their trainable per-point attention weights. No global originality claim.

## Hypothesis and proposed change

Hypothesis: raising IC weight while its training relative MSE remains above 0.05 will reduce validation IC L2 toward eligibility while retaining Trial 008 physics advantage. Keep Trial 008 20% IC-only stage, architecture and optimiser. During the final 80%, form a 0.99-decay EMA of batch IC relative MSE and set IC weight to clip(16*EMA/0.05,16,64) each step.

## Training objective and setup

Trial 008 anchored architecture, 735752 parameters, fresh weights. First 20% of 750 s: IC relative MSE alone. Final 80%: 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + w_IC*IC relative MSE, where w_IC is feedback-clipped between 16 and 64 from EMA target 0.05. Fresh PDE and IC batches 1024. Adam warmup 1e-4 to 1e-3 over 5% time then cosine to 1e-5; clip gradient 0.5. Locked validation.

## Expected outcome

Expect IC L2 below Trial 008 0.29883704, ideally <=0.25. Compare L_val against 0.12092633 and weighted physics against 0.03162275. A larger physics residual is anticipated; it must be measured, especially late Poisson. Also check density spread, mass drift, physical checks, steps and budget. If IC remains above threshold with worse physics, reject feedback rule.

## Observed results

L_val 0.13714651; weighted physics 0.05393877; IC relative L2 0.28845751 (ineligible). Early/middle/late totals 0.08670152/0.03858645/0.05004507. Early continuity/momentum/Poisson 0.02786328/0.04587545/0.01296280; middle 0.01217572/0.01746416/0.00894657; late 0.01391349/0.01830178/0.01782979. Physical checks passed, rho0 error 0, periodic max error 4.20e-6. At t=0.8 mean rho 0.98363662, mass drift -0.01636338, density std 0.67431253, p99 3.44599915. 735752 parameters, 21005 steps, 748.158 s. Recorded training loss 4.2320 at 187.6 s, 2.8673 at 375.1 s, 2.5158 at 562.6 s and 2.4308 at 748.2 s.

## Decision and interpretation

Feedback weighting modestly improved IC L2 versus Trial 008 (0.28846 vs 0.29884) but remained ineligible. Physics weighted error worsened from 0.03162 to 0.05394, with every temporal total worse; L_val rose from 0.12093 to 0.13715. The mechanism moved the expected IC/physics tradeoff but failed to achieve a useful balance in this form. Do not promote. Batch-based EMA weight values were not separately logged, limiting insight into controller dynamics. No numerical-reference accuracy claim follows.
