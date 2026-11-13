# Trial 040

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=augmented_lagrangian_signed_residual_means.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.039 conservativeformreducedCbutIC/momentumtradeoffworsened;040 retainscanonicalpointwiseFandaddsmean-constraintdualsinstead. Prior036usedpositiveweightsoneightMSEtasks;040usesSIGNEDresidualmeansandlinearLagrangeterms,substantivelydifferent. No warmstart.

## Novelty claim

Mechanism: stochasticprojectedaugmented-Lagrangian(weakmeanconstraints)training. KnownPINNaugmentedLagrangianprecedentLu etal. https://arxiv.org/html/2102.04626v1 Section2.6/Algorithm2read. Localadaptationuses8globalmeanconstraints,notmultipliersateachlocationorinversedesigninequalities;fixedrho1,boundedduals[-10,10],64-stepblockaverages,noincreasingpenaltyorconvergedinnersolve. NotexacthPINNreproduction/globalnovelty/hardpointwiseconstraintguarantee. RetainsallcanonicalMSEterms,soameanconstraintdoesnotreplacepointwisephysics.

## Hypothesis and proposed change

Primaryhypothesis: dualcorrectionstocoherentsignedPDE/ICbias improvecombinedvalidationtradeoffwithout036slossmagnitudeweighting. g=concat(mean5canonicalPDEresiduals,mean3ICvelocityerrors),PDEandICmeansnormalisedseparately. FirstphaseF=canonicalMSE+lambda.dot(g)+.5||g||^2. lambda starts0;every64primalupdateslambda=clip(lambda+meanof64detachedg,-10,10),thenresetblocksum. Noautogradthroughdualupdates;tailblockstatepreservedbutnotappliedaftertraining. Canonicalcontextbackwardthenextrastored-qPDEpassandstoredICpassbuildg/augmentationbackwardbeforeoptimiserstep. Secondforwardsbothcountedae,notextradraws. PointwiseresidualhelperASTexact038(manufacturedalgebraverifiedthere),028model/fullcanonicalfinishASTunchanged. CPU/nativeMPSsignedmeananalyticgradients,dualprojection,distinctionfromsign-insensitiveMSEandJensenlowerboundF>=-||lambda||^2/6checks passed onsyntheticresidualarrays,noPINNfits/newcoordinates.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677fieldparamsplus8boundedupdateddualvariables(148685combinedslots,dualsnotmodelparameters),under750000. Same028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM.94080hiddenweightsAdan lr.001betas(.98,.92,.99)eps1e-8;54597auxAdaBelief lr.001betas(.9,.999)eps1e-12. First80%1024PDE+1024ICreplacementpooldraws,canonicalsumfivePDE+sumthreeICabsoluteMSEallcoef1plusaugmentation;2048PDEand2048ICpointforwardsperinitialupdate,1024drawsperpool. Final20%canonicalFonly,noaugmentation/dualupdates,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpointcapperstep,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,onlyfrozenpools. Supplementbothownerpointcounterswithae;recorddualdates/clips/augmentationnorms. Augmentedobjectivecanlegitimatelybenegative,notavalidationloss.

## Expected outcome

Falsifiabletarget L_val<.16293784616066054 throughreducedcoherentresidualbiaswithoutIC/physicsimbalance. Globalmeanscanalreadybesmallorcancelpointwiseerrors;batchnoiseand64stepapproximateinneriterationsmaydrivedualoscillation;boxprojectionprecludesstandardunboundedmultipliertheorems;extraPDE/ICforwardsreduceupdates. Canonicalfinishcaneraseeffects. Reportallwindowcomponents/counts/dualnorms/clipping/physicaldiagnosticswithouteligibilitygates. Singlefreshfitisnotconvergence/KKTfeasibility/significance/Athenaaccuracyproof.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 7576 initial updates+118 dualblockupdates(24sampledtailiterationsretained,0clippedcomponents)+25 CG attempts(24 accepted),44 line values,4 restarts,0 nonfinite proposals,69 complete full-pool evaluations reconcile22415648 full PDE/20690648 full IC evaluations and9301 physics calls. OwnerPDEnum14657824/ICnum12932824 eachomit7757824directsame-batchaugmentationforwards;historyaeadds them,rawmetadataunchanged. Training741.979999 seconds,148677fieldparamsplus8boundeddualvariables. No execution error.

