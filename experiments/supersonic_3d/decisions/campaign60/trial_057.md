# Trial 057

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50; kind=mechanism; mechanism_id=finite_difference_inexact_newton_cg.

## Parent methods and evidence

Trial050 supplies common model/loss/first-half training. Currentbest054 scores0.11397143940087355.055 compressed GN had expensive8reverse Jacobians and0.118796607393381;056 cheaper SR1-cubic scored0.11422092571692875. This tests direct finite-difference curvature of the full scalar objective,without rank8 compression or secant-history Hessians.

## Novelty claim

Known inexact Newton-CG with parameter-gradient finite-difference Hessian actions. Read official SciPy _optimize.py _minimize_newtoncg and approx_fhess_p https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_optimize.py . Local differences: fixed identity damping1,max3CG iterations,L2relative residual.5,normalised parameter perturbationnorm.001,normcap.05 and bounded Armijo rather than SciPy strong-Wolfe. No true automatic-differentiation Hessian-vector or novel optimiser claim.

## Hypothesis and proposed change

At each full-pool base gradient g, approximate H v=(gradF(theta+h v)-g)/h with h=.001/max(norm(v),1e-20). All shifted gradients use the same cached training pools; only model parameters are perturbed,never coordinates. Finite float32 displacement/gradient subtraction can bias the action and need not be exactly symmetric. Solve(H_fd+I)p=-g by at most3CG products,tolerance.5norm(g). Nonpositive direction curvature endsCG,using partial solution or -g on firstiteration. Require descent angle>.001,otherwise -g;capnorm.05. Monotone Armijo c1e-4,up to4halving values,alpha starts1 and adapts after acceptance/rejection. Shifted parameters always restore base in finally,including deadline. Every FD action needs an extra full gradient and is counted.

## Training objective and setup

Unchanged050462405parameter width256 periodic19feature RWF/FiLM/Snake/input-skip immediate-density model. F=C+mean3momentum+P+sum3IC/E,E fixed75000target energy;target-only initial IC draws counted,no model evaluations. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%FDNewton full100000PDE/75000IC cycle cache via4096/3072microbatches+tail. Log base/perturbed-gradient/value passes,partial passes,CGbranches,finite-difference scales and realised parameter displacement.750seconds fresh MPS,physical82/RNG823001,all curvature work inbudget. No total point cap;8192per call;frozen score/data unchanged.

## Expected outcome

Target total<0.11397143940087355 through more faithful objective curvature. Extra full gradients reduce update count;finite-difference scale/roundoff,identity damping and3stepCG can cause undertraining or poor directions. CPUfloat64/MPSfloat32 synthetic checks passed dampedCG residual/negative-curvature/descent rules,normalised FD scale,and actual nested FD closure matched quadratic Hessian action/restored parameters on success and deadline. No PINN fit/new coordinates in checks. Report every component/count/diagnostic without gates;no exact-Hessian,theorem,significance or numerical-reference accuracy claim.

## Observed results

Actual metrics, metadata, complete history and12 FDNewton traces follow; run.log/all diagnostics read.5074 initial updates+12 completed Newton attempts(all accepted),13 complete base gradients+36 complete perturbed gradients+12 values=61 complete full-pool evaluations. Final37th FD action stopped after15 microbatches:61440 PDE/46080 IC extra forwards,restoring parameters in finally. Totals reconcile11357216 PDE/9816856 IC model evaluations and6614 physics calls;75000extra target-only IC draws,no model evaluations. Training746.219642 seconds,462405parameters,nf0.36 completed FD displacements norm~.001;all12 Armijo thresholds/acceptance independently reconciled.1 residual-target termination,11 iteration caps,no nonpositive-curvature/descent fallback,all alpha1. Final unfinished attempt adds no update.

