# Trial 052

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50,trial:51; kind=mechanism; mechanism_id=limited_memory_sr1_steihaug_trust_region.

## Parent methods and evidence

Trial050 supplies leading model/loss/first-half training, L_val0.1146599961747031. Trial051 BFGS-Dogleg scored0.11498676736863446, accepted28/38 and shrank from radius1 to below.01 before useful progress. This attempt uses a different trust-region subproblem/curvature model and starts radius.01 to avoid the observed oversized initial proposals.

## Novelty claim

Known Steihaug truncated-CG trust-region solver with limited-memory symmetric-rank-one(SR1) curvature, not a new method. Read official SciPy _trustregion_ncg.py Algorithm7.2 implementation and _hessian_update_strategy.py SR1 formula/denominator safeguard; controller source from051 retained. URLs https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion_ncg.py and https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_hessian_update_strategy.py . Local approximation uses secant actions, not exact Hessian-vector products.

## Hypothesis and proposed change

Allow indefinite SR1 curvature B=I+sum u*u^T/(u dot s),u=y-Bs,latest8 retained accepted-step pairs; rebuild after eviction and skip abs(u dot s)<=max(1e-20,1e-6 norm(u)norm(s)). Steihaug CG solves the model approximately, residual tolerance min(.5,sqrt(norm(g)))*norm(g),at most20 inner iterations. On nonpositive direction curvature choose the better of two sphere intersections; on radius crossing choose forward intersection. Same actual/predicted acceptance>.1 and radius*.25 belowratio.25/doubleabove.75boundary, max10/min1e-8. Initialradius.01 informed by051. CPUfloat64/native MPSfloat32 synthetic checks passed: SR1 actions match dense signed updates through memory rebuilding, denominator skip, CG converged solve, positive-curvature boundary, negative-curvature boundary choosing lower model value, and20-iteration cap path tested withcap1. Parent051 trainer prefix/model/loss/initial phase/full evaluator unchanged. No PINN fitting or new coordinates in checks. This can exploit negative model curvature unavailable to SPD Dogleg, but both curvature and radius changes confound comparison. Matrix actions cost no PDE evaluations and are logged separately from full passes.

## Training objective and setup

Unchanged050 model462405parameters and weighted F=C+mean3momentum+P+sum3IC/E, E fixed all75000training targets. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%SR1-Steihaug trust region with full100000PDE/75000IC cycle cache,4096/3072microbatches+tail, one base gradient and trial value per completed attempt. All initial target draws/setup/curvature work inside750second MPS fresh fit,physical82/RNG823001. Actual secant displacement,rejection/deadline rollback and finite checks retained. No total step point cap;8192per context call. Frozen data/scorer unchanged.

## Expected outcome

Target L_val<0.1146599961747031 through better local curvature/step adaptation. Indefinite secant noise, weak residual tolerance or restricted CG subspace may worsen physics/IC. Log all radius/predicted/actual/ratio/branch/pair and inner iteration records, point counts, all window and physical diagnostics with no gates. Negative SR1 curvature is approximate-model evidence,not proof of true PINN Hessian negativity. No theorem guarantee, statistical significance or numerical-reference accuracy claim.

## Observed results

Actual metrics, metadata, complete history and all37 trust-region traces follow; run.log/all diagnostics read.5015 initial updates+37 trust attempts(32 accepted,5 rejected),37 full gradients+37 values=74 complete full-pool evaluations. Counts reconcile12535360 PDE/10685360 IC model evaluations and6865 physics calls;75000 extra target-only IC draws have no model evaluations. Training739.559835 seconds,462405parameters,nf0. All ratios/acceptance/radius transitions independently reconciled. Four negative-curvature branches,two accepted; final radius.01,eight pairs. Inner iteration total74 counts approximate-model CG products,not PDE/HVP evaluations.

