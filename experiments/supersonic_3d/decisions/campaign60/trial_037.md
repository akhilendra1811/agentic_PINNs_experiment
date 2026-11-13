# Trial 037

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=full_ic_proximal_linear_readout_solves.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.036 taskminimaximprovedICbutphysicsworsened,score.1800193811.037 exploitsa separablelinearICreadoutsubproblemwithoutchangingscore/modelcapacity. Initialnetworkfresh,all75kICcoordinates/labelssolelyfromauthorisedcontext,noexternaltrajectories.

## Novelty claim

Mechanism: alternatecanonicalgradienttrainingwithperiodicproximalleast-squaressolvesofthreevelocityreadoutrows,biasincluded. Classicalseparableleast-squares/variableprojectionprecedentGolub,Pereyra https://doi.org/10.1137/0710036 (publisherabstractread;fulltextpaywalled). PDE-VarProDong,Yang https://arxiv.org/abs/2201.09989 abstractread. Our nonlinearEuler-PoissonPDEisNOTlinearised/eliminated;onlyICsubproblemissolvedevery256initialupdates. Notexactreduced-objectiveVarPro,notauthorsimplementation/globalnovelty. HiddenfeaturesstilloptimisedbycanonicalPDE/ICgradients,andAdan/AdaBeliefreadoutmomentsretainedwithoutreset.

## Hypothesis and proposed change

Primaryhypothesis: accuratelysolvingthefull-poolIClinearheadsubproblemimprovesnetIC/physicsbalanceatmatchedtime. Every256initialAdam-familyupdates,whilefraction<.78andremaining>30s,streamall75000ICpointsviacycle4096chunks+tail;fixedhiddenfeaturesh128augmentedwith1giveH129. CPUfloat64accumulateG=H^TH,C=H^TY,Ysquare;solve(G/N+.001I)B=C/N+.001Bprevious. Thisminimises||HB-Y||F^2/N+.001||B-Bprevious||F^2,includingbiasregularisation. Commitonlyvelocityrows1:4of5-outputheadoncefullsolvecomplete;rho/phirowsunchanged. NoPDEacceptancegate. Partialdeadlinequerycountsrecorded,headunchangedifnotcomplete. CPUfloat64smallsolveintentional,notimplicitMPSfallback;allfeatureworkMPS. Refactorraw_from_features optionalhiddenreturnonly,normalforwardpreserves028initialmap/derivativesthroughthirdexactCPU/MPS. Syntheticnormal-equation/proximaldecrease/rankdeficiencychecks passed,nocoordinatefitting. Headprojectionscountasadditionalweightupdates,ls/lf/lasuccess/featurequeries/attemptsrecorded.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677params,same028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM.94080hiddenweightsAdan lr.001betas(.98,.92,.99)eps1e-8;54597auxAdaBelief lr.001betas(.9,.999)eps1e-12. First80%1024PDE+1024ICreplacementpoolcanonicalF=sumfivephysics+sumthreeICabsoluteMSEallcoef1,plusperiodicICheadblocksolves. Eachheadsolvequeries75000ICfeaturesandlabels,countsadditionalICtrainingevaluations/drawsbutnopointwisePDEcalls;ownerICmetadataexcludesthem,supplementwithlf. Final20%canonicalfull-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail,noheadsolves;finishASTunchanged. No totalpointcapperupdate;8192percontextcall.750seconds,freshweights,seed82/train823001,MPSplusCPUfloat64smallsolves,750000paramcap.Onlyfrozenpools.

## Expected outcome

