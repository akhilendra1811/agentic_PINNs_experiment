# Trial 004

Research metadata (locked on preparation): research_area=optimisation; parents=trial:3; kind=mechanism; mechanism_id=lookahead_slow_fast_updates.

## Parent methods and evidence

Parent closed Trial 003, source only. Its fresh 750-second fit is the current lowest score: L_val 0.1791090870, weighted physics 0.0901053409, IC relative MSE 0.0890037461. P scored 0.1833311671 and Trial 002 scored 0.1842663685. Trial 003 improved middle/late physics to 0.0383838429/0.0626421251 while early total stayed near P (0.2363456274). Its unrectified AdaBelief update is a useful controlled parent for a distinct slow/fast optimisation mechanism. The fixed-pool investigation found that old/new W differ in sampling and backend/update exposure; that motivates examining stability, but does not prove the cause of W's deterioration or authorise changing the frozen protocol. Fresh random weights and fresh optimiser state are used; no trained parent weights or ensemble is imported.

## Novelty claim

Optimisation mechanism: Lookahead's coupled slow/fast parameter trajectories, wrapping the parent's inner optimiser during the initial phase. This changes the optimisation process rather than only a scalar learning rate. Credit Zhang, Lucas, Hinton and Ba, Lookahead Optimizer: k steps forward, 1 step back, https://arxiv.org/html/1907.08610v2 , Algorithm 1 and the inner-state discussion. The known mechanism is instantiated with the existing AdaBelief variant; it is not claimed as a new scientific optimiser. The historical campaign's final EMA did not repeatedly reset the fast iterates to interpolated slow weights during training, so this is distinct from that mechanism. AdaBelief attribution and BSD notice remain in the source.

## Hypothesis and proposed change

Hypothesis: a slow trajectory that periodically absorbs fast updates reduces stochastic wandering on the finite pools and lowers total validation loss beyond Trial 003. Keep the inner unrectified AdaBelief implementation unchanged. Clone initial parameters into nontrainable optimiser-state slow buffers. After every k=5 fast AdaBelief steps, set slow <- slow + 0.5*(fast-slow) and copy slow back to fast. Preserve the inner moments throughout. At the 80%-time boundary, use the last completed slow state to initialise the unchanged L-BFGS finish; any incomplete group of up to four fast steps is discarded. No slow-weight modification happens after checkpointing or during validation. Two synthetic CPU interpolation/reset checks passed, and AST checks confirmed the architecture and inner optimiser are unchanged. Risks: interpolation reduces progress within the time budget, the parent's gain may disappear, and stochastic L-BFGS can dominate final differences.

## Training objective and setup

Fresh seven-Linear, width-128 P sine network, three harmonics per spatial axis, 85765 parameters, startup_dt=0.05, rho=rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)). Training loss = continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, absolute component MSEs with coefficient 1; frozen validation remains relative-IC plus weighted-window physics. Initial 80% of 750 seconds: unrectified AdaBelief, lr=0.001, betas=(0.9,0.999), epsilon=1e-12 accumulated into variance and added to denominator, with Lookahead k=5, alpha=0.5. No clipping, decay, rectification or AMSGrad. Final phase: LBFGS(lr=1,max_iter=3,history_size=30,line_search_fn=strong_wolfe), inherited unchanged. Sample 1024 PDE and 1024 labelled IC points from full fixed pools with replacement per outer step; hold them fixed across repeated closures. This batch is a controlled choice, not a total-points-per-step cap. Per the user's clarification, any later method may accumulate over the full 100000 PDE and/or 75000 IC points while keeping individual context calls <=8192. No new or perturbed coordinates, validation access or reference targets. Record quarter/final history, actual draws/evaluations including closures, fast steps and synchronisations; return inner/L-BFGS state and slow buffers. Preserve the eight-second deadline reserve and owner-only checkpoint-then-score workflow. No PINN fit for this ID has run before PRE completion.

## Expected outcome

Expect L_val below Trial 003's 0.1791090870, potentially through lower middle/late residuals or IC MSE without losing more early physics than the net gain. No separate IC threshold is expected or imposed. A higher total loss contradicts the net improvement even if a diagnostic improves. Read every PDE component/window, IC MSE/L2, density/mass/periodicity diagnostic, history, counts, metadata and run.log. Compare actual throughput because slow synchronisation adds work within the same wall-clock limit. No component, density sign, mass drift or periodic error filters retention; use finite total L_val only. A numerical failure is counted and documented without reusing the ID. This single fit cannot establish statistical significance or reference-trajectory accuracy.

