# Trial 038

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=gradient_enhanced_euler_poisson_residuals.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.037 allICheadsolves reducedsubproblemtrainingerrorbutnetworse.038 returnsbestunchangedmodelandtestsdifferentphysicslearningcriterion,residualderivativeregularity. No warmstartortrainedstatereuse.

## Novelty claim

Mechanism: known gradient-enhancedPINN(gPINN),Yu,Lu,Meng,Karniadakis https://arxiv.org/html/2111.02801v1 Section2.2. AddcoordinatederivativesofunchangedPDEresidualsattheexistingcollocationpoints;notmerecanonicalweighttuning. Local5residual/4coordinatepenalty,weight.01,first80%only,canonicalPRfinish;notpaperproblem/architecture/RARreproduction. No new/perturbedcollocationpositionsorgradientlabels. Supersonicstrongform/shocksolutionaccuracyisnotestablishedbyresidualsmoothness.

## Hypothesis and proposed change

Primaryhypothesis: constraininglocalvariationofresiduals improvesfrozenvalidationtotaldespitehigherADcost. Addtraining-onlypointwiseresidualhelperusingexactunchangedcontinuity,rho-weightedadvectivemomentum+pressure+gravity,andPoissonformulasreadfromownerphysicscode. Separatefromscoring,noL_valimplementation. Sameqbatchdetachedandrequiresgrad(nochangesinvalues),secondmodelpass yieldsr5;G=mean_points sum_residuals sum_(x,y,z,t)(partial r)^2;firstphaseF=canonicalPDE+IC+.01G. CanonicalcontextbackwardthenGbackwardaccumulatesbeforeoptimiserstep. NoextraICforward. CountextraPDEquerypointsgeoutsideownercounters,notextradraws. CPU/nativeMPSmanufacturedpolynomial residuals,closedformresidualderivatives,parametergradientsofGandfourthfeaturederivativespassed;syntheticalgebracheckonly,nounrecordedPINNfit.028model/fullcanonicalchunk/evaluatefull/PRloopASTidentical.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677params,028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM.94080hiddenweightsAdan lr.001betas(.98,.92,.99)eps1e-8;54597auxAdaBelief lr.001betas(.9,.999)eps1e-12. First80%1024PDE+1024ICreplacementpooldraws;canonicalF=sumcontinuity/momxyz/Poisson+sumicxyzabsoluteMSEallcoef1,plus.01Gwithrawphysicalcoordinatederivatives(equalcoordinateweights,norescaling). PDEpointforwardevaluations2048perinitialupdate,draws1024;IC1024. Final20%canonicalFonly,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpersteppointcap,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,750000paramcap,onlyfrozenpools. Extraautodiffworkchargedinsidebudget;actualge/countersrecorded.

## Expected outcome

Falsifiabletarget L_val<.16293784616066054,lowerweightedphysicswithoutICincreaseerasinggain. Higherderivativegraphs/repeatedforwardmayseverelyreduceupdates;rawtime/spaceunitsscaleGunequally,derivativerestrictionsmayoversmoothflow,anddensitystartupclampatt.05onlypiecewisesmooth(autodiffignoresthekinkdistribution). AddedregularitycouldunderfitICorlaterdynamics. Reportallwindows/components/gradientpenalties/counts/physicaldiagnostics,noeligibilitygates. Singlefitdoesnotproveconvergence,statisticalsignificance,gPINNgeneralrankorAthenaaccuracy.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 1739 initial updates+25 CG attempts(22 accepted),45 line values,0 restarts/nonfinite proposals,70 complete full-pool evaluations reconcile10561472 full PDE/7030736 IC evaluations and3489 physics calls. OwnerPDEnum8780736 excludes1780736directsame-batchgradientpenaltyforwards;historygeadds them,rawmetadataunchanged. Training741.618396 seconds,148677parameters. Repeatedautodiffderivativesreuseeachforwardandarenotmiscountedasnewcoordinates. No execution error.

```json
{
  "metrics": {
    "L_val": 0.19171240917893428,
    "physics_weighted": 0.061082366156314134,
    "ic_relative_l2": 0.36142778396606445,
    "ic_relative_mse": 0.13063004302262016,
    "windows": {
      "early": {
        "continuity": 0.13215620135794998,
        "momentum": 0.02622017804269775,
        "poisson": 0.009907187813073795,
        "total": 0.1682835672137215
      },
      "middle": {
        "continuity": 0.010019666959256641,
        "momentum": 0.012566582085972387,
        "poisson": 0.006270505745022335,
        "total": 0.028856754790251363
      },
      "late": {
        "continuity": 0.012708562260280267,
        "momentum": 0.013078404767051396,
        "poisson": 0.011750285525657175,
        "total": 0.03753725255298884
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9950188398361206,
        "0.5": 0.9896425008773804,
        "0.8": 0.9886010885238647
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0049811601638793945,
        "0.5": -0.010357499122619629,
        "0.8": -0.011398911476135254
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.09345986694097519,
        "0.5": 0.2842258810997009,
        "0.8": 0.5095465183258057
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.219034194946289,
        "0.5": 1.7986929416656494,
        "0.8": 2.738107204437256
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.41359952092170715,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.0265579223632812e-06
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
    "training_seconds": 741.6183958750335,
    "optimizer_steps": 1764,
    "physics_calls": 3489,
    "pde_training_evaluations": 8780736,
    "ic_training_evaluations": 7030736,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 538,
      "loss": 0.7271522903442382,
      "elapsed_seconds": 187.56300991697935,
      "note": "gPINN raw_grad=1.43681; PDE_eval=1101824; IC_eval=550912; extra=550912"
    },
    {
      "step": 1083,
      "loss": 0.5988248586654663,
      "elapsed_seconds": 375.00456274999306,
      "note": "gPINN raw_grad=1.56055; PDE_eval=2217984; IC_eval=1108992; extra=1108992"
    },
    {
      "step": 1629,
      "loss": 0.5933971977233887,
      "elapsed_seconds": 562.5116962500033,
      "note": "gPINN raw_grad=1.58843; PDE_eval=3336192; IC_eval=1668096; extra=1668096"
    },
    {
      "step": 1764,
      "loss": 0.5521292546764016,
      "elapsed_seconds": 741.613198624982,
      "note": "final full PR+; PDE_eval=10561472; IC_eval=7030736; PDE_draws=1880736; IC_draws=1855736; cg=25; accepted=22; full=100000/75000; micro=4096; lines=45; nf=0; restarts=0; ge=1780736"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 10561472,
    "IC_eval": 7030736,
    "PDE_draws": 1880736,
    "IC_draws": 1855736,
    "cg": 25,
    "accepted": 22,
    "lines": 45,
    "nf": 0,
    "restarts": 0,
    "ge": 1780736
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0287745630 (17.66%) versus028. Weightedphysics improves0.0071537718,but IC MSE rises0.0359283348. Earlytotal improves,middle/lateworsen;allPoissoncomponentsworsen. Initialupdates1739versus02814643(about11.9%)showlargehigher-derivativecost;recordedrawgradientpenalty1.44..1.59addsabout.014..016atcheckpoints. Cannotisolateregularityfromundertrainingandrawcoordinateunitbias. Retainfinite resultwithoutdiagnosticgates;028 remainslowest,no generalgPINNverdict/significance/numericalaccuracyclaim.
