# Trial 051

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50; kind=mechanism; mechanism_id=limited_memory_bfgs_dogleg_trust_region.

## Parent methods and evidence

Trial050 supplies the current leading model, loss and first-half stochastic phase: L_val0.1146599961747031, weighted physics0.018807728169454165, IC MSE0.09585226800524893. Its second half used full-pool PR+/Armijo. This attempt replaces that second-half algorithm with a trust-region mechanism; all weights are fresh.

## Novelty claim

Known Dogleg trust-region method with limited-memory BFGS curvature, not a new optimiser. Read official SciPy _trustregion_dogleg.py (Cauchy/Newton path) and _trustregion.py (agreement/radius/acceptance), plus _hessian_update_strategy.py BFGS forward/inverse updates. Local implementation uses matrix-free BFGS actions, not SciPy code, dense Cholesky or true PINN Hessians. Sources: https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion_dogleg.py ; https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion.py ; https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_hessian_update_strategy.py .

## Hypothesis and proposed change

Classical model agreement may improve full-pool optimisation over PR+. Build B from I with the latest8 accepted secant pairs, requiring s dot y>max(1e-20,1e-6 norm(s)norm(y)); skip unsuitable curvature. Rebuild positive BFGS rank-two actions and consistent inverse two-loop from the same pairs. Use realised floating-point parameter displacement, not nominal proposal, for secants. Dogleg uses pN=-B^-1g, pU=-(g dot g)/(g dot Bg)g and sphere intersection on their path. Radius1 initially,max10,min1e-8; predicted=-g dot p-.5p dot Bp; rho=(Fbase-Ftrial)/predicted. Shrink radius*.25 ifrho<.25, double on boundary ifrho>.75; accept iff finiterho>.1. Rejection/deadline restores base. CPUfloat64/native MPSfloat32 synthetic checks passed: B actions match explicit dense BFGS, inverse consistency after12 updates/eight-pair truncation, negative-curvature pair rejection, all three Dogleg branches, exact SPD model ratio1, boundary norms and radius/accept/reject rules. AST verifies unchanged model/optimisers and byte-identical parent trainer prefix through full-pool evaluator. No PINN fit or new training coordinates in checks. This is SPD quasi-Newton curvature in RWF parameter coordinates, no true-Hessian or convergence guarantee for this nonconvex clamped model.

## Training objective and setup

Unchanged050 model462405parameters: width256 periodic19features, five RWF maps, six Snake, repeated input skips, bounded FiLM and immediate density. F=C+mean3momentum+P+sum3IC/E with E fixed pooled target energy; all75000target-only initial draws counted, no model evaluations. First50%1024PDE/1024IC pool updates, Adan directions lr.001 betas(.98,.92,.99) eps1e-8; auxiliaries AdaBelief lr.001 betas(.9,.999) eps1e-12. Remaining time Dogleg full100000PDE/75000IC via4096/3072cycle-cached microbatches+tail. Each attempt recomputes base gradient even after rejection and evaluates one proposal; all evaluations counted. Setup/curvature/CPU transfer work within750seconds, fresh MPS seed82/RNG823001. No total step-point cap,8192 per call only; frozen validation and data unchanged.

## Expected outcome

Target L_val<0.1146599961747031 through better full-pool physics/IC balance. Few expensive full gradients, noisy float32 agreement, limited-memory curvature and rejected radii can underperform. Record each radius/predicted/actual/ratio/branch/pair count in run.log and final counters; all windows, IC and physical diagnostics reported without gates. Classical local assumptions are not proven for this PINN and one fit does not establish significance or numerical-reference accuracy.

## Observed results

Actual metrics, metadata, complete history and all38 trust-region traces follow; run.log/all diagnostics read.5064 initial updates+38 trust attempts(28 accepted,10 rejected),38 full gradients+38 values =76 complete full-pool evaluations. Counts reconcile12785536 PDE/10885536 IC model evaluations and6964 physics calls;75000 extra IC target-only draws counted, no model evaluations. Training742.816572 seconds,462405parameters,nf0. All logged ratios, acceptance and radius updates independently reconciled. First four proposals rejected; initial identity-curvature/radius1 was severely overoptimistic. Final radius0.0078125,eight pairs.

