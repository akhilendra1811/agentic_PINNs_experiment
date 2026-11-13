# Experiment 020: written research decision log

This is explicit written rationale, not private hidden chain-of-thought.

## Hypothesis

In Trials 001–019, gradient descent was conducted using full batches over all 500 coordinates at every step. While full-batch evaluation provides exact deterministic gradients of the continuous residual MSE, it constrains iteration throughput and may cause parameters to settle into the nearest shallow local basin. Subsampling random mini-batches of size B = 250 (50% of the training coordinates, drawn without replacement at each step) reduces per-step compute time (increasing total gradient updates from ~25k to ~35k+ within 87 s) while injecting mild stochastic gradient noise that can assist in escaping sub-optimal local minima.

## Proposed method change

Collocation point mini-batching:
- At each gradient step, randomly draw a subset of 250 points from the 500 training coordinates:
  `idx = torch.randperm(500, device=train_t.device)[:250]`
  `batch_t = train_t[idx]`
  `physics, ic = context.physics_components(model, batch_t, case)`
- Architecture unchanged: 2-block ResNet Fourier-PINN with width 192, 8 learnable Fourier frequencies, Tanh activations (77,962 parameters, champion architecture from Trial 017/019).
- Optimization unchanged: Adam with Cosine Annealing (lr0 = 1.0e-3, lr1 = 1.0e-6), gradient norm clipping (max_norm = 1.0), and annealed IC loss weight (1000 -> 100 over first 10% of budget).
- 11 progress snapshots + final snapshot (final snapshot evaluated on full 500 coordinates).

## Training objective used

L(θ) = R_batch(θ) + λ_ic(f) * I(θ), where
- R_batch(θ) = (1/250) Σ_{j ∈ B} [(dz/dt(t_j) - v(t_j))^2 + (dv/dt(t_j) + z(t_j)/(z(t_j)^2 + ρ(t_j)^2)^{3/2})^2] over a randomly sampled mini-batch B ⊂ {1..500} with |B| = 250 at each step, via `context.physics_components(model, batch_t, case)`;
- I(θ) = (z(0) - z0)^2 + (v(0) - v0)^2.
Loss weighting: physics weight 1.0 (constant). IC weight λ_ic(f) = 100.0 + 900.0 * max(0.0, 1.0 - f / 0.10). Adam learning rate follows Cosine Annealing lr(f) = 1e-6 + 0.5 * (1e-3 - 1e-6) * (1 + cos(pi * f)) over 87.0 s budget. Gradient updates clipped to max L2 norm of 1.0.

## Expected effect

Comparison against Trial 019 (full-batch 500, mean 0.0008855, worst 0.001994). If mini-batching increases step throughput and enhances stochastic exploration, mean validation loss will decrease further. If stochastic gradient variance destabilizes the delicate multi-period phase coherence, validation error will increase.

## Evidence from previous experiments

Trial 019 achieved our current champion score (0.0008855) with 25,659 full-batch steps. Mini-batching is standard practice in large-scale PINNs, and testing B=250 rigorously evaluates whether stochasticity benefits this specific 500-coordinate setup.

## Observed results

All 10 cases completed (87.0 s each, ~23.8k steps, 79,962 parameters). Mean validation loss degraded to 0.001450 (Trial 019: 0.0008855, a 64% degradation!), worst case rose to 0.003273 (dev_09; Trial 019: 0.001994, a 64% degradation!), std 0.00115, mean IC 1.09e-09.
Per case comparison with Trial 019 (full-batch 500):
- dev_01: 0.000175 (Trial 019: 6.89e-05) - worse
- dev_02: 0.001700 (Trial 019: 0.001040) - worse
- dev_03: 0.001640 (Trial 019: 0.000867) - worse
- dev_04: 0.000332 (Trial 019: 0.000123) - worse
- dev_05: 5.02e-06 (Trial 019: 1.39e-06) - worse
- dev_06: 0.000406 (Trial 019: 0.000206) - worse
- dev_07: 0.002410 (Trial 019: 0.001550) - worse
- dev_08: 0.002430 (Trial 019: 0.001550) - worse
- dev_09: 0.003273 (Trial 019: 0.001994) - worse
- dev_10: 0.002130 (Trial 019: 0.001450) - worse

All 10 out of 10 cases were unambiguously superior under full-batch evaluation. Furthermore, iteration throughput did not increase (~23.8k steps vs ~25.6k steps in Trial 019) because generating random permutations and index slicing added Python/memory overhead that erased any tensor arithmetic savings on the compact 500-point grid.

## Agent decision

Reject mini-batching completely. Firmly retain deterministic full-batch evaluation on all 500 coordinates.

## Reason for decision

In continuous trajectory fitting of physical ODEs, subsampling introduces stochastic phase jitter and temporal discontinuities across collocation points. Because 500 coordinates easily fit into MPS on-chip registers, full-batch evaluation provides true gradient descent with zero variance and higher actual step throughput.

## Next experiment

Trial 021: Loss Formulation Investigation: Log-Cosh / Huber Loss on Physics Residual. In standard MSE loss, squared residuals ((dz-v)^2 + (dv+F)^2) penalize large errors quadratically while having near-zero gradient for small errors. Near convergence, errors are O(1e-4), where MSE gradients become tiny. We will test replacing MSE with the smooth pseudo-Huber / Charbonnier loss:
L_phys = sqrt((dz-v)^2 + (dv+F)^2 + eps^2) - eps
with eps = 1e-4, which is quadratic for small residuals but linear for larger residuals, maintaining active gradient magnitude even as residuals shrink toward zero. All architecture and schedule elements from champion Trial 019 remain intact.
