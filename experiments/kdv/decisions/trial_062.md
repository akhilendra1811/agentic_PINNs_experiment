# Trial 062 Decision Record: SOAP-AdEMAMix Preconditioning Frequency Calibration (`freq = 40`)

## Hypothesis
In Trial 061, we discovered that updating the Kronecker factor eigenbasis too frequently (`freq = 10`) caused the projected coordinate frame to rotate before the slow momentum buffer ($\nu_t$, $\beta_3 = 0.999$, half-life 693 steps) could stabilize, causing mean validation loss to rise to `0.0003112` compared to incumbent Trial 060 (`0.00011108` at `freq = 20`).
To complete the sensitivity bracket of SOAP preconditioning frequency, we test `precondition_frequency = 40`:
1. The coordinate frame $(Q_L, Q_R)$ remains fixed for 40 consecutive steps, allowing the dual-momentum buffers ($\tilde{m}_t$ and $\tilde{\nu}_t$) to accumulate coherent directional velocity along the principal Hessian eigenvectors without coordinate rotation jitter.
2. Halves the number of eigendecompositions over the training run (from ~330 down to ~165 calls), saving wall-clock time and recovering ~100 additional optimization steps.
3. Brackets the optimal preconditioning frequency $[10, 20, 40]$ to determine whether greater eigenspace persistence improves overall validation loss.

## Proposed method change
In `candidate.py`:
1. Change `precondition_frequency`:
   ```python
   precondition_frequency = 40
   ```
2. Retain all other winning hyperparameters of incumbent Trial 060:
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
A longer eigenspace stability window of 40 steps provides smoother momentum accumulation along the dominant curvature directions, testing whether increased persistence yields lower loss on the two-soliton collision (`dev_02`).

## Evidence from previous experiments
- In Trial 060: `freq = 20` gave our breakthrough mean loss 0.00011108.
- In Trial 061: `freq = 10` gave 0.0003112 (more frequent rotation was suboptimal).
- Testing `freq = 40` evaluates the opposite direction of the preconditioning frequency continuum.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false
- Novelty key: soap_precondition_frequency_40
- Sources:
  - Wei, Wang, Bhartari, Li, Perdikaris (arXiv:2502.00604, Feb 2025), "Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective".
  - Vyas et al. (arXiv:2409.11321, 2024), "SOAP: Improving and Stabilizing Shampoo using Adam".
- Distinctness: Systematic calibration of SOAP preconditioner eigendecomposition update frequency from 20 to 40 to enhance momentum stability in rotated coordinates.


## Observed results
- Validation loss:
  - Mean: 6.15449e-05 (**NEW ALL-TIME RECORD**, 1.80x error reduction vs Trial 060: 0.00011108; 8.88x reduction vs Trial 033: 0.0005464; **49.4x reduction vs baseline**: 0.0030404)
  - dev_01: 2.84182e-07 (Sub-microscale precision maintained)
  - dev_02: 0.00016391 (**NEW ALL-TIME RECORD on dev_02**, 1.86x reduction vs Trial 060: 0.0003042; 9.45x reduction vs Trial 033: 0.0015491; 43.8x reduction vs baseline: 0.007173)
  - dev_03: 2.04374e-05 (**NEW ALL-TIME RECORD on dev_03**, 1.41x reduction vs Trial 060: 2.8755e-05; 4.41x reduction vs Trial 033: 9.0035e-05)
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 3.15e-05 <= 1e-3, params = 219,650 <= 250,000).
- Optimizer step throughput: Gained ~100 extra steps/case (6,775–6,782 steps, ~22.8 steps/sec) by reducing eigendecomposition frequency.
- Comparison: Calibrating `precondition_frequency` to 40 steps provided the ideal compromise for SOAP-AdEMAMix. By maintaining the rotated eigenbasis $(Q_L, Q_R)$ stable for 40 consecutive steps, both fast ($m_t$) and slow ($\nu_t$) momentum buffers accumulate deep, coherent directional acceleration along the principal curvature coordinates without coordinate frame rotation jitter. Combined with the ~100 step throughput gain, this drove `dev_02` collision loss down to $0.0001639$ and mean validation loss down to $6.15 \times 10^{-5}$.

## Agent decision
**ACCEPT AND PROMOTE TO ALL-TIME INCUMBENT WINNER!**
Trial 062 replaces Trial 060 as the new campaign leader. Retain `candidate.py` with `precondition_frequency = 40` as the active codebase.

## Reason for decision
Trial 062 achieves a massive 49.4x error reduction over baseline and 1.8x reduction over Trial 060 across all three development cases (mean validation loss 6.154e-05 vs 1.111e-04; worst-case 1.639e-04 vs 3.042e-04).
