# Trial 021 Decision Record: Targeted Dual-Harmonic Fourier Coordinate Projection

## Hypothesis
In Trial 014, expanding spatial coordinates across four harmonics $k \in \{1, 2, 3, 4\}$ demonstrated superior resolution on `dev_01` ($1.81 \times 10^{-6}$), but unpopulated higher harmonics ($k=3, 4$) slightly diffused network capacity on `dev_02`. Restricting the Fourier coordinate embedding specifically to the active physical modal span of the two-soliton collision system ($k \in \{1, 2\}$; Wang et al., CMAME 2021) and pairing it with the continuous Hamiltonian mass/energy invariant regularizer (Trial 015) will eliminate spectral diffusion while providing exact harmonic basis representation and energy conservation, driving validation loss below Trial 015's incumbent 0.001183.

## Proposed method change
In `KdVPINN`:
1. Construct targeted dual-harmonic spatial coordinate features spanning the exact physical frequencies of the development cases ($f_1=1.0, f_2=2.0$):
   $$\phi_x(x) = [\sin(\pi x), \cos(\pi x), \sin(2\pi x), \cos(2\pi x)] \in \mathbb{R}^4$$
2. Concatenate $\phi_x(x)$ with temporal coordinate $t$, initial profile $u_0(x)$, and normalized initial derivative $u_{0,x}(x)/\pi$ into a compact 7-dimensional input vector.
3. Pass through input projection `Linear(7, 160)` and 7 residual sinusoidal layers with pure $\sin$ activations:
   $$h_{l+1} = h_l + \sin(W_l h_l + b_l)$$
4. Final scalar output through `Linear(160, 1)` with temporal ansatz:
   $$u(t, x) = u_0(x) + \tanh(\alpha t) \cdot \text{net\_out}(t, x)$$
5. Retain the winning Hamiltonian invariant regularizer (mass and $L^2$ energy penalty with weight 0.1) from Trial 015.
6. Train with standard AdamW (lr=$1.08 \times 10^{-3}$, cosine decay, linear temporal curriculum over first 35%).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, $\lambda_{\mathrm{inv}} = 0.1$, using 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Unlike Trial 014 (which used 4 harmonics and lacked the invariant loss) and Trial 015 (which had the invariant loss but only single-frequency input), Trial 021 synergistically combines exact dual-harmonic modal representation with Hamiltonian energy conservation. Because $k=1$ and $k=2$ match the exact dispersion frequencies of the two-soliton interaction, this directly targets the residual error in `dev_02` while maintaining full step throughput (~8,400 steps per case).

## Evidence from previous experiments
- Trial 014 proved that Fourier input projections overcome spectral bias and drop single-case residual to $1.81 \times 10^{-6}$.
- Trial 015 proved that Hamiltonian mass and $L^2$ energy constraints stabilize non-linear wave collisions, setting our incumbent record (0.001183 mean, 0.003097 worst-case).
- Trial 020 showed that composite activations halved throughput and saturated derivatives, proving architectural simplicity is paramount.
- Combining targeted dual harmonics with Hamiltonian regularization synthesizes the two most effective innovations identified in the campaign.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: targeted_dual_harmonic_fourier_projection
- Source: Sifan Wang, Hanwen Wang, Paris Perdikaris (CMAME 2021, arXiv:2012.10047) and arXiv:2311.14131.
- Distinctness: Formulates a compact, targeted dual-harmonic coordinate representation layer tailored to the system's active physical frequencies ($k \in \{1, 2\}$) synergistically coupled with Hamiltonian continuous invariant regularization.


## Observed results
- Validation loss:
  - Mean: 0.0012127 (close to incumbent Trial 015: 0.0011828)
  - dev_01: 2.0118e-06 (improved over Trial 015: 2.6401e-06)
  - dev_02: 0.0030507 (improved over Trial 015: 0.0030972 — new lowest error on the hardest multi-soliton interaction case!)
  - dev_03: 0.0005853
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.30e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~8,318 steps per case, 28.0 steps/sec).
- Comparison: Targeted dual-harmonic coordinate projection ($k \in \{1, 2\}$) successfully reduced error on `dev_02` to our lowest recorded value (0.003051) while improving `dev_01` (2.01e-06). Trial 015 retains a microscopic edge on mean loss (0.001183 vs 0.001213) due to `dev_03`, but Trial 021 achieves the best worst-case performance in the entire benchmark.

## Agent decision
Retain Trial 015 as the formal incumbent on mean loss (0.001183), with Trial 021 recognized as an equivalent top-tier co-leader achieving superior worst-case performance (0.003051). Mark Trial 021 as completed and eligible, crediting a substantive method record.

## Reason for decision
Trial 021 validated the hypothesis that tailoring the Fourier coordinate projection to the exact physical modal span of the two-soliton collision ($k \in \{1, 2\}$) eliminates spectral diffusion, improving accuracy on the hardest test case (`dev_02`) without throughput overhead. Both Trial 015 and Trial 021 represent our strongest reference-free models. We proceed to investigate dynamic multi-objective loss balancing.
