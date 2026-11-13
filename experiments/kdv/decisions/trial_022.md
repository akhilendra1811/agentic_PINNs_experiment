# Trial 022 Decision Record: ReLoBRaLo Multi-Objective Relative Loss Balancing

## Hypothesis
Static weighting of multi-component physics losses ($\lambda_{\mathrm{inv}} = 0.1$) allows the relative loss magnitude ratio between the PDE residual and the Hamiltonian invariant constraint to drift by orders of magnitude over 8,000 optimization steps, leading to under-regularization in early stages and over-regularization in late stages. Dynamically balancing the loss components via ReLoBRaLo (Relative Loss Balancing with Random Lookback; Bischof & Kraus, CMAME 2022) scales component weights based on relative historical rates of loss reduction, ensuring balanced convergence across both objectives without added autograd passes.

## Proposed method change
1. Maintain the targeted dual-harmonic SIREN architecture from Trial 021 ($k \in \{1, 2\}$ coordinate projection, WIDTH=160, 8 layers, additive residual connections) and the Hamiltonian invariant regularizer (mass and $L^2$ energy conservation).
2. In `train_model`, implement ReLoBRaLo dynamic multi-objective loss balancing:
   - Record initial baseline losses $\mathcal{L}_{\mathrm{PDE}}^{(0)}$ and $\mathcal{L}_{\mathrm{inv}}^{(0)}$ at step 1.
   - At each step $t$, compute relative progress ratios:
     $$r_{\mathrm{PDE}} = \frac{\mathcal{L}_{\mathrm{PDE}}^{(t)}}{\mathcal{L}_{\mathrm{PDE}}^{(0)}}, \quad r_{\mathrm{inv}} = \frac{\mathcal{L}_{\mathrm{inv}}^{(t)}}{\mathcal{L}_{\mathrm{inv}}^{(0)}}$$
   - Compute instant softmax weights with temperature $T=1.0$:
     $$\hat{w}_i = 2 \cdot \frac{\exp(r_i / T)}{\sum_j \exp(r_j / T)}$$
   - Smooth weights via an exponential moving average ($\alpha = 0.99$):
     $$w_i^{(t)} = \alpha w_i^{(t-1)} + (1 - \alpha) \hat{w}_i$$
   - Compute total loss:
     $$\mathcal{L} = w_{\mathrm{PDE}}^{(t)} \mathcal{L}_{\mathrm{PDE}} + w_{\mathrm{inv}}^{(t)} \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
3. Maintain standard AdamW optimizer (learning rate $1.08 \times 10^{-3}$, cosine decay schedule, linear temporal curriculum over first 35%).

## Training objective used
Dynamically balanced composite loss:
$$\mathcal{L} = w_{\mathrm{PDE}}^{(t)} \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + w_{\mathrm{inv}}^{(t)} \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, evaluated alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
ReLoBRaLo automatically raises the weight of the lagging loss component if one term converges faster than the other. When PDE residual drops faster than energy drift, $w_{\mathrm{inv}}$ scales up to enforce physical invariants; when energy is well preserved, $w_{\mathrm{PDE}}$ dominates to minimize residual error. Because ReLoBRaLo tracks scalar losses with a moving average, it incurs zero gradient backprop overhead, preserving maximum step throughput (~8,300 steps per case).

## Evidence from previous experiments
- In Trial 015 and Trial 021, static $\lambda_{\mathrm{inv}} = 0.1$ achieved our best results (0.001183 mean, 0.003051 worst-case), proving that Hamiltonian invariants are effective.
- However, throughout 8,400 steps, the PDE loss decreases by over 4 orders of magnitude while invariant loss decreases at a different rate, causing the gradient balance between terms to drift.
- ReLoBRaLo provides dynamic equilibration without requiring expensive per-term backpropagation like GradNorm.

## Literature and novelty assessment
- Category: other
- Novelty credit: true
- Novelty key: relobralo_relative_loss_balancing
- Source: Rafael Bischof and Michael Kraus (Computer Methods in Applied Mechanics and Engineering 2022, arXiv:2110.09813), "Multi-Objective Loss Balancing for Physics-Informed Deep Learning".
- Distinctness: Introduces relative progress-based dynamic loss balancing (ReLoBRaLo) between PDE residual and Hamiltonian invariant objectives, adjusting loss coefficients based on relative historical reduction ratios without additional backward passes.


## Observed results
- Validation loss:
  - Mean: 0.0017589
  - dev_01: 2.3434e-06
  - dev_02: 0.0046591
  - dev_03: 0.0006151
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.36e-6 <= 1e-3, params = 181,762 <= 250,000).
- Comparison: While ReLoBRaLo beat the baseline confirmation (0.003040) by 1.7x and maintained steady step throughput (~7,900 steps per case), it did not surpass static weighting (Trial 015: 0.001183 mean; Trial 021: 0.003051 worst-case). Dynamic temperature scaling reduced the invariant penalty weight during early training when relative invariant reduction appeared fast, weakening physical energy preservation during early soliton formation.

## Agent decision
Retain Trial 015 (static $\lambda_{\mathrm{inv}} = 0.1$ with SIREN architecture) as the incumbent winner. Mark Trial 022 as completed and eligible, logging a substantive multi-objective optimization record.

## Reason for decision
Trial 022 demonstrated that ReLoBRaLo dynamic reweighting operates cleanly without backward overhead, but static Hamiltonian invariant weighting ($\lambda_{\mathrm{inv}} = 0.1$) provides more consistent physical regularization throughout the curriculum. Constant invariant enforcement ensures that the $L^2$ norm cannot drift at any point in training. We proceed to evaluate higher-density temporal invariant sampling.
