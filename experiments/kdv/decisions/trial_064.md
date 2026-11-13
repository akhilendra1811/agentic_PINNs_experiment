# Trial 064 Decision Record: SOAP-AdEMAMix Preconditioning Frequency Calibration (`freq = 80`)

## Hypothesis
Across Trials 060, 062, and 063, extending the update interval of the SOAP Kronecker factor eigenbases yielded monotonic improvements in convergence:
- $\text{freq} = 10$ (Trial 061): mean val `0.0003112`
- $\text{freq} = 20$ (Trial 060): mean val `0.0001111`
- $\text{freq} = 40$ (Trial 062): mean val `0.0000615`
- $\text{freq} = 60$ (Trial 063): mean val `0.0000542` (**ALL-TIME RECORD**)
To locate the exact global optimum of preconditioning frequency and determine where curvature staleness sets in, we test `precondition_frequency = 80`:
1. The coordinate frame $(Q_L, Q_R)$ is held constant for 80 consecutive steps, allowing the dual-momentum buffers ($\tilde{m}_t$ and $\tilde{\nu}_t$) to accelerate steadily along the principal curvature directions without coordinate rotation disruptions.
2. Eigendecomposition calls are reduced to just ~85 operations across the entire training budget, maximizing optimizer step throughput.
3. Tests whether an 80-step persistence window continues to lower validation loss or whether the rotated eigenspace lags behind rapid curvature rotations during the non-linear two-soliton collision in `dev_02`.

## Proposed method change
In `candidate.py`:
1. Change `precondition_frequency`:
   ```python
   precondition_frequency = 80
   ```
2. Retain all other winning hyperparameters of incumbent Trial 063:
   - $\text{WIDTH} = 176$, $\text{HIDDEN\_LAYERS} = 8$ (219,650 parameters).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - SOAP-AdEMAMix with static $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, zero weight decay, base lr $1.08 \times 10^{-3}$, linear $\alpha$-warmup from $0 \to 2.0$ over first 35% of steps, continuous cosine decay down to $10^{-7}$ over remaining 65%.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$ stochastic time slices, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Longer eigenspace persistence provides steady directional momentum, testing whether 80 steps preserves curvature alignment during soliton interaction.

## Evidence from previous experiments
- Progressive improvements from `freq = 10` to `20` to `40` to `60` establish that longer eigenspace persistence directly stabilizes momentum in rotated space.
- Testing `freq = 80` completes the empirical response curve $[10, 20, 40, 60, 80]$.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: soap_precondition_frequency_80
- Sources:
  - Wei, Wang, Bhartari, Li, Perdikaris (arXiv:2502.00604, Feb 2025), "Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective".
  - Vyas et al. (arXiv:2409.11321, 2024), "SOAP: Improving and Stabilizing Shampoo using Adam".
- Distinctness: Systematic calibration of SOAP preconditioner update frequency to 80 steps to establish the exact curvature staleness threshold.


## Observed results
- Validation loss:
  - Mean: 4.85727e-05 (**NEW ALL-TIME RECORD**, 1.12x reduction vs Trial 063: 5.419e-05; 11.25x reduction vs Trial 033: 0.0005464; **62.6x reduction vs baseline**: 0.0030404)
  - dev_01: 1.28053e-07 (**NEW ALL-TIME RECORD on dev_01**, beating all previous trials)
  - dev_02: 0.00013222 (**NEW ALL-TIME RECORD on dev_02**, 1.14x reduction vs Trial 063: 1.502e-04; 11.72x reduction vs Trial 033: 0.0015491; **54.3x reduction vs baseline**: 0.007173)
  - dev_03: 1.33703e-05
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 7.41e-05 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Gained additional speed (6,744–6,836 steps/case, ~23.0 steps/sec) due to minimal eigendecomposition overhead (~85 calls across entire run).
- Comparison: Setting `precondition_frequency = 80` provided an 80-step eigenspace persistence window that perfectly harmonizes with AdEMAMix's long-term momentum buffer ($\beta_3 = 0.999$, half-life 693 steps). Because the coordinate frame remains fixed for 80 steps, both fast and slow momentum vectors build deep, unperturbed acceleration along the principal curvature axes of the loss landscape. This broke below the $5.0 \times 10^{-5}$ threshold, establishing all-time campaign records on mean validation loss ($4.857 \times 10^{-5}$), worst-case error ($1.322 \times 10^{-4}$ on `dev_02`), and single-mode wave precision ($1.281 \times 10^{-7}$ on `dev_01`).

## Agent decision
**ACCEPT AND PROMOTE TO ALL-TIME INCUMBENT WINNER!**
Trial 064 replaces Trial 063 as the new campaign leader. Retain `candidate.py` with `precondition_frequency = 80` as the active codebase.

## Reason for decision
Trial 064 achieves a monumental 62.6x error reduction over baseline, breaks below $5.0 \times 10^{-5}$ on mean validation loss (4.857e-05), sets a new worst-case record on `dev_02` (1.322e-04), sets an all-time record on `dev_01` (1.281e-07), and satisfies all eligibility criteria strictly.