```json
{
  "metrics": {
    "L_val": 0.167738550951457,
    "physics_weighted": 0.06295463515021389,
    "ic_relative_l2": 0.32370343804359436,
    "ic_relative_mse": 0.10478391580124313,
    "windows": {
      "early": {
        "continuity": 0.15987526299474533,
        "momentum": 0.028873978600816565,
        "poisson": 0.006284717343338471,
        "total": 0.19503395893890035
      },
      "middle": {
        "continuity": 0.009414560074553886,
        "momentum": 0.012008817508673435,
        "poisson": 0.004447701996938838,
        "total": 0.02587107958016616
      },
      "late": {
        "continuity": 0.013087750331792446,
        "momentum": 0.011672088651299675,
        "poisson": 0.0076131999936758215,
        "total": 0.032373038976767944
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9954410791397095,
        "0.5": 0.9916133880615234,
        "0.8": 0.990562915802002
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004558920860290527,
        "0.5": -0.008386611938476562,
        "0.8": -0.009437084197998047
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10553310811519623,
        "0.5": 0.3182089626789093,
        "0.8": 0.5736473798751831
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2535632848739624,
        "0.5": 1.9349825382232666,
        "0.8": 3.0531396865844727
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3381003141403198,
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
    "training_seconds": 741.9799989999738,
    "optimizer_steps": 7601,
    "physics_calls": 9301,
    "pde_training_evaluations": 14657824,
    "ic_training_evaluations": 12932824,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2354,
      "loss": 0.5561092179559637,
      "elapsed_seconds": 187.56658966699615,
      "note": "AL aug=0.00025824; gnorm=0.025784; dualnorm=0.088332; du=36; PDE_eval=4820992; IC_eval=4820992"
    },
    {
      "step": 4727,
      "loss": 0.5115887135034427,
      "elapsed_seconds": 375.0481797919492,
      "note": "AL aug=0.00023594; gnorm=0.015346; dualnorm=0.076208; du=73; PDE_eval=9680896; IC_eval=9680896"
    },
    {
      "step": 7102,
      "loss": 0.4551717581052799,
      "elapsed_seconds": 562.5501911249594,
      "note": "AL aug=6.4099e-05; gnorm=0.028083; dualnorm=0.06268; du=110; PDE_eval=14544896; IC_eval=14544896"
    },
    {
      "step": 7601,
      "loss": 0.44651445746421814,
      "elapsed_seconds": 741.9789376669796,
      "note": "final full PR+; PDE_eval=22415648; IC_eval=20690648; PDE_draws=7857824; IC_draws=7832824; cg=25; accepted=24; full=100000/75000; micro=4096; lines=44; nf=0; restarts=4; ae=7757824; du=118; dc=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 22415648,
    "IC_eval": 20690648,
    "PDE_draws": 7857824,
    "IC_draws": 7832824,
    "cg": 25,
    "accepted": 24,
    "lines": 44,
    "nf": 0,
    "restarts": 4,
    "ae": 7757824,
    "du": 118,
    "dc": 0
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0048007048 (2.95%) versus028. Weightedphysics improves0.0052815028,but IC MSE rises0.0100822075. Allwindowtotals,continuityandmomentumcomponentsimprove;allPoissoncomponentsworsen. Recordedmeanconstraintnorm.015..028,dualnorm.063..088andaugmentation~.000064..000258aresmall,zero dualclips. Meansalreadynearsmallvaluesandextra passcost7576initialupdatesversus02814643limitinterpretation;noevidenceofhardpointwisefeasibilityorlargeusefuldualcorrection. Retainfinite resultwithoutdiagnosticgates;028 remainslowest,nogeneralALmethodverdict/significance/numericalaccuracyclaim.
