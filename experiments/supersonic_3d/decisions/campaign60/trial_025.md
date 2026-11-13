# Trial 025

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:19; kind=mechanism; mechanism_id=time_conditioned_hidden_film.

## Parent methods and evidence

Closed019 source,lowest finite total.1652899712,physics.0723434671,IC.0929465040. ISRU024 total.1790356184 improved physics slightly but IC worsened;added branches/separation020-023 did not beat019. Retain compact Snake backbone and add temporal control of hidden features instead of changing spatial bandwidth or limiting raw-field rank. Prior75 had hidden-state-dependent residual gates;this is time-only scale+shift on preactivations,not the same gate. No trained weights/checkpoints/states reused.

## Novelty claim

Representation mechanism time-conditioned feature-wise affine modulation across six hidden layers. Credit Perez et al.,FiLM:Visual Reasoning with a General Conditioning Layer,https://arxiv.org/html/1709.07871 Section2.1 equations1-2. Known mechanism,no scientific novelty or transfer of visual-reasoning results. Local bounded generator uses physical time instead of language,and acts before Snake with no batch normalisation. Unlike scalar layer gains,scales/shifts are learned functions of time for every feature;unlike022s raw rank product,it changes hidden computation at every layer.

## Hypothesis and proposed change

Hypothesis:time-dependent hidden scales/shifts adapt spatial features through evolution without sacrificing IC,lowering total below019. Main19network unchanged,including time input. Conditioner1->32,Snake,32->1536 outputs6*2*128 values. Before hidden Snake layeri set h=(1+.5*tanh(g_i(t)))*h+.5*tanh(b_i(t)). Thus scale strictly(.5,1.5),shift(-.5,.5),no feature negation/shutoff. Conditioner first Linear Xavier/bias.01,final weight/bias zero;construct after main initialisation so main seed map exact and modulation initially identity.136517params,81920mainhidden Adan,54597auxiliary AdaBelief. Entire parent trainer/optimisers/PR+ and Snake AST equality passed. CPU exact main initial weights;CPU/native MPS identity raw map,finite all-parameter gradients,analytic first/second/third conditioner-logit derivatives passed on synthetic features. No PDE coordinates/fitting. Risks:bounded capacity compared with unrestricted FiLM,zero-head delay,extra time-derivative stiffness,larger auxiliary moments/AD cost and changed RNG consumption. Parent initial mapping identity does not control later minibatch RNG stream.

## Training objective and setup

Fresh mainseven-Linear width128,three spatial harmonics19features,six Snake layers modulated by timeconditioner above,136517parameters,parent density rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:mainfive128*128 hidden weights Adan(lr.001,betas .98/.92/.99,eps1e-8),allotherparameters includingconditioner UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap. Final all100000PDE/75000IC cycle cache once,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1652899712,through sufficient IC retention and weighted physics reduction. Higher total falsifies net hypothesis irrespective of diagnostics/throughput. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no eligibility gates. One fresh matched-time bounded time-FiLM setting cannot establish significance,general FiLM ranking or trajectory accuracy. Retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.15369 initial updates+27 CG attempts,24 accepted,44 line values,0 restarts/nonfinite proposals.71 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.16374612321085807,
    "physics_weighted": 0.06730568805350672,
    "ic_relative_l2": 0.3105486035346985,
    "ic_relative_mse": 0.09644043515735135,
    "windows": {
      "early": {
        "continuity": 0.17491996912625282,
        "momentum": 0.03269152034563628,
        "poisson": 0.004186947663735732,
        "total": 0.21179843713562482
      },
      "middle": {
        "continuity": 0.009874644416176777,
        "momentum": 0.012218617310779526,
        "poisson": 0.004315600047011545,
        "total": 0.026408861773967847
      },
      "late": {
        "continuity": 0.014382314197303353,
        "momentum": 0.012489758086006036,
        "poisson": 0.007174611905073406,
        "total": 0.034046684188382796
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9952101707458496,
        "0.5": 0.9911768436431885,
        "0.8": 0.9901311993598938
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004789829254150391,
        "0.5": -0.008823156356811523,
        "0.8": -0.009868800640106201
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10933671146631241,
        "0.5": 0.3299855589866638,
        "0.8": 0.5913198590278625
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2701565027236938,
        "0.5": 1.9808675050735474,
        "0.8": 3.144325017929077
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.40831443667411804,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.473592758178711e-06
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
    "params": 136517,
    "training_seconds": 740.8794127499568,
    "optimizer_steps": 15396,
    "physics_calls": 17144,
    "pde_training_evaluations": 22837856,
    "ic_training_evaluations": 21062856,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4814,
      "loss": 0.5117631554603577,
      "elapsed_seconds": 187.51793716696557,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4929536; IC_eval=4929536"
    },
    {
      "step": 9646,
      "loss": 0.48359179496765137,
      "elapsed_seconds": 375.03833199996734,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9877504; IC_eval=9877504"
    },
    {
      "step": 14415,
      "loss": 0.4344620108604431,
      "elapsed_seconds": 562.5046183329541,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=14760960; IC_eval=14760960"
    },
    {
      "step": 15396,
      "loss": 0.4104158924892545,
      "elapsed_seconds": 740.8787632079911,
      "note": "final full PR+; PDE_eval=22837856; IC_eval=21062856; PDE_draws=15837856; IC_draws=15812856; cg=27; accepted=24; full=100000/75000; micro=4096; lines=44; nf=0; restarts=0"
    }
  ]
}
```

## Decision and interpretation

New lowest finite score:total improves019 by0.0015438480 (0.93%). Physics falls0.0050377791 while IC MSE rises0.0034939311;all physics window totals improve. Net hypothesis supported in this fit;retain by total only despite higher IC error,no diagnostic gates.15369 initial updates/71 full evaluations show substantial conditioner/AD overhead. One fresh bounded time-FiLM test does not establish statistical significance,general FiLM superiority or isolated causal mechanism. Final matched1800-second comparison remains required after all60 attempts.
