# Trial 004

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=residual_adaptive_collocation.

## Parent methods and evidence

Parent B alone. B has the best weighted physics (0.04541517) but its IC L2 0.28621542 is ineligible. Trial 003 improved IC and total score with IC pretraining but worsened physics; Trials 001 and 002 worsened both. This trial isolates collocation selection using B, without importing Trial 003 pretraining.

## Novelty claim

Distinct campaign mechanism: residual-based adaptive collocation. No prior numbered trial selected domain points by current PDE residual. Inspired by Wu et al., “A comprehensive study of non-adaptive and residual-based adaptive sampling for physics-informed neural networks” (https://www.sciencedirect.com/science/article/pii/S0045782522006260). This uses the authorised context adaptive sampler, not a paper-exact RAD/RAR-D reproduction or global novelty claim.

## Hypothesis and proposed change

Hypothesis: allocating some physics updates to high-residual regions reduces validation physics loss, especially early continuity and late Poisson, without losing IC fit. Every eighth step, sample 2048 fresh candidates and choose 1024 with the context adaptive sampler (half largest residual and half random); all other steps use uniform fresh sampling. Change only sampling in B trainer.

## Training objective and setup

Exact B ResPINN architecture, width 256, ten sine residual blocks, three periodic harmonics, 664325 parameters, fresh weights. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. PDE and IC training batch 1024; adaptive PDE sample every eighth step with multiplier 2 and otherwise fresh uniform. Adam 1e-4 to 1e-3 warmup over first 5% of 750 s then cosine to 1e-5, clipping 0.5. Adaptive probes are included in training time.

## Expected outcome

Expect weighted physics below B 0.04541517 and no material increase in IC L2 above 0.28621542. Inspect early/middle/late totals, especially B early 0.07511238 and late Poisson 0.01178799. Adaptive probe overhead may reduce training steps; record steps, time, mass drift, density spread, positivity and periodicity. Eligibility requires IC L2 <=0.25.

## Observed results

No validation metrics, training history, or completed step count were produced. The worker remained CPU-active for approximately 49 minutes after start, far beyond the locked 750-second limit, without returning from training. It was terminated with SIGTERM at 2026-11-05 19:01:46 UTC; runner status is failed with return code -15. Therefore L_val, PDE residuals, IC L2, density diagnostics and eligibility are unavailable. The declared B architecture has 664325 parameters, but no completed evaluator parameter report was produced.

## Decision and interpretation

This attempt counts as a failed numbered trial. It provides no evidence that adaptive collocation improves the solution. The authorised residual-probe path appears computationally impractical in this exact configuration; the worker did not complete within the training budget. The cause of the excessive runtime is not fully established from the available logs. Do not promote it. Any follow-up must ensure probes and training terminate within the locked budget; no post-hoc validation was run.
