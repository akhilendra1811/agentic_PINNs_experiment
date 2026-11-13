# Trial 011

Research metadata (locked on preparation): research_area=optimisation; parents=trial:10; kind=mechanism; mechanism_id=adan_gradient_difference_momentum.

## Parent methods and evidence

Trial 010 source only: current best L_val 0.1682347303, physics 0.0780327827, IC MSE 0.0902019476. It improves 006 total by 0.51% through IC despite higher physics. Test gradient-change information in place of sign quantisation, keeping auxiliary AdaBelief, P model, loss, pools and full-pool PR+ identical. No parent weights, moments, checkpoints or trained state reused.

## Novelty claim

Distinct known optimisation mechanism Adan: gradient-difference momentum and extrapolated second moments, not another scalar adjustment to Lion/Adam. Credit Xie et al., Adan: Adaptive Nesterov Momentum Algorithm for Faster Optimizing Deep Models, https://arxiv.org/abs/2208.06677 ; official reference algorithm https://raw.githubusercontent.com/sail-sg/Adan/main/adan.py . Independently expressed minimal recurrence, omitting clipping/decay/foreach/fused paths. No scientific novelty claim. AdaBelief attribution/licence retained.

## Hypothesis and proposed change

Hypothesis: gradient-change anticipation improves net physics/IC balance beyond Lion. Hidden matrices use beta1=.98,beta2=.92,beta3=.99,lr=.001,eps=1e-8. Initialise previous gradient to first g so first delta=0; subsequent delta=g-g_previous. m=.98m+.02g; d=.92d+.08delta; v=.99v+.01(g+.92delta)^2. Bias-correct all three moments; parameter-=.001*(m/(1-.98^t)+.92d/(1-.92^t))/(sqrt(v/(1-.99^t))+1e-8). Copy current g into previous after update. No weight decay/clipping; sparse gradients unsupported. Same five hidden matrices/auxiliary partition. Syntax, model/auxiliary/PR+ AST and entire full-finish equality passed. Synthetic CPU/native MPS three-step formula, first delta zero, bias corrections and zero-gradient checks passed; no coordinate sampling or PINN training. Risks: noisy differences amplify stochastic errors, magnitude normalisation and overhead may impair time-limited convergence.

## Training objective and setup

Fresh unchanged P model: seven Linear layers width128, 85765 parameters, sine activations, three spatial harmonics, Xavier/bias .01, density startup .05. Training objective continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z, absolute component MSEs weight one. First80% of750s: hidden Adan settings above, input/output weights/biases UnrectifiedAdaBelief(lr=.001,betas=(.9,.999),eps=1e-12), same backward with all gradients cleared. Initial1024 PDE/1024 IC pool sampling with replacement is a controlled choice, not a total cap. Final phase caches all100000 PDE/75000 IC via cycle and uses exact separately weighted full-pool accumulation,25 microbatches max4096 PDE/3072 IC. Preserve PR+ restart and bounded Armijo c1=1e-4,four halvable proposals,seed min(1,1.5accepted_alpha),rejection reset, >12s attempt reserve,4s chunk/8s proposal deadline checks and rollback to last accepted parameters. All overhead inside budget. Log steps,draws,evaluations,CG/search/accepted/restart/nonfinite counts; return both initial optimisers and CG state. Fixed pools only; no coordinate generation/perturbation,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect L_val below0.1682347303, ideally lower physics without offsetting IC degradation. A larger total contradicts the hypothesis even if one window,IC or throughput improves. Read all metrics/windows/IC/density/mass/periodicity/history/metadata/log and reconcile pool counts. Only finite total ranks; no eligibility gates or significance/general-optimizer claims from one fresh matched-time run. Retain negative results and count execution failures without rerunning IDs.

## Observed results

All canonical metrics/metadata/history/log and diagnostics read. 30152 initial updates +109 CG attempts,107 accepted,175 line values,10 restarts,zero nonfinite proposals. 284 full-pool evaluations reconcile exactly, no partial evaluations. No backend warning or execution failure. Full actual records:

```json
{
  "metrics": {
    "L_val": 0.16784725940962605,
    "physics_weighted": 0.07252757727446266,
    "ic_relative_l2": 0.3087388575077057,
    "ic_relative_mse": 0.0953196821351634,
    "windows": {
      "early": {
        "continuity": 0.17455835922373908,
        "momentum": 0.02436421385851956,
        "poisson": 0.008686035284230634,
        "total": 0.20760860836648928
      },
      "middle": {
        "continuity": 0.010191092073617415,
        "momentum": 0.01208932678586612,
        "poisson": 0.00558127843906257,
        "total": 0.027861697298546102
      },
      "late": {
        "continuity": 0.017871917289779195,
        "momentum": 0.016163124822144742,
        "poisson": 0.011259650711277996,
        "total": 0.045294692823201935
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.995111346244812,
        "0.5": 0.990164041519165,
        "0.8": 0.9884902238845825
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.004888653755187988,
        "0.5": -0.009835958480834961,
        "0.8": -0.01150977611541748
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11028797179460526,
        "0.5": 0.3351534605026245,
        "0.8": 0.5949080586433411
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2696731090545654,
        "0.5": 2.0091254711151123,
        "0.8": 3.1464133262634277
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.30819112062454224,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 6.67572021484375e-06
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
    "training_seconds": 738.2321275830036,
    "optimizer_steps": 30261,
    "physics_calls": 37252,
    "pde_training_evaluations": 59275648,
    "ic_training_evaluations": 52175648,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9418,
      "loss": 0.499561607837677,
      "elapsed_seconds": 187.50208941602614,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=9644032; IC_eval=9644032"
    },
    {
      "step": 18847,
      "loss": 0.4540310502052307,
      "elapsed_seconds": 375.00662300002296,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=19299328; IC_eval=19299328"
    },
    {
      "step": 28269,
      "loss": 0.41615280508995056,
      "elapsed_seconds": 562.5053990830202,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=28947456; IC_eval=28947456"
    },
    {
      "step": 30261,
      "loss": 0.40829732874408364,
      "elapsed_seconds": 738.2319005000172,
      "note": "final full PR+; PDE_eval=59275648; IC_eval=52175648; PDE_draws=30975648; IC_draws=30950648; cg=109; accepted=107; full=100000/75000; micro=4096; lines=175; nf=0; restarts=10"
    }
  ]
}
```

## Decision and interpretation

New lowest finite score, improving Trial 010 by 0.0003874709 (0.23%). Physics fell 0.0055052054 and IC MSE rose 0.0051177345. All physics window totals improved. Net hypothesis supported locally, with a small single-fit difference that does not establish statistical significance or general Adan superiority. Retain by total only despite higher IC L2; no diagnostic gates.
