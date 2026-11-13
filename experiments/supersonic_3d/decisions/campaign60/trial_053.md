# Trial 053

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50; kind=mechanism; mechanism_id=alternating_bb_nonmonotone_spectral_gradient.

## Parent methods and evidence

Trial050 supplies leading model/loss and first-half training, total0.1146599961747031.051 Dogleg0.11498676736863446 and052 SR1-Steihaug0.11467932933115807 were near ties but did not improve total. This tests scalar secant curvature with nonmonotone globalisation rather than a trust-region matrix model.

## Novelty claim

Known Barzilai-Borwein(BB) spectral gradient with max-history nonmonotone Armijo safeguard. Read Yuan Step-Sizes for the Gradient Method Section2 formulas2.5/2.6 https://lsec.cc.ac.cn/pub/home/yyx/papers/p0504.pdf ; credit original Barzilai/Borwein1988 https://doi.org/10.1093/imanum/8.1.141 . Original full PDF fetch timed out; no claim to have read it fully. Birgin/Martinez/Raydan SPG publisher abstract https://doi.org/10.1137/S1052623497330963 supports nonmonotone spectral lineage; author PDF bmr2.pdf text was garbled and bmr.pdf timed out. Local unconstrained alternating-BB/max5/halving variant, not exact reproduction of SPG software.

## Hypothesis and proposed change

After the same first50%, full-pool gradient direction is -g with alternating BB1 alpha=(s dot s)/(s dot y) and BB2 alpha=(s dot y)/(y dot y), based on realised accepted displacement and next full gradient difference. Alternate by completed attempt parity. Require positive secant angle s dot y>max(1e-20,1e-6 norm(s)norm(y)),otherwise retain fallback alpha. Clamp initial spectral alpha to[1e-6,1],start.01. Accept Ftrial<=max(last5 accepted F values)-1e-4 alpha norm(g)^2; up to6 halving trials. Accepted steps may increase F relative to current base but must satisfy history safeguard. Rejected/deadline attempts restore base. Rejected final-alpha trace records actual last tested alpha, while next fallback uses halved alpha. CPUfloat64/native MPSfloat32 synthetic checks passed for actual BB1/BB2 formulas, positive-curvature requirement/fallback, upper/lower bounds and max5 history expiry/nonmonotone acceptance thresholds. Parent050 trainer prefix/model/loss/initial phase/full evaluator byte-identical. No PINN fitting/new training coordinates in checks. This is a distinct secant step/globalisation mechanism,not an Adam learning-rate sweep.

## Training objective and setup

Unchanged050462405parameter width256 RWF/FiLM/Snake/input-skip immediate-density model. F=C+mean3momentum+P+sum3IC/E, fixed E fromall75000training targets;75000target-only IC draws counted but no model evaluations. First50%1024PDE/1024IC pool updates with Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Final50%full100000PDE/75000IC cycle cache via4096/3072microbatches+tail, spectral gradients and repeated line values counted.750second fresh MPS,physical82/RNG823001. No total step point cap,8192per call only; frozen scoring/data unchanged.

## Expected outcome

Target total<0.1146599961747031 through cheaper curvature adaptation and nonmonotone progress. Scalar curvature may miss anisotropy, history may tolerate damaging rises, and limited line trials can fail. Log each variant/alpha/base/proposal/threshold/acceptance/value count and uphill accepts; reconcile all evaluations, all score components/diagnostics without gates. Classical convergence assumptions and unlimited line search do not hold automatically here; no theorem/significance/reference-accuracy claim.

## Observed results

Actual metrics, metadata, complete history and37 spectral traces follow; run.log/all diagnostics read.5148 initial updates+37 spectral attempts(all accepted),37 gradients+40 values=77 complete full-pool evaluations. Counts reconcile12971552 PDE/11046552 IC model evaluations and7073 physics calls;75000 extra target-only IC draws, no model evaluations. Training741.815751 seconds,462405parameters,nf0. Five uphill accepted steps and36 positive secant updates; three extra line values. Alpha range0.006494940768662488..0.8955255313369075. Logged alternating variants, acceptance, history maxima and uphill flags reconciled; raw trace does not include gradient norm,so exact Armijo decrement is not independently recomputed from trace alone.

