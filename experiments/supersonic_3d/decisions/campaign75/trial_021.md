# Trial 021

Research metadata (locked on preparation): parents=trial:1,trial:3; kind=mechanism; mechanism_id=moderate_harmonics_ic_pretraining.

## Parent methods and evidence

Parents Trials 001 and 003. Trial 001 extended spatial harmonics from three to eight on B and worsened IC L2 to 0.29519224 and L_val to 0.14317630, with only 4682 steps. Trial 003 kept three harmonics but used 20% IC-first training, improving IC L2 to 0.27059138 and L_val to 0.12452034. Trial 017 further reduced IC to 0.26769212 with a smoother transition but worse physics. This trial tests a smaller spectral expansion paired with IC-first optimisation.

## Novelty claim

Integration of moderate multiscale periodic representation and staged IC pretraining. Trial 001 tested eight harmonics without IC pretraining; Trial 003 tested three with pretraining. Five harmonics plus the same IC stage is materially different from both, though the underlying mechanisms are already known within the campaign. It is an integration hypothesis, not a global novelty claim. Fourier-feature PINN context is logged in internet_use.md.

## Hypothesis and proposed change

Hypothesis: five spatial harmonics supply enough extra turbulent IC bandwidth to improve validation IC fit, while causing less derivative and compute cost than eight harmonics, especially when the first 20% of time is devoted to IC fitting. Starting from Trial 003 candidate, change input layer 19 to 31 and spatial k loop 1..3 to 1..5. Keep all training stages and weights fixed.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, alpha 0.5, five periodic spatial harmonics, density exp(t*raw_rho), fresh weights, under 750000 parameters. First 20% of 750 s IC relative MSE only; remaining 80% B loss 3.5 continuity+7.5 momentum+2.5 Poisson+16 IC relative MSE. Fresh PDE/IC batches 1024. Adam warmup 1e-4 to 1e-3 for first 5%, cosine to 1e-5, gradient clipping 0.5. Locked validation.

## Expected outcome

Expect IC L2 below Trial 003 0.27059138, possibly <=0.25, and more completed steps than Trial 001 4682. Compare L_val to Trial 003 0.12452034 and physics weighted 0.05130065. Check early and late derivatives, mass drift, density spread, positivity, periodicity, parameter count and runtime. If extra frequency hurts both IC and physics, reject the integration.

## Observed results

The first evaluator invocation started at 2026-11-05 22:50:22 UTC, but its terminal session became unavailable without writing metrics or a checkpoint. The user explicitly authorized a human override. The original status and log were copied to `recovery/experiment_021/`, the local status was reset to `prepared`, and the standard CLI reran the unchanged candidate from fresh weights at 2026-11-05 23:58:09 UTC. The second run completed normally: L_val 0.14542435, weighted physics 0.07251232, IC relative L2 0.27002227, IC relative MSE 0.07291203, eligible false. Early/middle/late physics totals were 0.09055802/0.04328503/0.08283042; late Poisson was 0.05527592. Physical checks passed, initial density error 0, periodic error 1.97e-6. At t=0.8, mean density was 0.98372644, relative mass drift -0.01627356, density std 0.64027083, p99 3.29284024. The model had 667397 parameters and trained for 748.1117 seconds, 21821 steps.

## Decision and interpretation

The completed second run provides evidence against carrying this integration forward: IC error improved only slightly from Trial 003 (0.27059138 to 0.27002227), while L_val worsened from 0.12452034 to 0.14542435 and weighted physics worsened from 0.05130065 to 0.07251232. The IC threshold remains unmet. The first invocation is retained as an interrupted run in the override archive; only the completed second run supplies the reported metrics. Do not select this candidate as a finalist on present evidence.