## Observed results

Completed normally, return code 0. L_val 0.181127430963, weighted physics 0.085488589178, IC relative MSE 0.095638841786, IC L2 0.309255301952. 85765 parameters, 32703 outer steps, 742.012642 training seconds; 37100544 PDE and IC evaluations each, 33487872 draws each, all fixed-pool sampling with replacement. Lookahead made 30939 fast steps and 6187 synchronisations; the last four fast steps were discarded at the documented boundary. No adaptive probes or execution errors. All numerical records and run.log read; full records below.

```json
{
  "metrics": {
    "L_val": 0.18112743096333056,
    "physics_weighted": 0.08548858917768394,
    "ic_relative_l2": 0.30925530195236206,
    "ic_relative_mse": 0.09563884178564663,
    "windows": {
      "early": {
        "continuity": 0.18238830031911724,
        "momentum": 0.02765887355052244,
        "poisson": 0.011532070616779203,
        "total": 0.22157924448641889
      },
      "middle": {
        "continuity": 0.01590381611951188,
        "momentum": 0.015328658956282095,
        "poisson": 0.007011381180325682,
        "total": 0.03824385625611966
      },
      "late": {
        "continuity": 0.023353820124951102,
        "momentum": 0.021211316597332386,
        "poisson": 0.014834030084845044,
        "total": 0.059399166807128534
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9939037561416626,
        "0.5": 0.9881461262702942,
        "0.8": 0.9883458614349365
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.006096243858337402,
        "0.5": -0.01185387372970581,
        "0.8": -0.011654138565063477
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10859512537717819,
        "0.5": 0.3289949893951416,
        "0.8": 0.5826870799064636
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2631810903549194,
        "0.5": 1.983386754989624,
        "0.8": 3.106951951980591
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3357604742050171,
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
    "training_seconds": 742.0126421659952,
    "optimizer_steps": 32703,
    "physics_calls": 36231,
    "pde_training_evaluations": 37100544,
    "ic_training_evaluations": 37100544,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9580,
      "loss": 0.5090814828872681,
      "elapsed_seconds": 187.50575424998533,
      "note": "Lookahead-AdaBelief/LBFGS; PDE_eval=9809920; IC_eval=9809920"
    },
    {
      "step": 19206,
      "loss": 0.47056931257247925,
      "elapsed_seconds": 375.00456429098267,
      "note": "Lookahead-AdaBelief/LBFGS; PDE_eval=19666944; IC_eval=19666944"
    },
    {
      "step": 28976,
      "loss": 0.43254774808883667,
      "elapsed_seconds": 562.515405040991,
      "note": "Lookahead-AdaBelief/LBFGS; PDE_eval=29671424; IC_eval=29671424"
    },
    {
      "step": 32703,
      "loss": 0.42787283658981323,
      "elapsed_seconds": 742.0123750410276,
      "note": "final Lookahead-AdaBelief/LBFGS; PDE_eval=37100544; IC_eval=37100544; PDE_draws=33487872; IC_draws=33487872; mode=pool; fast=30939; syncs=6187"
    }
  ]
}
```

## Decision and interpretation

The net improvement hypothesis is not supported: L_val increased from Trial 003's 0.1791090870 to 0.1811274310, by 0.0020183440. Physics decreased 0.0046167517, but IC MSE increased 0.0066350957. All three physics window totals improved; those improvements cannot override the larger total. Trial 004 still improves on P's 0.1833311671 and remains a finite comparison, without displacing Trial 003. The IC L2 of 0.3092553 is a diagnostic, not an exclusion threshold. A single fit does not establish statistical significance, explain the fixed-pool effect, or prove Lookahead generally inferior. Retain the record and use Trial 003's lower total as the next source parent. A deterministic full-pool conjugate-gradient finish is a distinct optimisation hypothesis that also investigates the user's clarified freedom to use all 100000 PDE and 75000 IC points per update through microbatch accumulation. Full-pool updates alter gradient variance and curvature consistency but do not add new coordinate coverage. No checkpoint reuse, validation training or numerical-reference feedback.
