# Trial 055

Research metadata (locked on preparation): research_area=classical_optimisation; parents=trial:50; kind=mechanism; mechanism_id=compressed_component_levenberg_marquardt.

## Parent methods and evidence

Trial050 supplies common model/loss/first-half training,total0.1146599961747031. Currentbest054 Anderson0.11397143940087355 gives a competitive target. Prior053/054/secant methods use approximate curvature from history; here derive curvature from derivatives of eight pooled objective components.

## Novelty claim

Known Levenberg-style damped Gauss-Newton applied to a compressed residual map,not a new optimiser. Read official Ceres nonlinear least-squares documentation Levenberg-Marquardt section equations4-6: https://ceres-solver.readthedocs.io/latest/nnls_solving.html . Original ceres-solver.org URL timed out,official ReadTheDocs mirror succeeded. Local identity damping/dual8x8 solve/controller differ from Ceres defaults. This is explicitly NOT full pointwise Gauss-Newton: each residual is RMS of one pooled loss component,so curvature rank<=8 and within-component point directions are compressed.

## Hypothesis and proposed change

Let c contain eight nonnegative full-pool terms C,Mx/3,My/3,Mz/3,P,Ix/E,Iy/E,Iz/E. Set r_i=sqrt(c_i+1e-12),so sumr_i^2=F+8e-12 exactly. Stream eight parameter gradients of weighted component means per microbatch,aggregate dc_i/dtheta,then J_i=dc_i/(2r_i). Solve p=-J^T(JJ^T+lambdaI8)^-1r with lambda10 initially,clamp[1e-6,1e6],normcap.05. Native float32 Gram/products,small CPUfloat64 solve. Prediction=-2r dot Jp-norm(Jp)^2,compare actual full-pool F decrease; accept finiteratio>.1,lambda*=4below.25 or*.5above.75. Rejected/deadline restores base. Objective/gradient preserved but compressed GN curvature differs from pointwise GN and true Hessian. CPUfloat64/native MPSfloat32 synthetic checks passed: weighted RMS objective/gradient identity, dual8x8 vs primal damped solve, model prediction/normcap/damping rules. Actual streaming Jacobian closure on unequal synthetic chunks reproduced pooled values/J and exact point/chunk/reverse counters. Parent050 trainer prefix/model/loss/initial phase/full evaluator byte-identical. No PINN fitting/new training coordinates in checks. Eight reverse sweeps per microbatch are costly; repeated derivatives reuse coordinate forwards and do not count as new point evaluations.

## Training objective and setup

Unchanged050462405parameter width256 periodic19feature RWF/FiLM/Snake/input-skip immediate-density model. F=C+mean3momentum+P+sum3IC/E,E fixed75000target energy;75000target-only IC draws/no model evaluations. First50%1024PDE/1024IC pool updates,Adan directions lr.001 betas(.98,.92,.99) eps1e-8 and auxiliary AdaBelief lr.001 betas(.9,.999) eps1e-12. Remaining time compressed LM on full100000PDE/75000IC cycle cache via4096/3072microbatches+tail. Count Jacobian passes/chunks/reverse sweeps and proposal values separately,including interrupted passes.750second fresh MPS,physical82/RNG823001,all setup/derivatives/transfers inbudget. No total step point cap,8192per call only;frozen scorer/data unchanged.

## Expected outcome

Target total<0.11397143940087355 through component-Jacobian curvature balancing. Rank8 compression can lose useful directions and eight reverse sweeps may permit few updates; damping may be too cautious or require rejected trials. Report actual/predicted ratios,damping,step norms,all eight training terms,actual counts and all validation/physical diagnostics without gates. No full-GN,Newton-Hessian,theorem,significance or reference-accuracy claim.

## Observed results

Actual metrics, metadata, complete history and9 compressed-LM traces follow; run.log/all diagnostics read.5103 initial updates+9 LM attempts(7 accepted,2 rejected).9 complete Jacobians+9 complete values,plus15 microbatches in the tenth deadline-interrupted Jacobian.240 total Jacobian chunks;1917 reverse sweeps=1800 in nine complete passes+117 partial(14 complete microbatches*8+5 sweeps of the fifteenth). Partial coordinate forwards61440 PDE/46080 IC are counted once. Totals reconcile7086912 PDE/6621552 IC model evaluations and5568 physics calls;75000extra target-only IC draws,no model evaluations. Training746.343519 seconds,462405parameters,nf0. No weights committed during partial Jacobian. All model ratios/damping/acceptance/normcaps independently reconciled.

