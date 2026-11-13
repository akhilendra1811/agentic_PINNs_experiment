# Trial 020

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:19; kind=mechanism; mechanism_id=oblique_integer_fourier_embedding.

## Parent methods and evidence

Closed019 source,new lowest finite total.1652899712,physics.0723434671,IC.0929465040. Snake improved total1.52% versus011 but early/middle physics still bottlenecks. Prior75 Trials010 and046 already tested pairwise k(x_i+-x_j),k1/2:old010 total.12919127 versus oldB.12733444,old046 total.18966. Those old scores/protocols are not directly comparable and their IC eligibility is not used. Revisit directional embedding under new successful Snake trainer,with a different full three-axis/mixed-frequency set,not claim oblique features absent historically. Fresh weights/state,no checkpoints imported.

## Novelty claim

Representation mechanism deterministic integer 3D Fourier embedding including genuine three-axis modes and unequal pair harmonics,versus parent axis-only features. Credit Tancik et al.,https://arxiv.org/abs/2006.10739 and historical pairwise experiments above. This is new to this numbered campaign and extends an underexplored historical family,not global novelty or exact random-Gaussian Fourier-feature reproduction. It changes spatial directions/interactions and input dimension,not only a harmonic-count scalar. Prior pairwise equal harmonics do not contain the sixteen three-axis modes used here. No learned frequencies or new coordinates.

## Hypothesis and proposed change

Hypothesis: direct mixed-direction features improve IC and/or early physics enough to lower total with Snake. Keep original nine axis wavevectors h*e_j,h1..3. Add vectors k in{-2,-1,0,1,2}^3 with at least two nonzero components,first nonzero positive,and squared norm<=6:18 pairwise plus16 three-axis modes. Total43 modes,87 input channels including time. For each k use interleaved sin(theta dot k)/sqrt(||k||),cos(theta dot k)/sqrt(||k||),theta=2pi*(x,y,z)/14. Buffers are fixed nontrainable;amplitude=(sum k^2)^(-1/4). Input Linear87->128;all hidden/output shapes unchanged,Snake fixedalpha1. Parameters94469 (<750000),up8704. Entire parent activation/trainer/optimisers/PR+ AST equality passed. CPU/native MPS integer uniqueness/oblique structure,original-axis embedding equality,periodic angular shifts and analytic angular derivatives through third order passed on synthetic angles,no PDE coordinates/fitting. Risks:larger input/auxiliary optimisation and changed RNG consumption,derivative amplification,spectral overfitting,extra feature/AD cost. This does not isolate directional content from parameter count/initialisation stream.

## Training objective and setup

Fresh seven Linear,width128,Six Snake activations,43fixedinteger spatial modes+time87features,94469 parameters,Xavier uniform/bias.01,rho=rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:hidden five matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),input/output weights+biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,control choice not total cap. Final all100000PDE/75000IC cached once via cycle,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. Fourier mapping evaluates only supplied fixed-pool coordinates,no new/perturbed coordinates,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1652899712,with lower IC and/or early continuity sufficient for net gain. A larger total falsifies net hypothesis regardless of a diagnostic/throughput improvement. Read actual full metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no eligibility gates. One fresh matched-time local embedding test cannot establish significance,general Fourier-feature superiority or trajectory accuracy;retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.36376 initial updates+87 CG attempts,84 accepted,140 line values,12 restarts,0 nonfinite proposals.227 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.18392464994039925,
    "physics_weighted": 0.09875935990876594,
    "ic_relative_l2": 0.2918309271335602,
    "ic_relative_mse": 0.08516529003163331,
    "windows": {
      "early": {
        "continuity": 0.21494134827407382,
        "momentum": 0.04123435115384211,
        "poisson": 0.008434664436774438,
        "total": 0.2646103638646904
      },
      "middle": {
        "continuity": 0.01630082310832606,
        "momentum": 0.015016209762817805,
        "poisson": 0.009950963687243878,
        "total": 0.04126799655838774
      },
      "late": {
        "continuity": 0.022607866515993,
        "momentum": 0.01888505418127625,
        "poisson": 0.02542085563935384,
        "total": 0.06691377633662308
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9928364753723145,
        "0.5": 0.986440896987915,
        "0.8": 0.9838064312934875
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.007163524627685547,
        "0.5": -0.013559103012084961,
        "0.8": -0.01619356870651245
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11392632871866226,
        "0.5": 0.3403458297252655,
        "0.8": 0.5962063670158386
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2817796468734741,
        "0.5": 2.0320725440979004,
        "0.8": 3.1449646949768066
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3956860303878784,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.339482307434082e-06
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
    "params": 94469,
    "training_seconds": 740.1129267500364,
    "optimizer_steps": 36463,
    "physics_calls": 42051,
    "pde_training_evaluations": 59949024,
    "ic_training_evaluations": 54274024,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 11316,
      "loss": 0.45476090908050537,
      "elapsed_seconds": 187.51463491702452,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=11587584; IC_eval=11587584"
    },
    {
      "step": 22652,
      "loss": 0.42180681228637695,
      "elapsed_seconds": 375.01298008300364,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=23195648; IC_eval=23195648"
    },
    {
      "step": 34088,
      "loss": 0.37744420766830444,
      "elapsed_seconds": 562.5162220420316,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=34906112; IC_eval=34906112"
    },
    {
      "step": 36463,
      "loss": 0.36352503625676036,
      "elapsed_seconds": 740.112685042026,
      "note": "final full PR+; PDE_eval=59949024; IC_eval=54274024; PDE_draws=37349024; IC_draws=37324024; cg=87; accepted=84; full=100000/75000; micro=4096; lines=140; nf=0; restarts=12"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported: total rose0.0186346788 (11.27%) versus019. IC MSE improved0.0077812140 but physics worsened0.0264158928 and all window totals increased. Lower IC/training objective and higher throughput do not override total.36376 initial updates versus26615 parent show vectorised features changed throughput;parameter count/RNG stream also changed,so no pure direction-only causal claim. Retain finite result,no IC/physical gates,no general Fourier-feature verdict or significance claim.
