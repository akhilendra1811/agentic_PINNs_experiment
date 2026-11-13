# Trial 018

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:11; kind=mechanism; mechanism_id=real_gabor_windowed_sine_representation.

## Parent methods and evidence

Closed011 source remains lowest finite total.1678472594,physics.0725275773,IC MSE.0953196821. Swish017 improved physics to.0619809002 across all windows but IC worsened to.1097686885,total.1717495887. Tanh016 also failed net improvement. Test localised oscillations instead of globally oscillatory sine or self-gated/nonoscillatory functions. Keep all011 trainer/model linear shapes fixed. No parent weights/checkpoints/optimiser state reused.

## Novelty claim

Activation/representation mechanism real Gaussian-windowed sine f(x)=sin(x)*exp(-x^2/2). Known real Gabor-type function,inspired by Saragadam et al.,WIRE:Wavelet Implicit Neural Representations,https://arxiv.org/html/2301.05187 . This is an explicitly local real-valued adaptation,not complex WIRE architecture,its initialization,hyperparameters or published benchmark reproduction. SIREN periodic representation precedent https://arxiv.org/abs/2006.09661 also credited. Multiplicative Gaussian envelope changes function/derivative localisation,not a sine frequency-only scalar. No scientific novelty claimed.

## Hypothesis and proposed change

Hypothesis: Gaussian localisation preserves useful oscillatory IC representation while restraining global derivative interference,enabling lower total than011. Replace all six Sine functions with sin(x)*exp(-.5*x.square()),fixed unit frequency/window,no learned coefficients. Same seven Linear shapes,Xavier/bias,features/density transform. Entire parent trainer/optimisers/PR+ AST equality passed,85765params/six functions confirmed. Synthetic-logit CPU/native MPS first/second/third analytic derivatives and odd symmetry passed without PDE coordinates or fitting. Risks:envelope saturation/vanishing features,loss of high-amplitude gradients,unchanged initialization and extra exp/autodiff overhead;single real component loses complex WIRE expressivity. Paper image gains do not imply this PINN advantage.

## Training objective and setup

Fresh seven-Linear,width128,three spatial harmonics19features,six real Gabor hidden functions,85765parameters,Xavier uniform/bias.01,rho=rho0*exp(clamp(max(t-.05,0)*raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:hidden five matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),input/output weights+biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a controlled batch choice not total cap. Final all100000PDE/75000IC cycle cache once,25 separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal deadline checks and rollback. All overhead inside budget;return states and log actual draws/evaluations/steps/CG/search/restarts/nonfinite counts. Fixed-pool coordinates only,no generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite total below.1678472594,with IC improvement over017 and sufficient physics preservation for net gain. Larger total falsifies net hypothesis irrespective of any diagnostic or throughput improvement. Read actual full metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no IC/physical gates. One fresh matched-time local real-Gabor test cannot establish statistical significance,general wavelet/WIRE ranking or Athena++ accuracy;failures retained,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.23058 initial updates+58 CG attempts,57 accepted,96 line values,10 restarts,0 nonfinite proposals.154 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.17141623197315076,
    "physics_weighted": 0.07514422101437206,
    "ic_relative_l2": 0.3102773129940033,
    "ic_relative_mse": 0.09627201095877869,
    "windows": {
      "early": {
        "continuity": 0.17465738099132264,
        "momentum": 0.02326522174049342,
        "poisson": 0.010872480878778961,
        "total": 0.208795083610595
      },
      "middle": {
        "continuity": 0.010528486110464485,
        "momentum": 0.011609002450112874,
        "poisson": 0.006771628458180394,
        "total": 0.028909117018757754
      },
      "late": {
        "continuity": 0.0174803596839528,
        "momentum": 0.01545098352467533,
        "poisson": 0.01649359516462331,
        "total": 0.049424938373251445
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9949939250946045,
        "0.5": 0.9900173544883728,
        "0.8": 0.9882655143737793
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005006074905395508,
        "0.5": -0.009982645511627197,
        "0.8": -0.011734485626220703
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.1093592494726181,
        "0.5": 0.3342154622077942,
        "0.8": 0.5969480276107788
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2696278095245361,
        "0.5": 2.0135200023651123,
        "0.8": 3.1860740184783936
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3040301203727722,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.814697265625e-06
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
    "training_seconds": 739.8855540420045,
    "optimizer_steps": 23116,
    "physics_calls": 26908,
    "pde_training_evaluations": 39011392,
    "ic_training_evaluations": 35161392,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 7083,
      "loss": 0.4780457317829132,
      "elapsed_seconds": 187.51546020898968,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=7252992; IC_eval=7252992"
    },
    {
      "step": 14335,
      "loss": 0.44054630398750305,
      "elapsed_seconds": 375.0231281250017,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=14679040; IC_eval=14679040"
    },
    {
      "step": 21604,
      "loss": 0.43607741594314575,
      "elapsed_seconds": 562.5041089170263,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=22122496; IC_eval=22122496"
    },
    {
      "step": 23116,
      "loss": 0.4123716619797051,
      "elapsed_seconds": 739.8853481250117,
      "note": "final full PR+; PDE_eval=39011392; IC_eval=35161392; PDE_draws=23711392; IC_draws=23686392; cg=58; accepted=57; full=100000/75000; micro=4096; lines=96; nf=0; restarts=10"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported versus011:total rose0.0035689726 (2.13%),physics0.0026166437 and IC MSE0.0009523288 higher. All physics window totals increased versus011. Compared with017 IC improved0.0134966775,physics worsened0.0131633208,net improved0.0003333567,so localisation changed the balance but did not beat best. 23058 initial updates/154 full evaluations versus011 30152/284 show high derivative cost. Retain finite result without diagnostic gates;no general real-Gabor/WIRE ranking or significance claim.
