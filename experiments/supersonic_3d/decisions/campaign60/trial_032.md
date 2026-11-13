# Trial 032

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=pde_compatible_initial_time_jets.

## Parent methods and evidence

Trial028 parent backbone/trainer: lowest finiteL_val0.16293784616066054,weightedphysics0.0682361379091252,ICrelativeMSE0.09470170825153534.031 exactPoisson reducedearlycontinuity buttotal worsened0.1731245106 dueIC/latererrors.032 tests initial PDE compatibility instead of alltimePoisson,returning to028correctionbackbone and learning initialvelocity explicitly. No checkpoint reuse.

## Novelty claim

Mechanism: hard-code firsttime derivative jets implied by unchanged Euler-Poisson equations at uniforminitialdensity. Learnedperiodic u(x),d=divu,a=(u dot grad)u;rho=rho0 exp(clamp(-td+t^2 R,-4,4)),v=u-ta+t^2 V,phi=tF. At t0 continuity,momentum andPoisson cancel analytically for any smoothu/R/V/F. Lagaris et al. https://arxiv.org/abs/physics/9705023 supplies known hardconstraint trialsolution principle;particular Euler-Poisson jet cancellation independentlyderived inresearch_design.md,not claimed globallynovel. It is not a numerical trajectory or freezingICtargets,and is differentfrom031 spectralPoisson elimination.

## Hypothesis and proposed change

Primary hypothesis: compatible initialtime derivatives reduceearlyresidual without the later/IC penalty of031,sufficiently improvingtotal. Represent u via171nonzerointegermodes in[-3,3]^3,firstnonzero positive representative,342sin/cos by3coefficients dividedbysqrt171.1026trainablecoefficients startzero,learn onlythroughcanonicalIC/physics. Analytic FourierJacobian givesd andadvection insideforward withoutinternalautograd;no offpoolcoordinates.028FiLM/inputskip/Snake network providesR,V3,F;startupholdremoved(t0jet usesactualt).149703params. Entire028trainer AST unchanged. CPU/nativeMPS syntheticphase checks passed:nontrivial disposableu coefficients,initialfivePDEresiduals max1.79e-7CPU/1.19e-7MPS,analyticdivergence,periodicity,initialdensity,finite thirdfeaturederivatives/allparametergradients. Teststate discarded;runner freshu=0. Additionalparameter introducedaftermaininit,butfunctionalinitialmap changes byjet construction;not a pure pairedcausalablation.

## Training objective and setup

Canonical F=continuity+mom_x+mom_y+mom_z+poisson+IC_x+IC_y+IC_z absoluteMSE,allcoefficients1;frozenL_val=.2early+.3middle+.5late+ICrelativeMSE unchanged. Same028sevenaffinewidth128/sixSnake/five19inputskips/boundedtimeFiLM1->32->1536correctionnetwork.149703params:94080hiddenweights Adan lr.001,betas(.98,.92,.99),eps1e-8;55623aux including1026initialFouriercoefficients AdaBelief lr.001,betas(.9,.999),eps1e-12. First80%1024PDE+1024IC replacementpoolbatches;final20%full-pool PR+/Armijo100000PDE/75000IC via4096/3072microbatches+tail. No totalpersteppointcap,8192percontextcall.750seconds,freshweights,physicalseed82/training823001,MPS,750000parametercap.Onlyfrozenpools;actualcountersafterrun.

## Expected outcome

Falsifiabletarget L_val<0.16293784616066054 withlower earlycontinuity/momentum andnetIC/latertradeoff improvement. Initialidentitydoesnotguaranteefinite-time accuracy. Risks:bandlimitedu cannotfit allICfrequencies;largelearneddivergence/advection drivesexponentclamp andlargesecondderivatives;quadraticcorrections maystruggle later;extraJacobianADcost reducesupdates. Allphysicalchecksreported,nevereligibilitygates;singlefreshfit provesneithersignificance norAthenaaccuracy.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 11387 initial updates+21 CG attempts(19 accepted),36 line values,5 restarts,0 nonfinite proposals,57 complete full-pool evaluations reconcile17360288 PDE/15935288 IC evaluations and12812 physics calls. Training740.023541 seconds,149703parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.17884705815945587,
    "physics_weighted": 0.014895506627969641,
    "ic_relative_l2": 0.40490931272506714,
    "ic_relative_mse": 0.16395155153148622,
    "windows": {
      "early": {
        "continuity": 0.002261950980424896,
        "momentum": 0.002279572659693051,
        "poisson": 0.0006174226372528529,
        "total": 0.0051589462773708
      },
      "middle": {
        "continuity": 0.0035201988019136,
        "momentum": 0.004142084295946611,
        "poisson": 0.0021895575481351978,
        "total": 0.009851840645995409
      },
      "late": {
        "continuity": 0.010572774322575492,
        "momentum": 0.0071040415456237885,
        "poisson": 0.004139514489194436,
        "total": 0.021816330357393717
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9972374439239502,
        "0.5": 0.9945057034492493,
        "0.8": 0.9945050477981567
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0027625560760498047,
        "0.5": -0.005494296550750732,
        "0.8": -0.005494952201843262
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.14391128718852997,
        "0.5": 0.3719119131565094,
        "0.8": 0.6537625789642334
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3551623821258545,
        "0.5": 2.1413488388061523,
        "0.8": 3.409233331680298
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.37956127524375916,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.682209014892578e-06
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
    "params": 149703,
    "training_seconds": 740.023540583963,
    "optimizer_steps": 11408,
    "physics_calls": 12812,
    "pde_training_evaluations": 17360288,
    "ic_training_evaluations": 15935288,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 3755,
      "loss": 0.6252568960189819,
      "elapsed_seconds": 187.53233187494334,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=3845120; IC_eval=3845120"
    },
    {
      "step": 7134,
      "loss": 0.603919267654419,
      "elapsed_seconds": 375.0461029589642,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7305216; IC_eval=7305216"
    },
    {
      "step": 10643,
      "loss": 0.6025384664535522,
      "elapsed_seconds": 562.5440976669779,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=10898432; IC_eval=10898432"
    },
    {
      "step": 11408,
      "loss": 0.5969082172960043,
      "elapsed_seconds": 740.0231518339715,
      "note": "final full PR+; PDE_eval=17360288; IC_eval=15935288; PDE_draws=11760288; IC_draws=11735288; cg=21; accepted=19; full=100000/75000; micro=4096; lines=36; nf=0; restarts=5"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 17360288,
    "IC_eval": 15935288,
    "PDE_draws": 11760288,
    "IC_draws": 11735288,
    "cg": 21,
    "accepted": 19,
    "lines": 36,
    "nf": 0,
    "restarts": 5
  }
}
```

## Decision and interpretation

Net score hypothesis not supported: L_val rises0.0159092120 (9.76%) versus028. Physics falls0.0533406313 (78.17%) and every window/component improves,but IC MSE rises0.0692498433. Earlytotal dropsfrom0.2169899323 to0.0051589463. Compatiblejet configuration produces much smaller residuals but restrictive learnedinitialfield fitsIC worse;bandwidth,objective tradeoff and optimisation are not causally separated. Lowerphysics/physicaldiagnostics do not promote a larger total. Retain as promising complementary mechanism for later evidence-driven combination,028 remains lowest;singlefit establishes neither significance nor numericaltrajectoryaccuracy.
