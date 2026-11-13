# Trial 059

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50,trial:51; kind=mechanism; mechanism_id=cyclic_block_bfgs_gauss_seidel.

## Parent methods and evidence

Trial050 supplies common model/loss/first-half training. Currentbest054 scores0.11397143940087355;058 proximal subproblems scored0.11614543675569122. Trial051 supplies five-pair version of its tested positive-curvature BFGS action implementation,used independently per parameter block. No trained state reused.

## Novelty claim

Known cyclic block-coordinate/Gauss-Seidel method with local limited-memory BFGS directions. Read Wright Coordinate Descent Algorithms https://arxiv.org/html/1502.04759 Section2 algorithms/cyclic choice/block extension andSection3.1 nonconvex caveats. BFGS forward/inverse formula source retained from051. Local neural parameter grouping and bounded line search are adaptations,not a new optimiser or a convergence theorem for this PINN.

## Hypothesis and proposed change

Partition all parameters into main backbone359680,conditioner101440,and five-field output head1285. Cycle activeblock0,1,2,one full-gradient evaluation then one block-restricted inverse-BFGS direction and global objective Armijo test. Each block stores at most5 curvature pairs from I,positive-curvature angle threshold1e-6 as051;normcap.05 and descent fallback/reset. Form pending pair for the previously accepted block using the next full gradient BEFORE updating any other block,so the secant endpoints differ only in that block. Older block models become stale as other blocks move,not exact block Hessians. Per-block alpha starts1,grows1.5after acceptance,halves on rejection,up to4Armijo values c1e-4. CPU/native MPS synthetic checks passed actual462405parameter partition exhaustiveness/disjointness/sizes,zero inactive direction entries,descent/normcap,and valid fixed-other-block secant/inverse curvature on coupled quadratic. Parent050 trainer prefix/model/loss/initial phase/full evaluator byte-identical. No PINN fit/new training coordinates in checks. No coordinates/targets change;rejection/deadline restoresbase.

## Training objective and setup

Unchanged050462405parameter width256 periodic19feature RWF/FiLM/Snake/input-skip immediate-density model. F=C+mean3momentum+P+sum3IC/E,E fixed75000target energy;75000target-only IC draws/no model evaluations. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%cyclic block BFGS on full100000PDE/75000IC cycle cache via4096/3072microbatches+tail. Full gradient computes inactive blocks too;do not claim derivative cost savings.750second fresh MPS physical82/RNG823001;all block work inbudget. No total point cap,8192per call;frozen scorer/data unchanged.

## Expected outcome

Target total<0.11397143940087355 through less interference and more suitable local curvature per parameter group. Three-block cycling reduces eachgroups update frequency,ignores cross-block Hessian coupling and can make curvature stale. Log block/sizes/pairupdates/memory/alpha/slope/Armijo and actual evaluations,all validation/physical diagnostics without gates. No exact block minimisation,convex theorem,significance or numerical-reference accuracy claim.

## Observed results

Actual metrics, metadata, complete history and33 block traces follow; run.log/all diagnostics read.5195 initial updates+33 block attempts(all accepted,11per block),33 gradients+50 values=83 complete full-pool evaluations. Counts reconcile13619680 PDE/11544680 IC model evaluations and7270 physics calls;75000extra target-only IC draws,no model evaluations. Training740.603942 seconds,462405parameters,nf0,descentfallback0.32 valid positive-curvature pair updates;final accepted head step has no subsequent gradient for a new pair. All cyclic blocks/sizes/pair timing/Armijo thresholds/acceptance/memory limits independently reconciled. No partial coordinate pass or execution error.

