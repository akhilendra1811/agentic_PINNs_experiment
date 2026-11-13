# Trial 043

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:30; kind=refinement; mechanism_id=rwf_with_immediate_density_evolution.

## Parent methods and evidence

Trial030 is the successfully closed parent: L_val0.16324366095695075, weighted physics0.0759883854133878, IC relative MSE0.08725527554356294. It was close to028 with better IC but worse physics. Current leader042 scores0.15255327074817465 using compatible jets. Interrupted041 has no scientific result and is not a parent or source of trained state. This trial tests an immediate-density refinement on030s distinct RWF parameterisation/optimisation geometry, not a rerun of041.

## Novelty claim

Explicit refinement/combination, not a new mechanism: combine the established030 log-scale weight factorisation with removal of the P-style density hold. Only startup_dt0 and direct time gate t are new relative to030. RWF attribution remains Wang etal. https://arxiv.org/abs/2210.01274 as previously read; no new scientific novelty claim or new literature lookup needed. The source differs materially from interrupted041 through hidden row-scale/direction parameters and their optimiser allocation.

## Hypothesis and proposed change

Primary hypothesis: immediately learnable density time derivatives reduce the large early continuity contribution while retaining030s IC fitting advantage. Change self.startup_dt=.05->0 and dt=max(t-startup_dt,0)->t, yielding rho=rho0 exp(clamp(t*raw_rho,-4,4)). The direct gate avoids the zero derivative at the clamp boundary observed in041s pre-fit unit checks. Every other executable AST node equals030, including full trainer/optimisers. CPU/native MPS checks verified exactly these two changes, identical fresh state dictionaries,149317parameters, rho(0)=rho0 and correct first/second time derivatives for synthetic unsaturated logits. No PDE fitting, added coordinates or checkpoint reuse in checks.

## Training objective and setup

Frozen L_val=.2early+.3middle+.5late+IC_relative_MSE unchanged. Same030seven-affine width128/sixSnake/five19feature input skips/bounded time-FiLM;five hidden147->128weights parameterisedW=diag(exp(s))*V with640log-scales.149317parameters:94080directions Adan lr.001,betas(.98,.92,.99),eps1e-8;55237auxiliary includinglog-scales AdaBelief lr.001,betas(.9,.999),eps1e-12. Canonical F=sumfivePDE+sumthreeIC absolute MSE, allcoef1. First80%1024PDE/1024IC replacement-pool batches;final20%canonical full-pool PR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail, in factorised parameter space. No total points-per-step cap;8192 per context call.750seconds,fresh weights,seed82/training823001,MPS,750000parameter cap,only frozen pools. Actual counts afterrun.

## Expected outcome

Falsifiable target: improve030s total0.1632436610 and beat current leader042s0.1525532707 by reducing early continuity without IC/later deterioration erasing the gain. Gate changes affect the density trajectory at all positive times, and RWFs effective gradient scaling may amplify instability or exponent saturation. This result cannot fill in the missing041 outcome or isolate a universal startup effect across architectures. Report all windows/components/counts and physical diagnostics without gates; no significance or numerical-reference accuracy claim from one fit.

## Observed results

Actual metrics, metadata and complete history follow; all numerical diagnostics and run.log read. 14446 initial updates+25 completed CG attempts(23 accepted),43 line values,4 restarts,0 nonfinite proposals,68 complete full-pool evaluations reconcile21592704 PDE/19892704 IC evaluations and16146 physics calls. Training741.223098 seconds,149317parameters. No partial or extra uncompleted pool pass is needed for reconciliation. No execution error.

```json
{
  "metrics": {
    "L_val": 0.12657819355491223,
    "physics_weighted": 0.04193881132879733,
    "ic_relative_l2": 0.2909284830093384,
    "ic_relative_mse": 0.08463938222611489,
    "windows": {
      "early": {
        "continuity": 0.03291347078530978,
        "momentum": 0.036827745712833204,
        "poisson": 0.003780942407855778,
        "total": 0.07352215890599877
      },
      "middle": {
        "continuity": 0.011396825671534843,
        "momentum": 0.012523094308964212,
        "poisson": 0.004157139872577504,
        "total": 0.02807705985307656
      },
      "late": {
        "continuity": 0.01700693864645751,
        "momentum": 0.013973009696016482,
        "poisson": 0.006642574840875223,
        "total": 0.037622523183349216
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9928711652755737,
        "0.5": 0.9901013374328613,
        "0.8": 0.9904288053512573
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0071288347244262695,
        "0.5": -0.009898662567138672,
        "0.8": -0.009571194648742676
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.16560102999210358,
        "0.5": 0.40702369809150696,
        "0.8": 0.6862564086914062
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.4132784605026245,
        "0.5": 2.2570478916168213,
        "0.8": 3.5491883754730225
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.34139877557754517,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.2649765014648438e-06
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
    "params": 149317,
    "training_seconds": 741.2230979999877,
    "optimizer_steps": 14471,
    "physics_calls": 16146,
    "pde_training_evaluations": 21592704,
    "ic_training_evaluations": 19892704,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4476,
      "loss": 0.41313982009887695,
      "elapsed_seconds": 187.5200344590121,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4583424; IC_eval=4583424"
    },
    {
      "step": 9006,
      "loss": 0.3808721899986267,
      "elapsed_seconds": 375.03647299995646,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9222144; IC_eval=9222144"
    },
    {
      "step": 13539,
      "loss": 0.36597126722335815,
      "elapsed_seconds": 562.5030810839962,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=13863936; IC_eval=13863936"
    },
    {
      "step": 14471,
      "loss": 0.3306864849291742,
      "elapsed_seconds": 741.2227190000121,
      "note": "final full PR+; PDE_eval=21592704; IC_eval=19892704; PDE_draws=14892704; IC_draws=14867704; cg=25; accepted=23; full=100000/75000; micro=4096; lines=43; nf=0; restarts=4"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 21592704,
    "IC_eval": 19892704,
    "PDE_draws": 14892704,
    "IC_draws": 14867704,
    "cg": 25,
    "accepted": 23,
    "lines": 43,
    "nf": 0,
    "restarts": 4
  }
}
```

## Decision and interpretation

New lowest finite score. Versus030, total improves0.0366654674 (22.46%), weighted physics falls0.0340495741 and IC MSE falls0.0026158933. Early continuity falls from0.2006581968 to0.0329134708; early/middle totals improve, late total worsens slightly. Versus042, total improves0.0259750772 (17.03%); IC is lower but physics is higher, so ranking uses total only. Identical initial weights and unchanged trainer, with similar initial update counts14446versus03014513, support the immediate-density hypothesis within this configuration. They do not recover041s missing result or establish statistical significance/general architecture-independent causality. Retain043 by sole finite L_val, no diagnostic gates; fresh1800-second finalists after60 remain required.
