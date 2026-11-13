# Trial 056

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50,trial:52; kind=mechanism; mechanism_id=sr1_krylov_cubic_regularisation.

## Parent methods and evidence

Trial050 supplies common model/loss/first-half training; currentbest054 Anderson scores0.11397143940087355. Trial052 supplies eight-pair SR1 curvature,near-tied050 at0.11467932933115807. Trial055 compressed LM cost allowed only9 attempts and scored0.118796607393381. This explores a cheaper secant model with cubic globalisation.

## Novelty claim

Known adaptive cubic regularisation(ARC) principle credited to Cartis/Gould/Toint2011 PartI, read author PDF Sections2.1,3.1 and6.1 model/acceptance/global cubic optimality/secular equation: https://www.numerical.rl.ac.uk/media/people/nick-gould/CartGoulToin11_mp.pdf . Local six-dimensional Krylov/SR1 approximation and sigma choices are not an exact reproduction or new optimiser. Existing052 SR1 attribution retained.

## Hypothesis and proposed change

Model m(p)=F+g dot p+.5p dot Bp+sigma norm(p)^3/3 with eight-pair SR1 B from052. Build up to6 Krylov basis vectors starting -g,twice modified Gram-Schmidt,stop residual norm<=1e-7max(1,norm(Bq)). Project model; CPUfloat64 eigensystem/secular bisection solves small cubic,including hard-case minimum-eigenspace augmentation. Lift to parameter space,no explicit norm cap. Prediction includes cubic term. Accept finiteratio(actual/predicted)>.1; sigma1000initial,quadruple below.1,halve above.75,bounds[1e-6,1e12]. Rejection/deadline restores base. Secants use realised accepted displacements. SR1 curvature is approximate,small subspace can miss negative curvature orthogonal to its gradient-generated span,and no full-space stationary/global-optimality claim is made.

## Training objective and setup

Unchanged050462405parameter width256 RWF/FiLM/Snake/input-skip immediate-density model. F=C+mean3momentum+P+sum3IC/E,E fromall75000training targets;target-only IC draws counted,no model evaluations. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%cubic SR1/full100000PDE/75000IC cycle cache via4096/3072microbatches+tail,one base gradient/proposal value per attempt. Model products/eigensolves counted in750second native MPS time,physical82/RNG823001,fresh weights. No total step point cap,8192per call;frozen scoring/data unchanged.

## Expected outcome

Target L_val<0.11397143940087355 through cubic control of approximate curvature. Small subspace,SR1 noise,initial sigma and model mismatch can yield rejected or conservative steps. Log sigma/actual/predicted/ratio/subspace dimension/projected stationarity/hardcase/pairs/step norm,all point counts and all validation/physical diagnostics without gates. CPUfloat64/MPSfloat32 synthetic checks passed small cubic stationarity+shifted-PSD conditions includinghardcases,full-rank Krylov comparison,dimension1 breakdown,prediction and sigma controller. No PINN fit/new training coordinates in checks. ARC assumptions/theorems are not proven for this clamped nonconvex PINN;no significance/reference-accuracy claim.

## Observed results

Actual metrics, metadata, complete history and38 cubic traces follow; run.log/all diagnostics read.5174 initial updates+38 cubic attempts(32 accepted,6 rejected),38 full gradients+38 values=76 complete full-pool evaluations. Counts reconcile12898176 PDE/10998176 IC model evaluations and7074 physics calls;75000extra target-only IC draws,no model evaluations. Training742.295145 seconds,462405parameters,nf0. All logged ratios/acceptance/sigma transitions independently reconciled. Subspace dimension1->6;maximum projected stationarity9.622339790214011e-07,no hard case in this fit,finalsigma16000. These are approximate projected-model diagnostics,not full-space/true-Hessian optimality.

