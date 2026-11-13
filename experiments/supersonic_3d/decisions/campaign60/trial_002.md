# Trial 002

Research metadata (locked on preparation): research_area=optimisation; parents=P; kind=mechanism; mechanism_id=radam_variance_rectification.

## Parent methods and evidence

Parent P, alone. Fresh P leads the 750-second baseline comparison at L_val 0.1833311671, weighted physics 0.0931966237 and IC relative MSE 0.0901345434. Its early/middle/late physics totals are 0.2358406750 / 0.0411873131 / 0.0673445895. B scored 0.2332496972 and W 0.6010315363. Closed Trial 001 (W + NAdam) worsened W to 0.8293095970 across all physics windows, with almost unchanged IC MSE; it supplies no reason to prefer the W curriculum as the next optimiser control. P is chosen by total score, not its higher IC error. No checkpoint is reused. This is a single freshly trained paper-style model, not a weight ensemble.

## Novelty claim

Optimisation mechanism: RAdam's variance-rectified adaptive update replaces only P's initial Adam phase. It changes the update rule through the variance-rectification factor and initial nonadaptive updates, not just a learning rate. The final L-BFGS method is retained. RAdam is a known algorithm by Liu et al., On the Variance of the Adaptive Learning Rate and Beyond, https://arxiv.org/abs/1908.03265 ; implementation/equations: https://docs.pytorch.org/docs/2.15/generated/torch.optim.RAdam.html . No scientific novelty is claimed. It differs from Trial 001's Nesterov anticipation and from the historical Adam reset/PCGrad/EMA methods. This is not a faithful re-creation of the released CC-PINN paper's original iteration schedule.

## Hypothesis and proposed change

Hypothesis: rectifying unreliable early second-moment estimates provides a more stable starting trajectory for P's stochastic joint training and subsequent L-BFGS phase, lowering final frozen validation loss. Replace torch.optim.Adam(lr=0.001) with torch.optim.RAdam(lr=0.001, betas=(0.9,0.999), eps=1e-8, weight_decay=0). Retain P's architecture, objective, sampling, 80/20 wall-clock phase split and L-BFGS settings. Add accounting of sampling draws and every objective evaluation, including repeated closures. Static AST checks verified Sine, PaperModel and build_model are identical to P. Risks: slower initial progress, or stochastic L-BFGS curvature noise overwhelming any initial optimiser benefit.

## Training objective and setup

Fresh paper-style sine MLP: seven Linear layers, width 128, three harmonics per spatial axis, 85765 trainable parameters, Xavier weights and bias 0.01. rho=rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)); velocity and potential are raw channels. Preserve startup_dt=0.05. Training loss is continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, all component MSEs with coefficient 1; the IC terms here are absolute, whereas the unchanged scorer uses relative IC MSE. First 80% of the 750-second budget uses RAdam at constant 0.001 with the settings above. Remaining phase uses LBFGS(lr=1, max_iter=3, history_size=30, line_search_fn=strong_wolfe), exactly as P. No clipping or added weight decay. Each outer step draws 1024 PDE points and 1024 labelled IC points with replacement from the entire fixed pools (100000 PDE / 75000 IC); q/IC stay fixed across every closure re-evaluation within that step and are resampled for the next outer step. No coordinate generation/perturbation or validation access. All batches stay below 8192. Record quarter marks and final, return both optimiser states and step count, count all closure forwards separately from draws. Keep P's eight-second deadline reserve. Only the locked runner scores after checkpointing; no training has been executed for this ID before this recorded run.

## Expected outcome

Expect total L_val below P's 0.1833311671, with lower middle/late physics (P 0.0411873131 / 0.0673445895) as a possible route. Early continuity may remain limited by the retained startup representation. IC relative MSE may improve or worsen; only its contribution to the net score matters, and there is no threshold. A higher L_val contradicts the improvement hypothesis even if IC error improves. Read all PDE components/windows, IC MSE/L2, density/mass/periodicity diagnostics, steps, point counts and timing; diagnostics interpret outcomes without filtering them. A nonfinite/failed fit is documented and counted without reusing this ID. Final retention and selection use only finite total L_val at the appropriate matched budget.

