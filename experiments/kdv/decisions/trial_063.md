# Trial 063 Decision Record: SOAP-AdEMAMix Preconditioning Frequency Calibration (`freq = 60`)

## Hypothesis
In Trial 062, extending the SOAP preconditioner update interval to `precondition_frequency = 40` achieved our all-time record mean validation loss of `6.154 \times 10^{-5}` ($49.4\times$ reduction vs baseline) by stabilizing momentum accumulation in rotated eigenspace coordinates.
To explore the upper limit of eigenspace persistence and map the complete preconditioning frequency curve, we test `precondition_frequency = 60`:
1. The coordinate frame $(Q_L, Q_R)$ remains fixed for 60 consecutive steps, allowing the AdEMAMix dual-momentum buffers ($\tilde{m}_t$ and $\tilde{\nu}_t$) to build prolonged, undisturbed acceleration along the principal curvature axes without rotational disruption.
2. Minimizes eigendecomposition overhead to just ~110 calls across the entire 6,800-step budget, yielding maximum step throughput.
3. Evaluates whether 60 steps causes eigenspace staleness on the evolving two-soliton collision landscape in `dev_02` or achieves even deeper convergence.

## Proposed method change
In `candidate.py`:
1. Change `precondition_frequency`:
   ```python
   precondition_frequency = 60
   ```
2. Retain all other winning hyperparameters of incumbent Trial 062:
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
Increased eigenspace stability and further reduced computational overhead, testing whether 60-step persistence maintains second-order alignment on the dynamic two-soliton collision.

## Evidence from previous experiments
- In Trial 061: `freq = 10` gave 0.0003112 (too frequent rotation destabilized momentum).
- In Trial 060: `freq = 20` gave 0.00011108.
- In Trial 062: `freq = 40` gave our all-time record 0.00006154.
- Monotonic improvements from 10 to 40 motivate testing 60.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: soap_precondition_frequency_60
- Sources:
  - Wei, Wang, Bhartari, Li, Perdikaris (arXiv:2502.00604, Feb 2025), "Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective".
  - Vyas et al. (arXiv:2409.11321, 2024), "SOAP: Improving and Stabilizing Shampoo using Adam".
- Distinctness: Systematic calibration of SOAP preconditioner update frequency to 60 steps to evaluate the persistence boundary of eigenspace stability.


## Observed results
- Validation loss:
  - Mean: 5.41890e-05 (**NEW ALL-TIME RECORD**, 1.14x reduction vs Trial 062: 6.154e-05; 10.08x reduction vs Trial 033: 0.0005464; **56.1x reduction vs baseline**: 0.0030404)
  - dev_01: 1.91819e-07 (Sub-microscale precision maintained)
  - dev_02: 0.00015022 (**NEW ALL-TIME RECORD on dev_02**, 1.09x reduction vs Trial 062: 1.639e-04; 10.31x reduction vs Trial 033: 0.0015491; **47.7x reduction vs baseline**: 0.007173)
  - dev_03: 1.21570e-05 (**NEW ALL-TIME RECORD on dev_03**, 1.68x reduction vs Trial 062: 2.044e-05; 7.41x reduction vs Trial 033: 9.0035e-05)
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 3.73e-05 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Peak speed maintained (6,723–6,811 steps/case, ~22.9 steps/sec).
- Comparison: Setting `precondition_frequency = 60` provided an even longer 60-step eigenspace stability window, allowing the dual-momentum buffers ($\tilde{m}_t$ and $\tilde{\nu}_t$) to accelerate steadily along the principal curvature coordinates without coordinate frame rotation jitter. This continuous momentum buildup polished the two-soliton collision on `dev_02` down to an unprecedented $1.502 \times 10^{-4}$ and drove `dev_03` down to $1.216 \times 10^{-5}$, setting all-time records across every dev case.

## Agent decision
**ACCEPT AND PROMOTE TO ALL-TIME INCUMBENT WINNER!**
Trial 063 replaces Trial 062 as the new campaign leader. Retain `candidate.py` with `precondition_frequency = 60` as the active codebase.

## Reason for decision
Trial 063 achieves a monumental 56.1x error reduction over baseline and establishes new all-time bests on mean validation loss (5.419e-05), worst-case loss (1.502e-04 on `dev_02`), and `dev_03` (1.216e-05) while maintaining sub-microscale precision on `dev_01` (1.92e-07) and strict eligibility.
