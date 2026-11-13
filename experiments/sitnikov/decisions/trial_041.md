# Experiment 041: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 038, using Tanh on both encoders ($U, V$) achieved our all-time lowest mean validation loss (0.0002937), demonstrating superior performance on smooth, low-amplitude orbits (dev_01, dev_03, dev_05). In Trial 040, removing Tanh from both encoders achieved our all-time lowest worst-case error (0.0006257, a 24% reduction on dev_08), demonstrating superior performance on high-amplitude, high-eccentricity dynamics where uncompressed features prevent derivative attenuation.

In Hamiltonian celestial mechanics, the state vector consists of two fundamentally distinct physical quantities:
1. Position $z(t)$, which is inherently bounded and smooth (well-modeled by saturating, regularized Tanh features);
2. Velocity $v(t) = \dot{z}(t)$, which requires high dynamic range and steep gradients during primary pericenter passages (well-modeled by uncompressed linear Fourier synthesis).

In the Modified PINN gating equation:
$h_l = (1 - z_l) \odot U + z_l \odot V$
the gating units $z_l \in [-1, 1]$ interpolate between $U$ and $V$. We hypothesize that configuring an asymmetric hybrid encoder:
$U = \tanh(W_u x + b_u)$ (bounded displacement basis)
$V = W_v x + b_v$ (uncompressed kinematic/dynamic basis)
will allow the gating units to select bounded regularized features during smooth trajectory phases ($z_l \to 0$) and uncompressed linear features during rapid pericenter acceleration ($z_l \to 1$), uniting the strengths of Trial 038 and Trial 040.

## Proposed method change

Architecture modification:
- In `ModifiedPINN`:
  - `self.u_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
  - `self.v_proj = nn.Linear(n_feats, WIDTH)` (uncompressed linear)
  - `self.in_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
  - Two gating stages ($z_1, z_2$) with `WIDTH = 192` (84,874 parameters).
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Loss weighting: Asymmetric IC annealing from Trial 034/038 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (Cosine Annealing), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against Trial 038 (mean 0.0002937, worst 0.0008230) and Trial 040 (mean 0.0003100, worst 0.0006257). The asymmetric hybrid encoder aims to capture both advantages simultaneously: maintaining low mean loss (~0.00028) while preserving the sub-0.00065 worst-case ceiling on dev_08.

## Evidence from previous experiments

Trial 038 showed the power of Tanh encoders on smooth cases. Trial 040 showed the power of Linear encoders on high-eccentricity cases. Hybrid encoder synthesis explores the physical phase-space duality between bounded position and unbounded acceleration.

## Observed results

All 10 development cases completed (87.0 s each, ~19.6k steps, 84,874 parameters). The hybrid asymmetric encoder achieved strong individual milestones:
- dev_05 broke into single-digit nano-scale precision: 9.57e-09 (all-time campaign best for dev_05!).
- dev_04 achieved an all-time best of 1.63e-05 (Trial 038: 2.18e-05).
- Worst-case validation loss improved over Trial 038 from 0.0008230 to 0.0007796 (dev_08).
- Overall mean validation loss settled at 0.0003191 (Trial 038: 0.0002937, an 8.6% difference).
- Generalization was perfect: val/train ratio was 1.00 across all 10 cases; mean IC loss was 1.08e-08; standard deviation was 0.000267.

Physical and optimization explanation: When U is bounded in [-1, 1] by Tanh and V is uncompressed by Linear, the convex combination h_l = (1 - z_l) U + z_l V has asymmetric gradient scale properties: gradients flowing through the V branch are unattenuated, while gradients flowing through U are damped by (1 - U^2). Because the gating units z_l are initialized symmetrically around 0, the optimizer tends to assign more optimization updates to the unattenuated V branch. While this benefits localized velocity peaks, it slightly compromises the delicate harmonic cancellation in the symmetric U branch, leading to marginally higher mean residual across intermediate cases like dev_02 (0.000509 vs 0.000390). Symmetric Tanh encoders (Trial 038) maintain identical gradient scale across both encoders, preserving balanced dual-basis evolution.

## Agent decision

Reject / Retain Trial 038 as champion: While the hybrid encoder set impressive new records on dev_04 (1.63e-05) and dev_05 (9.57e-09) and beat Trial 038's worst case (0.000780 vs 0.000823), Trial 038's symmetric Tanh encoders deliver the lowest mean validation loss (0.0002937). Revert to symmetric Tanh encoders from Trial 038.

## Reason for decision

Trial 038 maintains lower mean validation error (0.0002937 vs 0.0003191). Symmetric activation across both encoders preserves reflection invariance in the dual-basis phase space.

## Next experiment

Trial 042: Learning Rate Magnitude Scaling (Testing LR0 = 8.0e-4 vs 1.0e-3 in Modified PINN).
In all trials, initial learning rate has been LR0 = 1.0e-3. The Modified PINN architecture contains multiplicative gating (1 - z) * U + z * V, which produces quadratic parameter interactions (the gradient with respect to U depends directly on z, and vice versa). In quadratic-interaction architectures, high initial learning rates can occasionally cause minor coordinate-wise overshooting before the gating units learn their primary phase-switching alignment. Testing a slightly moderated initial learning rate LR0 = 8.0e-4 (Cosine Annealing down to 1.0e-6) evaluates whether calmer initial step sizes allow the multiplicative gating parameters to coordinate more smoothly during early training. All other settings match champion Trial 038.
