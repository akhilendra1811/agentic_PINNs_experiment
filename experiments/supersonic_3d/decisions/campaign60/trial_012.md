# Trial 012

Research metadata (locked on preparation): research_area=optimisation; parents=trial:11; kind=mechanism; mechanism_id=sharpness_aware_minimization.

## Parent methods and evidence

Closed Trial 011 source is current best: L_val0.1678472594, physics0.0725275773, IC MSE0.0953196821. It improved total0.23% over Lion through physics despite worse IC. Finite-pool generalisation remains a concern from W audit and lower training loss has not reliably ranked trials. Test neighbourhood-aware gradients rather than another elementwise update. Same architecture, loss, initial optimiser partitions and full-pool PR+ finish. Fresh weights/states only; no checkpoint reuse.

## Novelty claim

Optimisation mechanism: first-order L2 sharpness-aware minimisation (SAM) wrapper on Adan/AdaBelief, known method credited to Foret et al., https://arxiv.org/html/2010.01412v3 Section2, equations2-3/Algorithm1, author code https://github.com/google-research/sam . Not scientific novelty or a scalar change. Temporary model-weight ascent changes the gradient evaluation point, while training coordinates remain byte-for-byte the same sampled points. Independent compact implementation; Adan/AdaBelief attribution retained. Full-pool final phase deliberately remains ordinary PR+, so this tests SAM only during initial optimisation.

## Hypothesis and proposed change

Hypothesis: local weight-neighbourhood gradients reduce total validation loss despite two-backward overhead. At each initial update compute ordinary batch gradient g across all85765 parameters; save exact base vector; temporarily set weights=base+.05*g/(||g||2+1e-12), treating ascent as detached. Clear all gradients; evaluate/backpropagate same PDE/IC coordinates/targets again; restore exact base copies in finally, then apply parent hidden Adan and auxiliary AdaBelief using probe gradients. No differentiating through perturbation, adaptive radius or weight decay. Before second backward require8s remaining; interruption restores base without optimizer update. Any other error also restores then propagates, counted honestly. Synthetic CPU/native MPS radius/quadratic gradient/exact interruption rollback checks passed. Model/optimizers/PR+ AST and mathematical entire full-phase equality passed. No coordinate sampling/PINN fitting in checks. Risks: half as many stochastic updates, radius bias, reduced IC fitting, sharpness not necessarily predictive of PDE generalisation.

## Training objective and setup

Fresh unchanged P sine model, seven Linear layers width128, three harmonics,85765 parameters, Xavier/bias.01,density startup.05. Same scalar F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z, absolute component MSE weights one, evaluated twice per initial SAM step. First80% of750s: hidden Adan(lr.001,betas .98/.92/.99,eps1e-8),auxiliary UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12). Initial1024PDE/1024IC pool replacement, same batch in both passes. No total points-per-step cap; this batch is controlled. Last phase caches all100000PDE/75000IC exactly once via cycle,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ descent restarts, four-trial Armijo c1=1e-4/halving,seed rules, >12s attempt/4s chunk/8s proposal deadline and exact last-accepted rollback. All sampling,probe/backward/optimiser/cache/search overhead inside budget. Log actual draws/evaluations/SAM probes/updates/CG/search/nonfinite counts. Return parent states,step,CG and SAM counters. No generated/perturbed coordinates,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite L_val below0.1678472594 with sufficient physics/IC balance for net gain. A higher total contradicts net hypothesis even if training sharpness,IC,any window or throughput improves. Read all numerical diagnostics,history,metadata,log; reconcile twice-per-update initial evaluations plus repeated full-pool calls, including any interrupted first pass. Diagnostic positivity/periodicity/mass/IC fields do not gate ranking. One fresh matched-time local wrapper test does not prove statistical significance, sharpness theory or general SAM superiority. Failure counts and IDs never rerun.

## Observed results

All metrics/metadata/history/log and diagnostics read. 15233 SAM updates/two passes each +112 CG attempts,106 accepted,172 line values,13 restarts,zero nonfinite proposals. 284 complete full-pool evaluations exactly reconcile; no interrupted first pass or partial full evaluation. No warning/execution failure. Actual canonical records:

```json
{
  "metrics": {
    "L_val": 0.17988972180975776,
    "physics_weighted": 0.07546144366211287,
    "ic_relative_l2": 0.32315364480018616,
    "ic_relative_mse": 0.10442827814764488,
    "windows": {
      "early": {
        "continuity": 0.16070761175205842,
        "momentum": 0.02345871697769706,
        "poisson": 0.013373455580209435,
        "total": 0.1975397843099649
      },
      "middle": {
        "continuity": 0.011816559954719986,
        "momentum": 0.01256629154258223,
        "poisson": 0.007581735987933619,
        "total": 0.03196458748523583
      },
      "late": {
        "continuity": 0.01662254698281681,
        "momentum": 0.015111604853909664,
        "poisson": 0.02099406927237179,
        "total": 0.052728221109098264
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9939392805099487,
        "0.5": 0.987577497959137,
        "0.8": 0.9861726760864258
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0060607194900512695,
        "0.5": -0.012422502040863037,
        "0.8": -0.013827323913574219
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10286165773868561,
        "0.5": 0.313209593296051,
        "0.8": 0.5526887774467468
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2426193952560425,
        "0.5": 1.90876305103302,
        "0.8": 2.9127933979034424
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4695836305618286,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.0265579223632812e-06
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
    "training_seconds": 738.9770684160176,
    "optimizer_steps": 15345,
    "physics_calls": 37566,
    "pde_training_evaluations": 59597184,
    "ic_training_evaluations": 52497184,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4726,
      "loss": 0.658057451248169,
      "elapsed_seconds": 187.51516229100525,
      "note": "SAM-Adan/AdaBelief before full PR+; PDE_eval=9678848; IC_eval=9678848"
    },
    {
      "step": 9495,
      "loss": 0.5484476685523987,
      "elapsed_seconds": 375.032149125007,
      "note": "SAM-Adan/AdaBelief before full PR+; PDE_eval=19445760; IC_eval=19445760"
    },
    {
      "step": 14276,
      "loss": 0.5189135074615479,
      "elapsed_seconds": 562.5392781660194,
      "note": "SAM-Adan/AdaBelief before full PR+; PDE_eval=29237248; IC_eval=29237248"
    },
    {
      "step": 15345,
      "loss": 0.4526659958064556,
      "elapsed_seconds": 738.9768992909812,
      "note": "SAM/PR+; sam=15233; PDE_eval=59597184; IC_eval=52497184; PDE_draws=15698592; IC_draws=15673592; cg=112; accepted=106; full=100000/75000; micro=4096; lines=172; nf=0; restarts=13"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported. Total rose 0.0120424624 (7.17%) versus Trial 011; physics rose 0.0029338664 and IC MSE 0.0091085960. Early physics improved but middle/late worsened, particularly Poisson. Initial updates fell to15233 from30152 due to two-pass cost; this time-limited wrapper does not isolate sharpness from throughput. No general SAM or significance claim. Retain finite result without IC/physical gates; leader remains Trial 011.