```json
{
  "metrics": {
    "L_val": 0.1147765190155679,
    "physics_weighted": 0.019138174921689063,
    "ic_relative_l2": 0.3092544972896576,
    "ic_relative_mse": 0.09563834409387884,
    "windows": {
      "early": {
        "continuity": 0.008190884155240415,
        "momentum": 0.024412654994415577,
        "poisson": 0.0015694822123498032,
        "total": 0.0341730213620058
      },
      "middle": {
        "continuity": 0.002487226019821627,
        "momentum": 0.009565668916160154,
        "poisson": 0.001073748131958677,
        "total": 0.013126643067940457
      },
      "late": {
        "continuity": 0.004967492908153702,
        "momentum": 0.00979346847267961,
        "poisson": 0.001970194076978221,
        "total": 0.016731155457811533
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9976950883865356,
        "0.5": 0.9970093369483948,
        "0.8": 0.9975075125694275
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0023049116134643555,
        "0.5": -0.0029906630516052246,
        "0.8": -0.0024924874305725098
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.15897105634212494,
        "0.5": 0.3954471945762634,
        "0.8": 0.6734082698822021
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3807646036148071,
        "0.5": 2.175618886947632,
        "0.8": 3.465078592300415
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.35399535298347473,
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
    "training_seconds": 740.6039421670139,
    "optimizer_steps": 5228,
    "physics_calls": 7270,
    "pde_training_evaluations": 13619680,
    "ic_training_evaluations": 11544680,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2593,
      "loss": 0.13176198303699493,
      "elapsed_seconds": 187.54373045900138,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2655232; IC_eval=2655232"
    },
    {
      "step": 5195,
      "loss": 0.11471119523048401,
      "elapsed_seconds": 375.0218975840253,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5319680; IC_eval=5319680"
    },
    {
      "step": 5212,
      "loss": 0.1065322564681992,
      "elapsed_seconds": 567.1832868339843,
      "note": "BQ a=17;ok=17;block=1;by=[6, 6, 5];alpha=1;pairs=[5, 5, 5]"
    },
    {
      "step": 5228,
      "loss": 0.10458098282106221,
      "elapsed_seconds": 740.603495916992,
      "note": "final BQ; PDE_eval=13619680; IC_eval=11544680; PDE_draws=5419680; IC_draws=5469680; bq=33; accepted=33; gp=33; vp=50; nf=0; fb=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 13619680,
    "IC_eval": 11544680,
    "PDE_draws": 5419680,
    "IC_draws": 5469680,
    "bq": 33,
    "accepted": 33,
    "gp": 33,
    "vp": 50,
    "nf": 0,
    "fb": 0,
    "initial_updates": 5195,
    "complete_full_evaluations": 83,
    "extra_ic_target_only_draws": 75000,
    "accepted_by_block": [
      11,
      11,
      11
    ],
    "completed_curvature_pairs": 32
  },
  "block_trace": [
    {
      "attempt": 1,
      "block": 0,
      "block_size": 359680,
      "pair_update": null,
      "pairs": [
        0,
        0,
        0
      ],
      "fallback": false,
      "alpha": 0.25,
      "slope": -0.03652821481227875,
      "base": 0.1155300650279969,
      "proposal": 0.1129216281697154,
      "threshold": 0.11552915182262659,
      "accepted": true,
      "values": 3
    },
    {
      "attempt": 2,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        1,
        0,
        0
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.0020696285646408796,
      "base": 0.1129216281697154,
      "proposal": 0.1125487182289362,
      "threshold": 0.11292142120685894,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 3,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        1,
        1,
        0
      ],
      "fallback": false,
      "alpha": 0.25,
      "slope": -0.009883108548820019,
      "base": 0.1125487182289362,
      "proposal": 0.11203257774468511,
      "threshold": 0.11254847115122248,
      "accepted": true,
      "values": 3
    },
    {
      "attempt": 4,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        1,
        1,
        1
      ],
      "fallback": false,
      "alpha": 0.1875,
      "slope": -0.018188033252954483,
      "base": 0.11203257774468511,
      "proposal": 0.11104270385112613,
      "threshold": 0.11203223671906162,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 5,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        2,
        1,
        1
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.0010028277756646276,
      "base": 0.11104270385112613,
      "proposal": 0.11048542358912528,
      "threshold": 0.11104260356834857,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 6,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        2,
        2,
        1
      ],
      "fallback": false,
      "alpha": 0.1875,
      "slope": -0.0039593977853655815,
      "base": 0.11048542358912528,
      "proposal": 0.11034187627956271,
      "threshold": 0.1104853493504168,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 7,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        2,
        2,
        2
      ],
      "fallback": false,
      "alpha": 0.140625,
      "slope": -0.011509728617966175,
      "base": 0.11034187627956271,
      "proposal": 0.10955146583728492,
      "threshold": 0.11034171442400402,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 8,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        3,
        2,
        2
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.0002146128681488335,
      "base": 0.10955146583728492,
      "proposal": 0.10938401555176824,
      "threshold": 0.1095514443759981,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 9,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        3,
        3,
        2
      ],
      "fallback": false,
      "alpha": 0.140625,
      "slope": -0.003527986351400614,
      "base": 0.10938401555176824,
      "proposal": 0.10932077537290752,
      "threshold": 0.10938396593946018,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 10,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        3,
        3,
        3
      ],
      "fallback": false,
      "alpha": 0.2109375,
      "slope": -0.006947680376470089,
      "base": 0.10932077537290752,
      "proposal": 0.10842473560478538,
      "threshold": 0.10932062882027457,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 11,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        4,
        3,
        3
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00019624159904196858,
      "base": 0.10842473560478538,
      "proposal": 0.10828670184127986,
      "threshold": 0.10842471598062547,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 12,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        4,
        4,
        3
      ],
      "fallback": false,
      "alpha": 0.10546875,
      "slope": -0.0019134911708533764,
      "base": 0.10828670184127986,
      "proposal": 0.10820053657516837,
      "threshold": 0.10828668165992768,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 13,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        4,
        4,
        4
      ],
      "fallback": false,
      "alpha": 0.31640625,
      "slope": -0.005151014309376478,
      "base": 0.10820053657516837,
      "proposal": 0.10739375895354897,
      "threshold": 0.10820037359385624,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 14,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        4,
        4
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00027696765027940273,
      "base": 0.10739375895354897,
      "proposal": 0.10721789998933673,
      "threshold": 0.10739373125678393,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 15,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        4
      ],
      "fallback": false,
      "alpha": 0.158203125,
      "slope": -0.0017585698515176773,
      "base": 0.10721789998933673,
      "proposal": 0.10712960257660598,
      "threshold": 0.10721787216821213,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 16,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.2373046875,
      "slope": -0.005291014909744263,
      "base": 0.10712960257660598,
      "proposal": 0.1066789822652936,
      "threshold": 0.10712947701834201,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 17,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00019404983322601765,
      "base": 0.1066789822652936,
      "proposal": 0.1065322564681992,
      "threshold": 0.10667896286031027,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 18,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.2373046875,
      "slope": -0.0019272558856755495,
      "base": 0.1065322564681992,
      "proposal": 0.10651325434446335,
      "threshold": 0.10653221073351363,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 19,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.177978515625,
      "slope": -0.004753148183226585,
      "base": 0.10651325434446335,
      "proposal": 0.10617846983950585,
      "threshold": 0.10651316974863753,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 20,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00017931613547261804,
      "base": 0.10617846983950585,
      "proposal": 0.10607423889450729,
      "threshold": 0.10617845190789231,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 21,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.177978515625,
      "slope": -0.0012913404498249292,
      "base": 0.10607423889450729,
      "proposal": 0.10606526292394847,
      "threshold": 0.10607421591142165,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 22,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.13348388671875,
      "slope": -0.003914358094334602,
      "base": 0.10606526292394847,
      "proposal": 0.10580844862852246,
      "threshold": 0.10606521067357522,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 23,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00011957479728152975,
      "base": 0.10580844862852246,
      "proposal": 0.10573280055541545,
      "threshold": 0.10580843667104273,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 24,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.13348388671875,
      "slope": -0.0004647887253668159,
      "base": 0.10573280055541545,
      "proposal": 0.10571728507056832,
      "threshold": 0.1057327943512349,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 25,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.200225830078125,
      "slope": -0.0025516608729958534,
      "base": 0.10571728507056832,
      "proposal": 0.10547316737938672,
      "threshold": 0.10571723397972668,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 26,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00014973283396102488,
      "base": 0.10547316737938672,
      "proposal": 0.10540167347062379,
      "threshold": 0.10547315240610333,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 27,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.1001129150390625,
      "slope": -0.000933038187213242,
      "base": 0.10540167347062379,
      "proposal": 0.105365299154073,
      "threshold": 0.10540166412970652,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 28,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.3003387451171875,
      "slope": -0.002048500580713153,
      "base": 0.105365299154073,
      "proposal": 0.1050514365779236,
      "threshold": 0.10536523762966363,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 29,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -0.00020404966198839247,
      "base": 0.1050514365779236,
      "proposal": 0.1049501170637086,
      "threshold": 0.1050514161729574,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 30,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.07508468627929688,
      "slope": -0.0008894649799913168,
      "base": 0.1049501170637086,
      "proposal": 0.10492123360745609,
      "threshold": 0.1049501103851887,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 31,
      "block": 0,
      "block_size": 359680,
      "pair_update": {
        "block": 2,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.22525405883789062,
      "slope": -0.0024560890160501003,
      "base": 0.10492123360745609,
      "proposal": 0.1046790728578344,
      "threshold": 0.10492117828305411,
      "accepted": true,
      "values": 2
    },
    {
      "attempt": 32,
      "block": 1,
      "block_size": 101440,
      "pair_update": {
        "block": 0,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 1.0,
      "slope": -7.826770888641477e-05,
      "base": 0.1046790728578344,
      "proposal": 0.10462034947704524,
      "threshold": 0.10467906503106351,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 33,
      "block": 2,
      "block_size": 1285,
      "pair_update": {
        "block": 1,
        "accepted": true
      },
      "pairs": [
        5,
        5,
        5
      ],
      "fallback": false,
      "alpha": 0.11262702941894531,
      "slope": -0.001125743379816413,
      "base": 0.10462034947704524,
      "proposal": 0.10458098282106221,
      "threshold": 0.10462033679813196,
      "accepted": true,
      "values": 1
    }
  ]
}
```

## Decision and interpretation

Does not improve total: rises0.0008050796 (0.706%) versus054 and0.0001165228 (0.102%) versus050. Versus054 physics rises0.0000469639 and IC MSE0.0007581158. Early/middle totals worsen,late improves via lower late momentum;only middle momentum and late momentum improve among components.33 accepted block steps give11updates pergroup and17 extra line values,with full-gradient cost for inactive groups. Pending pair construction operated correctly before otherblock updates,but old local models can become stale as coupling changes. Initial5195updates versus0545122 and coordinate partition/curvature/globalisation are confounded. Retain finite evidence without gates;054 remainslowest. No general block-CD convergence/significance/reference-accuracy claim. One classical trial060 remains before five fresh1800-second finalists and P/B/W.
