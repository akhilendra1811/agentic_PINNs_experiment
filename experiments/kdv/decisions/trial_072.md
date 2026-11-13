# Trial 072 Decision Record: Hamiltonian Invariant Slice Density ($S = 10$)

## Hypothesis
In KdV solitary wave interactions, non-linear dispersion models frequently suffer from numerical dissipation (amplitude decay) and artificial phase shifts during high-gradient wave collisions.
In Trial 023, introducing dense temporal Hamiltonian invariant regularization ($S=8$ time slices, $N_x=512$ points) dropped validation error by 2.6x. However, in Trial 031, pushing $S$ to 16 under first-order Adam disrupted `dev_01` because first-order gradients suffered from directional conflicts between the invariant constraint and interior residuals.
With the introduction of SOAP-AdEMAMix (Trial 067: mean val `4.689899 \times 10^{-5}`), Perdikaris et al. (2025) proved that quasi-second-order Kronecker preconditioning flattens directional gradient conflicts across multi-objective loss landscapes.
By increasing `INV_SLICES` from $S=8$ to $S=10$:
1. The model samples 10 independent temporal cross-sections per step (totaling 65,000 temporal slices over 6,500 training steps, a +25% increase).
2. Tighter temporal continuity of mass $\int_{-1}^1 u \, dx = 0$ and $L^2$ energy $\int_{-1}^1 u^2 \, dx = a_1^2 + a_2^2$ is enforced across the entire expansion curriculum ($t \in [0, 1]$).
3. The benchmarked MPS throughput drops by less than 6% (from 4.09 ms/step to 4.33 ms/step), preserving $\ge 6,000$ steps per 300-second case.
4. Tests whether enhanced temporal invariant density reduces worst-case two-soliton collision error on `dev_02`.

## Proposed method change
In `candidate.py`:
1. Update `INV_SLICES`:
   ```python
   INV_SLICES = 10
   ```
2. Retain all other winning hyperparameters of incumbent Trial 067:
   - $\text{WIDTH} = 176, \text{HIDDEN\_LAYERS} = 8$ (219,650 params).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - Synchronous rotated-space SOAP-AdEMAMix with `precondition_frequency = 80`.
   - $\text{LEARNING\_RATE} = 1.15 \times 10^{-3}$, $\beta_1=0.9, \beta_2=0.99, \beta_3=0.999$, $\alpha_{\max} = 2.0$.
   - Hamiltonian quadrature: $N_x=512, \lambda_{\mathrm{inv}} = 0.10$.
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=10$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (5,120 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Enhanced conservation along the temporal dimension, suppressing amplitude damping on `dev_02` while maintaining full eligibility.

## Evidence from previous experiments
- In Trial 023, $S=8$ delivered a 2.6x improvement over unconstrained training.
- In Trial 067, SOAP preconditioning achieved our all-time record (`4.689899 \times 10^{-5}`).
- In Trial 050 and 059, invariant weighting was proven to be essential for KdV stability.

## Literature and novelty assessment
- Category: other
- Novelty credit: false

## Observed results
- Mean validation loss: `5.115214e-05` ($5.12 \times 10^{-5}$) [vs Trial 067: `4.689899e-05`].
- dev_01 validation loss: `4.42478e-07` ($L_{\mathrm{IC}} = 0.0$, $L_{\mathrm{BC}} = 4.44 \times 10^{-8}$).
- dev_02 validation loss: `0.00014289` ($1.43 \times 10^{-4}$) [vs Trial 067: `1.3099 \times 10^{-4}`].
- dev_03 validation loss: `1.01222e-05` ($1.01 \times 10^{-5}$).
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, $L_{\mathrm{BC}} = 0.000176 \le 10^{-3}$, parameter count: 219,650).
- Runtime: 891.1s total (approx 6,429 optimizer steps per case on Apple Silicon MPS).

## Agent decision
**REJECT METHOD CHANGE; TRIAL 067 REMAINS INCUMBENT WINNER.**
Revert `INV_SLICES` to `8` in `candidate.py`.

## Reason for decision
1. **Computational Pareto Peak at $S=8$:**
   Increasing $S$ to 10 increased invariant points per batch to 5,120, costing approximately 140–250 optimizer steps per 300s development run.
2. **Slight Collision Degradation:**
   The lost training steps resulted in slightly higher validation error on the stiff two-soliton collision in `dev_02` (`1.43e-4` vs `1.31e-4` in Trial 067).
3. **Firm Incumbent Position:**
   $S=8$ provides sufficient temporal density for Hamiltonian conservation while allowing higher step throughput. Trial 067 remains our all-time best performer.
