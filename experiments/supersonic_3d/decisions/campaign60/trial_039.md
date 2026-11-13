# Trial 039

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=conservative_momentum_residual_training.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.038 derivativepenaltyhadverylargeoverhead/ICdegradation,so039 usesan equivalentfirst-derivativePDEtrainingformonbestunchangedmodel. Prior75Trial032 changedoutputparameterisationtom/rho;itdidnotchangemomentumtrainingresidualtoconservativefluxform. Historicalcontrolvolumefacepointsforbiddenhereandnotreproduced.

## Novelty claim

Mechanism: trainconservativemomentumresidualRcons_j=partial_t(rho v_j)+sum_i partial_i(rho v_i v_j)+cs^2partial_jrho+rho partial_jphi. ProductrulegivesRcons=Radv+vRcontinuityusingunchangeddensity-weightedownermomentum. Smoothzeroresidualsystemisequivalentwhencontinuityzero;off-manifoldtraininglossdifferent,notfixedscalarretuning. ConservationlawbackgroundprimaryClawpackRiemannbook https://www.clawpack.org/riemann_book/html/Euler.html mass/momentumsectionread;bookuses1DpolytropicEulerbutonlygenericmass/momentumfluxidentityused,ourisothermalpressureandgravityunchanged. cPINNpaperDOI403notread/notclaimedreproduced. Localstrongformtraining,nodomaindecomposition/fluxinterfacepenalty/weakshocksolutionguarantee.

## Hypothesis and proposed change

Primaryhypothesis: explicitmass-momentumresidualcouplingimprovesearlycontinuity/momentumtradeoffatmatchedtimewithoutICdamage. Same028model/outputs and1024PDE/ICpoolbatches. Ownercontextprovidescanonicalcontinuity/Poisson/IC;secondsame-qmodelpasswithtraining-onlyunchangedC/RadvhelpercomputesRcons=Radv+velocity*C. FirstphaseF=MSE(C)+sum_jMSE(Rcons_j)+MSE(Poisson)+sumICabsoluteMSEallcoef1. Owneradvectivemomentumtermnotusedinthisinitialphaseloss,butscorer/finalPRcanonicalFuntouched. ExtraPDEforwardcountsce,noextradraws/coordinates;ownhelperdoesnotcomputeunneededPoissonsecondderivative. CPU/nativeMPSmanufacturedpolynomialdirectfluxdivergenceidentity,parametergradientagreementandC0equivalencepassed;nounrecordedPINNfits.028model/fullcanonicalchunk/evaluatefull/PRloopASTidentical.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677params,028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM.94080hiddenweightsAdan lr.001betas(.98,.92,.99)eps1e-8;54597auxAdaBelief lr.001betas(.9,.999)eps1e-12. First80%1024PDE+1024ICreplacementpooldraws,canonicalC/Poisson/ICplusconservativemomentum;2048PDEpointforwardevaluationsperinitialupdate,1024draws;IC1024. Final20%canonicaladvectivesumfivePDE+sumICallcoef1,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpointcapperupdate,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,750000paramcap,onlyfrozenpools. OwnerPDEnumexcludesdirectpass,historycewill supplementit;actualcountsrecorded.

## Expected outcome

