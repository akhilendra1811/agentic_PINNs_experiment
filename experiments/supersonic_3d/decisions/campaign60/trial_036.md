# Trial 036

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=entropy_regularised_task_minimax_weights.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.034 gradientratiofeedbacksaturatedatICweight100;035 testedICmoments score0.1641821148.036 replacesunboundedtargetscalingwithboundedtask-adversarysimplexweights onbestunchangedmodel. No checkpointreuse;notbranchingfromfailedbalancingweights.

## Novelty claim

Mechanism: simultaneousmodeldescent/auxiliarytaskweightascent withentropyregularisation. McClenny,Braga-Neto https://arxiv.org/html/2009.04544v2 Section3 supportsknownminimaxPINNweightingprinciple. Local8-tasksoftmax/simplex variant differsfromtheirindividualpointmonotonepenaltyweights:ourscanincrease/decrease,eachweightbetween0and8,total8,entropytemperature.1. NotexactSA-PINNreproduction,notglobalnovelty,notanotherfixedICscalar. No point-specificcoordinatesorGaussianprocessweights.

## Hypothesis and proposed change

Primaryhypothesis: constrainedadversarialweightallocation tracksrelativelylargePDE/ICtasks without034s100foldICpenalty,improvingnetscore. Taskordercontinuity,momx,momy,momz,Poisson,ICx,ICy,ICz. p=softmax(z),modelF=8sum p.detach()*L_j;z starts0 =>allweights1. AuxiliarymaximisesJ=sum p*detach(L)+.1H(p),usingAdamdescenton-J,lr.01betas(.9,.999)eps1e-8. Bothgradientsusepreupdatesamebatch;modelgradanddualgradexplicitlydetachedacrossroles. Auxiliary8logitsoutsidefieldmodelarefreshandreturnedwithoptimiserstate. FrozenLoptformp*=softmax(L/.1)forinnerentropyproblemisverifiedbutinnerproblemonlyoneascentstep,andnonconvexmodelhasnoconvergenceguarantee. CPU/nativeMPSsimplexbounds/entropyanalyticgradient/innerstationarity/modelgradientdetachmentchecks passed,noPDEfits/newcoords.028model/fullcanonicalfinishASTexact.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged. Fieldmodel148677params plus8auxiliaryoptimisedlogits=148685total,under750000;ownermetadatacountsfieldmodelonly. Same028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM.94080hiddenweightsAdan lr.001betas(.98,.92,.99)eps1e-8;54597auxmodelparamsAdaBelief lr.001betas(.9,.999)eps1e-12. First80%1024PDE+1024ICreplacementpooldraws,weighted8canonicalabsoluteMSEtasks,onecontextcallperstep. Dualreusestaskscalars,noadditionalpointforward/backwardtomodel. Final20%canonicalsum8tasklossescoef1,dualnotused/updated,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpersteppointcap,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,onlyfrozenpools. Actualcounts/weights/entropy/dualstepsrecorded.

## Expected outcome

Falsifiabletarget L_val<0.16293784616066054 bybetterIC/PDEtradeoff;recordweights/entropyatcheckpoints. Maximisingabsolutetaskmagnitudescanmisprioritiseunlikegradientconflictmethods;simplexweightsmayconcentrate,ascentmaylagoroscillate,andcanonicalfinishmayerasegains. Auxiliaryoptimiseroverheadcountsinbudget. Reportallwindows/componentsandphysicaldiagnosticswithoutgates. SinglefreshfitdoesnotprovegeneralSA-PINNsuperiority,statisticalsignificanceorAthenaaccuracy.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 14466 initial modelupdates/14466 auxiliaryadversarysteps+25 CG attempts(23 accepted),44 line values,0 restarts/nonfinite proposals,69 complete full-pool evaluations reconcile21713184 PDE/19988184 IC evaluations and16191 physics calls. Training742.047440 seconds. Ownerfieldmodel148677params plus8trainedauxiliarylogits=148685total,allunder750000;auxiliaryscalarsreusetasklosseswithoutadditionalpointevaluations. No execution error.

