# Trial 001 Decision Record: Baseline Incumbent Confirmation

## Hypothesis
Replicating the frozen incumbent method from prior trial 46 under the locked KdV-B reference-free protocol will establish a valid, eligible baseline score across all three development initial conditions (dev_01, dev_02, dev_03).

## Proposed method change
No changes are made to the initial candidate source code. Trial 001 strictly evaluates the unchanged original frozen winner `baseline_trial46.py` as `candidate.py`, featuring an 8-layer residual MLP (width 160) with tanh activations, AdamW optimizer, cosine decay learning rate schedule, and a linear temporal curriculum.

## Training objective used
The training objective is the physics residual mean squared error plus weighted initial condition loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
where $\lambda_{\mathrm{IC}} = 1.0$, evaluated with 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each optimizer step, alongside 512 spatial IC points at $t=0$.

## Expected effect
The baseline model is expected to satisfy both eligibility requirements ($L_{\mathrm{IC}} \le 10^{-3}$ and periodic mismatch $\le 10^{-3}$) across all three development cases within the 300-second per-case computational budget, establishing the official reference-free benchmark for all subsequent exploration trials.

## Evidence from previous experiments
In the previous campaign, trial 46 was selected as the top-performing method due to its stable convergence, robust periodic feature formulation $(t, \sin(\pi x), \cos(\pi x), u_0, u_{0,x}/\pi)$, and effective temporal warm-up curriculum.

## Literature and novelty assessment
Trial 001 provides zero novelty credit (category: none, novelty_credit: false). It serves as the controlled scientific calibration baseline, verifying hardware execution on Apple Silicon Metal Performance Shaders (MPS), autograd through third-order spatial derivatives, and receipt logging before novel methodological exploration begins.

## Observed results
Trial 001 executed successfully across all three development cases in 891.07 seconds total (~297 seconds per case, ~8,550 optimizer steps per case on MPS).
- Mean validation loss: 0.0030397
- Case dev_01 validation: 3.0361e-06 (IC: 0.0, BC: 1.3569e-12)
- Case dev_02 validation: 0.0071730 (IC: 0.0, BC: 6.0808e-06)
- Case dev_03 validation: 0.0019431 (IC: 0.0, BC: 2.3056e-11)
- Strict eligibility: Fully satisfied. IC loss is exactly 0.0 across all cases (satisfying <= 1e-3); periodic boundary mismatch sum is <= 6.08e-06 across all cases (satisfying <= 1e-3).

## Agent decision
Accept and freeze Trial 001 as the official incumbent benchmark baseline. Retain its reference-free performance metrics (mean validation loss 0.0030397, worst-case dev_02 loss 0.0071730) as the target to beat for all subsequent exploration and exploitation trials.

## Reason for decision
Trial 001 provides reliable, hardware-verified replication of the incumbent method. The ansatz $u_0 + \tanh(\alpha t) \cdot \text{net}(t, x)$ enforces zero initial condition error identically at $t=0$, and periodic feature encoding enforces spatial boundary periodicity with high precision. Next trials can now systematically branch into novel activation functions and optimization techniques.
