# Supersonic Euler–Poisson research campaigns

## Physical setup and evaluation

The experiments use periodic 3D isothermal self-gravitating flow, generated turbulent velocity initial conditions and the interval t∈[0,0.8]. Agents train on coordinates and physical constraints, without Athena++ field labels. After method selection, frozen networks are retrained and compared with independently generated numerical fields. The density metric RMSδρ uses δρ=log₂(ρ_PINN/ρ_Athena); relative L2 is a separate norm ratio.

P is a locally trained paper-style baseline, not a published checkpoint. The original and newer campaigns differ in their selection policies and must be considered separately.

## Original 75-trial search

The numbered search uses 750 seconds per fit. Candidates and P/B/W baselines are then compared at 1,800 seconds. Trial 069 wins among methods satisfying IC relative L2≤0.25, with finalist validation score 0.12300614 and IC error 0.23536287. Its [decision](decisions/campaign75/trial_069.md) combines stronger Poisson coupling with early/middle/late collocation quotas 31.25%/25%/43.75%.

The selected representation has width 256, ten residual sine blocks, three axial Fourier harmonics and a five-component output. Density is represented positively as ρ₀ exp(clamp(t·raw_density,−4,4)). Adam first fits the initial velocity for 20% of training, then introduces equation residuals with staged weighting. The final physics weights are 3.5 for continuity, 7.5 for momentum and 6 for Poisson; IC relative-MSE weight rises to 33. Gradients are clipped at 0.5.

The campaign investigated harmonic features, sinusoidal activations, residual depth, hard density construction, optimisation and curriculum changes. All [75 written records](decisions/README.md) preserve the individual hypotheses and outcomes.

### Three physical-seed comparison

Both 069 and P are retrained from fresh weights for approximately 1,800 seconds per physical case. These are supersonic amplitude-1.1 cases with one fit per method/seed, scored at t=0.8 on the full 256³ grid.

| Physical seed | Trial 069 RMSδρ | Local P RMSδρ |
|---|---:|---:|
| 419 | 0.365740 | 0.450338 |
| 733 | 0.443737 | 0.526555 |
| 947 | 0.377685 | 0.462804 |
| Mean | 0.395721 | 0.479899 |

The reduction calculated from the means is 17.54%. Seed 733 has IC relative L2≈0.2731 and fails the original 0.25 eligibility condition. Athena++ grid dependence remains visible between 128³ and 256³, so these are finite-resolution comparisons.

## Newer 60-trial search

The search closes 60 attempts: 58 finite fits and two numerical/execution failures, 015 and 041. Each numbered fit has a 750-second budget. Physical seed 82 and training seed 823001 define this search. The fixed score combines early/middle/late equation residuals with global relative IC MSE; selection uses minimum finite score without the earlier IC gate.

| Research block | Approaches |
|---|---|
| Optimisation | RAdam, AdaBelief, Adan, matrix/gradient preconditioning, mixing and averaging |
| Activation and representation | Snake, ISRU, separable networks, polynomial features, input skips, random weight factorisation and FiLM |
| PINN training | Equation/loss balancing, hard constraints, sampling and full-pool finishing |
| Classical optimisation, trials 051–060 | BFGS Dogleg, SR1 Steihaug trust regions, spectral gradient, Anderson acceleration, compressed Levenberg–Marquardt, SR1/Krylov cubic regularisation, inexact Newton–CG, proximal point, block BFGS and DFP |

### Finalists and selected Trial 056

The three shortlisted candidates 054/053/056 and P/B/W each receive fresh 1,800-second fits:

| Method | Fixed validation score |
|---|---:|
| P | 0.19061710 |
| B | 0.55461895 |
| W | 1.06084077 |
| Trial 054, safeguarded Anderson | 0.10604834 |
| Trial 053, spectral gradient | 0.10566741 |
| **Trial 056, SR1/Krylov cubic** | **0.10566120** |

The small margin between 056 and 053 is a single-fit selection outcome. Trial 056 has 462,405 parameters: width 256, six Snake hidden activations, 19 periodic/time features, input skips, random weight factorisation and time-conditioned FiLM.

Its first half uses Adan for hidden weight directions and unrectified AdaBelief for auxiliary parameters, drawing 1,024 PDE and 1,024 IC samples per update. The second half uses full-pool loss evaluations with an eight-pair limited-memory SR1 Hessian approximation and a Krylov subspace of at most six dimensions. A projected cubic model is solved with a small CPU float64 eigen/secular calculation; actual/predicted reduction controls acceptance and cubic strength. This is a low-dimensional approximation, not an exact full-Hessian solver. At the finalist budget, 71 of 92 cubic attempts are accepted.

### Two-hour numerical evaluation

After selection, 056 and P are each trained for 7,200 seconds with paired training RNGs 823001/823002/823003 on physical IC seed 104729. The means and sample SDs are in the [experiment README](README.md); all six full-grid numerical records are in `results/campaign60/`. Training-seed variation on this one IC does not measure physical-case variation.

Full-grid density relative L2 is 0.341969 for 056 versus 0.372813 for P; density RMS log₂ is 0.411362 versus 0.465419. Extreme-density and extreme-speed subsets are retained in the numerical results because global means can hide local errors.

The separate one-training-seed five-field table includes potential and individual velocity components. Potential errors use full-volume mean alignment; display slices use slice-mean centring. Its density RMS values differ slightly from the three-seed extended outputs, so the aggregate comparison above consistently uses the extended outputs. Historical 069 on physical seed 419 is not directly ranked against 056 on seed 104729.

## Observations

Lower residual loss, tighter IC fitting and lower numerical field error can move in different directions. The classical experiments also trade stochastic-update throughput against expensive full-pool evaluations. The trial records report rejected steps, numerical failures and improvements separately; these are essential for interpreting which combinations merit further experiments.
