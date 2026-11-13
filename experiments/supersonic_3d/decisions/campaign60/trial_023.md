# Trial 023

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:19; kind=mechanism; mechanism_id=additive_coarse_fine_periodic_branches.

## Parent methods and evidence

Closed019 source,lowest finite total.1652899712,physics.0723434671,IC.0929465040. Rank64 space-time022 total.1783303810 worsened both components;MFN021 .1697211195 also failed net gain. Keep full space-time mapping and test separate coarse/fine branches to decouple input frequency scales. Historical001/021 expanded axis harmonics but did not establish this independent additive coarse/fine allocation;old006 had a dedicated spatial velocity branch,a different architecture. Historical scores/eligibility not compared numerically here. Fresh weights/state,no checkpoint reuse.

## Novelty claim

Representation mechanism independent additive coarse/fine periodic networks with disjoint input harmonic ranges and a zero initial correction head. Credit multiscale Fourier PINN principle Wang,Wang,Perdikaris https://arxiv.org/html/2012.10047 Section3.3. Local design uses independent Snake branches and summed raw outputs,not the paper shared-MLP/concatenation/tanh/random-feature architecture. Known multibranch idea,no scientific novelty claim. Distinct from merely increasing a single network harmonic count or tuning a sine frequency:trainable paths have separate weights,width/depth and input bands. Nonlinear branches are band-conditioned,not strictly Fourier-band-limited.

## Hypothesis and proposed change

Hypothesis:coarse branch models smooth physics while a smaller high-input-band correction improves IC detail enough for lower total. Main19network unchanged(19->128,five128->128,128->5,six Snake,axis harmonics1..3+time). Add fine network31->64,Snake,64->64,Snake,64->64,Snake,64->5,inputaxis harmonics4..8+time. Each feature sin/cos scaled1/sqrt(k). Sum raw outputs unscaled,before shared parent density transform. Fine hidden/input Linear Xavier/bias.01;fine final weight/bias zero. Build/init fine only after coarse init,so parent coarse initial tensors match exactly at same seed;fine begins identicallyzero but output-head gradient is nonzero.96458params,81920mainhidden Adan,14538auxiliary AdaBelief. Extra construction still changes subsequent RNG consumption. Entire parent trainer/optimisers/PR+ and Snake AST equality passed. CPU exact parent coarse initial weights check and CPU/native MPS zero-head/trainable-head gradient,high-band angular derivatives through third order passed without PDE coordinates/fitting. Risks:high-frequency derivative stiffness,branch interference/spectral leakage,zero-head early delay,larger auxiliary state and extra AD overhead.

## Training objective and setup

Fresh coarse/fine architecture above,96458params,shared density rho0*exp(clamp(max(t-.05,0)*summed_raw_rho,-4,4)). Other raw fields summed directly. F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:five main128*128 hidden weights Adan(lr.001,betas .98/.92/.99,eps1e-8),allotherparameters includingfinebranch UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap. Final all100000PDE/75000IC cycle cache once,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. Both branches see only provided frozen-pool coordinates,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1652899712,through IC reduction with sufficient physics preservation. Larger total falsifies net hypothesis regardless of individual component/throughput changes. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no diagnostic gates. One fresh matched-time local multibranch test cannot establish significance,general multiscale architecture superiority or numerical-reference accuracy. Retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.15419 initial updates+55 CG attempts,52 accepted,88 line values,2 restarts,0 nonfinite proposals.143 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.17377924631801853,
    "physics_weighted": 0.07704564724251248,
    "ic_relative_l2": 0.31102025508880615,
    "ic_relative_mse": 0.09673359907550605,
    "windows": {
      "early": {
        "continuity": 0.18605760803768676,
        "momentum": 0.052438568230420805,
        "poisson": 0.007107521081489283,
        "total": 0.24560369734959683
      },
      "middle": {
        "continuity": 0.010484452765569429,
        "momentum": 0.013693724265950459,
        "poisson": 0.005010601001301394,
        "total": 0.029188778032821282
      },
      "late": {
        "continuity": 0.0154135319831737,
        "momentum": 0.013782810941890065,
        "poisson": 0.00914020580042969,
        "total": 0.038336548725493455
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.994083821773529,
        "0.5": 0.9900857210159302,
        "0.8": 0.9893755912780762
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005916178226470947,
        "0.5": -0.009914278984069824,
        "0.8": -0.010624408721923828
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10850575566291809,
        "0.5": 0.32942676544189453,
        "0.8": 0.5880348086357117
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.264589786529541,
        "0.5": 1.9751554727554321,
        "0.8": 3.125241279602051
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4602798819541931,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.2782554626464844e-06
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
    "params": 96458,
    "training_seconds": 738.1431519589969,
    "optimizer_steps": 15474,
    "physics_calls": 18994,
    "pde_training_evaluations": 30089056,
    "ic_training_evaluations": 26514056,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4827,
      "loss": 0.514846682548523,
      "elapsed_seconds": 187.5215883339988,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4942848; IC_eval=4942848"
    },
    {
      "step": 9653,
      "loss": 0.4521004557609558,
      "elapsed_seconds": 375.03782891697483,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9884672; IC_eval=9884672"
    },
    {
      "step": 14455,
      "loss": 0.45441967248916626,
      "elapsed_seconds": 562.5195606669877,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=14801920; IC_eval=14801920"
    },
    {
      "step": 15474,
      "loss": 0.4098127265460789,
      "elapsed_seconds": 738.1429418749758,
      "note": "final full PR+; PDE_eval=30089056; IC_eval=26514056; PDE_draws=15889056; IC_draws=15864056; cg=55; accepted=52; full=100000/75000; micro=4096; lines=88; nf=0; restarts=2"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported:total rose0.0084892751 (5.14%) versus019,physics0.0047021801 and IC MSE0.0037870950 higher. Late physics improves slightly,but early/middle worsen;early momentum rises sharply.15419 initial updates/143 full evaluations versus019 26615/204 show high branch/feature differentiation cost. Exact matching initial coarse weights/zero correction did not yield net benefit. Retain finite result without diagnostic gates;no isolated branch-causality,general multiscale ranking or significance claim.
