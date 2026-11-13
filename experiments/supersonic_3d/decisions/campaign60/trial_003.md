# Trial 003

Research metadata (locked on preparation): research_area=optimisation; parents=P; kind=mechanism; mechanism_id=adabelief_gradient_prediction_variance.

## Parent methods and evidence

Parent P, alone, is the lowest-scoring completed method at 750 seconds: L_val 0.1833311671, weighted physics 0.0931966237, IC relative MSE 0.0901345434. Closed Trial 002 (RAdam in P's initial phase) scored 0.1842663685, with weighted physics 0.0947799669 and IC MSE 0.0894864016. Its Poisson and IC improvements did not offset continuity/momentum increases, so it does not displace P. Trial 001's NAdam/W result was much worse (0.8293095970). The small P/002 gap supports retaining the compact P setup as the control while testing a different variance mechanism. All weights and optimiser states are fresh; no combination of trained models or checkpoints is used.

## Novelty claim

Optimisation mechanism: belief-based gradient-prediction variance, replacing P's initial Adam update by an unrectified AdaBelief variant. Rather than Adam's squared gradient, its second-moment accumulator uses the squared deviation of the current gradient from the updated first-moment prediction. This is a substantive preconditioning change, not a learning-rate-only experiment, and differs from NAdam anticipation and RAdam rectification. Credit Zhuang et al., AdaBelief Optimizer: Adapting Stepsizes by the Belief in Observed Gradients, https://arxiv.org/abs/2010.07468 . The minimal local implementation follows the unrectified upstream update at https://github.com/juntang-zhuang/Adabelief-Optimizer/blob/update_0.2.0/pypi_packages/adabelief_pytorch0.2.1/adabelief_pytorch/AdaBelief.py ; the BSD notice is retained. No publication novelty or complete package reproduction is claimed.

## Hypothesis and proposed change

Hypothesis: scaling by gradient-prediction error trusts persistent descent directions and damps inconsistent ones, improving P's coupled fit enough to lower total validation loss. Use a minimal UnrectifiedAdaBelief class for P's first phase, with m=0.9*m+0.1*g, s=0.999*s+0.001*(g-m)^2+epsilon, denominator=sqrt(s/(1-0.999^t))+epsilon, and parameter update -lr*m/((1-0.9^t)*denominator). Set epsilon=1e-12 in both stated locations, instead of the package's current default 1e-16; this is deliberate damping against variance collapse. No rectification, AMSGrad or weight decay. P's L-BFGS phase, model, loss, coordinates and time split remain unchanged. Syntax, AST equality of P's Sine/PaperModel/build_model, a two-step scalar-formula CPU check, and a zero-gradient CPU check passed. The optimiser checks used only two-element tensors with prescribed gradients, not a PINN fit or field coordinates. Possible risks are over-amplified consistent gradients, damping that suppresses useful small updates, and stochastic curvature noise in the retained finish.

## Training objective and setup

Fresh P sine MLP with seven Linear layers, width 128, three harmonics per spatial axis and 85765 trainable parameters; Xavier initialisation and bias 0.01. Density is rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)); raw velocity/potential channels are unchanged. Loss = continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, component MSEs each weighted 1; IC training terms are absolute while frozen scoring uses relative IC MSE. First 80% of the 750-second budget: unrectified AdaBelief, lr=0.001, betas=(0.9,0.999), epsilon=1e-12 as above. Final phase: unchanged LBFGS(lr=1,max_iter=3,history_size=30,line_search_fn=strong_wolfe). No gradient clipping or decay. Each outer step samples 1024 PDE and 1024 IC points with replacement from the full immutable pools of 100000 and 75000 respectively, using context pool APIs. Hold q/IC/targets fixed across each L-BFGS closure group; resample for the next outer step. No extra/perturbed coordinates or validation access; all microbatches below 8192. Quarter/final history records include all repeated point evaluations and sampler draws. Return both optimiser states and steps. Preserve P's eight-second reserve and all scoring through the locked runner after saving final weights. No PINN training has been run for this ID before this PRE record.

## Expected outcome

Expect total L_val below P's 0.1833311671. A possible route is lower IC MSE than 0.0901345434 and/or lower middle/late physics than 0.0411873131 / 0.0673445895, with less continuity/momentum increase than RAdam produced. Early continuity may remain dominated by the retained startup representation. These component predictions can fail independently; none is a selection threshold. Higher total loss would contradict the net-improvement hypothesis even if some components improve. Read full metrics, all density/mass/periodicity and IC diagnostics, history, source/timing metadata, actual point counts and run.log before POST. Rank only finite total L_val, without IC, positivity or other eligibility gates. Document any execution failure and count the attempt without rerunning its ID; no reference-trajectory accuracy claim follows from a smaller score.