Falsifiabletarget L_val<.16293784616066054 throughICMSEimprovementwithphysicsincreaselessthanICgain. FullICtrainingLSerrorbefore/aftersolvesmustdecrease;thisdoesnotguaranteeheldoutICimprovement. Readoutchangesaffectvelocityatalltimes,canworsencontinuity/momentum,andstaleadaptiveheadmomentsmayundoit. Gramconditioning/ridgebias,CPUtransfer/fullfeaturepasscostandcanonicalfinishcanerasegains. Reportcounts/lastsolveICtrainingerrors/allwindowcomponents/diagnostics,noIC/density/periodicity/massgates. OnefreshfitisnotVarProconvergenceproof/significance/numericalaccuracy.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 14492 initial gradientupdates+55 completed readoutprojections+24 CG attempts(21 accepted),45 line values,0 restarts/nonfinite proposals,69 complete full-pool evaluations reconcile21739808 PDE/24139808 full IC trainingqueries and16217 physics calls. OwnerICmetadata20014808 excludes4125000penultimatefeaturequeries(55x75000),supplementedfromhistorylf;rawmetadataunchanged. No partial headsolve. Training739.806030 seconds,148677parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.17649304238395086,
    "physics_weighted": 0.06651441320059044,
    "ic_relative_l2": 0.33163025975227356,
    "ic_relative_mse": 0.10997862918336043,
    "windows": {
      "early": {
        "continuity": 0.15322696236130756,
        "momentum": 0.032785514089289564,
        "poisson": 0.0070897577309683105,
        "total": 0.19310223418156544
      },
      "middle": {
        "continuity": 0.011875484459841115,
        "momentum": 0.01390342187095955,
        "poisson": 0.004503760974910333,
        "total": 0.030282667305710997
      },
      "late": {
        "continuity": 0.015283029991246297,
        "momentum": 0.013489391033340563,
        "poisson": 0.008845911320541253,
        "total": 0.03761833234512811
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9943481683731079,
        "0.5": 0.989654541015625,
        "0.8": 0.9885282516479492
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.00565183162689209,
        "0.5": -0.010345458984375,
        "0.8": -0.011471748352050781
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.09791287779808044,
        "0.5": 0.2939057946205139,
        "0.8": 0.524266242980957
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2254817485809326,
        "0.5": 1.8195589780807495,
        "0.8": 2.7761619091033936
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.451499879360199,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 8.58306884765625e-06
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
    "training_seconds": 739.8060298329801,
    "optimizer_steps": 14571,
    "physics_calls": 16217,
    "pde_training_evaluations": 21739808,
    "ic_training_evaluations": 20014808,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4524,
      "loss": 0.5776497721672058,
      "elapsed_seconds": 187.50646754197078,
      "note": "readout ls=17; ICtrain=0.44123->0.41846; PDE_eval=4615168; IC_eval=5890168"
    },
    {
      "step": 9072,
      "loss": 0.5958864092826843,
      "elapsed_seconds": 375.01535449997755,
      "note": "readout ls=35; ICtrain=0.41593->0.39238; PDE_eval=9253888; IC_eval=11878888"
    },
    {
      "step": 13634,
      "loss": 0.5214976072311401,
      "elapsed_seconds": 562.5214834999642,
      "note": "readout ls=53; ICtrain=0.39002->0.37481; PDE_eval=13906944; IC_eval=17881944"
    },
    {
      "step": 14571,
      "loss": 0.4753306172788143,
      "elapsed_seconds": 739.8057449999615,
      "note": "final full PR+; PDE_eval=21739808; IC_eval=24139808; PDE_draws=14939808; IC_draws=19039808; cg=24; accepted=21; full=100000/75000; micro=4096; lines=45; nf=0; restarts=0; ls=55; lf=4125000; la=55"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 21739808,
    "IC_eval": 24139808,
    "PDE_draws": 14939808,
    "IC_draws": 19039808,
    "cg": 24,
    "accepted": 21,
    "lines": 45,
    "nf": 0,
    "restarts": 0,
    "ls": 55,
    "lf": 4125000,
    "la": 55
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0135551962 (8.32%) versus028. Weightedphysics improves0.0017217247,but IC MSE rises0.0152769209. Earlytotal improves,middle/lateworsen;allPoissoncomponentsworsen. All55proximalfullICsubproblemscompletedandpassedobjective-decreasecheck,recordedsnapshotICtrainingerrorsdrop,butfinalheldoutICdoesnotimprove. Cannotisolatefeature/readoutinteraction,retainedmomentstates,canonicalfinishorsamplerRNGconsumptionfromfullcyclequeries;nointermediatevalidationwasperformed. Throughput14492initialupdatesversus02814643issimilar,sosolvecostaloneisnotestablishedasmaincause. Retainfinite resultwithoutdiagnosticgates;028 remainslowest,no generalVarProverdict/significanceclaim.
