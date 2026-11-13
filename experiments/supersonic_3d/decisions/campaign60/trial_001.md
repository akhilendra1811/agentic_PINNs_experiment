# Trial 001

Research metadata (locked on preparation): research_area=optimisation; parents=W; kind=mechanism; mechanism_id=nadam_nesterov_adaptive.

## Parent methods and evidence

Parent W, alone. Fresh 750-second W: L_val 0.6010315363 = weighted physics 0.5516820270 + IC relative MSE 0.0493495093; early/middle/late physics 1.7540428258 / 0.3559001773 / 0.1882068172. Fresh P and B scored 0.1833311671 and 0.2332496972. W is the required starting reference, not the current score leader. Its IC-first curriculum and large sine residual representation provide a controlled setting for an optimiser-only test. The historical Trial 069 score is not treated as comparable evidence under the new fixed pools. No checkpoint or trained weights are reused. This is not a combination of separately trained models.

## Novelty claim

Mechanism within the optimisation block: replace W's Adam update by NAdam's Nesterov-adaptive first-moment update. This changes the update rule rather than a learning-rate scalar. NAdam is a known method credited to Dozat, implemented here through torch.optim.NAdam; no publication novelty is claimed. The prior reference-free campaign primarily used Adam and also tested a moment reset, PCGrad and EMA; this experiment instead changes momentum anticipation throughout the same curriculum. Official implementation reference: https://docs.pytorch.org/docs/2.15/generated/torch.optim.NAdam.html . Gradient stiffness and objective conflicts motivate the comparison, without assuming literature results transfer to this PDE.

## Hypothesis and proposed change

Hypothesis: a Nesterov-adaptive update tracks the IC-to-physics objective handoff more effectively and reduces W's large early continuity/momentum residual enough to lower total validation loss, without requiring a different representation or loss. Change torch.optim.Adam to torch.optim.NAdam with momentum_decay=0.004, default betas (0.9,0.999), epsilon 1e-8 and zero weight decay. Keep every W learning-rate, loss, architecture and sampling choice unchanged. Add non-training accounting counters and final-history counts for direct IC-only forwards, PDE evaluations and sampling draws. Static AST comparison verified that ResPINN and build_model are identical to W. Overshoot or extra update overhead could negate the hypothesis.

## Training objective and setup

Fresh ResPINN, width 256, ten residual sine blocks h+=0.5*sin(1.5*Linear(h)), three spatial Fourier harmonics per axis, 664325 parameters. Outputs rho=rho0*exp(clamp(t*raw_rho,-4,4)), raw velocity and potential. NAdam starts at lr=1e-4, warms linearly to 1e-3 over the first 5% of 750 seconds, then cosine-decays to 1e-5. Clip total gradient norm to 0.5. For elapsed fraction f<0.20, use IC velocity relative MSE only. Thereafter b=min(1,(f-0.20)/0.20), bP=min(1,(f-0.20)/0.05), and loss=b*(3.5*continuity+7.5*mean_momentum)+6*bP*Poisson+(1+32*b)*IC_relative_MSE. IC batch 1024 per step. PDE batch 1024, quotas 320 early / 256 middle / 448 late, selected from 2048 pool samples with a further 4096 fallback exactly as in W. All sampling is with replacement from the full immutable 100000 PDE / 75000 IC training pools; no new or perturbed coordinates and no validation access. Unique coverage is not assumed. Each PDE/IC microbatch stays below 8192. Training loop stops with the inherited two-second reserve; optimiser state, steps and accounting are returned, and history is recorded at quarter marks and final. Only the owner runner computes frozen L_val after saving weights. No unrecorded training has been performed.

## Expected outcome

Expect L_val below W's 0.6010315363, principally through lower early continuity (W 0.8111156858) and momentum (W 0.9073835514), while IC relative MSE may rise from W's 0.0493495093 as the coupled fit changes. A score above W contradicts the improvement hypothesis; even an improvement must be compared with P's stronger 0.1833311671 score. Inspect all residual windows, IC MSE/L2, density distribution, mass drift and periodicity, together with actual timing and point counts, to interpret the result. None is a separate acceptance threshold. Retention and eventual selection use total finite L_val only; a failure is documented and counts as Trial 001 rather than rerun.

