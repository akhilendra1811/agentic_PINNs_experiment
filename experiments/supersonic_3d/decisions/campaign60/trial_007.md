# Trial 007

Research metadata (locked on preparation): research_area=optimisation; parents=trial:6; kind=mechanism; mechanism_id=adafactor_factored_second_moments.

## Parent methods and evidence

Parent closed Trial 006, source only, is the current lowest score: L_val 0.1690991738, physics 0.0715177878 and IC relative MSE 0.0975813860. Relative to Trial 005's 0.1719146514, its matrix-momentum update improved all physics window totals but increased IC MSE; the total gain was 0.0028154776. It completed 28908 initial updates and 106 accepted full-pool CG updates. Keep its disjoint hidden/auxiliary partition and full-pool finish to test another matrix preconditioner, not a new model. The higher IC L2 is not a gate. No trained weights, optimiser state or checkpoint is reused; the entire fit is fresh.

## Novelty claim

Optimisation mechanism: Adafactor's row/column second-moment approximation, time-varying decay, parameter-relative step and update clipping on hidden matrices, replacing Muon's momentum orientation map. Credit Shazeer and Stern, Adafactor: Adaptive Learning Rates with Sublinear Memory Cost, https://arxiv.org/abs/1804.04235 . Use the explicit PyTorch variant documented at https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adafactor.html ; its epsilon handling differs from the paper. This is known work and a substantive factored scaling mechanism, not a learning-rate-only refinement or claim of new science. Auxiliary parameters retain the existing AdaBelief implementation/attribution, and PR+ remains unchanged.

## Hypothesis and proposed change

Hypothesis: factored second-moment scaling gives a better IC/physics balance than matrix momentum orthogonalisation in the same hidden layers, lowering total loss. Replace only the five hidden 128x128 matrices' optimiser with torch.optim.Adafactor(lr=0.01,beta2_decay=-0.8,eps=(None,0.001),d=1,weight_decay=0,foreach=False). The first epsilon is the float32 machine epsilon, approximately 1.1920929e-7, per the installed implementation. The relative-step cap is min(0.01,1/sqrt(t)); parameter scaling and update RMS clipping follow PyTorch. Remove the unused Muon helper. Input/output weights and all biases stay on exactly the parent's AdaBelief settings. Clear all model gradients and update both disjoint partitions from the same initial-phase backward pass. Model, objective, point choices and PR+ code are unchanged. Syntax, relevant AST equality and installed signature binding passed; no new numerical PINN fit was used to choose settings. Risks: rank-one factors lose coordinate information, parameter-relative updates may underfit, and synchronisation/throughput can change under a fixed time limit.

## Training objective and setup

Fresh P sine model, seven Linear layers width 128, three harmonics per spatial axis, 85765 parameters (81920 hidden-matrix / 3845 auxiliary), Xavier/bias 0.01, startup_dt=0.05, density rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)). Loss = continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, mean squared components weighted 1, unchanged; frozen selection still uses relative IC MSE. Initial 80% of 750 seconds: hidden Adafactor settings above; auxiliary UnrectifiedAdaBelief(lr=0.001,betas=(0.9,0.999),eps=1e-12), no decay/clipping beyond Adafactor's own update clipping. Initial batches 1024 PDE/1024 IC with replacement, a control choice rather than a cap. Cache every one of the 100000 PDE and 75000 IC points once by cycle sampling for the final phase. Each complete gradient/value uses 25 separately weighted chunks, max 4096 PDE/3072 IC, all cached coordinates fixed. Preserve PR+ direction/restart, four-trial Armijo search with c1=1e-4 and halving, alpha seed rules, >12-second attempt reserve, four-second chunk/eight-second proposal checks and rollback on interruption. No new or perturbed coordinates, validation access or references. Record actual draws, repeated full-pool evaluations, CG attempts/acceptance/restarts/nonfinite counts, timing and history; return both initial states and CG state. Owner checkpoint/scoring unchanged, and no fit for this ID has run before PRE completion.

## Expected outcome

Expect L_val below Trial 006's 0.1690991738. One possible route is recovering some of its increased IC MSE (0.0975813860) while retaining sufficient physics improvement; the factored approximation may instead worsen both. No IC recovery threshold is imposed: only the combined score decides. A larger total contradicts the net hypothesis even if lower memory, more steps, a component or a physical diagnostic improves. Read all metrics/windows and IC/density/mass/periodicity diagnostics, logs, actual timing and per-phase update/point counts before POST. The same full-pool finish controls coordinate coverage but cannot isolate all optimiser-throughput effects in one run. No physical/IC selection gates, post-validation updates, reruns of an ID or numerical-reference reward. Report finite outcomes and execution failures honestly without statistical-significance or Athena++ accuracy claims.

