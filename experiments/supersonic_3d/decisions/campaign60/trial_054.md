# Trial 054

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50; kind=mechanism; mechanism_id=regularized_anderson_gradient_acceleration.

## Parent methods and evidence

Trial050 supplies the common model/loss/first-half training, total0.1146599961747031. Trial053 spectral/nonmonotone mechanism now leads0.11407538375028281. This attempt tests vector multisecant extrapolation rather than scalar spectral steps; no source weights reused.

## Novelty claim

Known Anderson acceleration with local ridge/descent/line-search safeguards. Read Walker Anderson Acceleration: Algorithms and Implementations2011 pages1-2 difference-form least squares and iterate update https://users.wpi.edu/~walker/Papers/anderson_accn_algs_imps.pdf ; read Scieur/dAspremont/Bach Regularized Nonlinear Acceleration Section3.2 Algorithm2 https://arxiv.org/html/1606.04133 . Local ridge on difference coefficients is not exactly RNA constrained-weight Algorithm2. No novelty or universal acceleration claim.

## Hypothesis and proposed change

Fixed-point map G(x)=x-.01gradF(x), residual f=-.01gradF. Keep up to6 accepted-base states giving5 difference columns DX,DF. Solve(DF^TDF+lambdaI)gamma=DF^Tf, lambda=1e-4max(mean(diag(DF^TDF)),1e-12). Large products use native float32 device,small system CPUfloat64. Direction p=f-(DX+DF)gamma. Require finite coefficients norm<=10 and descent g dot p<-.001 norm(g)norm(p),otherwise restart history/use p=f. Cap direction norm.05,then monotone Armijo c1e-4 with up to4 halving trials. Reject/deadline restores base; rejected attempt resets history. CPUfloat64/native MPSfloat32 synthetic checks passed for actual difference-form ridge extrapolation, coefficient/descent fallbacks and norm cap. Parent050 trainer prefix/model/loss/initial phase/full evaluator byte-identical. No PINN fitting or new coordinates in checks. Accepted line-search states need not be pure fixed-point iterates,so this is a safeguarded local Anderson variant rather than exact unconstrained fixed-point theory.

## Training objective and setup

Unchanged050462405parameter width256 periodic19feature RWF/FiLM/Snake/input-skip model with immediate density. F=C+mean3momentum+P+sum3IC/E, E from fixed75000targets;75000target-only IC draws/no model evaluations. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%full100000PDE/75000IC cycle cache via4096/3072microbatches+tail, Anderson/line-search evaluation counts explicit.750second fresh MPS,physical82/RNG823001; all setup/solves/transfers withinbudget. No total step point cap,8192per call only; frozen scoring/data unchanged.

## Expected outcome

Target total<0.11407538375028281 through faster local convergence than currentbest053. Ill-conditioned differences, non-descent extrapolation,normal-equation reduction error and frequent restarts can remove acceleration or worsen total. Log every coefficient norm/ridge/history/used-fallback/alpha/slope/Armijo threshold and counts,all score/physical diagnostics without gates. No fixed-point contraction/strong convexity assumed proven; no significance/reference-accuracy claim.

## Observed results

Actual metrics, metadata, complete history and38 Anderson traces follow; run.log/all diagnostics read.5122 initial updates+38 Anderson attempts(all accepted),38 gradients+38 values=76 complete full-pool evaluations. Counts reconcile12844928 PDE/10944928 IC model evaluations and7022 physics calls;75000 target-only IC draws have no model evaluations. Training743.921861 seconds,462405parameters,nf0.37 accelerated accepted steps,no coefficient/descent fallback,no backtracking,all alpha1. All slopes/Armijo thresholds/acceptance/history sizes independently reconciled. Gamma norms0.016209685728082738..1.6431241234253575.

