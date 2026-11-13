# Three-agent research workflow

The framework assigns literature research, implementation and mathematical criticism to specialised agents. In the native Antigravity implementation, a parent session invokes `researcher`, `coder` and `math-critic` sequentially. It stores a proposal, the implemented candidate, a mathematical review and the experiment outcome for each trial.

The implementation exists in the local research project’s `.agents/agents/` role definitions and `.agents/AGENTS.md` routing instructions. Its `experiment.py::candidate_gate` requires a researcher proposal and approving critic review before training; a deterministic verifier can reject the implementation even after an approving review. The available run folders contain actual proposals and mathematical reviews, not just blank templates. The parent performs native role invocation; there is no separate Python orchestration service.

[Role specifications](native_roles/) adapt that implemented division of work to the three problems in this repository. They describe the reusable responsibilities, rather than copying another campaign's physical setup. The earlier Sitnikov, 75-trial KdV and historical supersonic searches used an LLM-led experiment loop. Their numerical results remain evidence for those earlier arrangements.

| Responsibility | Inputs | Outputs |
|---|---|---|
| Scientific research agent | Literature, previous decisions, fixed protocol | One testable hypothesis, proposed change and expected effect |
| Coding and experimentation agent | Proposal, existing candidate and experiment interface | Implementation, training runs, metrics and factual failure records |
| Mathematical critic | Proposal, actual implementation and diagnostics | Derivations, physical/derivative checks, approval or specific repair requests |
| Parent and evaluator | Approved candidate and fixed data/budget | Controlled experiment, recorded outcome, feedback and method selection |

The critic reviews the implementation rather than accepting its description. It checks coordinate order, derivatives, initial and boundary constraints, conservation assumptions and what the numerical comparisons actually establish. Failed checks return to the coder; a changed implementation receives a new review. Distinct roles do not by themselves prove mathematical correctness.

## Reference-free method selection

Training uses sampled coordinates, governing equations and supplied initial/boundary data. The fixed evaluator measures physics residuals and constraint errors. Agents can change architectures, activation functions, optimisers, sampling and training objectives while leaving the evaluation contract fixed.

After selection, the method is frozen and retrained on evaluation cases. Numerical trajectories or Athena++ fields then measure accuracy. Reference arrays are excluded from agent-guided selection. KdV's final trapezoidal-quadrature method is a later benchmark-informed modification of the selected method, as described beside its results.

## Implemented numerical methods

- **Sitnikov 049:** learnable Fourier frequencies, modified gated PINN, scheduled initial-condition weights and Adam with matched first/second moment decay factors.
- **KdV 067:** periodic features, sinusoidal residual network, hard initial conditions, conservation penalties and SOAP–AdEMAMix with temporal curriculum.
- **Supersonic 069:** periodic sinusoidal residual network, initial-velocity fitting, stratified time sampling and staged equation weighting.
- **Supersonic 056:** Snake activations, random weight factorisation, FiLM, input skips, Adan/AdaBelief and a limited-memory SR1/Krylov cubic finish.

These use established numerical and learning methods. The research contribution is their exploration, implementation and empirical evaluation in controlled PINN campaigns. [Trial decisions](../experiments/supersonic_3d/decisions/README.md) and [internet logs](../research_logs/README.md) retain the distinction between literature ideas and measured outcomes.