```json
{
  "metrics": {
    "L_val": 0.18001938108255555,
    "physics_weighted": 0.09312795355582904,
    "ic_relative_l2": 0.29477351903915405,
    "ic_relative_mse": 0.08689142752672652,
    "windows": {
      "early": {
        "continuity": 0.20386250007593698,
        "momentum": 0.06931709958610617,
        "poisson": 0.0054992813156016585,
        "total": 0.2786788809776448
      },
      "middle": {
        "continuity": 0.014362799709958568,
        "momentum": 0.01993463694910927,
        "poisson": 0.007747730617038012,
        "total": 0.04204516727610585
      },
      "late": {
        "continuity": 0.017101137438027634,
        "momentum": 0.01788198660309468,
        "poisson": 0.014574130313814304,
        "total": 0.04955725435493662
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9920376539230347,
        "0.5": 0.9861347675323486,
        "0.8": 0.9841167330741882
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.007962346076965332,
        "0.5": -0.013865232467651367,
        "0.8": -0.015883266925811768
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10950590670108795,
        "0.5": 0.3244013488292694,
        "0.8": 0.5706130862236023
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2674098014831543,
        "0.5": 1.9583078622817993,
        "0.8": 3.03340744972229
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3393915891647339,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.9073486328125e-06
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
    "training_seconds": 742.0474395410274,
    "optimizer_steps": 14491,
    "physics_calls": 16191,
    "pde_training_evaluations": 21713184,
    "ic_training_evaluations": 19988184,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4518,
      "loss": 0.62547767162323,
      "elapsed_seconds": 187.5139007079997,
      "note": "minimax w=[0.873, 0.665, 0.766, 0.645, 0.586, 1.356, 1.881, 1.228]; H=1.996; PDE_eval=4626432; IC_eval=4626432"
    },
    {
      "step": 9042,
      "loss": 0.5721502900123596,
      "elapsed_seconds": 375.03849674999947,
      "note": "minimax w=[0.993, 0.693, 0.798, 0.677, 0.595, 1.324, 1.756, 1.164]; H=2.014; PDE_eval=9259008; IC_eval=9259008"
    },
    {
      "step": 13564,
      "loss": 0.5545335412025452,
      "elapsed_seconds": 562.5124760000035,
      "note": "minimax w=[0.949, 0.706, 0.806, 0.695, 0.606, 1.324, 1.72, 1.193]; H=2.018; PDE_eval=13889536; IC_eval=13889536"
    },
    {
      "step": 14491,
      "loss": 0.4010419733822346,
      "elapsed_seconds": 742.0463252500049,
      "note": "final full PR+; PDE_eval=21713184; IC_eval=19988184; PDE_draws=14913184; IC_draws=14888184; cg=25; accepted=23; full=100000/75000; micro=4096; lines=44; nf=0; restarts=0; ta=14466"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 21713184,
    "IC_eval": 19988184,
    "PDE_draws": 14913184,
    "IC_draws": 14888184,
    "cg": 25,
    "accepted": 23,
    "lines": 44,
    "nf": 0,
    "restarts": 0,
    "ta": 14466
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0170815349 (10.48%) versus028. IC MSE improves0.0078102807,but weightedphysics rises0.0248918156;everywindow/componentworsens. Recordedweights~.59..1.88andentropy1.996..2.018(maxlog8=2.079)showmoderatepreferenceforIC,notcollapse. Boundedfeedbackavoids034s100foldsaturationbutdoesnotimprovenet. Similarinitialupdatecount14466versus02814643makesmajoroverheadlessprominentthan033;stilloneadaptivemethodfit,notisolatedcausality/significance/generalSA-PINNverdict. Retainfinite resultwithoutdiagnosticgates;028 remainslowest.