## Observed results

Completed normally, return code 0. L_val 0.178372505750, physics 0.089118745154, IC relative MSE 0.089253760596, IC L2 0.298753678799. 85765 parameters, 739.509630 actual seconds. 27831 initial updates and 113 CG attempts, 106 accepted; 173 line values, 15 restarts and zero nonfinite proposals. All 286 complete full-pool evaluations reconcile with 57098944 PDE / 49948944 IC evaluations, 28598944 PDE / 28573944 IC draws and 34981 physics calls. No partial evaluation needed for these counts. All required files, full numerical diagnostics and run.log read; no execution error. Full records follow.

```json
{
  "metrics": {
    "L_val": 0.17837250574995628,
    "physics_weighted": 0.0891187451542141,
    "ic_relative_l2": 0.29875367879867554,
    "ic_relative_mse": 0.0892537605957422,
    "windows": {
      "early": {
        "continuity": 0.19494919101441294,
        "momentum": 0.02756220851536819,
        "poisson": 0.012892321204331305,
        "total": 0.23540372073411242
      },
      "middle": {
        "continuity": 0.016070367425332136,
        "momentum": 0.014003118119487467,
        "poisson": 0.007636171437680234,
        "total": 0.03770965698249984
      },
      "late": {
        "continuity": 0.021086012327408702,
        "momentum": 0.019132351305592855,
        "poisson": 0.021231844192281774,
        "total": 0.061450207825283334
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9939026236534119,
        "0.5": 0.9870728254318237,
        "0.8": 0.9852783679962158
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.006097376346588135,
        "0.5": -0.01292717456817627,
        "0.8": -0.01472163200378418
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10929570347070694,
        "0.5": 0.3308754861354828,
        "0.8": 0.5786758065223694
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2614556550979614,
        "0.5": 1.9801784753799438,
        "0.8": 3.036184787750244
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4000132977962494,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.7881393432617188e-06
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
    "training_seconds": 739.5096296659904,
    "optimizer_steps": 27944,
    "physics_calls": 34981,
    "pde_training_evaluations": 57098944,
    "ic_training_evaluations": 49948944,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 8699,
      "loss": 0.5069395303726196,
      "elapsed_seconds": 187.51556516601704,
      "note": "Adafactor/AdaBelief before full PR+; PDE_eval=8907776; IC_eval=8907776"
    },
    {
      "step": 17385,
      "loss": 0.4520331621170044,
      "elapsed_seconds": 375.0170984999859,
      "note": "Adafactor/AdaBelief before full PR+; PDE_eval=17802240; IC_eval=17802240"
    },
    {
      "step": 26083,
      "loss": 0.441299706697464,
      "elapsed_seconds": 562.5171895829844,
      "note": "Adafactor/AdaBelief before full PR+; PDE_eval=26708992; IC_eval=26708992"
    },
    {
      "step": 27944,
      "loss": 0.38509541284292936,
      "elapsed_seconds": 739.5095023330068,
      "note": "final full PR+; PDE_eval=57098944; IC_eval=49948944; PDE_draws=28598944; IC_draws=28573944; cg=113; accepted=106; full=100000/75000; micro=4096; lines=173; nf=0; restarts=15"
    }
  ]
}
```

## Decision and interpretation

The net-improvement hypothesis is not supported. L_val rose from Trial 006's 0.1690991738 to 0.1783725057, by 0.0092733319 (about 5.48%). IC MSE improved 0.0083276254 but physics worsened 0.0176009573; all three window totals increased. The IC improvement does not override the total, and no IC/physical gate was used. The finite record still improves P but does not displace Trial 006 or Trial 005. The initial phase completed 27831 versus the parent's 28908 updates, so optimiser overhead/relative-step behaviour are part of the fixed-time result; one fit cannot isolate a universal factorisation disadvantage. Retain the documented finite comparison, not as leader. Next investigate a correlated rotating eigenbasis preconditioner on the same hidden matrices, keeping the lower-scoring Trial 006 as source parent and the full-pool finish controlled. No checkpoint reuse, protocol changes, statistical-significance claim or numerical-reference feedback.
