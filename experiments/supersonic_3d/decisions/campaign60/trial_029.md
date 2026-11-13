# Trial 029

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:28; kind=mechanism; mechanism_id=gaussian_hidden_ridge_units.

## Parent methods and evidence

Trial028 parent: L_val0.16293784616066054,weighted physics0.0682361379091252,IC_relative_MSE0.09470170825153534,new lowest finite. Retain its repeated-input-skip/bounded-time-FiLM architecture and trainer. Earlier018 Gaussian-windowed sine scored0.17141623197315076 on011,so locality alone is not assumed beneficial;029 tests a distinct nonoscillatory even shape on the current backbone.

## Novelty claim

Mechanism: six main hidden Gaussian scalar-ridge activations exp(-z^2),replacing unbounded linear-plus-periodic Snake. This is a known smooth Gaussian shape,not publication novelty or a scalar-frequency tweak. Bai et al. PIRBN https://arxiv.org/pdf/2304.06234 Section3 eq17 supplies Gaussian-basis precedent,but their single-layer radial-distance/fixed-centre network is NOT reproduced. Our deep affine ridges are not radial in the full input space. Conditioner remains Snake. Prior75 decision text contains no Gaussian/RBF/radial mention (text search only).

## Hypothesis and proposed change

Primary hypothesis: nonoscillatory localized hidden responses reduce residual amplification while input skips retain direct Fourier access,improving total at equal time. Add parameter-free GaussianActivation forward exp(-x.square());use it at all six main sites and in raw_from_features type dispatch. All main Linear shapes/initialisation,density transform,conditioner,and entire028 trainer unchanged. CPU/native MPS analytic first/second/third derivatives (-2xg,(4x^2-2)g,(12x-8x^3)g),evenness,148677parameter count,finite synthetic feature derivatives/all-parameter gradients passed. No PDE fitting/extra coordinates in checks.

## Training objective and setup

Canonical training F=continuity+mom_x+mom_y+mom_z+poisson+IC_x+IC_y+IC_z absolute MSE,all coefficients1. Frozen score0.2early+0.3middle+0.5late+IC_relative_MSE unchanged. Seven main affine layers width128,five19-feature input concatenations,six Gaussian units;time FiLM1->32->1536 with Snake conditioner.148677params:94080 hidden weights Adan lr.001,betas(.98,.92,.99),eps1e-8;54597aux unrectified AdaBelief lr.001,betas(.9,.999),eps1e-12. First80%1024PDE+1024IC replacement pool draws. Final20%full-pool restarted PR+/Armijo on100000PDE/75000IC via4096/3072 microbatches+tail. No total per-step point cap,8192percontextcall.750seconds,fresh weights,physical seed82/training823001,MPS,750000parameter cap;all sampling only frozen pools. Actual counts reported after run.

## Expected outcome

Falsifiable target L_val<0.16293784616066054,with lower weighted physics and IC degradation small enough to preserve net gain. Even/nonnegative hidden responses may instead saturate,lose signed signal or fit IC poorly;bounded FiLM and direct skips may only partly compensate. Report every window/component,throughput and density/mass/periodicity diagnostics. No diagnostic gates;single shared-seed fit does not prove significance or general Gaussian/RBF superiority.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 15082 initial updates+27 CG attempts(24 accepted),46 line values,8 restarts,0 nonfinite proposals,73 complete full-pool evaluations reconcile22743968 PDE/20918968 IC evaluations and16907 physics calls. Training741.762495 seconds,148677parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.17020454756795855,
    "physics_weighted": 0.06889858767238845,
    "ic_relative_l2": 0.3182859718799591,
    "ic_relative_mse": 0.10130595989557012,
    "windows": {
      "early": {
        "continuity": 0.1698043192809098,
        "momentum": 0.03286607015028545,
        "poisson": 0.003697595189396045,
        "total": 0.2063679846205913
      },
      "middle": {
        "continuity": 0.01122512120493797,
        "momentum": 0.01377006382589646,
        "poisson": 0.004909752862206605,
        "total": 0.029904937893041036
      },
      "late": {
        "continuity": 0.01488405845811555,
        "momentum": 0.012989458469749283,
        "poisson": 0.009433501832850907,
        "total": 0.03730701876071574
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9950789213180542,
        "0.5": 0.9909447431564331,
        "0.8": 0.9899783134460449
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004921078681945801,
        "0.5": -0.009055256843566895,
        "0.8": -0.010021686553955078
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10499290376901627,
        "0.5": 0.31745702028274536,
        "0.8": 0.5712878704071045
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2551372051239014,
        "0.5": 1.9381362199783325,
        "0.8": 3.0418801307678223
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.27749860286712646,
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
    "params": 148677,
    "training_seconds": 741.7624951659818,
    "optimizer_steps": 15109,
    "physics_calls": 16907,
    "pde_training_evaluations": 22743968,
    "ic_training_evaluations": 20918968,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4624,
      "loss": 0.565211832523346,
      "elapsed_seconds": 187.51203550002538,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4734976; IC_eval=4734976"
    },
    {
      "step": 9374,
      "loss": 0.4551928639411926,
      "elapsed_seconds": 375.00331129098777,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9598976; IC_eval=9598976"
    },
    {
      "step": 14125,
      "loss": 0.4513206481933594,
      "elapsed_seconds": 562.5235346659902,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=14464000; IC_eval=14464000"
    },
    {
      "step": 15109,
      "loss": 0.4336266862228513,
      "elapsed_seconds": 741.7621281250031,
      "note": "final full PR+; PDE_eval=22743968; IC_eval=20918968; PDE_draws=15543968; IC_draws=15518968; cg=27; accepted=24; full=100000/75000; micro=4096; lines=46; nf=0; restarts=8"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 22743968,
    "IC_eval": 20918968,
    "PDE_draws": 15543968,
    "IC_draws": 15518968,
    "cg": 27,
    "accepted": 24,
    "lines": 46,
    "nf": 0,
    "restarts": 8
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0072667014 (4.46%) versus028. IC MSE rises0.0066042516 and weighted physics0.0006624498. Early physics improves,but middle/late worsen,including all late components. Retain finite result without diagnostic gates;028 remains lowest. Similar throughput does not explain mechanism causally;no general Gaussian/RBF inferiority or significance claim.
