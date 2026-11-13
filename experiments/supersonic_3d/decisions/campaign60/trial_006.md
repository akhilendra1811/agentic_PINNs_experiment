# Trial 006

Research metadata (locked on preparation): research_area=optimisation; parents=trial:5; kind=mechanism; mechanism_id=muon_matrix_momentum_preconditioning.

## Parent methods and evidence

Parent closed Trial 005, source only, leads at L_val 0.1719146514 (physics 0.0827775070, IC relative MSE 0.0891371444). Its early/middle/late totals were 0.2287528181/0.0338119019/0.0537667457, with 108 accepted PR+ updates and 288 complete full-pool evaluations. It improved Trial 003's 0.1791090870 and P's 0.1833311671; all were fresh fits. Retaining the successful full-pool finish while changing the initial hidden-matrix update gives a controlled next optimisation hypothesis. Trial 004 showed that lower physics alone need not lower total score. No trained weights or optimiser state are imported, and no method is filtered by IC or physical diagnostics.

## Novelty claim

Optimisation mechanism: Muon-style matrix momentum preconditioning through a quintic Newton–Schulz map, replacing elementwise belief scaling for the five hidden weight matrices. Credit Keller Jordan's Muon and the official update/reference implementation documented at https://docs.pytorch.org/docs/2.15/generated/torch.optim.Muon.html and the installed torch/optim/_muon.py. This is a local float32 variant, not exact bfloat16 package execution or a new published optimiser. AdaBelief remains for nonhidden parameters and retains its attribution/licence. The mechanism differs from earlier anticipation, variance rectification, belief variance, Lookahead trajectories and PR+ conjugate directions. Matrix spectrum redistribution is substantive; it is not a scalar learning-rate refinement.

## Hypothesis and proposed change

Hypothesis: redistributing hidden-matrix update singular directions improves the initial joint fit and supplies a better starting point for the same full-pool PR+ finish, lowering total validation loss. Select the five 128x128 hidden Linear weight matrices (81920 parameters); keep input/output weights and all biases (3845 parameters) on the parent's unchanged AdaBelief. Hidden weights use momentum b <- 0.95*b+0.05*g and Nesterov mixture 0.05*g+0.95*b, with lr=0.02, no decay. Normalize its matrix Frobenius norm with floor 1e-7, transpose to the smaller Gram dimension if needed, and apply five steps X <- 3.4445*X + (-4.775*XX^T + 2.0315*(XX^T)^2)*X. Map back and use the original shape adjustment sqrt(max(1,rows/cols)), equal to 1 for these square hidden matrices. All arithmetic stays float32 rather than the installed implementation's bfloat16 cast. Clear ALL model gradients before a stochastic/full-gradient evaluation, then update both disjoint optimiser partitions from the same gradients. Model, loss, sampler and PR+ code remain unchanged. Syntax, model/inner-AdaBelief/PR+ AST equality and CPU zero/scale/orthogonal-equivariance/one-step momentum checks passed on synthetic matrices, without PINN training. Risks include excessive matrix update size, numerical/precision differences and lower throughput from the extra matrix products.

## Training objective and setup

Fresh unchanged P sine model, seven Linear layers width 128, three spatial harmonics, 85765 parameters, Xavier weights/bias 0.01, startup_dt=0.05; density rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)). Training loss = continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, mean squared components weighted 1, same as Trial 005. First 80% of 750 seconds: hidden Muon-style updates above, auxiliary UnrectifiedAdaBelief(lr=0.001,betas=(0.9,0.999),eps=1e-12), no clipping/decay. Sample 1024 PDE/1024 IC with replacement per initial step as a control choice, not a cap. Then cache all 100000 PDE and 75000 IC points once by cycle sampling, through 25 microbatches up to 4096 PDE/3072 IC. Every complete full gradient and line value reuses those full pools with separate exact chunk-size weights; no new coordinates, perturbation, validation access or references. Preserve parent's PR+: nonnegative Polak–Ribiere beta, descent restart at slope >= -0.001*||g||^2, at most four Armijo trials (c1=1e-4, halving), initial alpha=1, accepted seed min(1,1.5*alpha), rejected seed floor 1e-8. Preserve the >12-second iteration reserve, four-second chunk checks/eight-second proposal checks and rollback on deadline. Record actual draws/evaluations, all CG/line/restart/nonfinite counts and history, and return both initial optimiser states plus PR+ state. Owner checkpoint/scorer unchanged. No fit for this ID preceded PRE completion.

## Expected outcome

Expect total L_val below Trial 005's 0.1719146514, potentially through lower early continuity or middle/late physics while preserving enough IC accuracy for a net gain. Matrix updates could instead underfit or overstep, so IC and physics improvements are not assumed. Higher total loss contradicts the net hypothesis even if any component or diagnostic improves. Read every score component/window, IC and density/mass/periodicity diagnostic, history, exact pool exposure, timing and run.log; compare useful initial/CG update counts because matrix overhead is included in the same budget. Selection uses only finite total L_val, with no IC/positivity/periodicity gates. Count and document numerical failures without rerunning the ID. One fit does not establish statistical significance or reference-trajectory accuracy, and float32 Muon is an explicitly disclosed adaptation.