## Observed results

Completed normally, return code 0. L_val 0.184266368481 = weighted physics 0.094779966899 + IC relative MSE 0.089486401582, IC L2 0.299142777920. Early/middle/late totals 0.238913980882 / 0.041840496549 / 0.068890043516. 85765 parameters, 32916 outer optimiser steps, 742.056750 training seconds. 36450 objective evaluations, 37324800 PDE and 37324800 IC point evaluations, including repeated L-BFGS closures; 33705984 PDE and 33705984 IC sampling draws, all from fixed full pools with replacement. No adaptive probes or direct IC-only phase. All required numerical files, diagnostics and run.log were read; no execution error occurred. Full records follow.

```json
{
  "metrics": {
    "L_val": 0.18426636848072714,
    "physics_weighted": 0.09477996689917073,
    "ic_relative_l2": 0.2991427779197693,
    "ic_relative_mse": 0.08948640158155641,
    "windows": {
      "early": {
        "continuity": 0.1970706684656675,
        "momentum": 0.029227909316268487,
        "poisson": 0.012615403100466658,
        "total": 0.23891398088240265
      },
      "middle": {
        "continuity": 0.018145285816791378,
        "momentum": 0.01542954613548713,
        "poisson": 0.008265664597067802,
        "total": 0.04184049654934631
      },
      "late": {
        "continuity": 0.02649701167329843,
        "momentum": 0.022304522444048833,
        "poisson": 0.02008850939842534,
        "total": 0.0688900435157726
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9926672577857971,
        "0.5": 0.9831435680389404,
        "0.8": 0.9777253866195679
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.007332742214202881,
        "0.5": -0.01685643196105957,
        "0.8": -0.02227461338043213
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11118751764297485,
        "0.5": 0.334401935338974,
        "0.8": 0.5846662521362305
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2685041427612305,
        "0.5": 1.9874272346496582,
        "0.8": 3.104952573776245
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.4047278165817261,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.384185791015625e-06
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
    "training_seconds": 742.0567496250151,
    "optimizer_steps": 32916,
    "physics_calls": 36450,
    "pde_training_evaluations": 37324800,
    "ic_training_evaluations": 37324800,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9742,
      "loss": 0.48724043369293213,
      "elapsed_seconds": 187.51115345803555,
      "note": "RAdam/LBFGS; PDE_eval=9975808; IC_eval=9975808"
    },
    {
      "step": 19471,
      "loss": 0.4403996169567108,
      "elapsed_seconds": 375.0175022080075,
      "note": "RAdam/LBFGS; PDE_eval=19938304; IC_eval=19938304"
    },
    {
      "step": 29201,
      "loss": 0.43289750814437866,
      "elapsed_seconds": 562.500366125023,
      "note": "RAdam/LBFGS; PDE_eval=29901824; IC_eval=29901824"
    },
    {
      "step": 32916,
      "loss": 0.3828677237033844,
      "elapsed_seconds": 742.056513083051,
      "note": "final RAdam/LBFGS; PDE_eval=37324800; IC_eval=37324800; PDE_draws=33705984; IC_draws=33705984; mode=pool"
    }
  ]
}
```

## Decision and interpretation

The prespecified net improvement is not supported: L_val rose from P's 0.1833311671 to 0.1842663685, a difference of 0.0009352014. Weighted physics increased by 0.0015833432 while IC relative MSE decreased by 0.0006481418. All three window totals increased, contradicting the expected middle/late improvement. Poisson improved in each window but continuity and mean momentum increased; none of these components is an independent gate. The gap is small (about 0.51%) in a single matched-time fit and does not establish statistical significance or a universal optimiser ranking. RAdam completed 32916 outer steps versus P's 32270 and 36450 objective evaluations versus 35728; throughput differences are part of the fixed-time method. The final sampled training loss cannot establish generalisation. Retain the finite record: it is the best numbered score so far but does not displace the lower-scoring P baseline. Use P again as the control for the next distinct, belief-based variance experiment. Both IC error and physical diagnostics remain descriptive, with no thresholds. This is a completed scientific negative/near-tie result, not an execution failure; no ID rerun or checkpoint reuse, and no Athena++ accuracy claim.
