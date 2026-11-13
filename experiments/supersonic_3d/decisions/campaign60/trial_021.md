# Trial 021

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:19; kind=mechanism; mechanism_id=periodic_input_multiplicative_filter_network.

## Parent methods and evidence

Closed019 source,lowest finite total.1652899712,physics.0723434671,IC.0929465040. Input-enriched020 total.1839246499 improved IC(.0851652900) but worsened all physics windows(.0987593599 weighted),so adding modes alone did not help net. Test hierarchical multiplicative feature interactions while returning to parent19 axis features. No trained weights/checkpoints/optimiser states reused. Entire parent trainer retained;representation and stated initialisation change.

## Novelty claim

Representation mechanism periodic-input MFN,credited Fathony,Sahu,Willmott,Kolter,Multiplicative Filter Networks,ICLR2021,author presentation https://iclr.cc/media/iclr-2021/Slides/3198.pdf ,paper https://openreview.net/pdf?id=OmtmcPkkhT . Direct PDF fetch hit browser verification;accessible author slides supply recurrence. Independently implemented mathematical recurrence,no AGPL repository source copied. This is a local periodic-input version,not canonical raw-coordinate FourierNet or exact paper settings. It replaces compositional activation layers with products of input-conditioned sinusoidal filters;not scalar tuning or a new scientific method. Prior75 decision-text search showed no MFN mentions,not a complete source audit.

## Hypothesis and proposed change

Hypothesis: multiplicative combinations represent cross-coordinate structures with a better physics/IC compromise than020s larger fixed input dictionary,lowering total below019. Let f be original18axis sin/cos features+time. z0=sin(A0*f+b0). For i1..5, zi=(Wi*z_(i-1)+bi)*sin(Ai*f+ci),then raw=Wout*z5+bout. Same density transform. Main net contains19->128,five128->128,128->5 Linear layers;five extra19->128 filters. No compositional Snake activations. Parameters98565,including81920 hidden matrix weights on Adan;remaining16645 on auxiliary AdaBelief. Hidden/output linears Xavier/bias.01;all six input filters(includingmaininput) weights uniform[-sqrt(6/19),sqrt(6/19)],bias uniform[-pi,pi],a disclosed local random-phase initialisation. Entire parent trainer/optimisers/PR+ AST equality passed. CPU/native MPS isolated synthetic feature model reduces exactly to sin(x)*sin(2x)^5;analytic first/second/third derivatives passed. These unit parameter assignments are not PDE training or candidate tuning. Risks:product attenuation,derivative amplification,larger auxiliary partition,RNG/initialisation and overhead confound a pure architecture-only conclusion.

## Training objective and setup

Fresh periodic-input MFN above,width128,six sinusoidal input filters,five multiplicative stages,98565parameters,original three axis harmonics,density rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:mainfive hidden matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),allinputfilters/outputweights/biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap. Lastphase all100000PDE/75000IC cached once bycycle,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restart,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1652899712,through IC recovery without020s physics increase. Larger total falsifies net hypothesis regardless of component/throughput improvements. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no IC/physical gates. One fresh matched-time local MFN test cannot establish significance,general MFN superiority or trajectory accuracy;retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.23934 initial updates+78 CG attempts,76 accepted,123 line values,4 restarts,0 nonfinite proposals.201 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.16972111946885016,
    "physics_weighted": 0.07565705748238405,
    "ic_relative_l2": 0.30669865012168884,
    "ic_relative_mse": 0.09406406198646611,
    "windows": {
      "early": {
        "continuity": 0.1765463145790536,
        "momentum": 0.03565971735223217,
        "poisson": 0.005639794738364924,
        "total": 0.2178458266696507
      },
      "middle": {
        "continuity": 0.010638539654258391,
        "momentum": 0.015569104481392017,
        "poisson": 0.0047849254528487435,
        "total": 0.03099256958849915
      },
      "late": {
        "continuity": 0.018813924341297528,
        "momentum": 0.01912867719081818,
        "poisson": 0.007637641011692625,
        "total": 0.04558024254380833
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9943462610244751,
        "0.5": 0.9888723492622375,
        "0.8": 0.9866711497306824
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005653738975524902,
        "0.5": -0.011127650737762451,
        "0.8": -0.013328850269317627
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11026192456483841,
        "0.5": 0.3262542188167572,
        "0.8": 0.5584312081336975
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2702116966247559,
        "0.5": 1.9692388772964478,
        "0.8": 2.9137871265411377
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.37421101331710815,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.5762786865234375e-06
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
    "params": 98565,
    "training_seconds": 738.7246817919658,
    "optimizer_steps": 24012,
    "physics_calls": 28959,
    "pde_training_evaluations": 44608416,
    "ic_training_evaluations": 39583416,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 7409,
      "loss": 0.4751991033554077,
      "elapsed_seconds": 187.51476033299696,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7586816; IC_eval=7586816"
    },
    {
      "step": 14912,
      "loss": 0.45169728994369507,
      "elapsed_seconds": 375.01470612495905,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=15269888; IC_eval=15269888"
    },
    {
      "step": 22421,
      "loss": 0.3998947739601135,
      "elapsed_seconds": 562.5006119579775,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=22959104; IC_eval=22959104"
    },
    {
      "step": 24012,
      "loss": 0.4075348540209234,
      "elapsed_seconds": 738.7244990419713,
      "note": "final full PR+; PDE_eval=44608416; IC_eval=39583416; PDE_draws=24608416; IC_draws=24583416; cg=78; accepted=76; full=100000/75000; micro=4096; lines=123; nf=0; restarts=4"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported:total rose0.0044311483 (2.68%) versus019,physics0.0033135903 and IC MSE0.0011175580 higher. Early physics total improves slightly,but middle/late worsen. It beats020 total but does not improve its IC error.23934 initial updates/201 full evaluations reflect architecture/AD overhead and larger auxiliary state. Retain finite result without diagnostic gates;no general MFN ranking,significance or isolated architecture causality claimed.
