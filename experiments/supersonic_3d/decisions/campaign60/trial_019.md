# Trial 019

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:11; kind=mechanism; mechanism_id=snake_linear_periodic_representation.

## Parent methods and evidence

Closed011 source,current lowest finite total.1678472594,physics.0725275773,IC.0953196821. RealGabor018 total.1714162320 nearly recovers parent IC(.0962720110) but physics is worse(.0751442210),with only23058 initial updates/154 full evaluations. Swish017 improves physics but sacrifices IC. Test an oscillatory activation with a nonsaturating linear path instead of Gaussian localisation. Keep entire011 trainer and Linear shapes fixed. Fresh weights/state only,no parent checkpoint reuse.

## Novelty claim

Activation/representation mechanism Snake f(x)=x+sin^2(x),fixed alpha1. Credit Liu Ziyin,Hartwig,Ueda,Neural Networks Fail to Learn Periodic Functions and How to Fix It,https://arxiv.org/abs/2006.08195 . Known activation,no scientific novelty. It changes function family through additive linear and periodic terms,not merely sine frequency or learning rate. Periodicity of model coordinates comes from unchanged spatial Fourier inputs;Snake itself has a linear drift,not a globally periodic scalar output. Paper periodic extrapolation results do not imply this PINN advantage.

## Hypothesis and proposed change

Hypothesis: linear path avoids tanh/Gabor saturation while periodic derivative features retain IC bandwidth,lowering total versus011. Replace all six hidden sine functions with x+sin(x).square(),no learned alpha or rescaling. Same seven Linear shapes,Xavier uniform/bias.01,features,density transform. Entire trainer/optimisers/PR+ AST equality passed,85765params/six activations confirmed. Synthetic-logit CPU/native MPS analytic first/second/third derivatives (1+sin2x,2cos2x,-4sin2x) and f(x+pi)=f(x)+pi passed. No PDE coordinates/fitting in checks. Risks:nonzero hidden mean,unbounded feature amplitude,near-zero derivatives at isolated values,extra autodiff cost and initialisation mismatch. No gain assumed.

## Training objective and setup

Fresh seven Linear,width128,19features from three spatial harmonics+time,six Snake activations,85765params,Xavier/bias.01,rho=rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:hidden five matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),input/output weights+biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no clipping/decay. Initial1024PDE/1024IC pool replacement,a control choice not total cap. Final all100000PDE/75000IC cycle cache once,25 separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All overhead within750s;return states/log actual draws,evaluations,steps,CG/search/restarts/nonfinite counts. Frozen-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite L_val below.1678472594 through sufficient IC retention and lower weighted physics. A larger total falsifies net hypothesis regardless of individual components or throughput. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log and reconcile full-pool counts. Finite total alone ranks,no diagnostic gates. Single fresh matched-time local Snake setting cannot establish significance,general periodic activation superiority or numerical-reference accuracy. Retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.26615 initial updates+81 CG attempts,74 accepted,123 line values,3 restarts,0 nonfinite proposals.204 complete full-pool evaluations exactly reconcile,no partial work or backend warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.1652899711739012,
    "physics_weighted": 0.07234346714535389,
    "ic_relative_l2": 0.3048712909221649,
    "ic_relative_mse": 0.09294650402854732,
    "windows": {
      "early": {
        "continuity": 0.18270721548798116,
        "momentum": 0.029840708605717452,
        "poisson": 0.007005560288566245,
        "total": 0.21955348438226485
      },
      "middle": {
        "continuity": 0.01071719528841616,
        "momentum": 0.012293258348765242,
        "poisson": 0.005283098485915033,
        "total": 0.028293552123096435
      },
      "late": {
        "continuity": 0.015979519998114797,
        "momentum": 0.014919262594584246,
        "poisson": 0.008990626671244941,
        "total": 0.039889409263943985
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9948884844779968,
        "0.5": 0.9906706809997559,
        "0.8": 0.9894901514053345
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005111515522003174,
        "0.5": -0.00932931900024414,
        "0.8": -0.010509848594665527
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11186037957668304,
        "0.5": 0.33795151114463806,
        "0.8": 0.6018648147583008
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2737795114517212,
        "0.5": 2.016876459121704,
        "0.8": 3.1761255264282227
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.48594480752944946,
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
    "params": 85765,
    "training_seconds": 738.931800249964,
    "optimizer_steps": 26696,
    "physics_calls": 31715,
    "pde_training_evaluations": 47653760,
    "ic_training_evaluations": 42553760,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 8389,
      "loss": 0.46622487902641296,
      "elapsed_seconds": 187.50689170800615,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=8590336; IC_eval=8590336"
    },
    {
      "step": 16749,
      "loss": 0.44041380286216736,
      "elapsed_seconds": 375.0101944580092,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=17150976; IC_eval=17150976"
    },
    {
      "step": 24924,
      "loss": 0.4223037660121918,
      "elapsed_seconds": 562.501582500001,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=25522176; IC_eval=25522176"
    },
    {
      "step": 26696,
      "loss": 0.3960057767108083,
      "elapsed_seconds": 738.9315287909703,
      "note": "final full PR+; PDE_eval=47653760; IC_eval=42553760; PDE_draws=27353760; IC_draws=27328760; cg=81; accepted=74; full=100000/75000; micro=4096; lines=123; nf=0; restarts=3"
    }
  ]
}
```

## Decision and interpretation

New lowest finite score. Total improves011 by0.0025572882 (1.52%):physics falls0.0001841101 and IC MSE0.0023731781. Early/middle physics totals worsen,but late improves enough for weighted net reduction. Net hypothesis supported in this fit;retain as promising parent by finite total only,no diagnostic gates. 26615 initial updates/204 full evaluations versus011 30152/284 show activation overhead;not statistical significance or general Snake superiority. Final matched1800-second comparison remains required.
