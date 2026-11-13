# Trial 014

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=density_focused_collocation.

## Parent methods and evidence

Parent B alone. B L_val 0.12733444, IC L2 0.28621542, t=0.8 density p99 3.47331 and weighted physics 0.04541517. Trial 004 residual-based adaptive collocation exceeded budget and produced no metrics; its derivative-based probes were costly. None of Trials 001-013 targeted high-density predicted regions directly during sampling.

## Novelty claim

Distinct campaign mechanism: density-focused collocation with a forward-only probe and random coverage. This targets the stated difficulty of compressive/high-density structures. It differs from Trial 004 residual sampling because ranking uses predicted density and no PDE derivatives. The design is independently motivated by the physical objective; no specific paper or global novelty claim is asserted.

## Hypothesis and proposed change

Hypothesis: allocating one quarter of PDE updates partly to current high-density regions improves continuity and momentum in compressive structures without expensive residual probes. Every fourth training step sample 2048 fresh candidates, score density under no_grad, train on 512 highest-density plus 512 random candidates; other steps use 1024 uniform fresh points. Keep B model and loss.

## Training objective and setup

Exact B ResPINN architecture (664325 parameters) and fresh weights. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. PDE batch 1024 selected by stated mixture every fourth step, otherwise fresh uniform; IC batch 1024. Probe and selection time count within 750 s. Adam warmup 1e-4 to 1e-3 for 5% time then cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Expect reduced continuity/momentum validation losses or more realistic density spread, especially late, without unacceptable L_val increase versus B 0.12733444. IC L2 should not worsen from 0.28621542; eligibility needs <=0.25. Inspect early/middle/late residuals, density p99/std, mass drift, positivity, periodicity, steps and time. Density selection may overfocus on model artifacts; a negative result would reject this schedule.

## Observed results

L_val 0.12882566; weighted physics 0.04509879; IC relative L2 0.28935596 (ineligible). Early/middle/late totals 0.08254819/0.03254635/0.03765049. Early continuity/momentum/Poisson 0.03174379/0.03830889/0.01249551; middle 0.00909063/0.01623249/0.00722323; late 0.01056620/0.01559348/0.01149081. Physical checks passed, rho0 error 0, periodic max error 3.58e-6. At t=0.8 mean rho 0.98701423, mass drift -0.01298577, density std 0.66297817, p99 3.42281604. 664325 parameters, 6363 steps, 748.009 s. Training loss 2.3145 at 187.6 s to 1.5925 at 748.0 s.

## Decision and interpretation

Hypothesis not supported by reference-free validation: IC L2 worsened versus B (0.28936 vs 0.28622) and L_val worsened (0.12883 vs 0.12733). Weighted physics was nearly unchanged (0.04510 vs 0.04542), with early total worse and late total better. Late density std and p99 were lower than B, not evidence of better high-density capture. The forward-only probe was computationally feasible (6363 steps versus B 6852) unlike Trial 004. Do not promote this selection schedule. No numerical-reference accuracy claim follows.
