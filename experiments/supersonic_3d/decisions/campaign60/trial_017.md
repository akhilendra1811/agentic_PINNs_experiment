# Trial 017

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:11; kind=mechanism; mechanism_id=swish_hidden_representation.

## Parent methods and evidence

Closed011 source,current best finite L_val.1678472594,physics.0725275773,IC MSE.0953196821. Tanh016 total.1746118691 slightly reduced physics(.0719962681) but increased IC(.1026156010). Its saturating representation did not improve net score. Test a smooth nonmonotone self-gated activation with linear positive tail to reduce saturation bias while preserving exact trainer/model shapes. No trained states/checkpoints/weights reused.

## Novelty claim

Activation/representation mechanism Swish beta1: f(x)=x sigmoid(x),also called SiLU. Credit Ramachandran,Zoph,Le,Searching for Activation Functions,https://arxiv.org/abs/1710.05941 . Known activation,no scientific novelty claim. Changes function and derivative structure versus sine/tanh,not a coefficient-only sine experiment. All six hidden units use Swish;periodic input Fourier features remain. Original paper computer-vision gains are not evidence of this PINN advantage. No learned beta or extra trainable parameter.

## Hypothesis and proposed change

Hypothesis: smooth gating/linear positive tail improves IC representation enough to lower total versus011 while preserving useful PDE derivatives. Replace each hidden Sine with SwishActivation forward x*sigmoid(x),beta1 fixed. Same seven Linear shapes,initialisation,features,density transform. Entire parent trainer/optimisers/PR+ AST equality passed.85765 parameters,six activations confirmed. Synthetic-logit CPU/native MPS first/second/third derivative analytic formulas and forward SiLU equivalence passed,no model fit or PDE coordinates. Risks:nonzero hidden mean,negative-side saturation,spectral bias and unchanged Xavier initialisation may limit convergence;higher derivative cost reduces updates. No benefit presumed from paper claims.

## Training objective and setup

Fresh seven-Linear width128 model,three spatial harmonics19features,six Swish hidden activations,85765 parameters,Xavier uniform/bias.01,rho=rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). Objective continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:five hidden matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),input/output weights+biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pooled replacement,a controlled choice not a total cap. Final phase caches all100000PDE/75000IC via cycle once,25 exactly separately weighted microbatches max4096PDE/3072IC for each complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All work inside budget. Log actual draws/evaluations/steps/CG/search/restarts/nonfinite counts;return states. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite L_val below.1678472594,with lower IC error than016 and sufficient physics preservation for net gain. Larger total contradicts net hypothesis regardless of one component or throughput improvement. Read actual metrics/windows/IC/density/mass/periodicity/history/metadata/log and reconcile full-pool counts. Finite total alone ranks,no diagnostic gates. Single fresh matched-time fit cannot establish significance,general activation superiority or numerical-reference accuracy;retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.27220 initial updates+84 CG attempts,81 accepted,133 line values,9 restarts,0 nonfinite proposals.217 complete full-pool evaluations reconcile exactly,no partial work or backend warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.17174958871119644,
    "physics_weighted": 0.0619809002368346,
    "ic_relative_l2": 0.3313135802745819,
    "ic_relative_mse": 0.10976868847436183,
    "windows": {
      "early": {
        "continuity": 0.1538934894067609,
        "momentum": 0.02409169227704587,
        "poisson": 0.00550527100922198,
        "total": 0.18349045269302874
      },
      "middle": {
        "continuity": 0.009016570763719619,
        "momentum": 0.011227542295276588,
        "poisson": 0.004626610608322672,
        "total": 0.024870723667318878
      },
      "late": {
        "continuity": 0.014766285574038493,
        "momentum": 0.013674035110029396,
        "poisson": 0.007202864511998468,
        "total": 0.03564318519606636
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9953601360321045,
        "0.5": 0.9901065826416016,
        "0.8": 0.9886850118637085
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004639863967895508,
        "0.5": -0.009893417358398438,
        "0.8": -0.011314988136291504
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10583296418190002,
        "0.5": 0.32016006112098694,
        "0.8": 0.5768897533416748
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2565546035766602,
        "0.5": 1.9423637390136719,
        "0.8": 3.0413999557495117
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.5194141268730164,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.86102294921875e-06
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
    "params": 85765,
    "training_seconds": 738.8594365409808,
    "optimizer_steps": 27304,
    "physics_calls": 32645,
    "pde_training_evaluations": 49573280,
    "ic_training_evaluations": 44148280,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 8488,
      "loss": 0.6037175059318542,
      "elapsed_seconds": 187.51277570798993,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=8691712; IC_eval=8691712"
    },
    {
      "step": 17010,
      "loss": 0.5042577385902405,
      "elapsed_seconds": 375.0065860829782,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=17418240; IC_eval=17418240"
    },
    {
      "step": 25517,
      "loss": 0.4664650559425354,
      "elapsed_seconds": 562.5192971249926,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=26129408; IC_eval=26129408"
    },
    {
      "step": 27304,
      "loss": 0.46636182628571987,
      "elapsed_seconds": 738.8592585409642,
      "note": "final full PR+; PDE_eval=49573280; IC_eval=44148280; PDE_draws=27973280; IC_draws=27948280; cg=84; accepted=81; full=100000/75000; micro=4096; lines=133; nf=0; restarts=9"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported versus011: total rose0.0039023293 (2.32%). Physics improved0.0105466770 and all three window totals decreased,with early/middle/late continuity and Poisson improved. IC MSE worsened0.0144490063. Total improves016 by0.0028622804 but IC is also worse than016,contrary to that expected component. Retain finite result without diagnostic gates;011 remains leader. Initial27220 updates versus30152 and217 versus284 full evaluations expose derivative/activation overhead in matched time. One fit does not prove general Swish ranking or significance.