```json
{
  "metrics": {
    "L_val": 0.11498676736863446,
    "physics_weighted": 0.018784466049480933,
    "ic_relative_l2": 0.3101649582386017,
    "ic_relative_mse": 0.09620230131915353,
    "windows": {
      "early": {
        "continuity": 0.007825953596298636,
        "momentum": 0.023716172314006315,
        "poisson": 0.0015527116565077048,
        "total": 0.033094837566812654
      },
      "middle": {
        "continuity": 0.002355695794969561,
        "momentum": 0.009463011349514753,
        "poisson": 0.0010645323941223745,
        "total": 0.012883239538606688
      },
      "late": {
        "continuity": 0.004884042197455986,
        "momentum": 0.00971965362030264,
        "poisson": 0.001997357531314162,
        "total": 0.01660105334907279
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9986540675163269,
        "0.5": 0.9987474679946899,
        "0.8": 0.9993046522140503
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0013459324836730957,
        "0.5": -0.0012525320053100586,
        "0.8": -0.000695347785949707
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1586223840713501,
        "0.5": 0.39608898758888245,
        "0.8": 0.6773070096969604
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3781647682189941,
        "0.5": 2.179379940032959,
        "0.8": 3.465528964996338
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3319658041000366,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.7881393432617188e-06
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
    "training_seconds": 742.8165715409559,
    "optimizer_steps": 5102,
    "physics_calls": 6964,
    "pde_training_evaluations": 12785536,
    "ic_training_evaluations": 10885536,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2502,
      "loss": 0.13184703886508942,
      "elapsed_seconds": 187.54754449997563,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2562048; IC_eval=2562048"
    },
    {
      "step": 5064,
      "loss": 0.11130566895008087,
      "elapsed_seconds": 375.06067758298013,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5185536; IC_eval=5185536"
    },
    {
      "step": 5084,
      "loss": 0.10692416795063764,
      "elapsed_seconds": 568.6536860829801,
      "note": "Dogleg a=20; ok=13; R=0.0078125; pred=0.000350723; actual=0.000324839; ratio=0.9262; pairs=8"
    },
    {
      "step": 5102,
      "loss": 0.10492771514691412,
      "elapsed_seconds": 742.816122707969,
      "note": "final Dogleg; PDE_eval=12785536; IC_eval=10885536; PDE_draws=5285536; IC_draws=5335536; tr=38; accepted=28; gp=38; vp=38; nf=0; pairs=8; E=3.567659"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12785536,
    "IC_eval": 10885536,
    "PDE_draws": 5285536,
    "IC_draws": 5335536,
    "tr": 38,
    "accepted": 28,
    "gp": 38,
    "vp": 38,
    "nf": 0,
    "pairs": 8,
    "complete_full_evaluations": 76,
    "extra_ic_target_only_draws": 75000,
    "branches": {
      "newton": 1,
      "cauchy_boundary": 13,
      "dogleg_boundary": 24
    },
    "final_radius": 0.0078125
  },
  "trust_region_trace": [
    {
      "attempt": 1,
      "radius_before": 1.0,
      "radius_after": 0.25,
      "predicted": 0.21739986538887024,
      "actual": -683.2111195332836,
      "ratio": -3142.6473899199596,
      "accepted": false,
      "boundary": false,
      "branch": "newton",
      "pairs": 0
    },
    {
      "attempt": 2,
      "radius_before": 0.25,
      "radius_after": 0.0625,
      "predicted": 0.13359835743904114,
      "actual": -6.914030478103086,
      "ratio": -51.75236141101399,
      "accepted": false,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 0
    },
    {
      "attempt": 3,
      "radius_before": 0.0625,
      "radius_after": 0.015625,
      "predicted": 0.039258964359760284,
      "actual": -0.14111245214007795,
      "ratio": -3.5944007805951093,
      "accepted": false,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 0
    },
    {
      "attempt": 4,
      "radius_before": 0.015625,
      "radius_after": 0.00390625,
      "predicted": 0.010180952027440071,
      "actual": 0.0007787481881678104,
      "ratio": 0.07649070401951606,
      "accepted": false,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 0
    },
    {
      "attempt": 5,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.0025681261904537678,
      "actual": 0.0020049905870109797,
      "ratio": 0.7807212100651151,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 0
    },
    {
      "attempt": 6,
      "radius_before": 0.0078125,
      "radius_after": 0.015625,
      "predicted": 0.0022521293722093105,
      "actual": 0.0019469291437417269,
      "ratio": 0.8644837049622127,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 1
    },
    {
      "attempt": 7,
      "radius_before": 0.015625,
      "radius_after": 0.00390625,
      "predicted": 0.002934354357421398,
      "actual": -0.0012444977182894945,
      "ratio": -0.4241129620701683,
      "accepted": false,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 2
    },
    {
      "attempt": 8,
      "radius_before": 0.00390625,
      "radius_after": 0.00390625,
      "predicted": 0.0010446688393130898,
      "actual": 0.0007765986956655979,
      "ratio": 0.7433922276998725,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 2
    },
    {
      "attempt": 9,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.0007794558769091964,
      "actual": 0.0006138952448964119,
      "ratio": 0.7875946068053424,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 3
    },
    {
      "attempt": 10,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.0010943918023258448,
      "actual": 0.0005903602577745914,
      "ratio": 0.5394414107634345,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 4
    },
    {
      "attempt": 11,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.0014911864418536425,
      "actual": 0.0009879429126158357,
      "ratio": 0.662521388933605,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 5
    },
    {
      "attempt": 12,
      "radius_before": 0.0078125,
      "radius_after": 0.001953125,
      "predicted": 0.0013024588115513325,
      "actual": 0.00011884805280715227,
      "ratio": 0.09124899133324205,
      "accepted": false,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 6
    },
    {
      "attempt": 13,
      "radius_before": 0.001953125,
      "radius_after": 0.00390625,
      "predicted": 0.0004113719332963228,
      "actual": 0.00036482082214206457,
      "ratio": 0.8868393602323711,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 6
    },
    {
      "attempt": 14,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.0004548229626379907,
      "actual": 0.00035445624962449074,
      "ratio": 0.7793279555821695,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 7
    },
    {
      "attempt": 15,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.0007248283945955336,
      "actual": 0.00034029828384518623,
      "ratio": 0.46948806970383433,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 16,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.0010190492030233145,
      "actual": 0.0004947064444422722,
      "ratio": 0.485458840431431,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 17,
      "radius_before": 0.0078125,
      "radius_after": 0.001953125,
      "predicted": 0.0012418588157743216,
      "actual": -6.38177152723074e-06,
      "ratio": -0.005138886519279238,
      "accepted": false,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 18,
      "radius_before": 0.001953125,
      "radius_after": 0.00390625,
      "predicted": 0.00042876042425632477,
      "actual": 0.0003600061172619462,
      "ratio": 0.8396439990616407,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 8
    },
    {
      "attempt": 19,
      "radius_before": 0.00390625,
      "radius_after": 0.00390625,
      "predicted": 0.00021564020426012576,
      "actual": 0.00010320241563022137,
      "ratio": 0.47858615226374385,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 20,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.00035072327591478825,
      "actual": 0.00032483902759850025,
      "ratio": 0.9261975178329002,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 21,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.0004696861724369228,
      "actual": 0.00020126544404774904,
      "ratio": 0.42851047328794484,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 22,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.000656013551633805,
      "actual": 0.00034009478986263275,
      "ratio": 0.5184264700258477,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 23,
      "radius_before": 0.0078125,
      "radius_after": 0.001953125,
      "predicted": 0.0010304070310667157,
      "actual": -0.0006985929794609547,
      "ratio": -0.6779776907556087,
      "accepted": false,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 24,
      "radius_before": 0.001953125,
      "radius_after": 0.001953125,
      "predicted": 0.00035444670356810093,
      "actual": 0.0002461797557771206,
      "ratio": 0.6945466082739893,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 8
    },
    {
      "attempt": 25,
      "radius_before": 0.001953125,
      "radius_after": 0.001953125,
      "predicted": 0.00013880248297937214,
      "actual": 5.470577161759138e-05,
      "ratio": 0.39412675078529663,
      "accepted": true,
      "boundary": true,
      "branch": "cauchy_boundary",
      "pairs": 8
    },
    {
      "attempt": 26,
      "radius_before": 0.001953125,
      "radius_after": 0.001953125,
      "predicted": 0.00011614280811045319,
      "actual": 8.649216033518314e-05,
      "ratio": 0.7447052619300204,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 27,
      "radius_before": 0.001953125,
      "radius_after": 0.00390625,
      "predicted": 0.00010341274901293218,
      "actual": 8.556409738957882e-05,
      "ratio": 0.8274037602353911,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 28,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.00017408380517736077,
      "actual": 0.0001384420320391655,
      "ratio": 0.795260833700857,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 29,
      "radius_before": 0.0078125,
      "radius_after": 0.001953125,
      "predicted": 0.00040002987952902913,
      "actual": 1.0308460332453251e-05,
      "ratio": 0.02576922590029976,
      "accepted": false,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 30,
      "radius_before": 0.001953125,
      "radius_after": 0.00390625,
      "predicted": 0.0001118253858294338,
      "actual": 8.84507317095995e-05,
      "ratio": 0.7909718446624683,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 31,
      "radius_before": 0.00390625,
      "radius_after": 0.00390625,
      "predicted": 0.00017967401072382927,
      "actual": 0.00011441227979958057,
      "ratio": 0.6367770126500919,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 32,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.00019203106057830155,
      "actual": 0.0001480946084484458,
      "ratio": 0.7712013254650517,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 33,
      "radius_before": 0.0078125,
      "radius_after": 0.001953125,
      "predicted": 0.0003628991253208369,
      "actual": -0.00024450127966701984,
      "ratio": -0.6737444722437889,
      "accepted": false,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 34,
      "radius_before": 0.001953125,
      "radius_after": 0.001953125,
      "predicted": 0.00010569625737844035,
      "actual": 4.342722240835428e-05,
      "ratio": 0.4108681185641721,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 35,
      "radius_before": 0.001953125,
      "radius_after": 0.00390625,
      "predicted": 0.00010415868018753827,
      "actual": 9.20281745493412e-05,
      "ratio": 0.8835382167251349,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 36,
      "radius_before": 0.00390625,
      "radius_after": 0.00390625,
      "predicted": 0.00014606647891923785,
      "actual": 7.488741539418697e-05,
      "ratio": 0.5126940551198831,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 37,
      "radius_before": 0.00390625,
      "radius_after": 0.0078125,
      "predicted": 0.00020865171973127872,
      "actual": 0.00016523059457540512,
      "ratio": 0.7918966342007849,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    },
    {
      "attempt": 38,
      "radius_before": 0.0078125,
      "radius_after": 0.0078125,
      "predicted": 0.0002793791936710477,
      "actual": 0.00011717772576957941,
      "ratio": 0.41942180528858275,
      "accepted": true,
      "boundary": true,
      "branch": "dogleg_boundary",
      "pairs": 8
    }
  ]
}
```

## Decision and interpretation

Dogleg does not improve total: L_val rises0.0003267712 (0.285%) versus050. Weighted physics falls0.0000232621 but IC MSE rises0.0003500333. Continuity/momentum improve in every window,Poisson worsens in every window;early total improves,middle/late slightly worsen.28 accepted steps match050 accepted PR steps,with38 gradients+38 values versus05032+53. Trial051 used5064 initial updates versus5115,so equal-time initial trajectory differs. Rejecting oversized early steps demonstrates controller operation,not theoretical convergence or superior PINN accuracy. Retain finite classical mechanism evidence without gates;050 remains leader. Small single-fit difference is not statistically significant. Continue distinct classical methods before five fresh1800-second finalists and P/B/W.
