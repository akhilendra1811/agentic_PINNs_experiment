# Trial 026

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:25; kind=mechanism; mechanism_id=learned_chebyshev_hidden_activations.

## Parent methods and evidence

Closed025 source,new lowest finite total.1637461232,physics.0673056881,IC.0964404352. Time-FiLM improved physics over019 but worsened IC;test richer learned activation shapes while retaining successful hidden time-conditioning and entire trainer. Fixed tanh016 and ISRU024 were not net improvements under earlier compact architecture,so no assumption this bounded basis wins. Fresh weights/state,no checkpoint reuse. Campaign now60;026 remains assigned activation/representation block.

## Novelty claim

Representation mechanism per-feature learnable degree-three Chebyshev expansion on tanh logits. Known learned-basis activation family;credit Khalfaoui-Hassani,Kesselheim,Polynomial,trigonometric,and tropical activations,https://arxiv.org/abs/2502.01247 ,and adaptive linear-combination precedent Sutfeld et al.,https://arxiv.org/abs/1806.10064 . Local design uses Chebyshev rather than the cited Hermite/Fourier families and a tanh input map,not their exact orthonormal/variance-preserving implementation or moment-SOS training. Not scientific novelty or KAN(edge-function) reproduction. Learning four independent coefficients changes shape beyond a single gain/frequency scalar.

## Hypothesis and proposed change

Hypothesis:neuron-specific smooth activation shapes improve IC enough to lower total below025 while retaining physics/time conditioning. Let z=tanh(x);phi_c(x)=a0_c+a1_c*z+a2_c*(2z^2-1)+a3_c*(4z^3-3z). All four coefficients per feature are unconstrained trainable;init(.5,1,.5,0) gives z+z^2,matching Snake first two local terms but not its full function. Replace six128-wide main Snake activations and32-wide conditioner Snake with this module;FiLM detection updated to new class,conditioner remains zero final head. Added3200 activation params,total139717,81920mainmatrix Adan,57797auxiliary AdaBelief. Entire parent trainer/optimisers/PR+ and feature_modulate AST equality passed. CPU/native MPS initial-polynomial identity,analytic first/second/third derivatives,Chebyshev coefficient gradients,N*5 raw shape and finite all-parameter gradients passed. Synthetic logits/features only,no PDE coordinates/fitting. Risks:tanh bandwidth/saturation,unconstrained coefficient growth,more AD work,changed initial activation map;not a pure learned-versus-fixed coefficient ablation.

## Training objective and setup

Fresh mainseven-Linear width128,three axis harmonics19features,six mainlearned Chebyshev functions,conditioner1->32,Chebyshev32,32->1536,139717params. Main Linear Xavier/bias.01;conditionerfirstXavier/bias.01,finalzero;FiLM scale1+.5tanh(g),shift.5tanh(b) before each mainactivation. Density rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:five main128*128 hidden weights Adan(lr.001,betas .98/.92/.99,eps1e-8),allothers includingactivationcoefficients/conditioner UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap. Final all100000PDE/75000IC cycle cache once,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1637461232,with IC reduction and sufficient physics preservation. Higher total falsifies net hypothesis regardless of diagnostics/throughput. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no eligibility gates. One fresh matched-time local learned-polynomial setting cannot establish significance,general adaptive activation superiority or trajectory accuracy;retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.11647 initial updates+19 CG attempts,18 accepted,33 line values,0 restarts/nonfinite proposals.52 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.16593020894719915,
    "physics_weighted": 0.07065238737924831,
    "ic_relative_l2": 0.3086710572242737,
    "ic_relative_mse": 0.09527782156795084,
    "windows": {
      "early": {
        "continuity": 0.18116278064113792,
        "momentum": 0.033517064285195707,
        "poisson": 0.003160758982091841,
        "total": 0.21784060390842547
      },
      "middle": {
        "continuity": 0.011197905069533876,
        "momentum": 0.012883832115683662,
        "poisson": 0.0048382474837980975,
        "total": 0.028919984669015637
      },
      "late": {
        "continuity": 0.01590603355364184,
        "momentum": 0.01248344039471792,
        "poisson": 0.008427068445357285,
        "total": 0.036816542393717046
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9954202175140381,
        "0.5": 0.9922383427619934,
        "0.8": 0.992504358291626
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004579782485961914,
        "0.5": -0.007761657238006592,
        "0.8": -0.0074956417083740234
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10942664742469788,
        "0.5": 0.33136051893234253,
        "0.8": 0.5977611541748047
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2680975198745728,
        "0.5": 1.9984463453292847,
        "0.8": 3.1718504428863525
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.29471299052238464,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.9073486328125e-06
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
    "params": 139717,
    "training_seconds": 738.0807660000282,
    "optimizer_steps": 11666,
    "physics_calls": 12947,
    "pde_training_evaluations": 17126528,
    "ic_training_evaluations": 15826528,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 3623,
      "loss": 0.48969411849975586,
      "elapsed_seconds": 187.51426662498852,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=3709952; IC_eval=3709952"
    },
    {
      "step": 7281,
      "loss": 0.4431276321411133,
      "elapsed_seconds": 375.0073508750065,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7455744; IC_eval=7455744"
    },
    {
      "step": 10917,
      "loss": 0.4352903962135315,
      "elapsed_seconds": 562.5043133749859,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=11179008; IC_eval=11179008"
    },
    {
      "step": 11666,
      "loss": 0.40746444184333086,
      "elapsed_seconds": 738.0805394999916,
      "note": "final full PR+; PDE_eval=17126528; IC_eval=15826528; PDE_draws=12026528; IC_draws=12001528; cg=19; accepted=18; full=100000/75000; micro=4096; lines=33; nf=0; restarts=0"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported:total rose0.0021840857 (1.33%) versus025. IC MSE improved0.0011626136 but physics worsened0.0033466993;all physics window totals increased.11647 initial updates/52 full evaluations versus025 15369/71 show polynomial/AD overhead. Retain finite result without diagnostic gates;025 remains leader. Coefficient learning,initial function change and throughput are not isolated;no general learned-activation ranking or statistical-significance claim.
