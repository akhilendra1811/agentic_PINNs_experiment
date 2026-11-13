# Trial 022

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:19; kind=mechanism; mechanism_id=low_rank_space_time_separable_representation.

## Parent methods and evidence

Closed019 source,lowest finite total.1652899712,physics.0723434671,IC.0929465040. MFN021 total.1697211195 slightly worsened both components;oblique020 improved IC but worsened physics. Test explicit space-time separation to decouple spatial structure from time evolution without adding fixed spatial bandwidth. Keep Snake,loss,pools and full-pool trainer. Fresh weights/state,no parent checkpoint reuse.

## Novelty claim

Representation mechanism rank64 space-versus-time product-sum latent map. Credit separated-product PINN precedent Cho et al.,Separable Physics-Informed Neural Networks,https://arxiv.org/html/2306.15969v4 Section4.2 equation5. This is an explicitly local partial-separation adaptation:one3D spatial body and one time body,not four per-axis SPINN,nor its tanh/lattice/forward-AD algorithm. No claimed scientific novelty or reproduced SPINN speedups. All owner residuals remain pointwise reverse-AD on fixed random pools;no Cartesian-product coordinates are generated. Separation changes architecture/function family,not rank-only scalar tuning.

## Hypothesis and proposed change

Hypothesis: rank-limited temporal coefficients preserve IC spatial content while reducing destructive space-time parameter interference,lowering total below019. Spatial body original18axis Fourier features(no time),Linear18->128,five128->128,128->64 withsix Snake functions. Time body Linear1->64,Snake,64->64,Snake,64->320. Reshape time outputN*5*64;raw_a(x,t)=sum_r spatial_r(x)*temporal_(a,r)(t)/sqrt64. Same density exponential/startup transform afterward,so raw fields are rank64 while density need not remain rank64. Parameters118336 (<750000);five main hidden matrices81920params Adan,remaining36416 auxiliary AdaBelief. All Linear Xavier uniform/bias.01. Entire parent trainer/optimisers/PR+ and Snake AST equality passed. CPU/native MPS independent factor readout on analytic latent monomials/trigonometric factors,mixed/third derivatives,all-network finite parameter gradients andN*5 shape passed. Synthetic features only,no PDE coordinates or fitting. Risks:low-rank temporal bottleneck,shared spatial basis across fields,small initial factor products,larger auxiliary state/derivative overhead,parameter count/RNG differences.

## Training objective and setup

Fresh two-body rank64 architecture above,118336params,periodic three-harmonic spatial inputs,Six spatial+two temporal Snake functions,raw product-sum scaling1/8,density rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:mainfive128*128 hidden weights Adan(lr.001,betas .98/.92/.99,eps1e-8),allotherparameters includingtimebody UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap. Final all100000PDE/75000IC cycle cache once,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite L_val below.1652899712,through sufficient IC retention and reduced physics. Larger total falsifies net hypothesis regardless of individual component/throughput gains. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no diagnostic gates. One fresh matched-time partial-separation test cannot establish significance,general SPINN ranking,claimed lattice speedups or numerical-reference accuracy. Retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.21850 initial updates+57 CG attempts,54 accepted,92 line values,2 restarts,0 nonfinite proposals.149 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.1783303810347783,
    "physics_weighted": 0.07759401003357305,
    "ic_relative_l2": 0.31738993525505066,
    "ic_relative_mse": 0.10073637100120525,
    "windows": {
      "early": {
        "continuity": 0.1717145345469307,
        "momentum": 0.03948580518448503,
        "poisson": 0.00423353870744084,
        "total": 0.21543387843885656
      },
      "middle": {
        "continuity": 0.012278439202436289,
        "momentum": 0.015751926714028436,
        "poisson": 0.005461279473283167,
        "total": 0.033491645389747894
      },
      "late": {
        "continuity": 0.01843577968789399,
        "momentum": 0.01713632940883938,
        "poisson": 0.013347372361021374,
        "total": 0.048919481457754745
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9934999942779541,
        "0.5": 0.9879100322723389,
        "0.8": 0.9858521819114685
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0065000057220458984,
        "0.5": -0.012089967727661133,
        "0.8": -0.014147818088531494
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10484375804662704,
        "0.5": 0.3130423128604889,
        "0.8": 0.5505885481834412
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2576091289520264,
        "0.5": 1.9290975332260132,
        "0.8": 2.9248857498168945
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.47060221433639526,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.86102294921875e-06
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
    "params": 118336,
    "training_seconds": 738.0915943339933,
    "optimizer_steps": 21907,
    "physics_calls": 25575,
    "pde_training_evaluations": 37274400,
    "ic_training_evaluations": 33549400,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 6786,
      "loss": 0.5150443911552429,
      "elapsed_seconds": 187.51523304200964,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=6948864; IC_eval=6948864"
    },
    {
      "step": 13636,
      "loss": 0.4635392129421234,
      "elapsed_seconds": 375.00508679199265,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=13963264; IC_eval=13963264"
    },
    {
      "step": 20475,
      "loss": 0.4352763593196869,
      "elapsed_seconds": 562.5112874999759,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=20966400; IC_eval=20966400"
    },
    {
      "step": 21907,
      "loss": 0.43881124863401055,
      "elapsed_seconds": 738.0913489589584,
      "note": "final full PR+; PDE_eval=37274400; IC_eval=33549400; PDE_draws=22474400; IC_draws=22449400; cg=57; accepted=54; full=100000/75000; micro=4096; lines=92; nf=0; restarts=2"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported:total rose0.0130404099 (7.89%) versus019,physics0.0052505429 and IC MSE0.0077898670 higher. Early physics total improved slightly,but middle/late worsened.21850 initial updates/149 full evaluations expose cost of product-sum/extra body. Rank limit,shared spatial basis,initialisation and throughput are not causally separated. Retain finite result without diagnostic gates;no general SPINN/separability ranking,significance or speedup claim.