```json
{
  "metrics": {
    "L_val": 0.11407538375028281,
    "physics_weighted": 0.018639419033664947,
    "ic_relative_l2": 0.30892711877822876,
    "ic_relative_mse": 0.09543596471661786,
    "windows": {
      "early": {
        "continuity": 0.007972556963836043,
        "momentum": 0.024090132486872404,
        "poisson": 0.0015432747634306569,
        "total": 0.033605964214139104
      },
      "middle": {
        "continuity": 0.0023260282106234084,
        "momentum": 0.009483014390852015,
        "poisson": 0.0009957956690302401,
        "total": 0.012804838270505664
      },
      "late": {
        "continuity": 0.00475360844563831,
        "momentum": 0.009557231338741201,
        "poisson": 0.001842709634991342,
        "total": 0.016153549419370854
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9975301027297974,
        "0.5": 0.9965492486953735,
        "0.8": 0.995853066444397
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0024698972702026367,
        "0.5": -0.003450751304626465,
        "0.8": -0.004146933555603027
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.15918348729610443,
        "0.5": 0.3964749276638031,
        "0.8": 0.6749911904335022
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3810878992080688,
        "0.5": 2.1775403022766113,
        "0.8": 3.474938154220581
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3916262686252594,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 1.4901161193847656e-06
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
    "training_seconds": 741.8157511659665,
    "optimizer_steps": 5185,
    "physics_calls": 7073,
    "pde_training_evaluations": 12971552,
    "ic_training_evaluations": 11046552,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2563,
      "loss": 0.1292569935321808,
      "elapsed_seconds": 187.50294608296826,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2624512; IC_eval=2624512"
    },
    {
      "step": 5148,
      "loss": 0.11373528838157654,
      "elapsed_seconds": 375.0616775410017,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5271552; IC_eval=5271552"
    },
    {
      "step": 5167,
      "loss": 0.10523850400932133,
      "elapsed_seconds": 564.7168146659969,
      "note": "BB a=19;ok=19;alpha=0.00891688;BB1;up=3;values=21"
    },
    {
      "step": 5185,
      "loss": 0.1038521365262568,
      "elapsed_seconds": 741.8154836249887,
      "note": "final BB; PDE_eval=12971552; IC_eval=11046552; PDE_draws=5371552; IC_draws=5421552; sp=37; accepted=37; gp=37; vp=40; nf=0; up=5; E=3.567659"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 12971552,
    "IC_eval": 11046552,
    "PDE_draws": 5371552,
    "IC_draws": 5421552,
    "sp": 37,
    "accepted": 37,
    "gp": 37,
    "vp": 40,
    "nf": 0,
    "up": 5,
    "complete_full_evaluations": 77,
    "extra_ic_target_only_draws": 75000,
    "secant_used": 36,
    "alpha_min": 0.006494940768662488,
    "alpha_max": 0.8955255313369075
  },
  "spectral_trace": [
    {
      "attempt": 1,
      "variant": 1,
      "used_secant": false,
      "alpha": 0.01,
      "base": 0.11460039450321347,
      "proposal": 0.11299723130650818,
      "threshold": 0.11460015624051541,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 2,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.00993232716468929,
      "base": 0.11299723130650818,
      "proposal": 0.11229482293128967,
      "threshold": 0.11460031253891101,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 3,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.034789103413091826,
      "base": 0.11229482293128967,
      "proposal": 0.11095290817320347,
      "threshold": 0.11460021109030709,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 4,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.0215426492943398,
      "base": 0.11095290817320347,
      "proposal": 0.11063157394528389,
      "threshold": 0.11460030447736248,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 5,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.01689881571272792,
      "base": 0.11063157394528389,
      "proposal": 0.11055726697668433,
      "threshold": 0.11460024642961233,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 6,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.006914322632953586,
      "base": 0.11055726697668433,
      "proposal": 0.10995697102043778,
      "threshold": 0.11299711883205552,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 7,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.007478486128621803,
      "base": 0.10995697102043778,
      "proposal": 0.10983747721184045,
      "threshold": 0.11229481074155769,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 8,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.018397929141319123,
      "base": 0.10983747721184045,
      "proposal": 0.1095650406787172,
      "threshold": 0.11095288006942836,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 9,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.30028311419273634,
      "base": 0.1095650406787172,
      "proposal": 0.10737747442908585,
      "threshold": 0.11063116778661997,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 10,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.060394263170983856,
      "base": 0.10737747442908585,
      "proposal": 0.10870653495658189,
      "threshold": 0.11055714811107242,
      "accepted": true,
      "values": 2,
      "uphill": true
    },
    {
      "attempt": 11,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.014512128937862313,
      "base": 0.10870653495658189,
      "proposal": 0.10892184893600643,
      "threshold": 0.10995622262910865,
      "accepted": true,
      "values": 1,
      "uphill": true
    },
    {
      "attempt": 12,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.006759808190849212,
      "base": 0.10892184893600643,
      "proposal": 0.10676893312484026,
      "threshold": 0.10983701978279478,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 13,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.006494940768662488,
      "base": 0.10676893312484026,
      "proposal": 0.10673688002862036,
      "threshold": 0.10956503695073556,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 14,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.00707543137760212,
      "base": 0.10673688002862036,
      "proposal": 0.10670882824342698,
      "threshold": 0.10892184610795161,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 15,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.43039534812351743,
      "base": 0.10670882824342698,
      "proposal": 0.10574393917340785,
      "threshold": 0.10892168214180833,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 16,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.12274837386397298,
      "base": 0.10574393917340785,
      "proposal": 0.10622390953358263,
      "threshold": 0.10892174009112225,
      "accepted": true,
      "values": 1,
      "uphill": true
    },
    {
      "attempt": 17,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.021280680207499687,
      "base": 0.10622390953358263,
      "proposal": 0.10594428586773574,
      "threshold": 0.10676864234192136,
      "accepted": true,
      "values": 2,
      "uphill": false
    },
    {
      "attempt": 18,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.010397249366194449,
      "base": 0.10594428586773574,
      "proposal": 0.10529920749831945,
      "threshold": 0.10673672600115167,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 19,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.008916880733707083,
      "base": 0.10529920749831945,
      "proposal": 0.10523850400932133,
      "threshold": 0.1067088167430737,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 20,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.007731625291009969,
      "base": 0.10523850400932133,
      "proposal": 0.10522102285176516,
      "threshold": 0.10622390752571159,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 21,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.029810995854626283,
      "base": 0.10522102285176516,
      "proposal": 0.10517004458233714,
      "threshold": 0.10622390391734952,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 22,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.021986035035991384,
      "base": 0.10517004458233714,
      "proposal": 0.10513871791772544,
      "threshold": 0.10594428221830231,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 23,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.07759049843299724,
      "base": 0.10513871791772544,
      "proposal": 0.10526754416059703,
      "threshold": 0.10529919120149715,
      "accepted": true,
      "values": 1,
      "uphill": true
    },
    {
      "attempt": 24,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.006822002394566016,
      "base": 0.10526754416059703,
      "proposal": 0.10501804947853088,
      "threshold": 0.10526749486477735,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 25,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.006869084961711697,
      "base": 0.10501804947853088,
      "proposal": 0.1050085888709873,
      "threshold": 0.10526754319629059,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 26,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.01024692112318158,
      "base": 0.1050085888709873,
      "proposal": 0.10499500087462366,
      "threshold": 0.10526754279364614,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 27,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.8955255313369075,
      "base": 0.10499500087462366,
      "proposal": 0.10406535770744085,
      "threshold": 0.10526742674343066,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 28,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.06107184373024373,
      "base": 0.10406535770744085,
      "proposal": 0.10430681612342596,
      "threshold": 0.10526751795826733,
      "accepted": true,
      "values": 2,
      "uphill": true
    },
    {
      "attempt": 29,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.015829469168636836,
      "base": 0.10430681612342596,
      "proposal": 0.10408629092853516,
      "threshold": 0.10501796207622716,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 30,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.009475953812345105,
      "base": 0.10408629092853516,
      "proposal": 0.10399289417546242,
      "threshold": 0.10500856215565067,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 31,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.00725100748115363,
      "base": 0.10399289417546242,
      "proposal": 0.10397419717628509,
      "threshold": 0.1049949973374084,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 32,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.006604030653511236,
      "base": 0.10397419717628509,
      "proposal": 0.10396957758348435,
      "threshold": 0.10430681563845892,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 33,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.06938287571224468,
      "base": 0.10396957758348435,
      "proposal": 0.10392601508647203,
      "threshold": 0.10430681156950641,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 34,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.020587504678391814,
      "base": 0.10392601508647203,
      "proposal": 0.10391286201775074,
      "threshold": 0.10408628941651966,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 35,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.07913391354389433,
      "base": 0.10391286201775074,
      "proposal": 0.10387544299010187,
      "threshold": 0.1039928889317952,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 36,
      "variant": 2,
      "used_secant": true,
      "alpha": 0.01062448958656723,
      "base": 0.10387544299010187,
      "proposal": 0.10385959653649479,
      "threshold": 0.10397419427552354,
      "accepted": true,
      "values": 1,
      "uphill": false
    },
    {
      "attempt": 37,
      "variant": 1,
      "used_secant": true,
      "alpha": 0.011696028940888909,
      "base": 0.10385959653649479,
      "proposal": 0.1038521365262568,
      "threshold": 0.10396957652713802,
      "accepted": true,
      "values": 1,
      "uphill": false
    }
  ]
}
```

## Decision and interpretation

New lowest finite total: improves050 by0.0005846124 (0.510%). Physics falls0.0001683091 and IC MSE falls0.0004163033. Early total/all early components worsen,but middle/late totals and all their components improve. All37 spectral attempts accepted,includingfive temporary uphill moves,so nonmonotone mechanism was exercised.77 full evaluations versus05085 and5148 initial updates versus5115; initial trajectories/time allocation are close but not identical. Retain053 solely by L_val without gates. This small single-fit gain is exploratory,not proof of BB/nonmonotone causal contribution, significance or numerical-reference accuracy. Continue054-060 before five fresh1800-second finalists plus P/B/W.