## Observed results

Completed normally, return code 0. L_val 0.169099173828, physics 0.071517787810, IC relative MSE 0.097581386018, IC L2 0.312380194664. 85765 parameters, 738.294772 actual seconds within 750. 28908 initial updates and 112 CG attempts, 106 accepted; 173 line values, 15 restarts, zero nonfinite proposals. All 285 full-pool evaluations are reconciled against metadata: 58101792 PDE / 50976792 IC evaluations, 29701792 PDE / 29676792 IC draws and 36033 physics calls. No partial evaluation is needed to explain the totals. Required files, full diagnostics and run.log read; no execution error. Full records follow.

```json
{
  "metrics": {
    "L_val": 0.16909917382839523,
    "physics_weighted": 0.07151778781007577,
    "ic_relative_l2": 0.31238019466400146,
    "ic_relative_mse": 0.09758138601831945,
    "windows": {
      "early": {
        "continuity": 0.17296077109091995,
        "momentum": 0.022722903290867697,
        "poisson": 0.004715564015198933,
        "total": 0.2003992383969866
      },
      "middle": {
        "continuity": 0.01589302680048706,
        "momentum": 0.012203525380702702,
        "poisson": 0.004879985940847593,
        "total": 0.03297653812203735
      },
      "late": {
        "continuity": 0.01696130824515106,
        "momentum": 0.014785639889207933,
        "poisson": 0.011343009253775488,
        "total": 0.04308995738813448
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9942643046379089,
        "0.5": 0.9864622950553894,
        "0.8": 0.9849521517753601
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0057356953620910645,
        "0.5": -0.013537704944610596,
        "0.8": -0.015047848224639893
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10069422423839569,
        "0.5": 0.30840760469436646,
        "0.8": 0.5487011075019836
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2303967475891113,
        "0.5": 1.8609410524368286,
        "0.8": 2.8658523559570312
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4517337679862976,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.3113021850585938e-06
    },
    "window_weights": {
      "early": 0.2,
      "middle": 0.3,
      "late": 0.5
    },
    "time_windows": {
      "early": [
        0.0,
        0.2
      ],
      "middle": [
        0.2,
        0.5
      ],
      "late": [
        0.5,
        0.8
      ]
    },
    "warning": "Reference-free residual score, NOT numerical-solution accuracy"
  },
  "run_metadata": {
    "device": "mps",
    "params": 85765,
    "training_seconds": 738.2947724170517,
    "optimizer_steps": 29020,
    "physics_calls": 36033,
    "pde_training_evaluations": 58101792,
    "ic_training_evaluations": 50976792,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9134,
      "loss": 0.47961464524269104,
      "elapsed_seconds": 187.51114912499906,
      "note": "Muon/AdaBelief before full PR+; PDE_eval=9353216; IC_eval=9353216"
    },
    {
      "step": 18135,
      "loss": 0.484515517950058,
      "elapsed_seconds": 375.01409887504997,
      "note": "Muon/AdaBelief before full PR+; PDE_eval=18570240; IC_eval=18570240"
    },
    {
      "step": 27091,
      "loss": 0.5003244876861572,
      "elapsed_seconds": 562.5192268330138,
      "note": "Muon/AdaBelief before full PR+; PDE_eval=27741184; IC_eval=27741184"
    },
    {
      "step": 29020,
      "loss": 0.42205912759527564,
      "elapsed_seconds": 738.2945241670241,
      "note": "final full PR+; PDE_eval=58101792; IC_eval=50976792; PDE_draws=29701792; IC_draws=29676792; cg=112; accepted=106; full=100000/75000; micro=4096; lines=173; nf=0; restarts=15"
    }
  ]
}
```

## Decision and interpretation

The net-improvement hypothesis is supported by this single fit. Total L_val fell from Trial 005's 0.1719146514 to 0.1690991738, by 0.0028154776 (about 1.64%). Weighted physics decreased 0.0112597192, outweighing an IC MSE increase of 0.0084442417. All three physics totals improved, although middle continuity increased. The IC L2 0.3123802 is not an eligibility gate and does not disqualify the lower total score. This is the current lowest finite method, about 7.76% below P. Retain for further exploration and possible finalists, without claiming statistical significance, an isolated Muon causal effect or reference-trajectory accuracy. Initial update throughput changed (28908 versus 30356), the matrix precision is the disclosed float32 adaptation, and the full-pool finish is part of the complete method. The worse sampled training objective does not override validation loss. A factored-second-moment hidden-matrix update with the auxiliary optimiser and full-pool finish retained is a distinct next optimisation control. No checkpoint reuse, data/protocol changes, or numerical-reference feedback.