Falsifiabletarget L_val<.16293784616066054 throughlowercanonicalearlycontinuity/momentumwithIC/latertradeoffimprovement. RadvandvCcanpartlycancelwhenCnonzero;velocitysuppressionmayharmIC;secondPDEpassreducesupdates;canonicalfinishcanundodifferences. ConservativepointwiseresidualdoesnotimposeRankine-Hugoniot/entropyconditionsorstabiliseshocksautomatically. Reportallwindows/components/recordedcons-versusadvtrainingmoments/counts/physicaldiagnostics,noeligibilitygates. SinglefitisnotgeneralconservativePINNsuperiority/significance/numericalaccuracyproof.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 10590 initial updates+25 CG attempts(24 accepted),44 line values,0 restarts/nonfinite proposals,69 complete full-pool evaluations reconcile28588320 full PDE/16019160 IC evaluations and12315 physics calls. OwnerPDEnum17744160 excludes10844160directsame-batchconservativemomentumforwards;historyceadds them,rawmetadataunchanged. Training741.662556 seconds,148677parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.1717794908122806,
    "physics_weighted": 0.060682777067832316,
    "ic_relative_l2": 0.3333117365837097,
    "ic_relative_mse": 0.1110967137444483,
    "windows": {
      "early": {
        "continuity": 0.13723228113386854,
        "momentum": 0.04273093770059299,
        "poisson": 0.005382255410420513,
        "total": 0.18534547424488204
      },
      "middle": {
        "continuity": 0.00572481302245685,
        "momentum": 0.01721270811268692,
        "poisson": 0.004205705914249079,
        "total": 0.02714322704939285
      },
      "late": {
        "continuity": 0.008853746853413547,
        "momentum": 0.01473466380393231,
        "poisson": 0.007353017550730255,
        "total": 0.030941428208076112
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9956283569335938,
        "0.5": 0.9894582629203796,
        "0.8": 0.9882129430770874
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.00437164306640625,
        "0.5": -0.010541737079620361,
        "0.8": -0.011787056922912598
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.0942130833864212,
        "0.5": 0.3044354319572449,
        "0.8": 0.5485638380050659
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2361491918563843,
        "0.5": 1.910894751548767,
        "0.8": 2.9750022888183594
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.38242092728614807,
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
    "training_seconds": 741.6625556249637,
    "optimizer_steps": 10615,
    "physics_calls": 12315,
    "pde_training_evaluations": 17744160,
    "ic_training_evaluations": 16019160,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 3363,
      "loss": 0.570214033126831,
      "elapsed_seconds": 187.54632099997252,
      "note": "conservative mom=0.059219; adv=0.12186; PDE_eval=6887424; IC_eval=3443712"
    },
    {
      "step": 6653,
      "loss": 0.4906800389289856,
      "elapsed_seconds": 375.0232645829674,
      "note": "conservative mom=0.066052; adv=0.1843; PDE_eval=13625344; IC_eval=6812672"
    },
    {
      "step": 9933,
      "loss": 0.48065200448036194,
      "elapsed_seconds": 562.5051990000065,
      "note": "conservative mom=0.055463; adv=0.12182; PDE_eval=20342784; IC_eval=10171392"
    },
    {
      "step": 10615,
      "loss": 0.4843058306723833,
      "elapsed_seconds": 741.6616942079854,
      "note": "final full PR+; PDE_eval=28588320; IC_eval=16019160; PDE_draws=10944160; IC_draws=10919160; cg=25; accepted=24; full=100000/75000; micro=4096; lines=44; nf=0; restarts=0; ce=10844160"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 28588320,
    "IC_eval": 16019160,
    "PDE_draws": 10944160,
    "IC_draws": 10919160,
    "cg": 25,
    "accepted": 24,
    "lines": 44,
    "nf": 0,
    "restarts": 0,
    "ce": 10844160
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0088416447 (5.43%) versus028. Weightedphysics improves0.0075533608,but IC MSE rises0.0163950055. Allcontinuitycomponentsimprove,butallcanonicalmomentumandPoissoncomponentsworsen. Early/latetotalsimprove,middleworsens. RecordedconservativemomentumMSEsum.055..066versusadvective.122..184isconsistentwithnegativecross-termcancellationagainstnonzeroC;doesnotprovefinalcause.10590initialupdatesversus02814643reflectsecondforwardcost,butfarlessthan038higherderivativecost. Equivalentzero-setlossdoesnotguaranteesameoptimisation/validationoutcome. Retainfinite resultwithoutdiagnosticgates;028 remainslowest,no generalconservativePINNverdict/significance/numericalaccuracyclaim.
