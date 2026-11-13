# Methods and the status of the agent framework

## What the code implements

The source repositories implement an external LLM-led experiment loop around fixed Python evaluation code. The LLM reads instructions and trial logs, writes a hypothesis and method change into `decision.md`, edits `candidate.py`, invokes the harness, reviews results, and records an acceptance/rejection decision. The harness records metrics and source snapshots, enforces protocol checks, and freezes a selected method. Neural networks are trained with new weights per physical case.

The intended responsibilities are scientific hypothesis generation/literature research, implementation/experimentation, and independent mathematical criticism. The inspected code does not contain a deployed three-agent router, separate critic process, independently authenticated critic role or measured comparison between single-agent and three-agent operation. These responsibilities are a conceptual design; the archived campaign evidence supports an LLM performing multiple roles and a separate deterministic/owner evaluation path. Independence of the numerical evaluator does not establish independence of a mathematical critic.

| Role | Concrete evidence | Implementation limit |
|---|---|---|
| Scientific hypotheses and literature | `instructions.md`, `internet_use.md`, pre-run decision sections; novelty/mechanism records in newer campaigns | Written claims about literature are not validated literature replications; internet access varies by campaign |
| Coding and experiments | `candidate.py` functions `build_model` / `train_model`; `experiment.py` or `engine/experiment.py`; trial snapshots, timings, parameter counts and metrics | External LLM session supplies the iterative control; the harness is not itself a scientific agent |
| Criticism and verification | Post-run decision sections; derivative/finite-gradient and accounting checks; source-hash checks and protected evaluators | No evidence of a separately deployed mathematical-critic agent for all trials; historical rationales contain hypotheses and overstatements |
| Independent numerical assessment | Sitnikov `protected_evaluation/evaluate.py`; KdV protected evaluator and comparison runners; Euler owner-evaluation scripts | Intended owner-only access must be enforced externally; a directory name alone is not a security boundary |

The original Sitnikov report explicitly describes `/goal` as a natural-language instruction to the external LLM rather than a Python orchestrator. Read the frozen source links in [sources.json](../reproducibility/sources.json) for reproducible implementation context.

## Selected representations and algorithms

| Method | Representation | Training method and scope |
|---|---|---|
| Sitnikov 049 | Eight learnable Fourier frequencies initialised at k/3; width-192 modified PINN with two gating stages; 84,874 parameters; outputs position and velocity | Adam β=(0.99,0.99), cosine LR 10⁻³→10⁻⁶, IC weight 2000→10 during first 20% of time, gradient clipping 0.5, full 500-point training batch; ≈87 s/case |
| Historical cosine KdV 046 | Width 160, 8-layer residual tanh representation, 181,442 parameters; inputs time, periodic sin/cos, initial state and its derivative; exact IC through a learnable temporal envelope | AdamW, expanding time support and LR schedule. The 200k runner uses a step-based 35% curriculum, unlike the original time-based 30-minute schedule |
| Exploratory KdV 067 | Width-176 sinusoidal representation, 219,650 parameters; periodic features and hard IC | SOAP–AdEMAMix preconditioning, LR 1.15×10⁻³, precondition frequency 80, 35% temporal curriculum, Hamiltonian regulariser weight 0.10 with 512 spatial points × 8 time slices. The 4.68990×10⁻⁵ score is development residual loss, not solution relative L2 |
| Historical Euler 069 | Periodic residual PINN; frozen `ResPINN` implementation | Adam with time/LR scheduling; approximate 30-minute transfer evaluations and separate longer-budget evaluations. Do not import the newer 056 optimiser into this campaign |
| New Euler 056 | 462,405 parameters; width 256, six Snake hidden activations; 19 features from three axial Fourier harmonics and time; repeated input skips, random weight factorisation and time-conditioned FiLM; positive density transform | First half: Adan on hidden directions, unrectified AdaBelief on auxiliary parameters, 1,024 PDE + 1,024 IC samples/update. Second half: eight-pair limited-memory SR1 with ≤6-dimensional Krylov cubic model and actual/predicted reduction control. The small projected solve is CPU float64; this is not an exact full-Hessian solver |

[Verbatim frozen method snapshots](source_snapshots/) are for inspection. They depend on their original harness contexts and are not standalone training packages. The live `candidate.py` in a research branch can be the final attempted method rather than its selected winner: use `runs/selected_candidate.py` and its frozen hash.

The newer three-run KdV follow-up uses trapezoidal conservation quadrature. It retains the parent architecture/optimizer but has a distinct source hash and follows benchmark-based diagnosis. It is presented separately from the reference-free selection. Its original file names and historical wording are preserved in the evidence archive.

## Reference-free selection

Search uses governing equations, initial/boundary conditions, fixed collocation validation and protocol constraints. Numerical references are reserved for post-selection scoring. The purpose is to investigate discovery where trusted interior labels are unavailable, rather than optimise a validation set of known answers.

Sitnikov scores two first-order ODE residuals plus 100×IC error on fixed validation coordinates. Historical KdV scores the fixed PDE/IC objective and separately checks periodic eligibility. Historical Euler has an IC relative-L2 eligibility condition of 0.25. New Euler 056 instead wins by minimum finite total score: weighted early/middle/late PDE residual plus global relative IC MSE, with no diagnostic eligibility gate. These policies must remain distinct.

A finite sample of a differential equation is not a stability certificate. Residual integration, stiffness, trajectory sensitivity, unsampled errors, loss imbalance and finite precision can all break the connection between a lower residual and a better solution. Conservation checks, derivatives, IC tests and reference-grid comparisons improve the evidence but do not replace a proved error bound.

## Original decision logs

[Selected records](../reports/decisions/) are reproduced verbatim with their provenance. Historical superlatives and causal explanations are source statements, not endorsed conclusions. Full trial histories remain at the frozen source commits; this repository carries ledgers and selected decisions instead of duplicating every run.
