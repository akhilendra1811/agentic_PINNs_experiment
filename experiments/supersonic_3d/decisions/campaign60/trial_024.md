# Trial 024

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:19; kind=mechanism; mechanism_id=isru_algebraic_saturation_representation.

## Parent methods and evidence

Closed019 source,lowest finite total.1652899712,physics.0723434671,IC.0929465040. Added coarse/fine023 total.1737792463 increased early physics and IC,with15419 initial updates. Return to compact parent architecture. Tanh016 total.1746118691 suggests saturation can reduce physics but hurt IC;test a different smooth algebraic saturation law. Fresh weights/state,no trained checkpoint reuse.

## Novelty claim

Activation/representation mechanism inverse square root unit ISRU f(x)=x/sqrt(1+x^2),alpha1 fixed. Credit Carlile,Delamarter,Kinney,Marti,Whitney,Improving Deep Learning by Inverse Square Root Linear Units,https://arxiv.org/html/1710.09967 Section5 equation2. Use smooth symmetric ISRU,not piecewise ISRLU. Known function,no scientific novelty or speedup claim. This changes function/derivative structure rather than tuning a sine coefficient or an existing activation scalar. Periodic coordinates remain enforced by input features,not ISRU itself.

## Hypothesis and proposed change

Hypothesis:algebraic derivative tails offer a better saturation/conditioning compromise than tanh while preserving IC enough to beat019. Replace six Snake functions with x*rsqrt(1+x.square()),alpha1,all other model/trainer choices fixed. Positive denominator makes this smooth at zero and everywhere real. Entire parent trainer/optimisers/PR+ AST equality passed;85765params/six units confirmed. Synthetic-logit CPU/native MPS analytic first/second/third derivatives (1+x^2)^(-3/2),-3x(1+x^2)^(-5/2),(12x^2-3)(1+x^2)^(-7/2),and odd symmetry passed,no PDE coordinates/fitting. Risks:bounded nonoscillatory representation may lose turbulent IC detail,small gradients for large logits,rsqrt higher-order AD cost and unchanged initialisation. Original CPU/RNN discussion does not predict MPS/PINN performance.

## Training objective and setup

Fresh seven-Linear width128,three spatial harmonics19features,six ISRU activations,85765params,Xavier uniform/bias.01,density rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:five hidden128*128 weights Adan(lr.001,betas .98/.92/.99,eps1e-8),input/output weights+biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap. Final all100000PDE/75000IC cached once via cycle,25 exact separately weighted microbatches max4096PDE/3072IC per full gradient/value. Same PR+ restart,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All overhead within750s;return states/log actual draws,evaluations,steps,CG/search/restarts/nonfinite counts. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1652899712 with sufficient IC retention and physics reduction;also inspect versus016 without using that as promotion rule. Larger total falsifies net hypothesis irrespective of any diagnostic/throughput gains. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no IC/physical gates. One fresh matched-time ISRU setting cannot establish significance,general activation superiority or numerical-reference accuracy. Retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.24091 initial updates+64 CG attempts,59 accepted,100 line values,3 restarts,0 nonfinite proposals.164 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.17903561836868837,
    "physics_weighted": 0.07136588673455241,
    "ic_relative_l2": 0.32813066244125366,
    "ic_relative_mse": 0.10766973163413596,
    "windows": {
      "early": {
        "continuity": 0.1564623880806474,
        "momentum": 0.02309444566774081,
        "poisson": 0.010095751097250276,
        "total": 0.1896525848456385
      },
      "middle": {
        "continuity": 0.011138856562386853,
        "momentum": 0.011967805530702135,
        "poisson": 0.0075445989337882095,
        "total": 0.030651261026877197
      },
      "late": {
        "continuity": 0.016367265690431402,
        "momentum": 0.014953393296171935,
        "poisson": 0.017159323928119752,
        "total": 0.04847998291472309
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9944384694099426,
        "0.5": 0.9884872436523438,
        "0.8": 0.9867689609527588
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005561530590057373,
        "0.5": -0.01151275634765625,
        "0.8": -0.013231039047241211
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10273953527212143,
        "0.5": 0.31408631801605225,
        "0.8": 0.5613731741905212
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2460817098617554,
        "0.5": 1.9217177629470825,
        "0.8": 3.014671802520752
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3806692063808441,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.205371856689453e-06
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
    "training_seconds": 738.4844194169855,
    "optimizer_steps": 24155,
    "physics_calls": 28191,
    "pde_training_evaluations": 41069184,
    "ic_training_evaluations": 36969184,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 7590,
      "loss": 0.5750999450683594,
      "elapsed_seconds": 187.50657704198966,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7772160; IC_eval=7772160"
    },
    {
      "step": 15036,
      "loss": 0.49833250045776367,
      "elapsed_seconds": 375.00668366701575,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=15396864; IC_eval=15396864"
    },
    {
      "step": 22591,
      "loss": 0.48478394746780396,
      "elapsed_seconds": 562.5191546250135,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=23133184; IC_eval=23133184"
    },
    {
      "step": 24155,
      "loss": 0.4629876846447587,
      "elapsed_seconds": 738.4840819169767,
      "note": "final full PR+; PDE_eval=41069184; IC_eval=36969184; PDE_draws=24769184; IC_draws=24744184; cg=64; accepted=59; full=100000/75000; micro=4096; lines=100; nf=0; restarts=3"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported:total rose0.0137456472 (8.32%) versus019. Physics fell0.0009775804 but IC MSE rose0.0147232276. Early physics improves,middle/late worsen. It also exceeds tanh016 total by0.0044237492,despite slightly lower weighted physics.24091 initial updates/164 full evaluations reflect higher-derivative rsqrt cost. Retain finite result without diagnostic gates;no general ISRU ranking,speedup or significance claim.
