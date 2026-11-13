# Trial 060

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50; kind=mechanism; mechanism_id=limited_memory_dfp_inverse_metric.

## Parent methods and evidence

Trial050 supplies common model/loss/first-half training; currentbest054 Anderson0.11397143940087355.051 SPD-BFGS Dogleg scored0.11498676736863446 and059 cyclic block BFGS0.1147765190155679. This tests a global inverse-DFP metric with monotone line search,a different rank-two secant update and globalisation from those methods. No trained state reused.

## Novelty claim

Known Davidon-Fletcher-Powell(DFP) inverse-curvature update. Read original Fletcher/Powell1963 A rapidly convergent descent method for minimization Sections3-6 via https://galton.uchicago.edu/~lekheng/courses/302/classics/fletcher-powell.pdf ,DOI10.1093/comjnl/6.2.163. Local eight-pair rebuild,curvature skip,normcap and bounded Armijo are adaptations instead of full dense memory/exact line minimisation. Not a new optimiser or exact historical algorithm.

## Hypothesis and proposed change

Inverse metric H startsI;for positive-curvature secant(s,y),H_new=H+s*s^T/(s dot y)-(Hy)*(Hy)^T/(y dot Hy). Retain latest8 pairs,rebuild rank-two actions fromI after eviction;require s dot y>max(1e-20,1e-6norm(s)norm(y)),otherwise skip. Nonfinite/nonpositive y dot Hy resets model. Direction -Hg with descent-angle safeguard/fallback and normcap.05. Full-objective monotone Armijo c1e-4,up to4halving values,alpha starts1,grows1.5on success,otherwise shrinks. Pair uses realised accepted displacement and next full gradient;rejection/deadline restoresbase. CPUfloat64/native MPSfloat32 synthetic checks passed DFP actions vs dense updates through12updates/eight-pair eviction,latest secant relation,positive definiteness,negative-curvature pair skip and descent/normcap. Parent050 trainer prefix/model/loss/initial phase/full evaluator byte-identical. No PINN fitting/new training coordinates in checks. Unlike BFGS,DFP directly removes inverse curvature alongHy;global scalar loss unchanged.

## Training objective and setup

Unchanged050462405parameter width256 periodic19feature RWF/FiLM/Snake/input-skip immediate-density model. F=C+mean3momentum+P+sum3IC/E,E fixed75000target energy;75000target-only IC draws/no model evaluations. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%global limited-memory DFP onfull100000PDE/75000IC cycle cache via4096/3072microbatches+tail. All inverse-metric work/transfers/setup in750second fresh MPS budget,physical82/RNG823001. No total point cap,8192per call;frozen scorer/data unchanged.

## Expected outcome

Target L_val<0.11397143940087355 through a useful alternative secant metric. DFP can become poorly scaled or lose information after memory eviction;positive-curvature skipping and bounded Armijo may stall. Report pairs/skips/fallbacks/alpha/slope/threshold/actual counts,all validation and physical diagnostics without gates. Original quadratic/exact-line properties and global convergence are not asserted for this finite-budget nonconvex PINN. After this last attempt,run exactly THREE finalists plus P/B/W fresh at1800seconds per latest user instruction.

## Observed results

Actual metrics, metadata, complete history and31DFP traces follow;run.log/all diagnostics read.5146initial updates+31DFP attempts(all accepted),31gradients+54values=85complete full-pool evaluations. Counts reconcile13769504PDE/11644504IC model evaluations and7271physics calls;75000extra target-only IC draws,no model evaluations. Training738.803816seconds,462405parameters,nf0,fallback0.30positive curvature pairs formed,eight retained;finalacceptedstep has no nextgradient pair. All slopes/Armijo/acceptance/memory limits independently reconciled. No partial coordinate pass or execution error.

