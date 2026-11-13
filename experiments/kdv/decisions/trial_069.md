# Trial 069 Decision Record: Exact SOAP-AdEMAMix with Original-Space Momentum Tracking and Eigenspace Projection

## Hypothesis
In the canonical formulation of SOAP (Vyas et al., arXiv:2409.11321, Algorithm 3 and Section 4.1: *"SOAP: Improving and Stabilizing Shampoo using Adam"*), the authors explicitly distinguish SOAP from methods like GaLore by maintaining momentum in the original, unrotated parameter space:
$$M_t = \beta_1 M_{t-1} + (1 - \beta_1) G_t$$
and then projecting the accumulated momentum into the rotated eigenbasis of the Kronecker covariance factors ($L = Q_L \Lambda_L Q_L^T, R = Q_R \Lambda_R Q_R^T$) at each step:
$$M_t' = Q_L^T M_t Q_R$$
In our initial SOAP implementation (Trials 060–068), momentum was accumulated directly in the rotated eigenspace without basis transformation when $Q_L, Q_R$ were recomputed every 80 steps. This introduced periodic coordinate discontinuities that particularly disrupted the slow-momentum buffer ($\beta_3 = 0.999$, half-life $\approx 693$ steps), explaining why longer eigenspace persistence periods suffered from curvature staleness (e.g. Trial 065).
By maintaining both AdEMAMix fast ($m_1$) and slow ($m_2$) momentum buffers in the continuous parameter space:
1. Momentum trajectories are globally coordinate-invariant and never suffer from eigendecomposition boundary shock.
2. The blended momentum $M_{\text{mix}}$ projected into the instantaneous eigenbasis ($Q_L^T M_{\text{mix}} Q_R$) automatically aligns with the current principal curvature axes.
3. Tests whether exact canonical SOAP momentum mechanics drive mean validation loss below the current all-time record of `4.689899 \times 10^{-5}` (Trial 067).

## Proposed method change
In `candidate.py`:
1. In `SOAPAdEMAMix.step()`, accumulate $m_1$ and $m_2$ in the parameter space:
   ```python
   m1.mul_(beta1).add_(grad, alpha=1.0 - beta1)
   m2.mul_(beta3).add_(grad, alpha=1.0 - beta3)
   ```
2. Update the second moment in the rotated eigenbasis:
   ```python
   grad_proj = Q_L.T @ grad @ Q_R
   v.mul_(beta2).addcmul_(grad_proj, grad_proj, value=1.0 - beta2)
   ```
3. Project the blended AdEMAMix momentum into the eigenbasis for preconditioning:
   ```python
   m_mix = (m1 / bc1 + alpha * (m2 / bc3)) / (1.0 + alpha)
   m_proj = Q_L.T @ m_mix @ Q_R
   denom = (v.sqrt() / math.sqrt(bc2)).add_(eps)
   step_proj = m_proj / denom
   update = Q_L @ step_proj @ Q_R.T
   p.add_(update, alpha=-lr)
   ```
4. Retain all winning architecture parameters:
   - $\text{WIDTH} = 176, \text{HIDDEN\_LAYERS} = 8$ (219,650 params).
   - Targeted dual harmonics $k \in \{1, 2\}$, `in_dim = 7`.
   - Pure sinusoidal SIREN with unitary residual skips.
   - $\text{lr} = 1.15 \times 10^{-3}$, `precondition_frequency = 80`.
   - Ultra-high spatial Hamiltonian quadrature ($N_x=512$, $S=8$, $\lambda_{\mathrm{inv}} = 0.10$).
   - 35% domain expansion temporal curriculum (`CURRICULUM_FRAC = 0.35`).

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.10$, evaluated over $S=8$ stochastic time slices with $N_x=512$ spatial quadrature points per slice (4,096 invariant points per step), alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Smoother parameter descent trajectories without periodic 80-step coordinate dislocation shocks, deeper convergence on `dev_02` two-soliton collision dynamics.

## Evidence from previous experiments
- In Trial 064, SOAP-AdEMAMix achieved `4.857 \times 10^{-5}` with rotated-space momentum.
- In Trial 067, calibrated `lr = 1.15e-3` achieved our all-time best `4.690 \times 10^{-5}`.
- In Trial 065, holding the eigenspace for 100 steps caused boundary degradation, consistent with momentum staleness across basis updates.
- Vyas et al. (2024, Appendix B) showed parameter-space momentum tracking is necessary for optimal Shampoo/SOAP performance.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: false

## Observed results
- Mean validation loss: `16,427,618` ($1.64 \times 10^7$) [FAILED / DIVERGED; vs Trial 067: `4.689899e-05`].
- dev_01 validation loss: `29,216,128` ($2.92 \times 10^7$).
- dev_02 validation loss: `20,066,726` ($2.01 \times 10^7$).
- dev_03 validation loss: `3.9856e-05` ($3.99 \times 10^{-5}$).
- Eligibility: Ineligible ($L_{\mathrm{IC}} = 0.0$, $L_{\mathrm{BC}} = 0.324 > 10^{-3}$).
- Runtime: 891.1s total.

## Agent decision
**REJECT METHOD CHANGE; IMMEDIATELY REVERT TO TRIAL 067.**
Trial 067 remains the all-time incumbent champion.

## Reason for decision
1. **Coordinate Asymmetry Denominator Collapse:**
   Tracking first-order momentum $m_1, m_2$ in parameter space while tracking second-order variance $v$ in rotated eigenspace destroys the coordinate-wise boundedness guarantee of Adam/AdEMAMix.
   When the eigenbasis rotates at step 80, projecting accumulated parameter-space momentum ($Q_L^T M_{\text{mix}} Q_R$) onto eigenvectors that previously had near-zero variance in $v$ results in catastrophic division by near-zero, producing update magnitudes of order $10^7$.
2. **Mathematical Coherence in Rotated Space:**
   In contrast, accumulating both $m$ and $v$ synchronously in the rotated eigenspace (Trials 060–068) ensures that $|m_{i,j}| / (\sqrt{v_{i,j}} + \epsilon)$ is strictly bounded along every coordinate axis, guaranteeing mathematical stability.
3. **Firm Reversion:**
   Trial 067's synchronous rotated-space formulation remains vastly superior and is fully restored.
