# Trial 030

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:28; kind=mechanism; mechanism_id=hidden_logscale_random_weight_factorisation.

## Parent methods and evidence

Trial028 parent: lowest finite L_val0.16293784616066054,physics0.0682361379091252,IC_relative_MSE0.09470170825153534. Trial029 Gaussian shape worsened both terms;return to028 Snake/FiLM/input skips.030 changes hidden-weight parameterisation rather than activation. Fresh initial tensors only;no checkpoint reuse.

## Novelty claim

Mechanism: random weight factorisation W=diag(exp(s))*V in five147->128 hidden affine maps,with learned128log-scales per map. Known RWF Wang et al. https://arxiv.org/html/2210.01274v2 AppendixB/Algorithm1,not publication novelty. Distinct from changing scalar learning rates or output activations. This is a restricted hidden-layer log-scale variant;input/output/conditioner remain ordinary affine maps. Paper AppendixC code updates direct initialized scale while Algorithm1 writes exp(s);we explicitly optimise log-scales,so do not claim exact code reproduction. No unit-direction normalisation or weight-normalisation claim. Prior75 decision text has no RWF/factorisation/weight-norm match (text evidence only).

## Hypothesis and proposed change

Primary hypothesis: row-scale/direction redundancy changes optimisation geometry sufficiently to improve total at equal time while preserving initial map. After028 fresh main/skip initialisation,wrap five expanded weights in FactorizedLinear: s=1+0.1randn(128),V=W/exp(s),bias copied;forward F.linear(x,exp(s)[:,None]*V,bias).94080direction parameters use sameAdan;640newlogscales join auxiliary AdaBelief. Raw input-skip dispatch recognises wrapper. All other trainer AST identical after necessary partition adjustment. CPU/native MPS effective initial weights/raw map/feature derivatives through third order and analytic chain rule gradV=exp(s)gradW,grads=sum(gradW*W) passed;149317params,finite all-parameter gradients. Temporary AST-check indexing mistake corrected without candidate changes or fitting. Conditioner RNG and sampler stream differ due extra640randomdraws;not a pure paired causal ablation.

## Training objective and setup

Canonical training F=continuity+mom_x+mom_y+mom_z+poisson+IC_x+IC_y+IC_z absolute MSE,all coefficients1. Frozen L_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.028seven-affine width128/sixSnake/fiveoriginal19feature input skips/boundedtimeFiLM1->32->1536 retained.149317params:94080factor directions Adan lr.001,betas(.98,.92,.99),eps1e-8;55237aux including640logscales AdaBelief lr.001,betas(.9,.999),eps1e-12. First80%1024PDE+1024IC replacement pool minibatches. Final20%full-pool restartedPR+/Armijo in factorised parameter space,100000PDE/75000IC via4096/3072microbatches+tail. No total point cap per step,8192percontextcall.750seconds,freshweights,physicalseed82/train823001,MPS,750000parameter cap. Only frozen pools,no extra coordinates. Counts measured afterrun.

## Expected outcome

Falsifiable target L_val<0.16293784616066054 through improved physics/IC tradeoff;report all threewindows. Unboundedexp(s),redundant flat directions or effective larger weight steps may instead destabilise training or line search;extra differentiation/parameterisation may reduce throughput. Adam-family updates and nonconvexPINN do not inherit simple gradient-descent RWF theory automatically. Density/mass/periodicity diagnostics never gate;single fit establishes no statistical significance.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 14513 initial updates+25 CG attempts(23 accepted),42 line values,4 restarts,0 nonfinite proposals,67 complete full-pool evaluations reconcile21561312 PDE/19886312 IC evaluations and16188 physics calls. Training739.294464 seconds,149317parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.16324366095695075,
    "physics_weighted": 0.0759883854133878,
    "ic_relative_l2": 0.2953900396823883,
    "ic_relative_mse": 0.08725527554356294,
    "windows": {
      "early": {
        "continuity": 0.2006581967756422,
        "momentum": 0.04182415262467261,
        "poisson": 0.0033221937209072265,
        "total": 0.24580454312122205
      },
      "middle": {
        "continuity": 0.012012110327810546,
        "momentum": 0.01302949093793859,
        "poisson": 0.0036059910868638835,
        "total": 0.02864759235261302
      },
      "late": {
        "continuity": 0.016271203028437597,
        "momentum": 0.013786884166001559,
        "poisson": 0.0064083109722798196,
        "total": 0.036466398166718976
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9960784316062927,
        "0.5": 0.9961706399917603,
        "0.8": 1.0003011226654053
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.003921568393707275,
        "0.5": -0.003829360008239746,
        "0.8": 0.00030112266540527344
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1133994311094284,
        "0.5": 0.3415680229663849,
        "0.8": 0.6125866770744324
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2807769775390625,
        "0.5": 2.035358190536499,
        "0.8": 3.2379026412963867
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4723152220249176,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.862645149230957e-06
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
    "training_seconds": 739.294464208011,
    "optimizer_steps": 14538,
    "physics_calls": 16188,
    "pde_training_evaluations": 21561312,
    "ic_training_evaluations": 19886312,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4499,
      "loss": 0.4420921802520752,
      "elapsed_seconds": 187.5399477079627,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4606976; IC_eval=4606976"
    },
    {
      "step": 9051,
      "loss": 0.42185351252555847,
      "elapsed_seconds": 375.01001924998127,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9268224; IC_eval=9268224"
    },
    {
      "step": 13623,
      "loss": 0.3834660053253174,
      "elapsed_seconds": 562.506853208004,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=13949952; IC_eval=13949952"
    },
    {
      "step": 14538,
      "loss": 0.3672548970207572,
      "elapsed_seconds": 739.2939892919967,
      "note": "final full PR+; PDE_eval=21561312; IC_eval=19886312; PDE_draws=14961312; IC_draws=14936312; cg=25; accepted=23; full=100000/75000; micro=4096; lines=42; nf=0; restarts=4"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 21561312,
    "IC_eval": 19886312,
    "PDE_draws": 14961312,
    "IC_draws": 14936312,
    "cg": 25,
    "accepted": 23,
    "lines": 42,
    "nf": 0,
    "restarts": 4
  }
}
```

## Decision and interpretation

Net hypothesis narrowly not supported: L_val rises0.0003058148 (0.19%) versus028. IC MSE improves0.0074464327 but physics rises0.0077522475;all three physics totals worsen,although Poisson improves in each. Lower IC/training loss and smaller mass drift cannot promote a larger total. Retain finite close contender for later evidence-driven refinements;028 remains leader. Small single-fit difference,changed RNG/parameter geometry and adaptive optimisation prevent significance or isolated RWF-causality claims.