```json
{
  "metrics": {
    "L_val": 0.118796607393381,
    "physics_weighted": 0.020775870802693896,
    "ic_relative_l2": 0.31308263540267944,
    "ic_relative_mse": 0.09802073659068711,
    "windows": {
      "early": {
        "continuity": 0.009025422703298567,
        "momentum": 0.024950280947134956,
        "poisson": 0.0017113331410569682,
        "total": 0.03568703679149049
      },
      "middle": {
        "continuity": 0.003308116750280036,
        "momentum": 0.009917138858323609,
        "poisson": 0.001306816279341425,
        "total": 0.01453207188794507
      },
      "late": {
        "continuity": 0.006458777780463756,
        "momentum": 0.009689645935503767,
        "poisson": 0.0024092600400570314,
        "total": 0.018557683756024554
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9959533214569092,
        "0.5": 0.9917300939559937,
        "0.8": 0.9875472784042358
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.00404667854309082,
        "0.5": -0.008269906044006348,
        "0.8": -0.01245272159576416
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1549547016620636,
        "0.5": 0.3835650086402893,
        "0.8": 0.6489197611808777
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.3630304336547852,
        "0.5": 2.10831880569458,
        "0.8": 3.3311452865600586
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.39100775122642517,
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
    "training_seconds": 746.3435188749572,
    "optimizer_steps": 5112,
    "physics_calls": 5568,
    "pde_training_evaluations": 7086912,
    "ic_training_evaluations": 6621552,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 2547,
      "loss": 0.13760906457901,
      "elapsed_seconds": 187.52439170796424,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=2608128; IC_eval=2608128"
    },
    {
      "step": 5103,
      "loss": 0.11838898062705994,
      "elapsed_seconds": 375.0148412909475,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=5225472; IC_eval=5225472"
    },
    {
      "step": 5108,
      "loss": 0.11116670072078705,
      "elapsed_seconds": 569.9170800829888,
      "note": "CLM a=5;ok=3;lambda=80;pred=0.0015068;actual=0.000111574;rho=0.074047;reverse=1000"
    },
    {
      "step": 5112,
      "loss": 0.10932471882551908,
      "elapsed_seconds": 746.3430376249598,
      "note": "final CLM; PDE_eval=7086912; IC_eval=6621552; PDE_draws=5325472; IC_draws=5375472; lm=9; accepted=7; js=10; jc=9; jch=240; rs=1917; vp=9; nf=0"
    }
  ],
  "full_training_counts": {
    "PDE_eval": 7086912,
    "IC_eval": 6621552,
    "PDE_draws": 5325472,
    "IC_draws": 5375472,
    "lm": 9,
    "accepted": 7,
    "js": 10,
    "jc": 9,
    "jch": 240,
    "rs": 1917,
    "vp": 9,
    "nf": 0,
    "initial_updates": 5103,
    "complete_jacobian_passes": 9,
    "complete_value_passes": 9,
    "partial_jacobian_chunks": 15,
    "partial_pde_evaluations": 61440,
    "partial_ic_evaluations": 46080,
    "partial_reverse_sweeps": 117,
    "extra_ic_target_only_draws": 75000
  },
  "compressed_lm_trace": [
    {
      "attempt": 1,
      "damping_before": 10.0,
      "damping_after": 40.0,
      "predicted": 0.009149676188826561,
      "actual": -0.0010960707440972328,
      "ratio": -0.11979339175256683,
      "accepted": false,
      "step_norm": 0.01961403153836727,
      "components": [
        0.007014960050582886,
        0.003658042987808585,
        0.004809953272342682,
        0.003245879663154483,
        0.00176431133877486,
        0.028569059446454048,
        0.04164702445268631,
        0.024419762194156647
      ]
    },
    {
      "attempt": 2,
      "damping_before": 40.0,
      "damping_after": 40.0,
      "predicted": 0.0032376679591834545,
      "actual": 0.0021590236574411392,
      "ratio": 0.6668452987333663,
      "accepted": true,
      "step_norm": 0.006182699929922819,
      "components": [
        0.007014960050582886,
        0.003658042987808585,
        0.004809953272342682,
        0.003245879663154483,
        0.00176431133877486,
        0.028569059446454048,
        0.04164702445268631,
        0.024419762194156647
      ]
    },
    {
      "attempt": 3,
      "damping_before": 40.0,
      "damping_after": 20.0,
      "predicted": 0.0011126416502520442,
      "actual": 0.0008656787686049938,
      "ratio": 0.7780391543035384,
      "accepted": true,
      "step_norm": 0.0037017157301306725,
      "components": [
        0.0057164141908288,
        0.0035453252494335175,
        0.004619523882865906,
        0.0031602680683135986,
        0.0016045122174546123,
        0.02838725596666336,
        0.04156648367643356,
        0.024370193481445312
      ]
    },
    {
      "attempt": 4,
      "damping_before": 20.0,
      "damping_after": 20.0,
      "predicted": 0.001326725585386157,
      "actual": 0.0009376069065183401,
      "ratio": 0.7067074886065757,
      "accepted": true,
      "step_norm": 0.005694390740245581,
      "components": [
        0.005347544327378273,
        0.0034322631545364857,
        0.004519434180110693,
        0.0030878414399921894,
        0.0015744083793833852,
        0.02832796983420849,
        0.04149509593844414,
        0.02431974560022354
      ]
    },
    {
      "attempt": 5,
      "damping_before": 20.0,
      "damping_after": 80.0,
      "predicted": 0.0015067992499098182,
      "actual": 0.0001115740742534399,
      "ratio": 0.07404707313208286,
      "accepted": false,
      "step_norm": 0.006060726474970579,
      "components": [
        0.004899038467556238,
        0.0033407644368708134,
        0.004435104783624411,
        0.0030352300964295864,
        0.0015017357654869556,
        0.028272656723856926,
        0.041420310735702515,
        0.02426186203956604
      ]
    },
    {
      "attempt": 6,
      "damping_before": 80.0,
      "damping_after": 40.0,
      "predicted": 0.0003983883943874389,
      "actual": 0.00030188472010195255,
      "ratio": 0.757764845449702,
      "accepted": true,
      "step_norm": 0.0015726835699751973,
      "components": [
        0.004899038467556238,
        0.0033407644368708134,
        0.004435104783624411,
        0.0030352300964295864,
        0.0015017357654869556,
        0.028272656723856926,
        0.041420310735702515,
        0.02426186203956604
      ]
    },
    {
      "attempt": 7,
      "damping_before": 40.0,
      "damping_after": 20.0,
      "predicted": 0.0003494465781841427,
      "actual": 0.00033264688681811094,
      "ratio": 0.9519248651587051,
      "accepted": true,
      "step_norm": 0.0020856689661741257,
      "components": [
        0.004767600912600756,
        0.0033080282155424356,
        0.0044038924388587475,
        0.0030074373353272676,
        0.0014867434510961175,
        0.028254790231585503,
        0.04139060154557228,
        0.024245714768767357
      ]
    },
    {
      "attempt": 8,
      "damping_before": 20.0,
      "damping_after": 10.0,
      "predicted": 0.0005930103361606598,
      "actual": 0.0005504076834768057,
      "ratio": 0.9281586675880266,
      "accepted": true,
      "step_norm": 0.0038352098781615496,
      "components": [
        0.004633951000869274,
        0.0032711292151361704,
        0.004368532449007034,
        0.0029788075480610132,
        0.001466896035708487,
        0.028233177959918976,
        0.04135558381676674,
        0.024224089458584785
      ]
    },
    {
      "attempt": 9,
      "damping_before": 10.0,
      "damping_after": 10.0,
      "predicted": 0.0009737179498188198,
      "actual": 0.0006570341065526009,
      "ratio": 0.6747684035966016,
      "accepted": true,
      "step_norm": 0.006943477317690849,
      "components": [
        0.004398883320391178,
        0.003220959799364209,
        0.004319333005696535,
        0.002941435668617487,
        0.001422579400241375,
        0.028194217011332512,
        0.04129723832011223,
        0.024187112227082253
      ]
    }
  ]
}
```

## Decision and interpretation

Compressed LM does not improve total: rises0.0041366112 (3.61%) versus050 and0.0048251680 (4.23%) versus054. Versus050 physics rises0.0019681426 and IC MSE0.0021684686;every physics window total worsens,with only late momentum improving. Seven accepted steps compared with05438 reflect eight-reverse-sweep Jacobian cost. Rank8 curvature,identity damping,initial trajectory and fewer updates are not isolated;this cannot establish full pointwise GN inferiority. Partial final Jacobian is explicitly counted and adds no update. Retain finite classical evidence without gates;054 remains lowest. Continue056-060 then five fresh1800-second finalists and P/B/W;no significance/reference-accuracy claim.
