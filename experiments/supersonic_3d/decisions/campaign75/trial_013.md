# Trial 013

Research metadata (locked on preparation): parents=B; kind=mechanism; mechanism_id=feature_gated_residual_blocks.

## Parent methods and evidence

Parent B alone. B L_val 0.12733444, IC L2 0.28621542, weighted physics 0.04541517. Trials 001, 010 and 012 changed coordinate encodings; Trial 011 changed readout heads. None tested input-dependent control of B residual blocks. Trial 003 remains best IC L2 0.27059138; Trial 008 best score 0.12092633, both ineligible.

## Novelty claim

Distinct campaign mechanism: feature-dependent low-rank gates on each residual block. Unlike simply changing alpha=0.5, each gate uses the current hidden state to modulate its block contribution. The final gate layers start at zero so the initial effective multiplier equals B. Gated neural architectures are known; this specific adaptation is a campaign hypothesis, not a global originality claim.

## Hypothesis and proposed change

Hypothesis: spatially and temporally varying residual-block contributions help the model allocate capacity between turbulent IC structure and PDE evolution, improving IC or physics validation. Add ten 256-16-256 SiLU gate MLPs, one per block, and update h by h + 0.5*(2*sigmoid(gate(h)))*sin(linear(h)); initialize gate final layers at zero. Keep B encoder, heads and trainer.

## Training objective and setup

B width-256 ten sine residual block trunk with per-block bottleneck gates, three spatial harmonics, density exp(t*raw_rho). Parameter count 748965, verified below cap 750000. Fresh weights. Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and IC batches 1024. Adam warmup 1e-4 to 1e-3 over first 5% of 750 s, cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Expect IC L2 below B 0.28621542, ideally <=0.25, or weighted physics below 0.04541517 without a worse L_val. Gate overhead may reduce steps; record actual steps/time and residual components. Inspect early/middle/late physics, density spread, mass drift, positivity and periodicity. If validation worsens, reject despite added capacity.

## Observed results

L_val 0.13834404; weighted physics 0.04803164; IC relative L2 0.30052021 (ineligible). Early/middle/late totals 0.08512926/0.03552400/0.04069718. Early continuity/momentum/Poisson 0.03137341/0.04004625/0.01370959; middle 0.00959054/0.01816231/0.00777115; late 0.01193651/0.01747895/0.01128172. Physical checks passed, rho0 error 0, periodic max error 2.38e-6. At t=0.8 mean rho 0.98683333, mass drift -0.01316667, density std 0.65599912, p99 3.39019012. 748965 parameters, 3425 steps, 748.035 s. Recorded loss 2.5043 at 187.6 s to 1.6970 at 748.0 s.

## Decision and interpretation

Hypothesis not supported at matched time: IC L2 worsened versus B 0.28622 to 0.30052 and L_val worsened 0.12733 to 0.13834. Weighted physics also worsened 0.04542 to 0.04803. The gated model completed only 3425 steps versus B 6852, so compute overhead plausibly limited optimisation; one run cannot isolate architecture from step count. No validation benefit offsets the cost. Do not promote. No numerical-reference accuracy claim follows.
