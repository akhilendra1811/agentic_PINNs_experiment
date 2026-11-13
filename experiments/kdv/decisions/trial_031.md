# Trial 031 Decision Record: Ultra-Dense Temporal Hamiltonian Invariant Slices (S = 16)

## Hypothesis
In structure-preserving PINNs for the Korteweg-de Vries equation, evaluating mass ($\int_{-1}^1 u dx = 0$) and Hamiltonian $L^2$ energy ($\int_{-1}^1 u^2 dx = a_1^2 + a_2^2$) invariants on $S=8$ time slices leaves an average temporal interval of $\Delta t \approx 0.125$ between slices. During the stiff collision phase of `dev_02` ($t \in [0.4, 0.7]$), rapid non-linear crest interactions evolve on a fast timescale $\tau \approx 0.05$, allowing localized transient energy dissipation to occur undetected between sampled slices (Obieke & Oguadimma, arXiv:2511.00418). Doubling the temporal invariant slice density to $S=16$ slices ($16 \times 256 = 4,096$ forward-mode quadrature points per step) cuts the temporal sampling interval to $\Delta t \approx 0.062$, providing a continuous spatio-temporal lattice of exact physical conservation that suppresses transient energy drift and improves worst-case validation loss on `dev_02` below Trial 029's record 0.0019268.

## Proposed method change
In `candidate.py`:
1. Retain the winning targeted dual-harmonic SIREN architecture ($k \in \{1, 2\}$, WIDTH=160, 8 layers, pure $\sin$ activations with additive residuals and unitary scaling).
2. Retain high-density spatial Hamiltonian quadrature ($N_x=256$).
3. Retain the winning AdEMAMix optimizer with linear $\alpha$-warmup ($\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, $\alpha$ linearly warmed up from 0.0 to 2.0 over first 35%, zero weight decay, base lr $1.08 \times 10^{-3}$ with cosine decay).
4. Update temporal invariant slice density:
   - Change `INV_SLICES = 8` to `INV_SLICES = 16`.
   - Maintain `INV_POINTS = 256` and `INV_WEIGHT = 0.1`.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, evaluated over $S=16$ time slices with $N_x=256$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Doubling the temporal invariant resolution from 8 to 16 slices guarantees that at any training step, the collision interval contains at least 3–5 dedicated spatial quadrature cross-sections enforcing exact mass and energy conservation. Because these 4,096 points are evaluated purely in forward mode (zero spatial or temporal autograd derivatives), step throughput is expected to remain $\ge 25$ steps/sec.

## Evidence from previous experiments
- In Trial 023, doubling $S$ from 4 to 8 broke below 0.003 on `dev_02` for the first time.
- In Trial 027, doubling $N_x$ from 128 to 256 dropped mean loss from 0.000803 to 0.000732.
- In Trial 029, AdEMAMix with $\alpha$-warmup reached 0.001927 on `dev_02`, with validation loss continuing to decline steadily through the final second.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: ultradense_temporal_hamiltonian_slices
- Source: V. C. Obieke, E. E. Oguadimma (arXiv:2511.00418, Nov 2025), "Structure-Preserving Physics-Informed Neural Network for the Korteweg-de Vries (KdV) Equation".
- Distinctness: Evaluates ultra-dense temporal invariant slice tracking ($S=16$) combined with high-density spatial quadrature ($N_x=256$) and curriculum-aligned AdEMAMix optimization.


## Observed results
- Validation loss:
  - Mean: 0.0265215 (Higher than incumbent Trial 029: 0.0006826)
  - dev_01: 0.0776222 (Over-regularization noise prevented convergence to micro-scale fixed point; best posthoc was 0.02177)
  - dev_02: 0.0018102 (**All-time best on dev_02 across the entire campaign**; down from 0.0019268 in Trial 029 and baseline 0.007173; **3.96x reduction over baseline**)
  - dev_03: 0.0001320
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.31e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~7,970 steps per case, 26.85 steps/sec).
- Comparison: Doubling temporal slice density to $S=16$ set another new campaign benchmark on the two-soliton collision case (`dev_02` reached an unprecedented 0.001810). However, evaluating 4,096 invariant points per step injected stochastic quadrature gradient variance that dominated the tiny $10^{-7}$ PDE residual on `dev_01`, destabilizing single-frequency convergence at the final checkpoint.

## Agent decision
Keep Trial 029 as the **INCUMBENT WINNER**. Revert `INV_SLICES` to 8 in `candidate.py`. Mark Trial 031 as completed and eligible, logging a critical insight on the trade-off between dense invariant tracking for collisions and gradient noise in near-zero residual regimes.

## Reason for decision
Trial 029 maintains superior mean validation loss (0.0006826 vs 0.0265215) and balanced excellence across all three cases (`dev_01`: 3.34e-07, `dev_02`: 0.001927, `dev_03`: 0.000121). $S=8$ provides sufficient temporal coverage for collision dynamics while keeping invariant gradient noise low enough to permit micro-scale convergence on simple waves.