## Observed results

Completed normally, return code 0. L_val 0.829309597016 = weighted physics 0.779783161736 + IC relative MSE 0.049526435281; IC L2 0.222545355558. Early/middle/late totals 2.202311882629 / 0.620939189980 / 0.306078056432. 664325 parameters; 60901 optimiser steps in 748.032253 seconds. Candidate counters: 15666176 PDE evaluations, 62362624 IC evaluations including 46696448 direct IC-only evaluations; 31332352 PDE draws and 62362624 IC draws, all pool sampling. Context metadata omits the direct IC-only phase; the final history note supplies the full accounting. No adaptive probes. All numerical records were read, including run.log, which contains no error. Full metrics, metadata and recorded history follow; physical quantities are diagnostics only.

```json
{
  "metrics": {
    "L_val": 0.8293095970164892,
    "physics_weighted": 0.7797831617358766,
    "ic_relative_l2": 0.22254535555839539,
    "ic_relative_mse": 0.049526435280612624,
    "windows": {
      "early": {
        "continuity": 1.193257318877047,
        "momentum": 0.9708845193736876,
        "poisson": 0.03817004437840977,
        "total": 2.2023118826291443
      },
      "middle": {
        "continuity": 0.41402994100078994,
        "momentum": 0.18772968869539317,
        "poisson": 0.019179560283422856,
        "total": 0.620939189979606
      },
      "late": {
        "continuity": 0.19950085519807342,
        "momentum": 0.07660472693721193,
        "poisson": 0.02997247429704654,
        "total": 0.3060780564323319
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9464549422264099,
        "0.5": 0.9222068190574646,
        "0.8": 0.910292387008667
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.05354505777359009,
        "0.5": -0.0777931809425354,
        "0.8": -0.08970761299133301
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11056222766637802,
        "0.5": 0.22757059335708618,
        "0.8": 0.3482533395290375
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.213488221168518,
        "0.5": 1.504319667816162,
        "0.8": 1.919132947921753
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3709011673927307,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 3.0994415283203125e-06
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
    "params": 664325,
    "training_seconds": 748.0322529589757,
    "optimizer_steps": 60901,
    "physics_calls": 15299,
    "pde_training_evaluations": 15666176,
    "ic_training_evaluations": 15666176,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.0,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 46585,
      "loss": 0.9757040739059448,
      "elapsed_seconds": 187.52847808401566,
      "note": "NAdam; lr=0.000896; IC_eval=47703040; PDE_eval=1006592"
    },
    {
      "step": 51222,
      "loss": 1.674177885055542,
      "elapsed_seconds": 375.03198124998016,
      "note": "NAdam; lr=0.000546; IC_eval=52451328; PDE_eval=5754880"
    },
    {
      "step": 56023,
      "loss": 1.1282154321670532,
      "elapsed_seconds": 562.5037817499833,
      "note": "NAdam; lr=0.00017; IC_eval=57367552; PDE_eval=10671104"
    },
    {
      "step": 60901,
      "loss": 0.8790454864501953,
      "elapsed_seconds": 748.0319892090047,
      "note": "final NAdam; IC_eval=62362624; PDE_eval=15666176; PDE_draws=31332352; IC_draws=62362624; mode=pool"
    }
  ]
}
```

## Decision and interpretation

The prespecified improvement hypothesis is contradicted. Total L_val rose by 0.2282780607 from W's 0.6010315363 to 0.8293095970. Early continuity increased from 0.8111156858 to 1.1932573189 and early momentum from 0.9073835514 to 0.9708845194; middle and late totals also worsened. IC relative MSE was nearly unchanged (0.0493495093 to 0.0495264353), so it does not explain the physics increase. NAdam completed 60901 steps versus W's 63316 and 15299 physics calls versus 15731; changed throughput is part of this matched-time method, but this single fit cannot isolate the cause or establish a general optimiser ranking. The final sampled training loss is not a validation surrogate. Do not promote this configuration while lower total scores are available; this is a finite completed attempt, not an execution failure. Density, mass drift and periodicity do not gate retention. P remains the strongest fresh baseline at L_val 0.1833311671, motivating the next independent optimiser control on P. No claim about Athena++ accuracy follows.
