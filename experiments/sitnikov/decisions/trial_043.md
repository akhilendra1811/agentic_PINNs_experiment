# Experiment 043: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trial 038, our champion Modified PINN architecture (dual feature encoders $U, V$ with multiplicative convex gating $h_l = (1 - z_l) \odot U + z_l \odot V$) achieved our all-time best mean validation loss of 0.0002937 using `WIDTH = 192` (84,874 parameters).

In Trial 039, we saw that increasing architectural depth to 3 gating stages slowed down second-derivative autograd throughput by 18%, degrading optimization within the fixed 87-second training limit. In contrast, increasing hidden layer width preserves the shallow 2-stage depth while expanding the parallel subspace dimensionality across which the Fourier modes in $U$ and $V$ are combined and filtered.

Expanding hidden layer width from `WIDTH = 192` to `WIDTH = 224` (a 16.7% width expansion) increases model capacity from 84,874 to 113,354 parameters (comfortably within the 250,000 parameter budget). In high-eccentricity Sitnikov IVPs (e.g. dev_07, dev_08), the trajectory requires synthesizing sharp, asymmetric accelerations while maintaining smooth turning points. 224 channels provide 32 additional orthogonal degrees of freedom per layer to disentangle competing harmonic frequencies without incurring depth-related autograd slowdowns.

## Proposed method change

Architecture width modification:
- In `ModifiedPINN`:
  - Set `WIDTH = 224`.
  - Maintain 2 gating stages ($z_1, z_2$) with symmetric Tanh encoders:
    `self.u_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
    `self.v_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
    `self.in_proj = nn.Sequential(nn.Linear(n_feats, WIDTH), nn.Tanh())`
    `self.z1 = nn.Sequential(nn.Linear(WIDTH, WIDTH), nn.Tanh())`
    `self.z2 = nn.Sequential(nn.Linear(WIDTH, WIDTH), nn.Tanh())`
    `self.out_proj = nn.Linear(WIDTH, 2)`
- Total parameters: 113,354.
- N_FREQ = 8 with domain-orthogonal initialization $\omega_k = k / 3.0$.
- Loss weighting: Asymmetric IC annealing from Trial 034/038 (2000 -> 10 over first 20% of budget, 10 thereafter).
- Optimizer settings: Adam with betas=(0.9, 0.99), unified parameter group at lr0=1e-3, lr1=1e-6 (reverting Trial 042), gradient norm clipping (max_norm = 1.0) over 87.0 s budget.
- Full batch on all 500 training points every step.
- 11 progress snapshots + final snapshot.

## Training objective used

L(θ) = R(θ) + λ_ic(f) * I(θ), where
- R(θ) = (1/500) Σ_i [(dz/dt(t_i) - v(t_i))^2 + (dv/dt(t_i) + z(t_i)/(z(t_i)^2 + ρ(t_i)^2)^{3/2})^2] over all 500 training points via `context.physics_components`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) dynamically scheduled as λ_ic(f) = 10.0 + 1990.0 * max(0.0, 1.0 - f / 0.20), starting at 2000.0 and decaying linearly to 10.0 over the first 20% of training time, remaining constant at 10.0 thereafter. Adam optimizer configured with betas=(0.9, 0.99) with unified parameter group at lr0=1e-3, lr1=1e-6. Gradient updates clipped to max L2 norm of 1.0. Full batch on all 500 training points every step.

## Expected effect

Comparison against champion Trial 038 (mean 0.0002937, worst 0.0008230). Wider representations should enhance parallel harmonic feature mixing, targeting mean validation loss below 0.00026 while maintaining high optimization throughput (>19,000 steps).

## Evidence from previous experiments

In Trial 009, increasing width from 128 to 192 gave an immediate boost. In the Modified PINN architecture, evaluating width 224 tests the capacity ceiling under our fixed 87-second compute budget.

## Observed results

All 10 development cases completed (87.0 s each, ~19.1k steps, 113,354 parameters). Sizing width to 224 yielded solid performance:
- Worst-case validation loss improved over Trial 038 from 0.0008230 to 0.0006879 (dev_08, a 16.4% reduction in worst-case bottleneck error!).
- All 10 cases achieved sub-0.00069 precision (dev_01: 5.28e-06, dev_02: 0.000433, dev_03: 0.000250, dev_04: 2.39e-05, dev_05: 1.25e-07, dev_06: 0.000327, dev_07: 0.000552, dev_08: 0.000688, dev_09: 0.000242, dev_10: 0.000615).
- However, mean validation loss settled at 0.0003137, which is slightly above Trial 038's 0.0002937 (+6.8%).
- The throughput was ~19,116 steps per case, compared to ~20,433 steps in Trial 038 (a 6.4% throughput reduction due to the 33% increase in weight matrix sizes from 192^2 to 224^2).

Physical and optimization explanation: While 224 channels provide extra representation capacity that relieves the dev_08 turning-point bottleneck (0.000823 -> 0.000688), the 6.4% throughput reduction means the network executes ~1,300 fewer gradient steps within the 87.0 s limit. For the majority of cases, 192 channels are already fully expressive, and those extra 1,300 optimization steps allow the optimizer to descend deeper into the terminal loss basin. WIDTH = 192 represents the optimal sweet spot between parameter expressivity and step throughput.

## Agent decision

Reject / Retain Trial 038 as champion: While width 224 demonstrated improved worst-case error on dev_08 (0.000688), Trial 038 with WIDTH = 192 achieves the lowest mean validation loss (0.0002937) with superior optimization throughput. Revert to WIDTH = 192.

## Reason for decision

Mean validation loss was lower in Trial 038 (0.0002937 vs 0.0003137). Width 192 yields superior step throughput within the fixed 87-second window.

## Next experiment

Trial 044: Gradient Clipping Threshold Tuning (Testing MAX_GRAD_NORM = 0.5 vs 1.0 in Modified PINN).
In all trials since Trial 015, gradient clipping has used max_norm = 1.0. In the Modified PINN architecture, multiplicative gating naturally bounds the output scale of each layer, and domain-orthogonal frequencies prevent high-frequency gradient spikes. However, during early training under IC_W = 2000, gradient norms can reach values near 1.0. Testing a tighter clipping threshold max_norm = 0.5 will restrict maximum parameter step updates to a narrower radius, potentially preventing transient trajectory drift during the first 20% of training while the IC weight is high. All other settings match champion Trial 038 (WIDTH = 192, 2 stages, symmetric Tanh encoders).
