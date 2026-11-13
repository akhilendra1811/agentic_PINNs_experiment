# Internet research log

## Post-freeze figure and metric reference — 2026-11-06

After Trial 069 was selected and frozen, consulted [De et al., *Physics Informed Neural Network for Multi-dimensional Turbulent Self-gravitating Flows*](https://arxiv.org/pdf/2610.32840v1) for the Figure 6 display and error definitions. The paper defines the signed field discrepancy as δ=log₂(f_PINN/f_Athena++) for density or velocity magnitude, displays three orthogonal faces of the 3D box, and reports signed mean, RMS, and maximum absolute δ. This source was used for **post-selection presentation and analysis only**; no paper numerical output or Athena++ reference result influenced the 75-trial search or finalist selection. Our plots and statistics identify their own grid, time, and sample domain so they are not confused with the paper's numerical values.

## Pre-campaign research — 2026-11-05

Objective: Find representations for multiscale turbulent initial conditions and spatial derivatives in PINNs, and identify later hard-IC options. Tool: web search. Queries: “Fourier features physics informed neural networks multiscale Wang Perdikaris 2021”; “SIREN implicit neural representations periodic activation Sitzmann 2020”; “hard initial condition physics informed neural networks exact imposition”.

Sources consulted: [Wang, Wang & Perdikaris, Fourier-feature networks for multi-scale PINNs](https://www.sciencedirect.com/science/article/pii/S0045782521002759); [Sitzmann et al., SIREN paper](https://arxiv.org/abs/2006.09661); [SIREN official implementation](https://github.com/vsitzmann/siren); [Cornell SciML hard-constraint overview](https://cvw.cac.cornell.edu/SciML/pinns/constraint-stage-2-hard-constraint-approach).

Findings: Fourier coordinate features can help represent multiple scales in PINNs; sinusoidal networks can represent signals and derivatives; exact constraints can be built into an output ansatz using a factor that vanishes at the constrained boundary. These are methodological ideas, not benchmark data.

Application: Trial 001 tests eight periodic harmonics in B's spatial encoding while retaining its other settings. Hard initial-condition enforcement is deferred because the supplied IC is a sampled turbulent field rather than an analytic expression.

## During Trial 001 — 2026-11-05

Objective: Identify a distinct next mechanism addressing temporal consistency or inefficient collocation, and understand PINN loss imbalance. Tool: web search. Queries: “physics informed neural networks causal training temporal curriculum Wang Sankaran Perdikaris 2022”; “PINN gradient pathology adaptive loss balancing Wang Teng Perdikaris 2021”; “residual based adaptive refinement PINN Wu Zhu Tan Kartha Lu 2023”.

Sources consulted: [Wang, Sankaran & Perdikaris, causal PINN training](https://arxiv.org/abs/2203.07404); [Wu et al., residual-based adaptive sampling](https://www.sciencedirect.com/science/article/pii/S0045782522006260); [Wang, Yu & Perdikaris, PINN neural tangent kernel analysis](https://www.sciencedirect.com/science/article/pii/S002199912100663X).

Findings: A causal training objective emphasizes earlier-time convergence before later-time residuals. Residual-based sampling reallocates points to large-error regions. PINN loss components can converge at disparate rates. These are methodological findings only; none supplies reference solutions for this benchmark.

Application: Candidate directions for later trials, pending Trial 001 results. No change to the active Trial 001 candidate.

## During Trial 002 — 2026-11-05

Objective: Examine alternatives for the persistent IC fit problem and understand why simply extending harmonics might fail. Tool: web search. Queries: “Fourier feature networks high frequency frequency bias PINN optimization multiscale Fourier features paper”; “physics informed neural networks hard initial condition turbulence velocity field neural ansatz initial conditions”; “self-adaptive physics informed neural networks loss weights McClenny Braga-Neto 2020”.

Sources consulted: [Tancik et al., Fourier Features Let Networks Learn High Frequency Functions](https://proceedings.neurips.cc/paper/2020/file/55053683268957697aa39fba6f231c68-Paper.pdf); [Wang, Wang & Perdikaris, multiscale Fourier feature PINNs](https://arxiv.org/abs/2012.10047); [McClenny & Braga-Neto, self-adaptive PINNs](https://arxiv.org/abs/2009.04544).

Findings: Fourier feature bandwidth changes the learning bias, but adding features alone need not overcome compute and loss-balancing limits, as Trial 001 suggests. Self-adaptive weighting offers a different mechanism to focus optimisation on difficult regions. This is a hypothesis for this campaign, not a conclusion from the sources about this benchmark.

Application: Consider an adaptive IC/physics balance or spatial sampling trial after the current causal curriculum result. No active candidate changed during Trial 002.

## After Trial 019 — 2026-11-05

Objective: Explain the steep IC-versus-physics tradeoff in Trials 017–019 and identify optimisation methods that address opposing task gradients. Tool: web search. Queries: “physics informed neural network initial conditions exact imposition learned initial condition interpolant data”; “PINN gradient conflict multi task learning physics initial condition gradient surgery PCGrad paper”; “physics informed neural networks separate initial condition network temporal correction ansatz”.

Sources consulted: [Yu et al., Gradient Surgery for Multi-Task Learning](https://papers.neurips.cc/paper_files/paper/2020/file/3fe78a8acf5fda99de95303940a2420c-Paper.pdf); [Liu et al., Conflict-Averse Gradient Descent](https://proceedings.neurips.cc/paper/2021/file/9d27fdf2477ffbff837d73ef7ae23db9-Paper.pdf); [exact temporal continuity in sequential PINNs](https://www.sciencedirect.com/science/article/pii/S0045782524004535); [causally enhanced IC soft constraints](https://cpb.iphy.ac.cn/en/article/doi/10.1088/1674-1056/adacd0).

Findings: PCGrad projects a task gradient when it conflicts with another task gradient; CAGrad studies conflict-averse updates. The observed Trial 017–019 tradeoff is compatible with gradient conflict but does not prove that conflict is present. Exact temporal constraints and initial derivative constraints are other possible directions, subject to the sampled-IC and fixed-physics contract.

Application: Trial 020 will test a two-task PCGrad-style projection between the canonical weighted PDE loss and IC relative MSE, using only authorised training batches and keeping the same model and evaluator. This is an adaptation, not a reproduction of a PINN-specific result.

## After Trial 034 — 2026-11-06

Objective: Review shock-aware PINN objectives for future mechanisms without changing the locked canonical evaluator. Tool: web search. Queries: “physics informed neural networks compressible Euler shocks entropy viscosity loss weak form”; “physics informed neural networks Euler Poisson conservation weak form”.

Primary sources consulted: [Weak and entropy physics-informed neural networks for conservation laws](https://arxiv.org/abs/2603.24819); [Physics-Informed Neural Networks for Parametric Compressible Euler Equations](https://arxiv.org/abs/2307.14045); [Physics-informed neural networks for shock capturing in inviscid flows around an airfoil](https://arxiv.org/abs/2607.08130).

Findings: Recent conservation-law PINN work motivates weak/control-volume objectives and entropy or artificial-viscosity treatments near discontinuities. Those papers do not establish benefit on this periodic, self-gravitating 3D benchmark. An auxiliary weak-form loss could be tested while retaining the locked strong-form evaluator; changing the Euler-Poisson equations or validation remains prohibited.

Application: Hold as a future research direction. Trial 034's mass penalty was an integral constraint, but did not implement a full weak-form flux balance.

## Before Trial 039 — 2026-11-06

Objective: Look for a primary source on local velocity-increment or structure-function losses for turbulent PINN initial conditions. Tool: web search. Queries: “arxiv turbulence neural network structure function loss velocity increments physics informed initial conditions”; “arxiv neural turbulence structure function loss local velocity increments training”.

Relevant primary context: [NSFnets: Physics-informed neural networks for the incompressible Navier-Stokes equations](https://arxiv.org/abs/2003.06496) discusses PDE and initial-condition losses, but does not validate the proposed local-increment loss on this problem. The search did not identify a direct match for the precise Trial 039 objective.

Finding and application: Treat local velocity increments as an independent campaign hypothesis about IC spatial structure. Trial 039 uses only authorized IC coordinates and targets; no external turbulence field or protected reference is used. No claim of publication originality follows from this limited search.
