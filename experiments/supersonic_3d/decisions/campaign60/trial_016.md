# Trial 016

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:11; kind=mechanism; mechanism_id=tanh_hidden_representation.

## Parent methods and evidence

Closed Trial011 source,current best finite total.1678472594,physics.0725275773,IC MSE.0953196821. Optimisation block finished15 attempts,14 finite plus015 nonfinite failure. Early continuity.1745583592 remains the largest parent PDE component. Test a smooth saturating hidden representation while holding the successful Adan/AdaBelief and full-pool PR+ trainer exactly fixed. No parent trained weights,checkpoints or optimiser state reused.

## Novelty claim

Activation/representation mechanism: replace all six hidden sine activations with hyperbolic tangent. This changes the function and derivative structure,not a sine frequency scalar. Known activation,not scientific novelty. Credit canonical tanh PINN precedent Raissi,Perdikaris,Karniadakis https://arxiv.org/html/1711.10561 Section2.1(line describing20-neuron hidden layers with hyperbolic tangent). Prior75 decision-text search found no tanh mention,which is not proof all historical sources lacked it. This is new to this numbered campaign. Keep sinusoidal spatial input features for periodicity;the tanh units themselves need not be periodic.

## Hypothesis and proposed change

Hypothesis: monotone bounded smooth hidden activations improve derivative conditioning and early physics enough to lower total despite possible high-frequency IC bias. Change Sine.forward sin(x) to TanhActivation.forward tanh(x) in six locations;all seven Linear shapes/weights/bias initialisation,density transform and input Fourier features unchanged. No trainable activation coefficients or gain tuning. Parent entire trainer,optimisers,PR+ AST equality passed. Model construction confirms85765 parameters,six activations. Synthetic scalar-logit first/second/third derivative formulas passed CPU/native MPS;no extra PDE coordinates,model fitting or scoring. Risks:tanh saturation/vanishing derivatives,spectral bias,initialisation optimised for sine may not be ideal. No general superiority assumed.

## Training objective and setup

Fresh model seven Linear,width128,three spatial harmonics19features,six tanh hidden functions,85765 parameters,Xavier uniform/bias.01,rho=rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). Objective continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:five hidden matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),input/output weights and biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pooled replacement,controlled choice not total cap. Final full-pool PR+ caches100000PDE/75000IC once bycycle,25 separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Unchanged descent restart,bounded4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and exact rollback. All overhead inside750s;record actual draws,evaluations,steps,CG/search/restarts/nonfinite counts;return optimiser/CG state. No coordinate generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1678472594,preferably reduced early continuity and weighted physics with tolerable IC change. Higher total contradicts net hypothesis even if one component or throughput improves. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log and reconcile full-pool counts. Finite total alone ranks,no IC/physical gates. One fresh matched-time fit cannot establish significance,general tanh superiority or Athena++ accuracy. Numerical failure counts,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.31090 initial updates+116 CG attempts,110 accepted,180 line values,5 restarts,0 nonfinite proposals.296 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.17461186914605603,
    "physics_weighted": 0.07199626810861387,
    "ic_relative_l2": 0.3203366994857788,
    "ic_relative_mse": 0.10261560103744216,
    "windows": {
      "early": {
        "continuity": 0.16401424209002652,
        "momentum": 0.02275675042194917,
        "poisson": 0.010290254155670916,
        "total": 0.1970612466676466
      },
      "middle": {
        "continuity": 0.01080614991449863,
        "momentum": 0.011674965115835313,
        "poisson": 0.007265405153472738,
        "total": 0.02974652018380668
      },
      "late": {
        "continuity": 0.016235430689645176,
        "momentum": 0.015147244100256323,
        "poisson": 0.015937450649983573,
        "total": 0.04732012543988507
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9950063824653625,
        "0.5": 0.9896615743637085,
        "0.8": 0.9883097410202026
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004993617534637451,
        "0.5": -0.010338425636291504,
        "0.8": -0.011690258979797363
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1055850014090538,
        "0.5": 0.3229283094406128,
        "0.8": 0.5769867897033691
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2561132907867432,
        "0.5": 1.9595000743865967,
        "0.8": 3.070044994354248
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.5329119563102722,
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
    "training_seconds": 738.0431179159787,
    "optimizer_steps": 31206,
    "physics_calls": 38490,
    "pde_training_evaluations": 61436160,
    "ic_training_evaluations": 54036160,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9745,
      "loss": 0.5442484021186829,
      "elapsed_seconds": 187.50873399997363,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9978880; IC_eval=9978880"
    },
    {
      "step": 19438,
      "loss": 0.4734901487827301,
      "elapsed_seconds": 375.00571125000715,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=19904512; IC_eval=19904512"
    },
    {
      "step": 29150,
      "loss": 0.44780346751213074,
      "elapsed_seconds": 562.5120594159816,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=29849600; IC_eval=29849600"
    },
    {
      "step": 31206,
      "loss": 0.4406118602491915,
      "elapsed_seconds": 738.0429513329873,
      "note": "final full PR+; PDE_eval=61436160; IC_eval=54036160; PDE_draws=31936160; IC_draws=31911160; cg=116; accepted=110; full=100000/75000; micro=4096; lines=180; nf=0; restarts=5"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported: total rose0.0067646097 (4.03%) versus011. Physics fell0.0005313092,IC MSE rose0.0072959189. Early total/continuity improved,but middle/late totals and all Poisson components worsened. Retain finite result without diagnostic gates;011 remains leader. This single fresh fit with fixed sine-era initialisation cannot establish general tanh inferiority or statistical significance.