```json
{
  "metrics": {
    "L_val": 0.11491507979067812,
    "physics_weighted": 0.01878931903515131,
    "ic_relative_l2": 0.31004154682159424,
    "ic_relative_mse": 0.09612576075552681,
    "windows": {
      "early": {
        "continuity": 0.007947063296536272,
        "momentum": 0.02391983990555382,
        "poisson": 0.0015522196361526456,
        "total": 0.03341912283824274
      },
      "middle": {
        "continuity": 0.0024015785127870534,
        "momentum": 0.009513930377978442,
        "poisson": 0.0010441451769721175,
        "total": 0.012959654067737613
      },
      "late": {
        "continuity": 0.004890537118625378,
        "momentum": 0.009631579209042581,
        "poisson": 0.001913080166694997,
        "total": 0.016435196494362956
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9978658556938171,
        "0.5": 0.9972072839736938,
        "0.8": 0.9975712299346924
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0021341443061828613,
        "0.5": -0.0027927160263061523,
        "0.8": -0.002428770065307617
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.15796639025211334,
        "0.5": 0.39366546273231506,
        "0.8": 0.6717516779899597
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3764277696609497,
        "0.5": 2.166712522506714,
        "0.8": 3.4407286643981934
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.40058064460754395,
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
    "params": 462405,
    "training_seconds": 746.2196423329879,
    "optimizer_steps": 5086,
    "physics_calls": 6614,
    "pde_training_evaluations": 11357216,
    "ic_training_evaluations": 9816856,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2484,
      "loss": 0.1307445913553238,
      "elapsed_seconds": 187.55304112500744,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2543616; IC_eval=2543616"
    },
    {
      "step": 5074,
      "loss": 0.11497907340526581,
      "elapsed_seconds": 375.0104660829529,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5195776; IC_eval=5195776"
    },
    {
      "step": 5081,
      "loss": 0.10576262651011348,
      "elapsed_seconds": 585.1681699169567,
      "note": "FDNCG a=7;ok=7;hp=21;inner=3;rr=0.72605;alpha=1;iteration_cap"
    },
    {
      "step": 5086,
      "loss": 0.10484963748604059,
      "elapsed_seconds": 746.2192024579854,
      "note": "final FDNCG; PDE_eval=11357216; IC_eval=9816856; PDE_draws=5295776; IC_draws=5345776; nt=12; accepted=12; bg=13; hs=37; hc=36; vp=12; nf=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 11357216,
    "IC_eval": 9816856,
    "PDE_draws": 5295776,
    "IC_draws": 5345776,
    "nt": 12,
    "accepted": 12,
    "bg": 13,
    "hs": 37,
    "hc": 36,
    "vp": 12,
    "nf": 0,
    "initial_updates": 5074,
    "complete_base_gradients": 13,
    "complete_perturbed_gradients": 36,
    "complete_value_passes": 12,
    "partial_perturbed_gradient_chunks": 15,
    "partial_pde_evaluations": 61440,
    "partial_ic_evaluations": 46080,
    "extra_ic_target_only_draws": 75000,
    "branches": {
      "relative_residual": 1,
      "iteration_cap": 11
    }
  },
  "fd_newton_trace": [
    {
      "attempt": 1,
      "inner": 3,
      "branch": "relative_residual",
      "residual_ratio": 0.467459636282857,
      "fallback": false,
      "step_norm": 0.022910334169864655,
      "alpha": 1.0,
      "base": 0.11418149992823601,
      "slope": -0.008492717519402504,
      "proposal": 0.10969957965426147,
      "threshold": 0.11418065065648407,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.0018184970976717748,
          "realised_parameter_norm": 0.0009999996982514858
        },
        {
          "epsilon": 0.002619153969675842,
          "realised_parameter_norm": 0.000999998301267624
        },
        {
          "epsilon": 0.002165231199370611,
          "realised_parameter_norm": 0.001000001560896635
        }
      ]
    },
    {
      "attempt": 2,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 0.9032719787644679,
      "fallback": false,
      "step_norm": 0.0166796762496233,
      "alpha": 1.0,
      "base": 0.10969957965426147,
      "slope": -0.0028123464435338974,
      "proposal": 0.10817026346921921,
      "threshold": 0.10969929841961712,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.004010007321628885,
          "realised_parameter_norm": 0.0009999991161748767
        },
        {
          "epsilon": 0.004399983713687145,
          "realised_parameter_norm": 0.0010000014444813132
        },
        {
          "epsilon": 0.0035637796182129587,
          "realised_parameter_norm": 0.0010000005131587386
        }
      ]
    },
    {
      "attempt": 3,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 0.6536653354525819,
      "fallback": false,
      "step_norm": 0.010049518197774887,
      "alpha": 1.0,
      "base": 0.10817026346921921,
      "slope": -0.0014985604211688042,
      "proposal": 0.10737297334708273,
      "threshold": 0.10817011361317709,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.004333696536529367,
          "realised_parameter_norm": 0.000999998301267624
        },
        {
          "epsilon": 0.006617955089250222,
          "realised_parameter_norm": 0.0010000010952353477
        },
        {
          "epsilon": 0.004800254873457031,
          "realised_parameter_norm": 0.0009999986505135894
        }
      ]
    },
    {
      "attempt": 4,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 1.0835280933481881,
      "fallback": false,
      "step_norm": 0.010263915173709393,
      "alpha": 1.0,
      "base": 0.10737297334708273,
      "slope": -0.0010561347007751465,
      "proposal": 0.10679550166241825,
      "threshold": 0.10737286773361265,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.0066630477163112005,
          "realised_parameter_norm": 0.0010000013280659914
        },
        {
          "epsilon": 0.007013880423176904,
          "realised_parameter_norm": 0.0010000012116506696
        },
        {
          "epsilon": 0.00577601970507287,
          "realised_parameter_norm": 0.0009999999310821295
        }
      ]
    },
    {
      "attempt": 5,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 0.7007409595709149,
      "fallback": false,
      "step_norm": 0.007392091676592827,
      "alpha": 1.0,
      "base": 0.10679550166241825,
      "slope": -0.000778746441937983,
      "proposal": 0.10637996147852391,
      "threshold": 0.10679542378777405,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.00605169411978373,
          "realised_parameter_norm": 0.0010000027250498533
        },
        {
          "epsilon": 0.009315345754606097,
          "realised_parameter_norm": 0.0009999996982514858
        },
        {
          "epsilon": 0.0064341121287895,
          "realised_parameter_norm": 0.0009999993490055203
        }
      ]
    },
    {
      "attempt": 6,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 1.1351428648541722,
      "fallback": false,
      "step_norm": 0.007876735180616379,
      "alpha": 1.0,
      "base": 0.10637996147852391,
      "slope": -0.0006278958753682673,
      "proposal": 0.10603623185306787,
      "threshold": 0.10637989868893637,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.008645544393483409,
          "realised_parameter_norm": 0.0010000017937272787
        },
        {
          "epsilon": 0.008945336682792805,
          "realised_parameter_norm": 0.0010000000474974513
        },
        {
          "epsilon": 0.007643133102103099,
          "realised_parameter_norm": 0.000999998301267624
        }
      ]
    },
    {
      "attempt": 7,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 0.726045606216052,
      "fallback": false,
      "step_norm": 0.006096875760704279,
      "alpha": 1.0,
      "base": 0.10603623185306787,
      "slope": -0.0005114888772368431,
      "proposal": 0.10576262651011348,
      "threshold": 0.10603618070418015,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.007522110683270513,
          "realised_parameter_norm": 0.0010000006295740604
        },
        {
          "epsilon": 0.011625356455902194,
          "realised_parameter_norm": 0.0009999999310821295
        },
        {
          "epsilon": 0.007722800288064982,
          "realised_parameter_norm": 0.0009999991161748767
        }
      ]
    },
    {
      "attempt": 8,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 1.1468437385522683,
      "fallback": false,
      "step_norm": 0.006489295978099108,
      "alpha": 1.0,
      "base": 0.10576262651011348,
      "slope": -0.00043498509330675006,
      "proposal": 0.10552463214844465,
      "threshold": 0.10576258301160414,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.010357622454026372,
          "realised_parameter_norm": 0.0009999994654208422
        },
        {
          "epsilon": 0.010539877329519585,
          "realised_parameter_norm": 0.0010000010952353477
        },
        {
          "epsilon": 0.009334994399743161,
          "realised_parameter_norm": 0.0009999979520216584
        }
      ]
    },
    {
      "attempt": 9,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 0.7480416218878471,
      "fallback": false,
      "step_norm": 0.005296977702528238,
      "alpha": 1.0,
      "base": 0.10552463214844465,
      "slope": -0.0003730609896592796,
      "proposal": 0.10532458906527609,
      "threshold": 0.10552459484234569,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.008940292198367273,
          "realised_parameter_norm": 0.000999998883344233
        },
        {
          "epsilon": 0.01364782999693727,
          "realised_parameter_norm": 0.0010000013280659914
        },
        {
          "epsilon": 0.008780293030722322,
          "realised_parameter_norm": 0.0010000000474974513
        }
      ]
    },
    {
      "attempt": 10,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 1.1438542475092839,
      "fallback": false,
      "step_norm": 0.005558744538575411,
      "alpha": 1.0,
      "base": 0.10532458906527609,
      "slope": -0.00032668429776094854,
      "proposal": 0.10514606221113354,
      "threshold": 0.1053245563968463,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.011937304521328398,
          "realised_parameter_norm": 0.0009999993490055203
        },
        {
          "epsilon": 0.011884971154415768,
          "realised_parameter_norm": 0.0009999974863603711
        },
        {
          "epsilon": 0.010895620027855657,
          "realised_parameter_norm": 0.0010000026086345315
        }
      ]
    },
    {
      "attempt": 11,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 0.7684090910843017,
      "fallback": false,
      "step_norm": 0.004739024210721254,
      "alpha": 1.0,
      "base": 0.10514606221113354,
      "slope": -0.00028932755230925977,
      "proposal": 0.10499055660329759,
      "threshold": 0.1051460332783783,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.010347212442151536,
          "realised_parameter_norm": 0.0010000013280659914
        },
        {
          "epsilon": 0.015458138279775617,
          "realised_parameter_norm": 0.0009999991161748767
        },
        {
          "epsilon": 0.009670170283471481,
          "realised_parameter_norm": 0.0009999986505135894
        }
      ]
    },
    {
      "attempt": 12,
      "inner": 3,
      "branch": "iteration_cap",
      "residual_ratio": 1.135889084424182,
      "fallback": false,
      "step_norm": 0.004886757582426071,
      "alpha": 1.0,
      "base": 0.10499055660329759,
      "slope": -0.00025821299641393125,
      "proposal": 0.10484963748604059,
      "threshold": 0.10499053078199795,
      "accepted": true,
      "values": 1,
      "perturbations": [
        {
          "epsilon": 0.013440236997587285,
          "realised_parameter_norm": 0.0010000010952353477
        },
        {
          "epsilon": 0.013045661170198704,
          "realised_parameter_norm": 0.0009999993490055203
        },
        {
          "epsilon": 0.012341433344465516,
          "realised_parameter_norm": 0.001000001560896635
        }
      ]
    }
  ]
}
```

## Decision and interpretation

Does not improve total: rises0.0009436404 (0.828%) versus054 and0.0002550836 (0.222%) versus050. Versus054 physics falls0.0003018920 but IC rises0.0012455324. Early/late totals improve,middle worsens.11/12 CG solves hit the3product limit,frequently residual ratio>.5;do not describe those as converged Newton solves.12 accepted parameter updates versus05438 show full-gradient FD cost despite modest coordinate-forward count. Finite-difference error,identity damping,inner truncation and initial5074vs0545122updates are confounded. Retain finite classical evidence without gates;054 remainslowest. No general Newton-CG verdict,theorem/significance/reference-accuracy claim. Continue058-060 then five fresh1800-second finalists plus P/B/W.
