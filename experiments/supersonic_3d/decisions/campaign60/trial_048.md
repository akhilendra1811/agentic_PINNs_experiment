# Trial 048

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:47,trial:42; kind=refinement; mechanism_id=spatial_feature_bandwidth_five_wide_rwf.

## Parent methods and evidence

Trial047 supplies the leading width256 RWF/FiLM immediate-density model and50/50 training split: L_val0.12310839192730305, physics0.03965088854812371, IC MSE0.08345750337917934. IC is the larger score term. Trial042 found a larger initial Fourier bandwidth improved total in the different initial-jet representation; that motivates but does not prove this input-bandwidth hypothesis.

## Novelty claim

Explicit spatial-feature cutoff refinement, not a new representation mechanism or novelty claim. Retain periodic harmonic encoding, Snake, RWF, FiLM and repeated input skips with parent sources. No new literature lookup required for increasing a numerical cutoff.

## Hypothesis and proposed change

Increase each axial periodic harmonic range1..3 to1..5, giving30 spatial features plus time rather than18+time. Change dependent19->31 and275->287 constants. CPU/native MPS checks passed: exact AST changes only, counts/shapes, identity FiLM, zero skip columns, finite third feature derivatives and all output-loss parameter gradients, periodicity at synthetic endpoints. No fit or new training coordinates. Width256 and conditioner1->32->3072 unchanged. Seven main affines31->256,five287->256,256->5. Parameters480837:367360 hidden directions and113477 auxiliaries including1280 log scales. Extra harmonic features may fit IC better but derivative amplification and cost can harm physics. Changed dimensions/RNG/initial function are confounds.

## Training objective and setup

Canonical F=sumfivePDE+sumthreeIC absolute MSE, coefficient1. Immediate rho gate; unconstrained velocities/potential; six Snake, repeated input skips, bounded time FiLM, five hidden RWF maps. Directions Adan lr.001 betas(.98,.92,.99) eps1e-8; auxiliaries AdaBelief lr.001 betas(.9,.999) eps1e-12. First50%1024PDE/1024IC pool updates; remaining full-pool PR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No total point cap;8192per call only. Fresh MPS750seconds, physical82/RNG823001, frozen score/data unchanged.

## Expected outcome

Target L_val<0.12310839192730305 through improved IC fit without greater physics cost. Report all windows, counts, density/mass/periodicity without gates. A cutoff change alters capacity, frequency gradients, initialization and throughput simultaneously; one fit cannot establish causal isolation, significance or reference-solution accuracy.

## Observed results

Actual metrics, metadata and complete history follow; run.log and all diagnostics read.4686 initial updates+30 completed CG attempts(28 accepted),50 line values,2 restarts,0 nonfinite proposals.81 complete full-pool evaluations comprise30 completed-attempt gradients,50 line values and one gradient in the final unfinished deadline-limited attempt; its base is restored with no extra step. Counts reconcile12898464 PDE/10873464 IC evaluations and6711 physics calls. Training743.702962 seconds,480837parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.13017978405582073,
    "physics_weighted": 0.04764392777598699,
    "ic_relative_l2": 0.2872905433177948,
    "ic_relative_mse": 0.08253585627983373,
    "windows": {
      "early": {
        "continuity": 0.03762855030137935,
        "momentum": 0.04484774606352363,
        "poisson": 0.009480041160594267,
        "total": 0.09195633752549724
      },
      "middle": {
        "continuity": 0.011546521189992536,
        "momentum": 0.013023824484507155,
        "poisson": 0.005669911152056814,
        "total": 0.030240256826556504
      },
      "late": {
        "continuity": 0.01697855181591961,
        "momentum": 0.01332416243775524,
        "poisson": 0.010058452192166334,
        "total": 0.04036116644584119
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.990903377532959,
        "0.5": 0.9866795539855957,
        "0.8": 0.9847666025161743
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.009096622467041016,
        "0.5": -0.013320446014404297,
        "0.8": -0.015233397483825684
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.16647709906101227,
        "0.5": 0.40659278631210327,
        "0.8": 0.6792535185813904
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.4091652631759644,
        "0.5": 2.2457382678985596,
        "0.8": 3.489105463027954
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3973439335823059,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.6689300537109375e-06
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
    "params": 480837,
    "training_seconds": 743.7029617500375,
    "optimizer_steps": 4716,
    "physics_calls": 6711,
    "pde_training_evaluations": 12898464,
    "ic_training_evaluations": 10873464,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2415,
      "loss": 0.4198418855667114,
      "elapsed_seconds": 187.52147091605002,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2472960; IC_eval=2472960"
    },
    {
      "step": 4686,
      "loss": 0.3716334402561188,
      "elapsed_seconds": 375.0063251249958,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4798464; IC_eval=4798464"
    },
    {
      "step": 4716,
      "loss": 0.3222374450415373,
      "elapsed_seconds": 743.700660625007,
      "note": "final full PR+; PDE_eval=12898464; IC_eval=10873464; PDE_draws=4898464; IC_draws=4873464; cg=30; accepted=28; full=100000/75000; micro=4096; lines=50; nf=0; restarts=2"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12898464,
    "IC_eval": 10873464,
    "PDE_draws": 4898464,
    "IC_draws": 4873464,
    "cg": 30,
    "accepted": 28,
    "lines": 50,
    "nf": 0,
    "restarts": 2,
    "complete_full_evaluations": 81,
    "uncompleted_attempt_full_gradients": 1
  }
}
```

## Decision and interpretation

Cutoff5 does not improve total: L_val rises0.0070713921 (5.74%) versus047. IC MSE falls0.0009216471, while physics rises0.0079930392. Every continuity, momentum and Poisson window component worsens.4686 initial updates versus4952,81 full evaluations each reflect moderate extra feature cost as well as different trajectory/initialisation. Retain finite evidence without gates;047 remains leader. The input-bandwidth tradeoff differs from042 initial-jet bandwidth; no general Fourier bandwidth verdict or significance/reference-accuracy claim. Five1800-second finalists remain pending after60.
