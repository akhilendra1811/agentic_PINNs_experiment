# Trial 033

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=residual_dependent_causal_temporal_gates.

## Parent methods and evidence

Trial028 parent:bestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.032 reducedphysics78% butICworsened,so retainbestunconstrainedmodel forlossmethodtest. Prior75 Trial002 was stagedsampling30%early/30%through.5/finalalltimes,not residualdependentgating;itsbadlatererror motivates keepingalltimes sampledthroughout. Historicallaterrecord calls002 causalweights inconsistently;actual002 hypothesis specifies sampling,disclosed here.

## Novelty claim

Mechanism: currentresidual-dependent causal temporal weights,not fixedscalarcoefficients or prescribedtimecurriculum. Wang,Sankaran,Perdikaris https://arxiv.org/pdf/2203.07404 Section3 eq3.2/Algorithm1 providesexponentialprefixweights withstopgradient. Localvariant:threecoarsewindows[0,.2],(.2,.5],(.5,.8],epsilon1 fixed,ICoutsideprefix,noIC1000coefficient,noepsilonanneal/weightthresholdstopping. Last20%returns tocanonicalfull-poolPR+. Knownmethod/localadaptation,notglobalnovelty.

## Hypothesis and proposed change

Primaryhypothesis: residualfeedback directs effort towardearlydynamics without withholdinglatepoints,improving total. Keep028modelASTexact andglobal1024PDE/1024IC pooldraws. PartitionPDEnaturalbatch bytimewindows;splitICbatchacrosspopulatedwindows soeachdrawnICusedonce. ComputeFj=continuity+summomcomponents+Poisson,detachedwj=exp(-sumpreviousF),withwfirst1. Initialphase loss=sum(nj/n)wjFj+sum(ni/nIC)ICj. No differentiationthroughweights;normalisationretainsglobalempiricalmeanwhenallweights1. Emptywindows skippedwithoutfabricatedpoints;orderedpopulatedprefixused. Canonicalevaluationchunk/fullfinish/PR+ASTunchanged;ownercallcountinitialupto3perstep explicitlyloggedcc. CPU/nativeMPS gatearithmetic/stopgradient/monotonicity/zeroloss/windowboundarytests passed,noPDEfitsorcoordinatesgenerated.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677params,same028sevenaffinewidth128/sixSnake/five19featureinputskips/boundedtimeFiLM1->32->1536.94080hiddenweightsAdan lr.001,betas(.98,.92,.99),eps1e-8;54597auxAdaBelief lr.001,betas(.9,.999),eps1e-12. First80%causallyweightedcanonicalphysicsplusunweightedICabsoluteMSE;IC_x+IC_y+IC_zcoef1. Final20%canonicalF=sumfivephysics+sumthreeICallcoef1,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpointcapperstep,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,750000paramcap. Allcoordinatesfrozenpool,noaddedpoints. Recordactualevaluations,draws,cc,weights.

## Expected outcome

Falsifiabletarget L_val<0.16293784616066054 throughlower earlyresidual withoutIC/latepenaltyerasinggain. Samplewindowresidualnoise maymisgate;wlate mayremainlow;coarsewindows/extraownerPythoncalls canreducespeed. Epsilonfixed1notpaperannealing,andcanonicalfinish mayundoearlybenefits. Reportwindowlosses/weightsandallphysicaldiagnostics withouteligibilitygates. Singlefreshfit isexploratory,nosignificance/generalcausalityalgorithmaccuracyclaim.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 5513 initial updates/16539 causal contextcalls+25 CG attempts(23 accepted),43 line values,7 restarts,0 nonfinite proposals,68 complete full-pool evaluations reconcile12445312 PDE/10745312 IC evaluations and18239 physics calls. Training738.355950 seconds,148677parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.17459712428282353,
    "physics_weighted": 0.06897219014594576,
    "ic_relative_l2": 0.3249998986721039,
    "ic_relative_mse": 0.10562493413687779,
    "windows": {
      "early": {
        "continuity": 0.1600904584117382,
        "momentum": 0.02978690752144713,
        "poisson": 0.006111306236474291,
        "total": 0.19598867216965962
      },
      "middle": {
        "continuity": 0.011803300929776099,
        "momentum": 0.013841724936161011,
        "poisson": 0.0051695126100387324,
        "total": 0.030814538475975845
      },
      "late": {
        "continuity": 0.01577401358279345,
        "momentum": 0.01471613955863503,
        "poisson": 0.01057003519701366,
        "total": 0.04106018833844214
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9949246644973755,
        "0.5": 0.9892926216125488,
        "0.8": 0.9872201681137085
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005075335502624512,
        "0.5": -0.010707378387451172,
        "0.8": -0.012779831886291504
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10458550602197647,
        "0.5": 0.3127947449684143,
        "0.8": 0.5603957176208496
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2537864446640015,
        "0.5": 1.9046883583068848,
        "0.8": 2.956591844558716
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.38899508118629456,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.1457672119140625e-06
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
    "training_seconds": 738.3559503749711,
    "optimizer_steps": 5538,
    "physics_calls": 18239,
    "pde_training_evaluations": 12445312,
    "ic_training_evaluations": 10745312,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 1724,
      "loss": 0.5642770528793335,
      "elapsed_seconds": 187.59970745799365,
      "note": "causal eps1; w=[1.0, 0.794125497341156, 0.7371107339859009]; PDE_eval=1765376; IC_eval=1765376"
    },
    {
      "step": 3439,
      "loss": 0.48643648624420166,
      "elapsed_seconds": 375.04459862498334,
      "note": "causal eps1; w=[1.0, 0.768507182598114, 0.7173522114753723]; PDE_eval=3521536; IC_eval=3521536"
    },
    {
      "step": 5162,
      "loss": 0.47707825899124146,
      "elapsed_seconds": 562.5313722909777,
      "note": "causal eps1; w=[1.0, 0.7783406972885132, 0.7348527908325195]; PDE_eval=5285888; IC_eval=5285888"
    },
    {
      "step": 5538,
      "loss": 0.45904938224703074,
      "elapsed_seconds": 738.3528525829897,
      "note": "final full PR+; PDE_eval=12445312; IC_eval=10745312; PDE_draws=5745312; IC_draws=5720312; cg=25; accepted=23; full=100000/75000; micro=4096; lines=43; nf=0; restarts=7; cc=16539"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12445312,
    "IC_eval": 10745312,
    "PDE_draws": 5745312,
    "IC_draws": 5720312,
    "cg": 25,
    "accepted": 23,
    "lines": 43,
    "nf": 0,
    "restarts": 7,
    "cc": 16539
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0116592781 (7.16%) versus028. Weighted physics rises0.0007360522 and IC MSE0.0109232259. Earlytotal improves0.0210012601,but middle/late worsen,including everylatecomponent. Recordedgatesapproximately[1,.77-.79,.72-.74]aremoderate,notcompletewithholdinglatepoints. Initialupdates5513versus02814643 showmajor overhead ofthreecontextcalls/smallerbatches/graphpartition andhostweightlogging;notisolatedcausalweightingevidence. Retain finite result,noIC/physicalgates;028 remains lowest,no general causalPINN verdict or significance claim.