```json
{
  "metrics": {
    "L_val": 0.11422092571692875,
    "physics_weighted": 0.018760009089049276,
    "ic_relative_l2": 0.3089675009250641,
    "ic_relative_mse": 0.09546091662787948,
    "windows": {
      "early": {
        "continuity": 0.008058091959085512,
        "momentum": 0.023990980107929844,
        "poisson": 0.0015589610507522845,
        "total": 0.03360803311776764
      },
      "middle": {
        "continuity": 0.0024202988966743177,
        "momentum": 0.009544549870699524,
        "poisson": 0.001019937139593318,
        "total": 0.01298478590696716
      },
      "late": {
        "continuity": 0.004815468604240834,
        "momentum": 0.00959086389805798,
        "poisson": 0.0018796008845123821,
        "total": 0.016285933386811197
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9972826242446899,
        "0.5": 0.9956041574478149,
        "0.8": 0.9942498207092285
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0027173757553100586,
        "0.5": -0.004395842552185059,
        "0.8": -0.005750179290771484
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.15892189741134644,
        "0.5": 0.3954622149467468,
        "0.8": 0.6725485324859619
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3800328969955444,
        "0.5": 2.1728384494781494,
        "0.8": 3.456312656402588
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.34328439831733704,
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
    "training_seconds": 742.2951449159882,
    "optimizer_steps": 5212,
    "physics_calls": 7074,
    "pde_training_evaluations": 12898176,
    "ic_training_evaluations": 10998176,
    "adaptive_probes": 0,
    "source_sha256": "c17b898b69142be7552e5a23cd44d508f14ef102664878cfb419910fdedb9aea",
    "training_data_sha256": "6a5df6f7262d46faec72dd862d1f9e9cfe380545a9a5fd9090b6ac6ebab78e49",
    "validation_data_sha256": "34eae811ad9a6fe8f91f82d7a967ea54bf3adfc65a27cb4e5a6a80fa362699ac",
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2583,
      "loss": 0.13341057300567627,
      "elapsed_seconds": 187.5441049580113,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2644992; IC_eval=2644992"
    },
    {
      "step": 5174,
      "loss": 0.11998201161623001,
      "elapsed_seconds": 375.01583383296384,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5298176; IC_eval=5298176"
    },
    {
      "step": 5194,
      "loss": 0.10509871039539576,
      "elapsed_seconds": 567.7300619580201,
      "note": "Cubic a=20; ok=17; sigma=4000; pred=0.000325973; actual=-2.41561e-05; ratio=-0.074105; pairs=8"
    },
    {
      "step": 5212,
      "loss": 0.10403610940556973,
      "elapsed_seconds": 742.2947235829779,
      "note": "final cubic; PDE_eval=12898176; IC_eval=10998176; PDE_draws=5398176; IC_draws=5448176; tr=38; accepted=32; gp=38; vp=38; nf=0; pairs=8; E=3.567659"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12898176,
    "IC_eval": 10998176,
    "PDE_draws": 5398176,
    "IC_draws": 5448176,
    "tr": 38,
    "accepted": 32,
    "gp": 38,
    "vp": 38,
    "nf": 0,
    "pairs": 8,
    "complete_full_evaluations": 76,
    "extra_ic_target_only_draws": 75000,
    "subspace_dimensions": {
      "1": 2,
      "2": 1,
      "4": 1,
      "5": 1,
      "6": 33
    },
    "maximum_projected_stationarity": 9.622339790214011e-07,
    "hard_cases": 0,
    "final_sigma": 16000.0
  },
  "cubic_trace": [
    {
      "attempt": 1,
      "sigma_before": 1000.0,
      "sigma_after": 4000.0,
      "predicted": 0.008226626785704284,
      "actual": -0.0054395918268710375,
      "ratio": -0.661217771094663,
      "accepted": false,
      "dimension": 1,
      "stationarity": 0.0,
      "hard_case": false,
      "step_norm": 0.02286103554069996,
      "pairs": 0
    },
    {
      "attempt": 2,
      "sigma_before": 4000.0,
      "sigma_after": 4000.0,
      "predicted": 0.004179347017625736,
      "actual": 0.0015991181135177612,
      "ratio": 0.38262391392093864,
      "accepted": true,
      "dimension": 1,
      "stationarity": 0.0,
      "hard_case": false,
      "step_norm": 0.011553509160876274,
      "pairs": 0
    },
    {
      "attempt": 3,
      "sigma_before": 4000.0,
      "sigma_after": 2000.0,
      "predicted": 0.0027659762404638744,
      "actual": 0.002250647987239063,
      "ratio": 0.8136902820472575,
      "accepted": true,
      "dimension": 2,
      "stationarity": 2.767184973928101e-07,
      "hard_case": false,
      "step_norm": 0.00906751211732626,
      "pairs": 1
    },
    {
      "attempt": 4,
      "sigma_before": 2000.0,
      "sigma_after": 2000.0,
      "predicted": 0.0017373719946779651,
      "actual": 0.0009391147177666426,
      "ratio": 0.5405375018380646,
      "accepted": true,
      "dimension": 4,
      "stationarity": 8.181811694478552e-07,
      "hard_case": false,
      "step_norm": 0.010356186889111996,
      "pairs": 2
    },
    {
      "attempt": 5,
      "sigma_before": 2000.0,
      "sigma_after": 2000.0,
      "predicted": 0.0015204874148887536,
      "actual": 0.0007689319318160415,
      "ratio": 0.5057141047578485,
      "accepted": true,
      "dimension": 5,
      "stationarity": 6.330844347493544e-07,
      "hard_case": false,
      "step_norm": 0.009226314723491669,
      "pairs": 3
    },
    {
      "attempt": 6,
      "sigma_before": 2000.0,
      "sigma_after": 2000.0,
      "predicted": 0.0013322795474076134,
      "actual": 0.0007650383049622178,
      "ratio": 0.5742325673698516,
      "accepted": true,
      "dimension": 6,
      "stationarity": 9.622339790214011e-07,
      "hard_case": false,
      "step_norm": 0.008414041250944138,
      "pairs": 4
    },
    {
      "attempt": 7,
      "sigma_before": 2000.0,
      "sigma_after": 2000.0,
      "predicted": 0.000988050935720381,
      "actual": 0.0007040177006274462,
      "ratio": 0.7125317887727638,
      "accepted": true,
      "dimension": 6,
      "stationarity": 4.867380149915072e-07,
      "hard_case": false,
      "step_norm": 0.007662823423743248,
      "pairs": 5
    },
    {
      "attempt": 8,
      "sigma_before": 2000.0,
      "sigma_after": 1000.0,
      "predicted": 0.0006792105501757073,
      "actual": 0.0005297018215060234,
      "ratio": 0.7798786714502493,
      "accepted": true,
      "dimension": 6,
      "stationarity": 3.2036193324178456e-07,
      "hard_case": false,
      "step_norm": 0.00696522556245327,
      "pairs": 6
    },
    {
      "attempt": 9,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.0006420403544089135,
      "actual": 0.000446713762357831,
      "ratio": 0.6957720948383259,
      "accepted": true,
      "dimension": 6,
      "stationarity": 5.542765820773408e-07,
      "hard_case": false,
      "step_norm": 0.008762504905462265,
      "pairs": 7
    },
    {
      "attempt": 10,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.0006234419315201762,
      "actual": 0.00035265868064016104,
      "ratio": 0.5656640383174935,
      "accepted": true,
      "dimension": 6,
      "stationarity": 4.353419072099762e-07,
      "hard_case": false,
      "step_norm": 0.008154609240591526,
      "pairs": 8
    },
    {
      "attempt": 11,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.0006179440227277263,
      "actual": 0.0003775922814384103,
      "ratio": 0.6110460940647079,
      "accepted": true,
      "dimension": 6,
      "stationarity": 6.65886555022886e-07,
      "hard_case": false,
      "step_norm": 0.007669053040444851,
      "pairs": 8
    },
    {
      "attempt": 12,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.0005150632252833832,
      "actual": 0.0003384732408449054,
      "ratio": 0.6571489173172487,
      "accepted": true,
      "dimension": 6,
      "stationarity": 3.6166311521311947e-07,
      "hard_case": false,
      "step_norm": 0.0071264347061514854,
      "pairs": 8
    },
    {
      "attempt": 13,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.000428792548081804,
      "actual": 0.0002615444827824831,
      "ratio": 0.6099557558835801,
      "accepted": true,
      "dimension": 6,
      "stationarity": 2.8797350483794975e-07,
      "hard_case": false,
      "step_norm": 0.006587212439626455,
      "pairs": 8
    },
    {
      "attempt": 14,
      "sigma_before": 1000.0,
      "sigma_after": 500.0,
      "predicted": 0.00035750331241167813,
      "actual": 0.00029712310060858727,
      "ratio": 0.8311058675351213,
      "accepted": true,
      "dimension": 6,
      "stationarity": 3.810254343937111e-07,
      "hard_case": false,
      "step_norm": 0.006046556867659092,
      "pairs": 8
    },
    {
      "attempt": 15,
      "sigma_before": 500.0,
      "sigma_after": 250.0,
      "predicted": 0.0002719133790149942,
      "actual": 0.00027589115779846907,
      "ratio": 1.0146288453987973,
      "accepted": true,
      "dimension": 6,
      "stationarity": 9.393167073695817e-07,
      "hard_case": false,
      "step_norm": 0.007387872319668531,
      "pairs": 8
    },
    {
      "attempt": 16,
      "sigma_before": 250.0,
      "sigma_after": 1000.0,
      "predicted": 0.0002155492352721935,
      "actual": -9.148847311735153e-05,
      "ratio": -0.42444350592021707,
      "accepted": false,
      "dimension": 6,
      "stationarity": 5.795070069057697e-07,
      "hard_case": false,
      "step_norm": 0.00884565245360136,
      "pairs": 8
    },
    {
      "attempt": 17,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.00014807974646161189,
      "actual": 7.631699554622173e-05,
      "ratio": 0.5153776756769779,
      "accepted": true,
      "dimension": 6,
      "stationarity": 3.1775603528121195e-07,
      "hard_case": false,
      "step_norm": 0.0049113258719444275,
      "pairs": 8
    },
    {
      "attempt": 18,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.00018584805514285883,
      "actual": 7.203128188848495e-05,
      "ratio": 0.3875815748145199,
      "accepted": true,
      "dimension": 6,
      "stationarity": 2.5751803693991965e-07,
      "hard_case": false,
      "step_norm": 0.004783964715898037,
      "pairs": 8
    },
    {
      "attempt": 19,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 0.00024123203231195782,
      "actual": 4.1363644413650036e-05,
      "ratio": 0.1714682914089915,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.7344498048545815e-07,
      "hard_case": false,
      "step_norm": 0.005139756482094526,
      "pairs": 8
    },
    {
      "attempt": 20,
      "sigma_before": 1000.0,
      "sigma_after": 4000.0,
      "predicted": 0.00032597258145442584,
      "actual": -2.4156062863767147e-05,
      "ratio": -0.07410458498069845,
      "accepted": false,
      "dimension": 6,
      "stationarity": 4.150801957259857e-07,
      "hard_case": false,
      "step_norm": 0.005537364631891251,
      "pairs": 8
    },
    {
      "attempt": 21,
      "sigma_before": 4000.0,
      "sigma_after": 4000.0,
      "predicted": 0.00025675810703076695,
      "actual": 0.00018764869309961796,
      "ratio": 0.7308384349364762,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.6744633113621236e-07,
      "hard_case": false,
      "step_norm": 0.0032415096648037434,
      "pairs": 8
    },
    {
      "attempt": 22,
      "sigma_before": 4000.0,
      "sigma_after": 4000.0,
      "predicted": 0.0001614129400464769,
      "actual": 5.104532465338707e-05,
      "ratio": 0.3162405978026866,
      "accepted": true,
      "dimension": 6,
      "stationarity": 2.5009965778340613e-07,
      "hard_case": false,
      "step_norm": 0.0030792176257818937,
      "pairs": 8
    },
    {
      "attempt": 23,
      "sigma_before": 4000.0,
      "sigma_after": 4000.0,
      "predicted": 0.0001857044666443811,
      "actual": 6.541970651596785e-05,
      "ratio": 0.3522785838061977,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.1560922723128273e-07,
      "hard_case": false,
      "step_norm": 0.003171011107042432,
      "pairs": 8
    },
    {
      "attempt": 24,
      "sigma_before": 4000.0,
      "sigma_after": 4000.0,
      "predicted": 0.00019540433246658423,
      "actual": 5.11405523866415e-05,
      "ratio": 0.2617165737376215,
      "accepted": true,
      "dimension": 6,
      "stationarity": 8.31338053007523e-08,
      "hard_case": false,
      "step_norm": 0.003300440264865756,
      "pairs": 8
    },
    {
      "attempt": 25,
      "sigma_before": 4000.0,
      "sigma_after": 16000.0,
      "predicted": 0.0002183489488977943,
      "actual": 8.247443474829197e-06,
      "ratio": 0.037771848760717854,
      "accepted": false,
      "dimension": 6,
      "stationarity": 1.4126120881353705e-07,
      "hard_case": false,
      "step_norm": 0.003367759520187974,
      "pairs": 8
    },
    {
      "attempt": 26,
      "sigma_before": 16000.0,
      "sigma_after": 8000.0,
      "predicted": 0.00015721312638731876,
      "actual": 0.00012088112998753786,
      "ratio": 0.7688997271749979,
      "accepted": true,
      "dimension": 6,
      "stationarity": 5.722232582240423e-08,
      "hard_case": false,
      "step_norm": 0.0019420209573581815,
      "pairs": 8
    },
    {
      "attempt": 27,
      "sigma_before": 8000.0,
      "sigma_after": 8000.0,
      "predicted": 0.00012033310848031528,
      "actual": 1.3762270100414753e-05,
      "ratio": 0.11436810927780576,
      "accepted": true,
      "dimension": 6,
      "stationarity": 4.643502680250411e-08,
      "hard_case": false,
      "step_norm": 0.002486392855644226,
      "pairs": 8
    },
    {
      "attempt": 28,
      "sigma_before": 8000.0,
      "sigma_after": 8000.0,
      "predicted": 0.0001615469711379524,
      "actual": 2.0284438505768776e-05,
      "ratio": 0.12556371910214867,
      "accepted": true,
      "dimension": 6,
      "stationarity": 3.193166482358963e-07,
      "hard_case": false,
      "step_norm": 0.002600903157144785,
      "pairs": 8
    },
    {
      "attempt": 29,
      "sigma_before": 8000.0,
      "sigma_after": 8000.0,
      "predicted": 0.00017023934846668274,
      "actual": 7.285072933882475e-05,
      "ratio": 0.42793120389016437,
      "accepted": true,
      "dimension": 6,
      "stationarity": 6.407370104804045e-08,
      "hard_case": false,
      "step_norm": 0.0024297030176967382,
      "pairs": 8
    },
    {
      "attempt": 30,
      "sigma_before": 8000.0,
      "sigma_after": 4000.0,
      "predicted": 0.00012809191412129186,
      "actual": 0.00011019466910511255,
      "ratio": 0.8602781046801113,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.9473572375172663e-07,
      "hard_case": false,
      "step_norm": 0.002196815563365817,
      "pairs": 8
    },
    {
      "attempt": 31,
      "sigma_before": 4000.0,
      "sigma_after": 2000.0,
      "predicted": 7.50146475842055e-05,
      "actual": 6.020150613039732e-05,
      "ratio": 0.8025300133926495,
      "accepted": true,
      "dimension": 6,
      "stationarity": 2.2896792977760613e-07,
      "hard_case": false,
      "step_norm": 0.0026637280825525522,
      "pairs": 8
    },
    {
      "attempt": 32,
      "sigma_before": 2000.0,
      "sigma_after": 2000.0,
      "predicted": 9.548471028535803e-05,
      "actual": 6.709876470267773e-05,
      "ratio": 0.7027173722594087,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.367845922627386e-07,
      "hard_case": false,
      "step_norm": 0.0035655307583510876,
      "pairs": 8
    },
    {
      "attempt": 33,
      "sigma_before": 2000.0,
      "sigma_after": 2000.0,
      "predicted": 0.00010329595332940521,
      "actual": 6.668560672551394e-05,
      "ratio": 0.6455781139156259,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.766119355449059e-07,
      "hard_case": false,
      "step_norm": 0.0033981262240558863,
      "pairs": 8
    },
    {
      "attempt": 34,
      "sigma_before": 2000.0,
      "sigma_after": 1000.0,
      "predicted": 9.841549400744706e-05,
      "actual": 8.059584069997072e-05,
      "ratio": 0.8189344727962455,
      "accepted": true,
      "dimension": 6,
      "stationarity": 1.5335921215333686e-07,
      "hard_case": false,
      "step_norm": 0.003216161159798503,
      "pairs": 8
    },
    {
      "attempt": 35,
      "sigma_before": 1000.0,
      "sigma_after": 1000.0,
      "predicted": 8.267163341321718e-05,
      "actual": 4.452711436897516e-05,
      "ratio": 0.5386020879303972,
      "accepted": true,
      "dimension": 6,
      "stationarity": 4.415352485104238e-07,
      "hard_case": false,
      "step_norm": 0.003981159534305334,
      "pairs": 8
    },
    {
      "attempt": 36,
      "sigma_before": 1000.0,
      "sigma_after": 4000.0,
      "predicted": 0.00012627458690186506,
      "actual": -7.180310785770416e-05,
      "ratio": -0.5686267492088991,
      "accepted": false,
      "dimension": 6,
      "stationarity": 1.1218217099341416e-07,
      "hard_case": false,
      "step_norm": 0.00431497348472476,
      "pairs": 8
    },
    {
      "attempt": 37,
      "sigma_before": 4000.0,
      "sigma_after": 4000.0,
      "predicted": 9.617259532050309e-05,
      "actual": 5.0264643505215645e-05,
      "ratio": 0.5226503801598011,
      "accepted": true,
      "dimension": 6,
      "stationarity": 5.814350268230064e-08,
      "hard_case": false,
      "step_norm": 0.0023520125541836023,
      "pairs": 8
    },
    {
      "attempt": 38,
      "sigma_before": 4000.0,
      "sigma_after": 16000.0,
      "predicted": 9.223680317069887e-05,
      "actual": -3.885081969201565e-05,
      "ratio": -0.42120735277561633,
      "accepted": false,
      "dimension": 6,
      "stationarity": 1.4384584586621104e-07,
      "hard_case": false,
      "step_norm": 0.0025073520373553038,
      "pairs": 8
    }
  ]
}
```

## Decision and interpretation

Does not improve currentbest054: L_val rises0.0002494863 (0.219%). Weighted physics falls0.0003312020 but IC MSE rises0.0005806883. Early/late totals improve versus054,middle worsens. Versus050 total improves0.0004390705 with physics lower0.0000477191 and IC lower0.0003913514.32 accepted cubic steps and76 full evaluations demonstrate the mechanism operated at similar coordinate cost to054,but model algebra,initial sigma and5174 initial updates versus0545122 confound comparison. No hard case exercised in numbered fit despite synthetic verification. Retain finite classical evidence without gates;054 remainslowest. Small single-fit differences are not significance,theorem guarantees or numerical-reference accuracy. Continue057-060 then five fresh1800-second finalists plus P/B/W.
