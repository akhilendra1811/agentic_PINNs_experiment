# Experiment 030: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In all trials since Trial 017, the 8 learnable Fourier frequencies (`self.omega`) were optimized within the same Adam parameter group as the network weights and biases, using lr0 = 1.0e-3. However, frequency parameters scale the temporal input directly inside trigonometric basis functions: $\sin(\omega_k t)$ and $\cos(\omega_k t)$. In celestial mechanics, a perturbation $\Delta \omega$ accumulates temporal phase discrepancy linearly with time: $\Delta \phi(t) = t \cdot \Delta \omega$. Over our domain $t \in [0, 6\pi]$, at the boundary $t = 6\pi \approx 18.85$, a small frequency change $\Delta \omega = 0.05$ produces an orbital phase shift of nearly a full radian ($\approx 0.94$ rad), shifting crests into troughs. Consequently, early noisy gradients under a full lr0 = 1.0e-3 cause wild frequency jitter and premature detuning before the network can properly shape the trajectory envelope. Assigning `self.omega` to a dedicated parameter group with a moderated learning rate ($\text{lr}_\omega = 0.3 \times \text{lr}_\text{weights}$, starting at $3.0 \times 10^{-4}$ and annealing to $3.0 \times 10^{-7}$) will stabilize frequency adaptation, enabling smooth phase-tracking while allowing spatial weights to settle quickly.

## Proposed method change

Architecture & Optimizer parameter group separation:
- In `train_model`, divide parameters into two groups:
  1. `weights`: all parameters excluding `model.omega`, initialized at `lr = 1.0e-3`.
  2. `frequencies`: `[model.omega]`, initialized at `lr = 3.0e-4` (0.3x scaling).
- Both groups follow the same Cosine Annealing schedule proportionally:
  - $\text{lr}_\text{net}(f) = 10^{-6} + 0.5 \times (10^{-3} - 10^{-6}) \times (1 + \cos(\pi f))$
  - $\text{lr}_\omega(f) = 3 \times 10^{-7} + 0.5 \times (3 \times 10^{-4} - 3 \times 10^{-7}) \times (1 + \cos(\pi f))$
- Architecture: Highway Input Injection ResNet Fourier-PINN with width 192, 8 learnable Fourier frequencies, single-layer residual branches, Tanh activations (84,490 parameters, identical to Trial 029).
- Loss weighting: Asymmetric IC annealing from Trial 029 (2000 -> 50 over first 15% of budget, 50 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 50.0 + 1950.0 * max(0.0, 1.0 - f / 0.15), starting at 2000.0 and decaying linearly to 50.0 over the first 15% of training time, remaining constant at 50.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with separate parameter groups: network weights at lr0=1e-3, lr1=1e-6; omega frequencies at lr0=3e-4, lr1=3e-7. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 029 (mean 0.0006638, worst 0.001170). Taming early frequency volatility should prevent phase distortion across late times ($t > 3\pi$), particularly benefiting the more non-linear high-eccentricity cases (dev_08, dev_09, dev_10), aiming to push worst-case error below 0.0010 and improve mean validation loss toward 0.00060.

## Evidence from previous experiments

Trial 017 showed that making frequencies learnable reduced validation loss from 0.001787 to 0.001181 (a 34% drop). Trial 023 showed that initializing frequencies to physical harmonics without smooth learnability degraded performance, confirming that gradient updates on frequencies are delicate and high-leverage.

## Observed results

All 10 cases ran to completion (87.0 s each, ~23.3k steps, 84,490 parameters). The hypothesis was conclusively falsified:
- Mean validation loss degraded by nearly an order of magnitude: 0.006194 (Trial 029: 0.0006638).
- Worst-case validation loss suffered catastrophic late-stage divergence on dev_09, blowing up to 0.05358 (v/t ratio = 38.90). In dev_09, the validation loss was 0.00253 at snapshot 8 (step 17,181), but then diverged dramatically through 0.0062 -> 0.034 -> 0.054 over the final quarter of training.
- Every single development case degraded compared to Trial 029:
  - dev_01: 4.61e-05 (Trial 029: 7.03e-06) - 6.5x worse
  - dev_02: 0.001550 (Trial 029: 0.001080) - 44% worse
  - dev_03: 0.000767 (Trial 029: 0.000612) - 25% worse
  - dev_04: 0.000202 (Trial 029: 0.000149) - 36% worse
  - dev_05: 4.77e-06 (Trial 029: 1.04e-06) - 4.6x worse
  - dev_06: 0.000771 (Trial 029: 0.000593) - 30% worse
  - dev_07: 0.001990 (Trial 029: 0.000981) - 2x worse
  - dev_08: 0.001580 (Trial 029: 0.001170) - 35% worse
  - dev_09: 0.053580 (Trial 029: 0.001030) - 52x worse
  - dev_10: 0.001450 (Trial 029: 0.001020) - 42% worse

Physical and optimization explanation: In the Sitnikov problem, the true natural oscillation frequencies depend strongly on initial amplitude z0 and eccentricity e due to anharmonic potential distortion. Starting from a rigid uniform grid (0.5, 1.0, ..., 4.0), the frequencies MUST migrate significantly to align with the true physical harmonics. Throttling the frequency learning rate to 0.3x trapped the frequencies in an off-resonance state. The network's spatial weights were then forced to compensate for the phase mismatch by synthesizing high-frequency corrections through deep linear layers, causing spectral conflict and terminal divergence. Frequencies must be updated at full speed (lr = 1.0e-3) alongside the network weights.

## Agent decision

Reject: Separate lower learning rate for frequencies degraded all 10 cases and caused late-stage instability. Revert immediately to the unified parameter group with lr0 = 1.0e-3 from Trial 029.

## Reason for decision

Mean validation error increased from 0.0006638 to 0.006194, worst-case error jumped from 0.001170 to 0.05358, and all 10 cases performed worse. Frequencies require full learning agility to escape the uniform initialization and discover the true physical frequencies of each orbit.

## Next experiment

Trial 031: Kinematic vs Dynamic Residual Balancing (Independent Loss Weighting for dz/dt vs dv/dt). In the Sitnikov first-order ODE system, the residual consists of two distinct physical terms:
1. Kinematic residual: R_kin = (dz/dt - v)^2, enforcing exact velocity definition;
2. Dynamic residual: R_dyn = (dv/dt + z/(z^2 + rho^2)^(3/2))^2, enforcing Newton's gravitational law.
Currently, context.physics_components averages both terms equally. However, if kinematic consistency (z' = v) is not satisfied with high precision, the dynamic equation (v' = F(z, t)) acts on an uncoupled phase space. We hypothesize that weighting the kinematic loss term higher (lambda_kin = 2.0 vs lambda_dyn = 1.0) will tighten phase-space coupling, reducing orbital trajectory drift.