```json
{
  "metrics": {
    "L_val": 0.11397143940087355,
    "physics_weighted": 0.019091211059107757,
    "ic_relative_l2": 0.30802634358406067,
    "ic_relative_mse": 0.0948802283417658,
    "windows": {
      "early": {
        "continuity": 0.008098288465561215,
        "momentum": 0.024316753084758242,
        "poisson": 0.0015513768259299324,
        "total": 0.03396641837624939
      },
      "middle": {
        "continuity": 0.002344058323978308,
        "momentum": 0.009584375263746617,
        "poisson": 0.0009934353544449144,
        "total": 0.01292186894216984
      },
      "late": {
        "continuity": 0.0049053379604021155,
        "momentum": 0.010061823403287614,
        "poisson": 0.0018755720387241253,
        "total": 0.016842733402413854
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.997704267501831,
        "0.5": 0.9967687726020813,
        "0.8": 0.9963576197624207
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0022957324981689453,
        "0.5": -0.003231227397918701,
        "0.8": -0.0036423802375793457
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.16030234098434448,
        "0.5": 0.39973264932632446,
        "0.8": 0.6826236248016357
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3858287334442139,
        "0.5": 2.1980438232421875,
        "0.8": 3.520059823989868
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.33885520696640015,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.1457672119140625e-06
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
    "training_seconds": 743.9218612089753,
    "optimizer_steps": 5160,
    "physics_calls": 7022,
    "pde_training_evaluations": 12844928,
    "ic_training_evaluations": 10944928,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2537,
      "loss": 0.13411355018615723,
      "elapsed_seconds": 187.55785512499278,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2597888; IC_eval=2597888"
    },
    {
      "step": 5122,
      "loss": 0.11499322950839996,
      "elapsed_seconds": 375.02702462498564,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5244928; IC_eval=5244928"
    },
    {
      "step": 5142,
      "loss": 0.10499329213052988,
      "elapsed_seconds": 568.9113355000154,
      "note": "AA a=20;ok=20;acc=19;fb=0;gamma=1.3943;alpha=1"
    },
    {
      "step": 5160,
      "loss": 0.10332701168954372,
      "elapsed_seconds": 743.9203508339706,
      "note": "final AA; PDE_eval=12844928; IC_eval=10944928; PDE_draws=5344928; IC_draws=5394928; aa=38; accepted=38; gp=38; vp=38; nf=0; ac=37; fb=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12844928,
    "IC_eval": 10944928,
    "PDE_draws": 5344928,
    "IC_draws": 5394928,
    "aa": 38,
    "accepted": 38,
    "gp": 38,
    "vp": 38,
    "nf": 0,
    "ac": 37,
    "fb": 0,
    "complete_full_evaluations": 76,
    "extra_ic_target_only_draws": 75000,
    "gamma_norm_min": 0.016209685728082738,
    "gamma_norm_max": 1.6431241234253575
  },
  "anderson_trace": [
    {
      "attempt": 1,
      "used": false,
      "reason": "no_history",
      "gamma_norm": 0.0,
      "ridge": 0.0,
      "history": 1,
      "alpha": 1.0,
      "slope": -0.0021224780939519405,
      "base": 0.11436619563028216,
      "proposal": 0.1128900166368112,
      "threshold": 0.11436598338247277,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 2,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 0.016209685728082738,
      "ridge": 1.2747352229780517e-09,
      "history": 2,
      "alpha": 1.0,
      "slope": -0.0008194666588678956,
      "base": 0.1128900166368112,
      "proposal": 0.11216268839780241,
      "threshold": 0.11288993469014531,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 3,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.183323590742337,
      "ridge": 6.904056931489322e-10,
      "history": 3,
      "alpha": 1.0,
      "slope": -0.0013724376913160086,
      "base": 0.11216268839780241,
      "proposal": 0.111011678352952,
      "threshold": 0.11216255115403329,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 4,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.0683835084810762,
      "ridge": 4.975881893187762e-10,
      "history": 4,
      "alpha": 1.0,
      "slope": -0.0009738889057189226,
      "base": 0.111011678352952,
      "proposal": 0.11016692407429218,
      "threshold": 0.11101158096406143,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 5,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.1304253338950838,
      "ridge": 3.8407371789617176e-10,
      "history": 5,
      "alpha": 1.0,
      "slope": -0.0007815562421455979,
      "base": 0.11016692407429218,
      "proposal": 0.10947427235078067,
      "threshold": 0.11016684591866797,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 6,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.1793715593603982,
      "ridge": 3.1211534633257545e-10,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.000666566367726773,
      "base": 0.10947427235078067,
      "proposal": 0.10887898644432425,
      "threshold": 0.1094742056941439,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 7,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.3347441926545385,
      "ridge": 6.040590193379103e-11,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0005585696781054139,
      "base": 0.10887898644432425,
      "proposal": 0.10837242309935391,
      "threshold": 0.10887893058735644,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 8,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2002742178728656,
      "ridge": 4.111438428822112e-11,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0004635817895177752,
      "base": 0.10837242309935391,
      "proposal": 0.1079455038998276,
      "threshold": 0.10837237674117496,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 9,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.4790712273388316,
      "ridge": 1.9863725526647612e-11,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0004910249263048172,
      "base": 0.1079455038998276,
      "proposal": 0.1074981375131756,
      "threshold": 0.10794545479733497,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 10,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.1788896251821883,
      "ridge": 1.2322606437464856e-11,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0003643259115051478,
      "base": 0.1074981375131756,
      "proposal": 0.10715993889607489,
      "threshold": 0.10749810108058445,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 11,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.3357549145815422,
      "ridge": 8.085223726084223e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0003562999772839248,
      "base": 0.10715993889607489,
      "proposal": 0.1068302298663184,
      "threshold": 0.10715990326607716,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 12,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 0.8993177655317208,
      "ridge": 5.453317655224055e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0002621377934701741,
      "base": 0.1068302298663184,
      "proposal": 0.10658351029269397,
      "threshold": 0.10683020365253906,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 13,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.5059618763553702,
      "ridge": 3.882708163871485e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0002799118810798973,
      "base": 0.10658351029269397,
      "proposal": 0.10632178816013038,
      "threshold": 0.10658348230150587,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 14,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.0748276633997642,
      "ridge": 3.106871595548455e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00024034800298977643,
      "base": 0.10632178816013038,
      "proposal": 0.10609558620490134,
      "threshold": 0.10632176412533008,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 15,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.4848914443409718,
      "ridge": 2.196764388173733e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00022651648032478988,
      "base": 0.10609558620490134,
      "proposal": 0.10588210937567055,
      "threshold": 0.10609556355325331,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 16,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.4664126719802837,
      "ridge": 1.7837666632658512e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00023372196301352233,
      "base": 0.10588210937567055,
      "proposal": 0.10566285089589655,
      "threshold": 0.10588208600347425,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 17,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2324414718105083,
      "ridge": 1.3913174257140781e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00019062009232584387,
      "base": 0.10566285089589655,
      "proposal": 0.10548242670483887,
      "threshold": 0.10566283183388732,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 18,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.6431241234253575,
      "ridge": 1.1814620037853274e-12,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00020011409651488066,
      "base": 0.10548242670483887,
      "proposal": 0.10529383493121713,
      "threshold": 0.10548240669342922,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 19,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.0485179920937713,
      "ridge": 9.779171961099565e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00016137985221575946,
      "base": 0.10529383493121713,
      "proposal": 0.10514042025897652,
      "threshold": 0.10529381879323191,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 20,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.3943279150536751,
      "ridge": 8.419637520518108e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0001547370629850775,
      "base": 0.10514042025897652,
      "proposal": 0.10499329213052988,
      "threshold": 0.10514040478527022,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 21,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2852777147120618,
      "ridge": 7.454226125247487e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00015084678307175636,
      "base": 0.10499329213052988,
      "proposal": 0.10485006764065474,
      "threshold": 0.10499327704585157,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 22,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2834500242120155,
      "ridge": 6.282560516268632e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.0001332215906586498,
      "base": 0.10485006764065474,
      "proposal": 0.10472309682518244,
      "threshold": 0.10485005431849567,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 23,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2574297995086476,
      "ridge": 5.631327226751637e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00012639898341149092,
      "base": 0.10472309682518244,
      "proposal": 0.10460254037752748,
      "threshold": 0.1047230841852841,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 24,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.4727460116850564,
      "ridge": 4.66470733151425e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00012512602552305907,
      "base": 0.10460254037752748,
      "proposal": 0.10448335483670235,
      "threshold": 0.10460252786492492,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 25,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.3251115696911473,
      "ridge": 4.071875370215139e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00011889419693034142,
      "base": 0.10448335483670235,
      "proposal": 0.10437007830478251,
      "threshold": 0.10448334294728265,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 26,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.1522864573640081,
      "ridge": 3.5269407838711686e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -9.891342051560059e-05,
      "base": 0.10437007830478251,
      "proposal": 0.10427512158639729,
      "threshold": 0.10437006841344046,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 27,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.593750276704054,
      "ridge": 2.953206346134607e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -0.00011093731882283464,
      "base": 0.10427512158639729,
      "proposal": 0.10416928515769541,
      "threshold": 0.10427511049266541,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 28,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2833590366420675,
      "ridge": 2.723067948906533e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -9.849515481619164e-05,
      "base": 0.10416928515769541,
      "proposal": 0.10407496802508831,
      "threshold": 0.10416927530817993,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 29,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.477208273842733,
      "ridge": 2.490656614284603e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -9.599504119250923e-05,
      "base": 0.10407496802508831,
      "proposal": 0.10398304264526814,
      "threshold": 0.10407495842558419,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 30,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.3103667061624127,
      "ridge": 2.2846238678653207e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -9.036020492203534e-05,
      "base": 0.10398304264526814,
      "proposal": 0.10389639553613961,
      "threshold": 0.10398303360924765,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 31,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.5339668643427473,
      "ridge": 2.0717503934619687e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -9.131484694080427e-05,
      "base": 0.10389639553613961,
      "proposal": 0.103809007210657,
      "threshold": 0.10389638640465491,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 32,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2486410926665983,
      "ridge": 2.0000818334864338e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -8.213842374971136e-05,
      "base": 0.103809007210657,
      "proposal": 0.10373016411904246,
      "threshold": 0.10380899899681463,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 33,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.2408434563396824,
      "ridge": 1.7494807158513481e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -7.438087050104514e-05,
      "base": 0.10373016411904246,
      "proposal": 0.10365855391137302,
      "threshold": 0.10373015668095541,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 34,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.421270962743474,
      "ridge": 1.584249598174381e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -7.575687050120905e-05,
      "base": 0.10365855391137302,
      "proposal": 0.10358574031852186,
      "threshold": 0.10365854633568597,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 35,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.1832851825445665,
      "ridge": 1.454518305799013e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -6.680561637040228e-05,
      "base": 0.10358574031852186,
      "proposal": 0.10352128837257624,
      "threshold": 0.10358573363796023,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 36,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.5001546141860862,
      "ridge": 1.3095834416887442e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -6.897368439240381e-05,
      "base": 0.10352128837257624,
      "proposal": 0.10345482896082103,
      "threshold": 0.1035212814752078,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 37,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.280497848864495,
      "ridge": 1.1693112700328357e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -6.528057565446943e-05,
      "base": 0.10345482896082103,
      "proposal": 0.10339184105396271,
      "threshold": 0.10345482243276347,
      "accepted": true,
      "values": 1
    },
    {
      "attempt": 38,
      "used": true,
      "reason": "accelerated",
      "gamma_norm": 1.616591176594386,
      "ridge": 1.0610797351873203e-13,
      "history": 6,
      "alpha": 1.0,
      "slope": -6.726971332682297e-05,
      "base": 0.10339184105396271,
      "proposal": 0.10332701168954372,
      "threshold": 0.10339183432699138,
      "accepted": true,
      "values": 1
    }
  ]
}
```

## Decision and interpretation

New lowest finite total: improves053 by0.0001039443 (0.0911%). IC MSE falls0.0005557364 while weighted physics rises0.0004517920. Every physics window total worsens; only middle Poisson improves. Versus050,total improves0.0006885568 with physics higher0.0002834829 and IC lower0.0009720397. Anderson extrapolation was used37times with no fallback/backtracking,demonstrating the mechanism operated.76 full evaluations/5122 initial updates are close to05377/5148,but distinct initial trajectories still confound isolated attribution. Retain054 solely by total despite worse physics,no gates. Tiny single-fit margin is not statistical significance or proof of general acceleration/reference accuracy. Continue055-060 before five fresh1800-second finalists and P/B/W.
