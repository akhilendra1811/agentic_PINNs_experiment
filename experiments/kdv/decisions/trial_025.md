# Trial 025 Decision Record: Accelerated Domain Curriculum Expansion

## Hypothesis
Accelerating temporal domain curriculum expansion from 35% to 25% of the total budget reaches the full temporal domain $t \in [0, 1.0]$ earlier (at 75s instead of 105s), providing 75% of the computational budget (~6,200 optimizer steps) for full-domain multi-soliton interaction fine-tuning under cosine learning rate decay (Krishnapriyan et al., 2021; arXiv:2007.14527). Since the initial grounding on early time slices ($t \in [0, 0.05]$) occurs rapidly in the first 1,500 steps, allocating more iterations to the complex multi-frequency soliton collisions at $t > 0.5$ will improve worst-case validation loss on `dev_02`.

## Proposed method change
In `candidate.py`:
1. Retain the winning targeted dual-harmonic SIREN architecture from Trial 024 ($k \in \{1, 2\}$, 8 layers, WIDTH=160, pure $\sin$ activations with additive residuals).
2. Retain the dense Hamiltonian invariant regularizer ($S=8$ time slices, $N_x=128$ points, $\lambda_{\mathrm{inv}} = 0.1$).
3. Retain unconstrained AdamW with `weight_decay = 0.0` and base learning rate $1.08 \times 10^{-3}$.
4. Update `CURRICULUM_FRAC` from 0.35 to 0.25:
   - For `fraction < 0.25`: expand time horizon linearly from $t \in [0, 0.05]$ to $[0, 1.0]$, maintaining peak learning rate $1.08 \times 10^{-3}$.
   - For `fraction >= 0.25`: train over the complete domain $t \in [0, 1.0]$ with cosine learning rate decay down to $10^{-7}$ over the remaining 75% of the training budget.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, using $S=8$ time slices, evaluated alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Reaching full domain coverage 30 seconds earlier will increase the number of gradient steps devoted to resolving late-time soliton wave-front interactions by ~800 steps (~13% increase in full-domain iterations). Because late-time collisions generate the highest spatial gradients and contribute the bulk of validation error on `dev_02` and `dev_03`, more full-domain optimization should further lower the validation error floor below 0.00114.

## Evidence from previous experiments
- In Trial 017, introducing curriculum pacing improved early trajectory stability.
- In Trial 024, the network achieved an unprecedented 1.75e-06 on `dev_01`, demonstrating that simple single-soliton dynamics converge very quickly.
- However, multi-soliton cases (`dev_02` at 0.00287) require extended optimization to resolve rapid dispersion wave packets after collision.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: accelerated_domain_curriculum_expansion
- Source: A. Krishnapriyan et al. (NeurIPS 2021), "Characterizing possible failure modes in physics-informed neural networks", arXiv:2007.14527.
- Distinctness: Formulates optimized domain curriculum expansion pacing specifically tuned for multi-scale dispersive PDE wave packet interactions.


## Observed results
- Validation loss:
  - Mean: 0.0012890 (Baseline: 0.0030404, Trial 024 incumbent: 0.0011418)
  - dev_01: 2.1749e-06
  - dev_02: 0.0034291 (Higher than Trial 024's 0.0028732)
  - dev_03: 0.0004357 (All-time best on dev_03; down from 0.0005505 in Trial 024, a 21% error reduction)
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.33e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~8,284 steps per case, 27.89 steps/sec).
- Comparison: While accelerating curriculum expansion to 25% allowed extended cosine decay that unlocked an all-time best validation score on `dev_03` (0.0004357), it truncated early temporal grounding on `dev_02`, where the steeper wave collision required the full 35% curriculum ramp to avoid early residual lock-in.

## Agent decision
Keep Trial 024 as the **INCUMBENT WINNER**. Mark Trial 025 as completed and eligible. Retain `CURRICULUM_FRAC = 0.35` as the preferred pacing for subsequent trials while noting that extended cosine decay strongly benefits lower-amplitude dispersion cases.

## Reason for decision
Trial 024 retains superior mean validation loss (0.0011418 vs 0.0012890) and superior worst-case loss on dev_02 (0.0028732 vs 0.0034291). The 35% domain expansion window provides the optimal balance between initial condition grounding and full-domain refinement for stiff multi-soliton collisions.
