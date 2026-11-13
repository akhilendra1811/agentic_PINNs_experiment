# Trial 035

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=negative_order_fourier_ic_moment_constraints.

## Parent methods and evidence

Trial028 parent lowestfiniteL_val0.16293784616066054,physics0.0682361379091252,ICrelativeMSE0.09470170825153534.034 max/meangradientmethod saturatedICcoef100andworsenedbothterms.035 targetsstructureofICerrorratherthanuniformlyenlargingit.032 physicsgainwithpoorICmotivatesattentiontoinitialfieldbutdoesnotjustifyselectingit. Samebest028backbone,no warmstart.

## Novelty claim

Mechanism: add finite-band weighted Fourier testmoments ofICvelocityresidual,globallycouplingerrorsacrossbatch. Kharazmi,Zhang,Karniadakis https://arxiv.org/html/1912.00873v1 Section4.1/eq4.11,4.17/Discussionprojection suppliesknownsinetestmomentprinciple. LocalIC-onlynegative-orderFouriernorm differsfromPDEweakformVPINN: no integrationbyparts,no newquadrature,no claimofweakEulersolutionorregularityspeedup. Notgloballynovel andnot merelyanICscalarcoefficient. Prior75hadmass/controlvolume/ICsamplingmechanisms;noclaimallmomentmethodsabsent.

## Hypothesis and proposed change

Primaryhypothesis: coherentlarge-scaleinitialvelocityerrorscanbefitmoreeffectivelybyaddingtestedICmomentswithoutdrivingallpointwiseerrorswithlargeICweight. For171nonzeromodes k in[-3,3]^3,one+/-representative(firstnonzeropositive),342sin/cosbasispsi atstoredICpoints: M=||mean(delta)||^2+2 sum_k ||mean(delta psi_k)||^2/|k|^2,includingbothsin/cos,delta=vpred-vtarget. InitialphaseF=PDE+pointIC+M,coefficient1. This isfinite-bandnegative-orderlike normup tophysicalLaplacianconstant,notexactcontinuumHminus1;MonteCarlo batchsquarebiasedbyvariance,Gramnotorthogonal. SameICbatchreevaluatedforMaftercanonicalbackward,gradientsaccumulatedbeforeoptimiserstep. ExtraICforwardcountedexplicitly,noextradraws/PDEpositions. CPU/nativeMPS analyticmomentgradient/nonnegativity/equalpointMSEbutdistinctmomentlosschecks passed onsyntheticangles,notPDEfits.028model/fullfinishASTexact.

## Training objective and setup

FrozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged.148677params,028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM1->32->1536.94080hiddenweightsAdan lr.001,betas(.98,.92,.99),eps1e-8;54597auxAdaBelief lr.001,betas(.9,.999),eps1e-12. First80%1024PDE+1024ICreplacementpooldraws;canonicalPDE=sumcontinuity/momxyz/Poisson,pointIC=sumicxyzabsoluteMSE,plusM. ActualICevaluations2048perinitialupdate,draws1024,reusecoordinatebatch. Final20%canonicalPDE+ICallcoef1,noM,full-poolPR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpersteppointcap,8192percontextcall.750seconds,freshweights,seed82/train823001,MPS,750000parametercap;onlyfrozenpools. Actualcounts/me/historymomentsafterrun.

## Expected outcome

Falsifiabletarget L_val<0.16293784616066054 throughlowerICMSEwithoutlargerphysicsincrease. LowfrequencyemphasismayneglecthighfrequencyIC,MonteCarlomomentvarianceaddsimplicitpointwiseresidualpenalty,andextraICpass/basisproductcostreducesupdates. Canonicalfinishcoulderasemomentbenefits. Reporteverywindow/component,actualICevaluationcounts andphysicaldiagnostics,nevereligibilitygates. Singlefreshfitdoesnotprovesignificance,convergencetheoremsorAthenaaccuracy.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 13481 initial updates+25 CG attempts(24 accepted),43 line values,0 restarts/nonfinite proposals,68 complete full-pool evaluations reconcile20604544 PDE/32709088 full IC evaluations and15181 physics calls. Owner IC metadata18904544 excludes13804544 direct same-batch IC moment forwards;history includes them andraw metadata unchanged. Training741.594634 seconds,148677parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.16418211475503486,
    "physics_weighted": 0.06739624928949951,
    "ic_relative_l2": 0.31110426783561707,
    "ic_relative_mse": 0.09678586546553536,
    "windows": {
      "early": {
        "continuity": 0.1755283038479783,
        "momentum": 0.033072366808087277,
        "poisson": 0.004561452615692039,
        "total": 0.2131621232717576
      },
      "middle": {
        "continuity": 0.01001121423863281,
        "momentum": 0.012490696366867974,
        "poisson": 0.004163144093499821,
        "total": 0.026665054699000608
      },
      "late": {
        "continuity": 0.01426762910846573,
        "momentum": 0.012441256549635423,
        "poisson": 0.006819730792794466,
        "total": 0.03352861645089562
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9953497052192688,
        "0.5": 0.9926273226737976,
        "0.8": 0.992904543876648
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004650294780731201,
        "0.5": -0.007372677326202393,
        "0.8": -0.007095456123352051
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10955506563186646,
        "0.5": 0.33174577355384827,
        "0.8": 0.597625732421875
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2703489065170288,
        "0.5": 1.9921936988830566,
        "0.8": 3.153014659881592
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.24216462671756744,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.0994415283203125e-06
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
    "training_seconds": 741.5946335829794,
    "optimizer_steps": 13506,
    "physics_calls": 15181,
    "pde_training_evaluations": 20604544,
    "ic_training_evaluations": 18904544,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4191,
      "loss": 0.5162683874368668,
      "elapsed_seconds": 187.51048933295533,
      "note": "IC moments=0.0224676; PDE_eval=4291584; IC_eval=8583168; moment_eval=4291584"
    },
    {
      "step": 8414,
      "loss": 0.47446845658123493,
      "elapsed_seconds": 375.01666262495564,
      "note": "IC moments=0.0191244; PDE_eval=8615936; IC_eval=17231872; moment_eval=8615936"
    },
    {
      "step": 12637,
      "loss": 0.4740925710648298,
      "elapsed_seconds": 562.5362991250004,
      "note": "IC moments=0.0156715; PDE_eval=12940288; IC_eval=25880576; moment_eval=12940288"
    },
    {
      "step": 13506,
      "loss": 0.41371922474354506,
      "elapsed_seconds": 741.5940054579987,
      "note": "final full PR+; PDE_eval=20604544; IC_eval=32709088; PDE_draws=13904544; IC_draws=13879544; cg=25; accepted=24; full=100000/75000; micro=4096; lines=43; nf=0; restarts=0; me=13804544"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 20604544,
    "IC_eval": 32709088,
    "PDE_draws": 13904544,
    "IC_draws": 13879544,
    "cg": 25,
    "accepted": 24,
    "lines": 43,
    "nf": 0,
    "restarts": 0,
    "me": 13804544
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0012442686 (0.76%) versus028. Weighted physics improves0.0008398886 but IC MSE rises0.0020841572. Allwindowtotals improve slightly,but allPoissoncomponents worsen;recordedICmomentpenalty decreases. Coherentmomentobjective doesnotimprovepointwiseICvalidation inthisfit.13481initialupdates versus02814643 reflectextraIC/basiswork. Finitebatchmomentbias,lowfrequencyprior andthroughputnotisolated;retainfinite resultwithoutdiagnosticgates,028 remainslowest,nosignificance/generalvariationalmethodverdict.
