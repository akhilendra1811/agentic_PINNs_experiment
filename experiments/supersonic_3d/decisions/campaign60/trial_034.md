# Trial 034

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=gradient_statistic_ic_loss_annealing.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.032/033 demonstrate physicsgain canbeoffsetbyICerror;034 directlyadaptsdata/physicsgradientbalance onbestunmodifiedmodel. Prior75 usedPCGrad andfixedICweights/curricula;searcheddecisiontext has no gradient-statistic max/mean annealing mechanism. Not aclaim everyhistoricalsourceabsent.

## Novelty claim

Mechanism: feedbackICtrainingcoefficient derivedfromcurrentparametergradientstatistics,notanothermanuallyfixedscalarweight. KnownWang,Teng,Perdikaris https://arxiv.org/html/2001.04536v1 Section2.5 Algorithm1 eq40-41. Localtwo-task adaptation: every32steps,allparameters,unweightedPDEmaxabsolutegradient dividedbyunweightedICmeanabsolutegradient,cliptarget[.1,100],EMAupdate .9old+.1target fromlambda1. Paperrecommendsalpha.9;weuse.1 andcapexplicitly,nopublishedimplementationreproductionorGradNormlabel. FullPRfinishreturnsunweightedcanonicalF.

## Hypothesis and proposed change

Primaryhypothesis: onlinegradientbalance improvesICwithoutphysicsincreaseerasingtotalgain. Same028modelandglobal1024PDE/ICpooldraws. Every32stepsincluding0,autograd.gradretain_graph True obtainsseparatephysics/ICparametergradients onthealreadycomputedbatch,withNonezerosincludedinmeanoverall148677coordinates. lambda_hat=maxabs(gPDE)/max(meanabs(gIC),1e-12),clippedtargetthenEMA;weightsdetachedPythonstatistics,nostatisticsgradient. InitialphaseF=PDE+lambdaIC. Noextra forwardPDEcoordinates/contextcallsforprobes;tworeversesweepscountinsidebudget. Recordprobe/clippedcounts,lambdas. CPU/nativeMPS arithmetic/EMA/clipping/unusedgradient/summedlossgradientchecks passed;model/fullcanonicalevaluatechunk/evaluatefull/PRloopASTidenticalto028. NoPDEfitsornewcoordinates inchecks.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677params,same028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM1->32->1536.94080hiddenweightsAdan lr.001,betas(.98,.92,.99),eps1e-8;54597auxAdaBelief lr.001,betas(.9,.999),eps1e-12. First80%1024PDE+1024IC replacementpoolminibatches,PDE=continuity+mom_x+mom_y+mom_z+poisson,IC=ic_x+ic_y+ic_z absoluteMSE,onlyICcoefadapted. Final20%canonicalF=PDE+IC withallcoef1,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpersteppointcap,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,750000paramcap.Onlyfrozenpools;actualcounts/probesafterrun.

## Expected outcome

Falsifiabletarget L_val<0.16293784616066054,ICMSE<.0947017083withweightedphysicsincrease less thanICgain. Max/meanstatisticcanbedominatedbyoutliers/zeroICgradientcoordinates;clipmaydominate;largeICweightmaydamagePDE;probeworkandcanonicalfinishmayerasebenefits. Reportlambdas/clipping/throughputandallphysicaldiagnostics,noeligibilitygates. Onefreshfitdoesnotestablishsignificance,generalgradientbalancingrankoraccuracyagainstnumericalreferences.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 14159 initial updates/443 gradient-statistic probes(all443clipped)+25 CG attempts(24 accepted),43 line values,1 restart,0 nonfinite proposals,68 complete full-pool evaluations reconcile21298816 PDE/19598816 IC evaluations and15859 physics calls. Training740.375434 seconds,148677parameters. Probes reusecomputedbatchgraphs andaddreversework,noextra pointevaluations. No execution error.

```json
{
  "metrics": {
    "L_val": 0.3425228721416494,
    "physics_weighted": 0.22231356257257145,
    "ic_relative_l2": 0.3467121422290802,
    "ic_relative_mse": 0.12020930956907794,
    "windows": {
      "early": {
        "continuity": 0.29753789284452886,
        "momentum": 0.21249414565073543,
        "poisson": 0.004308581632181071,
        "total": 0.5143406201274454
      },
      "middle": {
        "continuity": 0.07001647071135202,
        "momentum": 0.058670325032675774,
        "poisson": 0.014453629004228587,
        "total": 0.1431404247482564
      },
      "late": {
        "continuity": 0.05286153498725502,
        "momentum": 0.041820169538831706,
        "poisson": 0.05832491771912419,
        "total": 0.15300662224521092
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9665662050247192,
        "0.5": 0.9498260021209717,
        "0.8": 0.942493200302124
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.03343379497528076,
        "0.5": -0.05017399787902832,
        "0.8": -0.05750679969787598
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.06336972862482071,
        "0.5": 0.18423467874526978,
        "0.8": 0.3217340409755707
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.1190744638442993,
        "0.5": 1.4464203119277954,
        "0.8": 1.9198119640350342
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.5343431234359741,
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
    "training_seconds": 740.3754341659951,
    "optimizer_steps": 14184,
    "physics_calls": 15859,
    "pde_training_evaluations": 21298816,
    "ic_training_evaluations": 19598816,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4516,
      "loss": 19.84901237487793,
      "elapsed_seconds": 187.50077137502376,
      "note": "gradient balance; lambda=100; probes=142; clipped=142; PDE_eval=4624384; IC_eval=4624384"
    },
    {
      "step": 8714,
      "loss": 15.706358909606934,
      "elapsed_seconds": 375.0231952909962,
      "note": "gradient balance; lambda=100; probes=273; clipped=273; PDE_eval=8923136; IC_eval=8923136"
    },
    {
      "step": 13244,
      "loss": 14.5487699508667,
      "elapsed_seconds": 562.526983208023,
      "note": "gradient balance; lambda=100; probes=414; clipped=414; PDE_eval=13561856; IC_eval=13561856"
    },
    {
      "step": 14184,
      "loss": 0.7948926575481892,
      "elapsed_seconds": 740.3747768750181,
      "note": "final full PR+; PDE_eval=21298816; IC_eval=19598816; PDE_draws=14598816; IC_draws=14573816; cg=25; accepted=24; full=100000/75000; micro=4096; lines=43; nf=0; restarts=1; bp=443; bc=443"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 21298816,
    "IC_eval": 19598816,
    "PDE_draws": 14598816,
    "IC_draws": 14573816,
    "cg": 25,
    "accepted": 24,
    "lines": 43,
    "nf": 0,
    "restarts": 1,
    "bp": 443,
    "bc": 443
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.1795850260 (110.22%) versus028. Weighted physics rises0.1540774247 and IC MSE0.0255076013;allwindowcomponents worsen. All443gradientprobes clippedthetarget,lambda reached100byfirstsnapshot andremainedthere. The intendedfeedback thereforedegenerates intoanapproximatelyfixedlargeICcoefficientafterEMAtransient;do notclaimsuccessfuldynamicbalance. Max/meanstatistic,allparameterzeros,clippingandcanonicalfinishareconfounded;no phase-separatedvalidation wasperformed. Retainfinite negative result,no diagnosticgates;028 remainslowest,no generalgradientannealingverdict orsignificanceclaim.