```json
{
  "metrics": {
    "L_val": 0.11426485956351264,
    "physics_weighted": 0.01862034031346517,
    "ic_relative_l2": 0.30926448106765747,
    "ic_relative_mse": 0.09564451925004747,
    "windows": {
      "early": {
        "continuity": 0.007912527675515051,
        "momentum": 0.023950860933358298,
        "poisson": 0.0015415593069485528,
        "total": 0.0334049479158219
      },
      "middle": {
        "continuity": 0.0023819919890390993,
        "momentum": 0.009491274305574457,
        "poisson": 0.0009988858373969655,
        "total": 0.012872152132010522
      },
      "late": {
        "continuity": 0.004805889300122656,
        "momentum": 0.009523039356597474,
        "poisson": 0.001826481524675135,
        "total": 0.016155410181395265
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9979512691497803,
        "0.5": 0.9979276061058044,
        "0.8": 0.9984133243560791
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0020487308502197266,
        "0.5": -0.0020723938941955566,
        "0.8": -0.0015866756439208984
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.15855810046195984,
        "0.5": 0.39501047134399414,
        "0.8": 0.6726399064064026
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3803887367248535,
        "0.5": 2.173234224319458,
        "0.8": 3.4630985260009766
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.28008711338043213,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.337860107421875e-06
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
    "training_seconds": 738.8038157090195,
    "optimizer_steps": 5177,
    "physics_calls": 7271,
    "pde_training_evaluations": 13769504,
    "ic_training_evaluations": 11644504,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2542,
      "loss": 0.13042417168617249,
      "elapsed_seconds": 187.52356691699242,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2603008; IC_eval=2603008"
    },
    {
      "step": 5146,
      "loss": 0.11204934120178223,
      "elapsed_seconds": 375.0047025840031,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5269504; IC_eval=5269504"
    },
    {
      "step": 5162,
      "loss": 0.10596631886437535,
      "elapsed_seconds": 563.7492276249686,
      "note": "DFP a=16;ok=16;pairs=8;fb=0;alpha=0.10691"
    },
    {
      "step": 5177,
      "loss": 0.10412786668166518,
      "elapsed_seconds": 738.7992088749888,
      "note": "final DFP; PDE_eval=13769504; IC_eval=11644504; PDE_draws=5369504; IC_draws=5419504; df=31; accepted=31; gp=31; vp=54; nf=0; fb=0; pairs=8"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 13769504,
    "IC_eval": 11644504,
    "PDE_draws": 5369504,
    "IC_draws": 5419504,
    "df": 31,
    "accepted": 31,
    "gp": 31,
    "vp": 54,
    "nf": 0,
    "fb": 0,
    "pairs": 8,
    "initial_updates": 5146,
    "complete_full_evaluations": 85,
    "extra_ic_target_only_draws": 75000,
    "completed_curvature_pairs": 30
  },
  "dfp_trace": [
    {
      "attempt": 1,
      "pair_update": null,
      "pairs": 0,
      "fallback": false,
      "alpha": 0.25,
      "slope": -0.019939668476581573,
      "base": 0.11447487073019147,
      "proposal": 0.11280343018006533,
      "threshold": 0.11447437223847956,
      "accepted": true,
      "values": 3
    },
    {
      "attempt": 2,
      "pair_update": true,
      "pairs": 1,
      "fallback": false,
      "alpha": 0.375,
      "slope": -0.013122384436428547,
      "base": 0.11280343018006533,
      "proposal": 0.11162675567902625,
      "threshold": 0.11280293809064897,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 3,
      "pair_update": true,
      "pairs": 2,
      "fallback": false,
      "alpha": 0.28125,
      "slope": -0.010498923249542713,
      "base": 0.11162675567902625,
      "proposal": 0.11095576384104788,
      "threshold": 0.11162646039680986,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 4,
      "pair_update": true,
      "pairs": 3,
      "fallback": false,
      "alpha": 0.421875,
      "slope": -0.008945400826632977,
      "base": 0.11095576384104788,
      "proposal": 0.1108345000538975,
      "threshold": 0.11095538645695051,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 5,
      "pair_update": true,
      "pairs": 4,
      "fallback": false,
      "alpha": 0.31640625,
      "slope": -0.008793176151812077,
      "base": 0.1108345000538975,
      "proposal": 0.11007748963311315,
      "threshold": 0.11083422183230832,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 6,
      "pair_update": true,
      "pairs": 5,
      "fallback": false,
      "alpha": 0.2373046875,
      "slope": -0.008354227058589458,
      "base": 0.11007748963311315,
      "proposal": 0.10910434217657894,
      "threshold": 0.110077291383389,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 7,
      "pair_update": true,
      "pairs": 6,
      "fallback": false,
      "alpha": 0.35595703125,
      "slope": -0.007564324885606766,
      "base": 0.10910434217657894,
      "proposal": 0.10877934319432825,
      "threshold": 0.10910407291911597,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 8,
      "pair_update": true,
      "pairs": 7,
      "fallback": false,
      "alpha": 0.533935546875,
      "slope": -0.007928039878606796,
      "base": 0.10877934319432825,
      "proposal": 0.10860999790020287,
      "threshold": 0.10877891988809743,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 9,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.40045166015625,
      "slope": -0.00987370777875185,
      "base": 0.10860999790020287,
      "proposal": 0.10841350595001131,
      "threshold": 0.10860960250593568,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 10,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.15016937255859375,
      "slope": -0.008493050932884216,
      "base": 0.10841350595001131,
      "proposal": 0.10811698203906417,
      "threshold": 0.10841337841039834,
      "accepted": true,
      "values": 3
    },
    {
      "attempt": 11,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.22525405883789062,
      "slope": -0.00819029938429594,
      "base": 0.10811698203906417,
      "proposal": 0.10800365323666483,
      "threshold": 0.10811679754924623,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 12,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.16894054412841797,
      "slope": -0.008254589512944221,
      "base": 0.10800365323666483,
      "proposal": 0.10779399855528027,
      "threshold": 0.10800351378318045,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 13,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.12670540809631348,
      "slope": -0.008147364482283592,
      "base": 0.10779399855528027,
      "proposal": 0.10731541458517313,
      "threshold": 0.1077938953237661,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 14,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.19005811214447021,
      "slope": -0.00717015378177166,
      "base": 0.10731541458517313,
      "proposal": 0.1069621630012989,
      "threshold": 0.10731527831058398,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 15,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.2850871682167053,
      "slope": -0.007020233199000359,
      "base": 0.1069621630012989,
      "proposal": 0.10620264778845012,
      "threshold": 0.10696196286345862,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 16,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.1069076880812645,
      "slope": -0.006984898820519447,
      "base": 0.10620264778845012,
      "proposal": 0.10596631886437535,
      "threshold": 0.10620257311451169,
      "accepted": true,
      "values": 3
    },
    {
      "attempt": 17,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.16036153212189674,
      "slope": -0.00717840576544404,
      "base": 0.10596631886437535,
      "proposal": 0.10551608679816127,
      "threshold": 0.10596620375036069,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 18,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.12027114909142256,
      "slope": -0.007626678794622421,
      "base": 0.10551608679816127,
      "proposal": 0.10511432064231485,
      "threshold": 0.10551599507121903,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 19,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.09020336181856692,
      "slope": -0.004663827363401651,
      "base": 0.10511432064231485,
      "proposal": 0.10493327502626926,
      "threshold": 0.10511427857302413,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 20,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.06765252136392519,
      "slope": -0.005371649283915758,
      "base": 0.10493327502626926,
      "proposal": 0.10477564972825348,
      "threshold": 0.10493323868570746,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 21,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.10147878204588778,
      "slope": -0.00453869579359889,
      "base": 0.10477564972825348,
      "proposal": 0.10465340921655297,
      "threshold": 0.10477560367012136,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 22,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.07610908653441584,
      "slope": -0.003013131907209754,
      "base": 0.10465340921655297,
      "proposal": 0.104576425277628,
      "threshold": 0.10465338628388127,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 23,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.05708181490081188,
      "slope": -0.003874066984280944,
      "base": 0.104576425277628,
      "proposal": 0.10453236580360681,
      "threshold": 0.10457640316375055,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 24,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.08562272235121782,
      "slope": -0.003219763282686472,
      "base": 0.10453236580360681,
      "proposal": 0.10440657311119139,
      "threshold": 0.10453233823511705,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 25,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.06421704176341336,
      "slope": -0.0032375629525631666,
      "base": 0.10440657311119139,
      "proposal": 0.10436399525497109,
      "threshold": 0.10440655232051986,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 26,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.09632556264512004,
      "slope": -0.00249881437048316,
      "base": 0.10436399525497109,
      "proposal": 0.10432552022393793,
      "threshold": 0.10436397118500107,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 27,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.07224417198384003,
      "slope": -0.001800885540433228,
      "base": 0.10432552022393793,
      "proposal": 0.10426116734743118,
      "threshold": 0.10432550721358946,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 28,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.10836625797576005,
      "slope": -0.0017032470786944032,
      "base": 0.10426116734743118,
      "proposal": 0.10425421909894794,
      "threshold": 0.10426114888997995,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 29,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.08127469348182004,
      "slope": -0.0015221755020320415,
      "base": 0.10425421909894794,
      "proposal": 0.10420694621279836,
      "threshold": 0.1042542067275132,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 30,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.030478010055682514,
      "slope": -0.0033086345065385103,
      "base": 0.10420694621279836,
      "proposal": 0.10415982909034938,
      "threshold": 0.10420693612873878,
      "accepted": true,
      "values": 3
    },
    {
      "attempt": 31,
      "pair_update": true,
      "pairs": 8,
      "fallback": false,
      "alpha": 0.022858507541761885,
      "slope": -0.0028641701210290194,
      "base": 0.10415982909034938,
      "proposal": 0.10412786668166518,
      "threshold": 0.10415982254328394,
      "accepted": true,
      "values": 2
    }
  ]
}
```

## Decision and interpretation

Does not improve currentbest054:total rises0.0002934202(0.257%). Physics falls0.0004708707 but IC MSE rises0.0007642909. All physics window totals improve versus054;only middle continuity/Poisson worsen among components. Versus050 total improves0.0003951366 with physics lower0.0001873879 and IC lower0.0002077488.31accepted DFPsteps/23extra linevalues show metric operated with more backtracking than054.5146initialupdates versus0545122,globalisation/normcap andmemoryupdate choices prevent isolated DFP-vs-BFGS attribution. Retain finite classical evidence without gates;054 remainslowest. No original exact-line/quadratic guarantee,statistical significance or numerical-reference accuracy claim. All60attempts nowfinished;latest user amendment requires exactlyTHREE finalists,chosen by lowest finite750second L_val,plusfreshP/B/W at1800seconds.