```json
{
  "metrics": {
    "L_val": 0.11467932933115807,
    "physics_weighted": 0.018594866751830055,
    "ic_relative_l2": 0.30997493863105774,
    "ic_relative_mse": 0.09608446257932801,
    "windows": {
      "early": {
        "continuity": 0.007858764981119218,
        "momentum": 0.02373194464219025,
        "poisson": 0.0015912428993182105,
        "total": 0.03318195252262768
      },
      "middle": {
        "continuity": 0.002358428347410221,
        "momentum": 0.00949161563623404,
        "poisson": 0.0010272649839421738,
        "total": 0.012877308967586435
      },
      "late": {
        "continuity": 0.004718274287408265,
        "momentum": 0.009596649390175838,
        "poisson": 0.001875643436473074,
        "total": 0.016190567114057176
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9975508451461792,
        "0.5": 0.9961556196212769,
        "0.8": 0.9953673481941223
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0024491548538208008,
        "0.5": -0.0038443803787231445,
        "0.8": -0.0046326518058776855
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1586713343858719,
        "0.5": 0.39513102173805237,
        "0.8": 0.6737651228904724
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3774319887161255,
        "0.5": 2.1744508743286133,
        "0.8": 3.4647061824798584
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3598920702934265,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.384185791015625e-06
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
    "params": 462405,
    "training_seconds": 739.5598351250519,
    "optimizer_steps": 5052,
    "physics_calls": 6865,
    "pde_training_evaluations": 12535360,
    "ic_training_evaluations": 10685360,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2481,
      "loss": 0.1396791934967041,
      "elapsed_seconds": 187.52865229104646,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2540544; IC_eval=2540544"
    },
    {
      "step": 5015,
      "loss": 0.1180281788110733,
      "elapsed_seconds": 375.0607314160443,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5135360; IC_eval=5135360"
    },
    {
      "step": 5035,
      "loss": 0.10582792107015848,
      "elapsed_seconds": 572.0636383329984,
      "note": "SR1-CG a=20; ok=17; R=0.00125; pred=6.34168e-05; actual=3.9735e-05; ratio=0.62657; pairs=8"
    },
    {
      "step": 5052,
      "loss": 0.10464825760573149,
      "elapsed_seconds": 739.559386833047,
      "note": "final SR1-CG; PDE_eval=12535360; IC_eval=10685360; PDE_draws=5235360; IC_draws=5285360; tr=37; accepted=32; gp=37; vp=37; nf=0; pairs=8; E=3.567659"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12535360,
    "IC_eval": 10685360,
    "PDE_draws": 5235360,
    "IC_draws": 5285360,
    "tr": 37,
    "accepted": 32,
    "gp": 37,
    "vp": 37,
    "nf": 0,
    "pairs": 8,
    "complete_full_evaluations": 74,
    "extra_ic_target_only_draws": 75000,
    "branches": {
      "cg_boundary": 25,
      "cg_converged": 8,
      "negative_curvature": 4
    },
    "inner_iterations": 74,
    "negative_curvature_accepted": 2,
    "final_radius": 0.01
  },
  "trust_region_trace": [
    {
      "attempt": 1,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.006025813985615969,
      "actual": 0.0019285001326352358,
      "ratio": 0.32003977176174003,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 1,
      "pairs": 0
    },
    {
      "attempt": 2,
      "radius_before": 0.01,
      "radius_after": 0.0025,
      "predicted": 0.0031041856855154037,
      "actual": 0.0007102370727807283,
      "ratio": 0.2287998028258429,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 1
    },
    {
      "attempt": 3,
      "radius_before": 0.0025,
      "radius_after": 0.005,
      "predicted": 0.0012477580457925797,
      "actual": 0.0011813364690169692,
      "ratio": 0.9467672622912888,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 1,
      "pairs": 2
    },
    {
      "attempt": 4,
      "radius_before": 0.005,
      "radius_after": 0.01,
      "predicted": 0.0009172490681521595,
      "actual": 0.0008504915749654174,
      "ratio": 0.927219884429833,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 3
    },
    {
      "attempt": 5,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.0011448251316323876,
      "actual": 0.0007063340162858367,
      "ratio": 0.6169798310408214,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 4
    },
    {
      "attempt": 6,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.0005414917832240462,
      "actual": 0.0005139568820595741,
      "ratio": 0.9491499187660262,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 5
    },
    {
      "attempt": 7,
      "radius_before": 0.01,
      "radius_after": 0.02,
      "predicted": 0.0008365625981241465,
      "actual": 0.0006623041117563844,
      "ratio": 0.791697014953205,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 6
    },
    {
      "attempt": 8,
      "radius_before": 0.02,
      "radius_after": 0.005,
      "predicted": 0.001133223995566368,
      "actual": -4.093546885997057e-05,
      "ratio": -0.03612301629697812,
      "accepted": false,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 7
    },
    {
      "attempt": 9,
      "radius_before": 0.005,
      "radius_after": 0.01,
      "predicted": 0.0004972211318090558,
      "actual": 0.00038543122354894876,
      "ratio": 0.7751706411725138,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 7
    },
    {
      "attempt": 10,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.0006971024558879435,
      "actual": 0.00043732556514441967,
      "ratio": 0.6273476179156053,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    },
    {
      "attempt": 11,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.00035225600004196167,
      "actual": 0.0003147327806800604,
      "ratio": 0.8934774159774953,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 12,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.0004495190514717251,
      "actual": 0.00012992671690881252,
      "ratio": 0.28903495076222585,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    },
    {
      "attempt": 13,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.00043006936903111637,
      "actual": 0.0003994833678007126,
      "ratio": 0.928881237695887,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 14,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.0004090011934749782,
      "actual": 0.000303710694424808,
      "ratio": 0.7425667681905881,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    },
    {
      "attempt": 15,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.00020360335474833846,
      "actual": 0.0001940719084814191,
      "ratio": 0.9531862022671453,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 16,
      "radius_before": 0.01,
      "radius_after": 0.02,
      "predicted": 0.00031642327667213976,
      "actual": 0.00028222554828971624,
      "ratio": 0.8919241063992353,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    },
    {
      "attempt": 17,
      "radius_before": 0.02,
      "radius_after": 0.02,
      "predicted": 0.00012634615995921195,
      "actual": 0.0001343239564448595,
      "ratio": 1.06314237400031,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 18,
      "radius_before": 0.02,
      "radius_after": 0.005,
      "predicted": 0.002434477210044861,
      "actual": -0.004351999727077782,
      "ratio": -1.7876526874521805,
      "accepted": false,
      "boundary": true,
      "branch": "negative_curvature",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 19,
      "radius_before": 0.005,
      "radius_after": 0.00125,
      "predicted": 0.0002790862927213311,
      "actual": -0.00013524817768484354,
      "ratio": -0.48461060687021784,
      "accepted": false,
      "boundary": true,
      "branch": "negative_curvature",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 20,
      "radius_before": 0.00125,
      "radius_after": 0.00125,
      "predicted": 6.341678817989305e-05,
      "actual": 3.973499406129122e-05,
      "ratio": 0.626569008013711,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 21,
      "radius_before": 0.00125,
      "radius_after": 0.00125,
      "predicted": 4.820390313398093e-05,
      "actual": 3.302469849586487e-05,
      "ratio": 0.6851042415398182,
      "accepted": true,
      "boundary": true,
      "branch": "negative_curvature",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 22,
      "radius_before": 0.00125,
      "radius_after": 0.0025,
      "predicted": 5.284832150209695e-05,
      "actual": 4.7368346713483334e-05,
      "ratio": 0.8963074960025706,
      "accepted": true,
      "boundary": true,
      "branch": "negative_curvature",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 23,
      "radius_before": 0.0025,
      "radius_after": 0.005,
      "predicted": 9.008955385070294e-05,
      "actual": 8.200097363442183e-05,
      "ratio": 0.9102162251831597,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 24,
      "radius_before": 0.005,
      "radius_after": 0.005,
      "predicted": 0.00016735927783884108,
      "actual": 4.9385824240744114e-05,
      "ratio": 0.29508865524802447,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 25,
      "radius_before": 0.005,
      "radius_after": 0.005,
      "predicted": 0.0001421209453837946,
      "actual": 0.00013357086572796106,
      "ratio": 0.9398394118984768,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 26,
      "radius_before": 0.005,
      "radius_after": 0.00125,
      "predicted": 0.0001342028408544138,
      "actual": -6.404786836355925e-05,
      "ratio": -0.47724674049962756,
      "accepted": false,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 27,
      "radius_before": 0.00125,
      "radius_after": 0.00125,
      "predicted": 3.821780774160288e-05,
      "actual": 2.0394567400217056e-05,
      "ratio": 0.5336404311337847,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 28,
      "radius_before": 0.00125,
      "radius_after": 0.0025,
      "predicted": 5.3433686844073236e-05,
      "actual": 5.138001870363951e-05,
      "ratio": 0.9615660407932057,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 29,
      "radius_before": 0.0025,
      "radius_after": 0.005,
      "predicted": 7.32922853785567e-05,
      "actual": 6.586534436792135e-05,
      "ratio": 0.8986668109436758,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 30,
      "radius_before": 0.005,
      "radius_after": 0.01,
      "predicted": 0.00012510758824646473,
      "actual": 0.00011056556832045317,
      "ratio": 0.8837638857096065,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 31,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 6.77610223647207e-05,
      "actual": 6.702204700559378e-05,
      "ratio": 0.989094388878175,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 32,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.00017122483404818922,
      "actual": 8.103065192699432e-05,
      "ratio": 0.4732412349962576,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 2,
      "pairs": 8
    },
    {
      "attempt": 33,
      "radius_before": 0.01,
      "radius_after": 0.01,
      "predicted": 0.00021181817282922566,
      "actual": 0.00018529826775193214,
      "ratio": 0.8747987260815686,
      "accepted": true,
      "boundary": false,
      "branch": "cg_converged",
      "inner_iterations": 1,
      "pairs": 8
    },
    {
      "attempt": 34,
      "radius_before": 0.01,
      "radius_after": 0.0025,
      "predicted": 0.00022324617020785809,
      "actual": -8.960417471826077e-05,
      "ratio": -0.4013693701210323,
      "accepted": false,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 4,
      "pairs": 8
    },
    {
      "attempt": 35,
      "radius_before": 0.0025,
      "radius_after": 0.0025,
      "predicted": 8.068499300861731e-05,
      "actual": 5.926366429775953e-05,
      "ratio": 0.7345066546814977,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    },
    {
      "attempt": 36,
      "radius_before": 0.0025,
      "radius_after": 0.005,
      "predicted": 7.835473661543801e-05,
      "actual": 6.243691314011812e-05,
      "ratio": 0.7968492504359507,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    },
    {
      "attempt": 37,
      "radius_before": 0.005,
      "radius_after": 0.01,
      "predicted": 0.00014088163152337074,
      "actual": 0.00013105571269989014,
      "ratio": 0.9302540812650186,
      "accepted": true,
      "boundary": true,
      "branch": "cg_boundary",
      "inner_iterations": 3,
      "pairs": 8
    }
  ]
}
```

## Decision and interpretation

Near tie but no score improvement: L_val rises0.0000193332 (0.0169%) versus050. Weighted physics falls0.0002128614 while IC MSE rises0.0002321946. Early/late physics totals improve,middle slightly worsens; continuity/momentum improve in all windows,Poisson worsens early/middle and improves late. SR1 negative-curvature branches were actually exercised,four proposals/two accepted,but do not prove true-Hessian negative curvature.32 accepted steps versus05128,with lower rejected-step overhead and smaller informed starting radius; SR1/CG/radius changes and5015 initial updates versus0505115 prevent isolated attribution. Retain finite evidence without gates;050 remains lowest by total. This tiny single-fit gap is not statistically significant. Continue053-060 before five fresh1800-second finalists plus P/B/W.