## Observed results

Completed normally, return code 0. L_val 0.179109086970 = weighted physics 0.090105340898 + IC relative MSE 0.089003746072, IC L2 0.298334956169. Early/middle/late physics 0.236345627357 / 0.038383842853 / 0.062642125141. 85765 parameters, 32102 outer steps, 742.005839 training seconds, 35540 objective calls. 36392960 PDE and IC point evaluations each, including repeated closures; 32872448 PDE and IC draws each, with replacement from the fixed full pools. No adaptive probes, no execution errors. All required result files and numerical diagnostics were read. Full records follow.

```json
{
  "metrics": {
    "L_val": 0.17910908697026368,
    "physics_weighted": 0.0901053408978279,
    "ic_relative_l2": 0.2983349561691284,
    "ic_relative_mse": 0.08900374607243577,
    "windows": {
      "early": {
        "continuity": 0.1967455960724913,
        "momentum": 0.027470220978701592,
        "poisson": 0.012129810305826173,
        "total": 0.23634562735701908
      },
      "middle": {
        "continuity": 0.01583577838045138,
        "momentum": 0.014676099989706386,
        "poisson": 0.007871964482530044,
        "total": 0.03838384285268781
      },
      "late": {
        "continuity": 0.023984616555427534,
        "momentum": 0.02062870928278691,
        "poisson": 0.01802879930302105,
        "total": 0.06264212514123549
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9937934279441833,
        "0.5": 0.9873268008232117,
        "0.8": 0.9861559867858887
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.00620657205581665,
        "0.5": -0.01267319917678833,
        "0.8": -0.013844013214111328
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11093592643737793,
        "0.5": 0.3362424671649933,
        "0.8": 0.5917965769767761
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2680529356002808,
        "0.5": 2.0000922679901123,
        "0.8": 3.1392345428466797
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.2967512607574463,
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
    "params": 85765,
    "training_seconds": 742.00583941699,
    "optimizer_steps": 32102,
    "physics_calls": 35540,
    "pde_training_evaluations": 36392960,
    "ic_training_evaluations": 36392960,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9282,
      "loss": 0.47725793719291687,
      "elapsed_seconds": 187.50894104200415,
      "note": "AdaBelief/LBFGS; PDE_eval=9504768; IC_eval=9504768"
    },
    {
      "step": 18866,
      "loss": 0.4548889696598053,
      "elapsed_seconds": 375.0030242089997,
      "note": "AdaBelief/LBFGS; PDE_eval=19318784; IC_eval=19318784"
    },
    {
      "step": 28472,
      "loss": 0.4252031445503235,
      "elapsed_seconds": 562.5073334170156,
      "note": "AdaBelief/LBFGS; PDE_eval=29155328; IC_eval=29155328"
    },
    {
      "step": 32102,
      "loss": 0.40462687611579895,
      "elapsed_seconds": 742.0054159589927,
      "note": "final AdaBelief/LBFGS; PDE_eval=36392960; IC_eval=36392960; PDE_draws=32872448; IC_draws=32872448; mode=pool"
    }
  ]
}
```

## Decision and interpretation

The net-improvement hypothesis is supported by this single 750-second fit. L_val decreased from P's 0.1833311671 to 0.1791090870, a reduction of 0.0042220801 (about 2.30%). Weighted physics decreased by 0.0030912828 and IC MSE by 0.0011307973. Middle/late totals improved from 0.0411873131/0.0673445895 to 0.0383838429/0.0626421251. Early total rose slightly (0.2358406750 to 0.2363456274), with higher continuity but lower momentum/Poisson. The aggregate gain is not based on filtering any individual component or diagnostic. This is the lowest finite score observed so far, warranting retention and a controlled optimisation follow-up. It is not a final winner or proof of statistical significance; actual steps (32102 versus P 32270), stochastic samples, hardware and the L-BFGS finish prevent an isolated causal interpretation. The implementation is explicitly unrectified AdaBelief with epsilon 1e-12, not the package default or a newly invented optimiser. A Lookahead slow/fast wrapper on this parent is a substantive next optimisation hypothesis. No IC or physical eligibility gates, checkpoint reuse, or Athena++ accuracy claim.
