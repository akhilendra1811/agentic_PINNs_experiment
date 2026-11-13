# Trial 031

Research metadata (locked on preparation): research_area=pinn_methodology; parents=trial:28; kind=mechanism; mechanism_id=analytic_fourier_poisson_coupled_fields.

## Parent methods and evidence

Trial028 parent backbone/trainer: lowest finite L_val0.16293784616066054,weightedphysics0.0682361379091252,ICrelativeMSE0.09470170825153534. Its earlycontinuity0.1791681846 dominates.030 improvesIC but worsensphysics;028 retained.031 begins substantive PINN-method block with analytic constraint elimination,not an activation or scalar-weight refinement.

## Novelty claim

Mechanism: density and gravitational potential share time-dependent integer Fourier coefficients,eliminating independent Poisson degrees of freedom and imposing meanrho0/initialrho0 analytically. Elementary Fourier inversion derived here: Lap psi_k=-lambda_k psi_k,so rho=rho0+t sum a psi/sqrt171 and phi=-grav*t sum a psi/(lambda sqrt171). Known hard-constraint neural trial-solution principle credited to Lagaris et al. https://arxiv.org/abs/physics/9705023 ;this particular spectral coupling is an independent local adaptation,not claimed globally novel or a reproduction of their boundary examples. Fixed integer basis does not generate collocation coordinates or use numerical trajectories.

## Hypothesis and proposed change

Primary hypothesis: enforcing Poisson identity frees the time-limited optimisation to improve continuity,momentum and IC sufficiently to beat028 total. Use all nonzero k in[-3,3]^3,one representative per+/-pair(firstnonzero positive):171modes,342sin/cosbasis. lambda=(2pi/14)^2|k|^2. Coefficientnet1->64->128->342 with twoSnake,zero finalhead;head becomes trainable immediately,upstream coefficient gradients initially zero. Velocity retains028 periodic19features/fiveinputskips/timeFiLM/sixSnake/sevenaffines,output3. Forward density is linear Fourier sum,no exponential/clamp/startuphold;phi linked as above,zero spatial mean. Changedoutputdimension/extra net changeRNG,so not pure paired causal ablation. CPU/native MPS syntheticphase-variable checks(no PDE fits) verified171modes/200985params,Poisson through autodiff at5.96e-8error for nontrivial coefficient test,periodicity,initialdensity,finite third derivatives/all-parameter gradients. Temporary nonzero test coefficients discarded;fresh runner construction startsheadzero.

## Training objective and setup

Canonical F=continuity+mom_x+mom_y+mom_z+poisson+IC_x+IC_y+IC_z absoluteMSE,coefficientsall1;Poisson still computed/included by untouched owner context. Frozen score .2early+.3middle+.5late+ICrelativeMSE unchanged.200985trainableparams:94080velocityhiddenweights Adan lr.001,betas(.98,.92,.99),eps1e-8;106905aux includingconditioner/coefficientnet AdaBelief lr.001,betas(.9,.999),eps1e-12. Entire028trainer AST unchanged. First80%1024PDE+1024IC replacementpoolbatches;final20%full-pool PR+/Armijo on100000PDE/75000IC via4096/3072microbatches+tail. No total per-step point cap,8192percontextcall.750seconds,750000paramcap,freshweights,physicalseed82/training823001,nativeMPS.Onlyfrozenpools. Actualcounts recorded afterrun.

## Expected outcome

Falsifiable target L_val<0.16293784616066054,Poisson residual nearroundoff in allwindows,and improved non-Poisson/IC tradeoff. ExactPoisson alone cannot ensure improvedtotal. Finitemodes may underresolve density;time-onlycoefficients and largerADgraphs may reducethroughput;linear density may be negative and can alter momentum weighting. No positivity/mass/periodicity/IC thresholds imposed. Report all diagnostics and failures honestly;singlefit doesnot establish significance or numericalsolutionaccuracy.

## Observed results

Actual metrics, metadata and complete history follow;all numerical diagnostics and run.log read. 11524 initial updates+19 CG attempts(18 accepted),33 line values,1 restart,0 nonfinite proposals,52 complete full-pool evaluations reconcile17000576 PDE/15700576 IC evaluations and12824 physics calls. Training738.210146 seconds,200985parameters. No execution error.

```json
{
  "metrics": {
    "L_val": 0.1731245106388552,
    "physics_weighted": 0.06781130485540116,
    "ic_relative_l2": 0.32451996207237244,
    "ic_relative_mse": 0.10531320578345404,
    "windows": {
      "early": {
        "continuity": 0.06494482283936567,
        "momentum": 0.047580153988239685,
        "poisson": 1.0772093398641496e-15,
        "total": 0.11252497682760644
      },
      "middle": {
        "continuity": 0.024829482079105233,
        "momentum": 0.018623617326867185,
        "poisson": 3.6910910684478156e-15,
        "total": 0.04345309940597611
      },
      "late": {
        "continuity": 0.05120354493411379,
        "momentum": 0.01333721440204923,
        "poisson": 1.1054869533499149e-14,
        "total": 0.06454075933617408
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9999998807907104,
        "0.5": 1.0,
        "0.8": 1.0
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -1.1920928955078125e-07,
        "0.5": 0.0,
        "0.8": 0.0
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11966512352228165,
        "0.5": 0.2926632761955261,
        "0.8": 0.49051550030708313
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.255681037902832,
        "0.5": 1.7286134958267212,
        "0.8": 2.4297921657562256
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3678199052810669,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.6226043701171875e-06
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
    "params": 200985,
    "training_seconds": 738.2101464580046,
    "optimizer_steps": 11543,
    "physics_calls": 12824,
    "pde_training_evaluations": 17000576,
    "ic_training_evaluations": 15700576,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 3743,
      "loss": 0.5183849930763245,
      "elapsed_seconds": 187.54684437497053,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=3832832; IC_eval=3832832"
    },
    {
      "step": 7096,
      "loss": 0.48436853289604187,
      "elapsed_seconds": 375.05853749997914,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7266304; IC_eval=7266304"
    },
    {
      "step": 10775,
      "loss": 0.4525942802429199,
      "elapsed_seconds": 562.512829083018,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=11033600; IC_eval=11033600"
    },
    {
      "step": 11543,
      "loss": 0.43879539147019386,
      "elapsed_seconds": 738.2096866249922,
      "note": "final full PR+; PDE_eval=17000576; IC_eval=15700576; PDE_draws=11900576; IC_draws=11875576; cg=19; accepted=18; full=100000/75000; micro=4096; lines=33; nf=0; restarts=1"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 17000576,
    "IC_eval": 15700576,
    "PDE_draws": 11900576,
    "IC_draws": 11875576,
    "cg": 19,
    "accepted": 18,
    "lines": 33,
    "nf": 0,
    "restarts": 1
  }
}
```

## Decision and interpretation

Net hypothesis not supported: L_val rises0.0101866645 (6.25%) versus028. Weighted physics improves0.0004248331,but IC MSE rises0.0106114975. Poisson identity succeeds with MSE~1e-15..1e-14 and massmean nearroundoff. Earlycontinuity improves0.1142233618 and earlytotal improves0.1044649555,but all momentum terms and middle/latecontinuity worsen. ExactPoisson/mass diagnostics do not override total.11524initial updates versus028 14643 expose extra spectral/AD cost;finite densitybandwidth and parameterallocation also confound causal interpretation. Retain finite mechanism evidence,028 remains lowest;no general hardconstraint verdict,significance or numericaltrajectoryaccuracy claim.
