# Trial 008

Research metadata (locked on preparation): parents=trial:3,trial:7; kind=mechanism; mechanism_id=anchored_ic_pretraining_integration.

## Parent methods and evidence

Parents Trial 003 and Trial 007. Trial 003 (B with 20% IC-only training) reached campaign-best L_val 0.12452034 and IC L2 0.27059138 but physics weighted 0.05130065. Trial 007 anchored velocity achieved physics weighted 0.01946885, far lower, but IC L2 0.36665267, ineligible. The combination aims to retain their complementary strengths.

## Novelty claim

Campaign integration mechanism combining an anchored initial-velocity decomposition with staged IC-first optimisation. Neither Trial 003 nor Trial 007 tested both together; this is an integration hypothesis, not a claim of global originality. The components are described in their decision records and the pre-campaign hard-IC methodological sources in internet_use.md.

## Hypothesis and proposed change

Hypothesis: 20% IC-only training will push the anchored branch toward the turbulent initial field before PDE optimisation, reducing Trial 007 IC L2 substantially while preserving its low physics residual. Use Trial 007 architecture unchanged and add Trial 003 first-20%-of-time relative IC MSE stage, then standard B joint loss.

## Training objective and setup

Trial 007 anchored architecture: B ResPINN width 256, ten sine residual blocks, plus width-256 SiLU spatial branch; velocity = spatial(x)+t*dynamic(x,t), density exp(t*raw_rho), potential raw_phi; 735752 parameters. Fresh weights. First 20% of 750 s: IC relative MSE only. Remaining 80%: 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and IC batches 1024; Adam warmup 1e-4 to 1e-3 over first 5%, cosine to 1e-5, gradient clip 0.5. Locked evaluator.

## Expected outcome

Expect IC L2 well below Trial 007 0.36665267, ideally <=0.25. Physics weighted may increase from 0.01946885; compare with B 0.04541517. Aim for L_val below Trial 003 0.12452034. Inspect all temporal terms, density spread, mass drift, positivity, periodicity and training steps. If IC stays ineligible or physics advantage disappears, do not promote.

## Observed results

L_val 0.12092633 (lowest so far); weighted physics 0.03162275; IC relative L2 0.29883704 (ineligible). Early/middle/late totals 0.05201631/0.02264573/0.02885154. Early continuity/momentum/Poisson 0.01566125/0.02792665/0.00842842; middle 0.00716542/0.01112006/0.00436025; late 0.00941739/0.01236851/0.00706564. Physical checks passed, rho0 error 0, periodic max error 3.87e-6. At t=0.8 mean rho 0.99060446, mass drift -0.00939554, density std 0.68948972, p99 3.53604364. 735752 parameters, 20404 steps, 748.103 s. Recorded joint-stage training loss 2.6041 at 187.5 s, 1.9162 at 375.0 s, 1.6809 at 562.5 s and 1.5923 at 748.1 s.

## Decision and interpretation

Integration partially supported: versus Trial 007, IC L2 improved substantially (0.36665 to 0.29884) while weighted physics remained better than B (0.03162 vs 0.04542). L_val improved from Trial 007 0.15390 and Trial 003 0.12452 to 0.12093. However, IC L2 is still above 0.25 and worse than Trial 003 0.27059, so the method is ineligible. Do not select yet. The result suggests the anchored model can trade some physics residual for IC fit, but further work must address IC without assuming low residual implies reference accuracy.
