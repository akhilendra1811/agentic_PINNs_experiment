# Trial 005

Research metadata (locked on preparation): research_area=optimisation; parents=trial:3; kind=mechanism; mechanism_id=full_pool_restarted_conjugate_gradient.

## Parent methods and evidence

Parent closed Trial 003, source only, remains the lowest observed score at 0.1791090870 (physics 0.0901053409, IC MSE 0.0890037461). Trial 004's Lookahead reduced physics to 0.0854885892 but increased IC MSE to 0.0956388418, giving the higher total 0.1811274310. Thus its lower physics alone does not justify promotion. P scored 0.1833311671. The W investigation and the user's no-total-per-step-cap clarification motivate a deterministic full-pool optimiser test, without changing the frozen pools or claiming fresh coordinates would necessarily fix the gap. No checkpoint or parent weights are reused; all phases belong to one fresh 750-second fit.

## Novelty claim

Optimisation mechanism: restarted nonlinear Polak–Ribiere-plus conjugate directions with bounded Armijo search on the complete training objective, replacing the parent's stochastic L-BFGS finish. This changes direction construction and acceptance, not merely batch size or learning rate. Conjugate gradient is established numerical optimisation; related primary software documentation is https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cg.html . This local implementation uses PR+, a sufficient-descent restart and Armijo-only backtracking; it is not SciPy's full Wolfe line-search implementation or a new published method. Full-pool accumulation supplies the consistent objective needed for conjugate directions and permits more than 8192 total points per update. The unchanged inner AdaBelief implementation retains its attribution and BSD notice.

## Hypothesis and proposed change

Hypothesis: after the same stochastic AdaBelief phase, consistent full-pool gradients and conjugate directions improve the final score relative to stochastic mini-batch L-BFGS. For successive full gradients g and g_old, beta=max(0,g dot (g-g_old)/(g_old dot g_old)); propose d=-g+beta*d_old. Restart to -g for a nonfinite or insufficiently descending direction, defined by g dot d >= -0.001*||g||^2. Initial alpha=1; accept if F(theta+alpha*d)<=F(theta)+1e-4*alpha*(g dot d), testing at most four halvings. Next accepted alpha seed is min(1,1.5*alpha); rejection restores the original parameters, resets conjugacy and retains the reduced seed (floor 1e-8). Nonfinite trial proposals backtrack; a nonfinite base gradient fails the run. Deadline interruption restores the last accepted parameters. No Hessian, L-BFGS state or numerical trajectory is used. Syntax/model/inner-optimiser AST checks, synthetic PR+ direction/restart checks and exact microbatch weight/count arithmetic passed; none trained a PINN.

## Training objective and setup

Fresh unchanged P architecture (85765 parameters, seven Linear layers width 128, sine, three spatial harmonics, startup_dt=0.05). Retain density rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)). Objective F = mean continuity residual squared + sum of three mean momentum residuals squared + mean Poisson residual squared + sum of three mean absolute IC velocity errors squared, coefficients all 1, as in Trial 003; frozen scorer remains unchanged. First 80% of 750 seconds: unrectified AdaBelief(lr=0.001,betas=(0.9,0.999),eps=1e-12), 1024 PDE and 1024 IC points sampled with replacement per step. At the transition, cache exactly one complete cycle of 100000 PDE and 75000 IC coordinates/targets through context sampling. A complete full-objective evaluation uses 25 microbatches: PDE chunks up to 4096, IC allocations up to 3072, ending with 1696 PDE/1272 IC. Weight PDE means by chunk_PDE/100000 and IC means by chunk_IC/75000; both sets of weights sum to 1. Backward each weighted chunk before the parameter update, so each full gradient uses ALL points. Each line-search value also uses all points but no parameter backward. Cached coordinates stay identical across all full-gradient and line-search evaluations. One CG attempt therefore may evaluate the same full pools multiple times; there is no total-per-step cap, but every context call respects <=8192. Initial mode pool, cache mode cycle; no new/perturbed coordinates or validation access. Counts distinguish draws, repeated evaluations, CG attempts and accepted updates. The final phase uses the documented PR+/Armijo method, not L-BFGS. Begin CG attempts only with >12 seconds remaining; check the four-second reserve before each full-evaluation chunk and eight seconds before proposals, rolling back incomplete proposals. Return inner state, conjugate-direction state and counts, record quarter/final history, and allow only the owner runner to checkpoint then score. No training for this ID preceded PRE completion.

## Expected outcome

Expect L_val below Trial 003's 0.1791090870 through a better final physics/IC balance, potentially reducing stochastic curvature noise in middle/late physics (parent 0.0383838429/0.0626421251). Full-pool training does not create new coverage beyond the fixed arrays and may overfit their objective or make too few useful updates; Armijo-only PR+ has no claimed global convergence guarantee here. IC error can move either way and cannot independently select or exclude the method. A larger total contradicts the net-improvement hypothesis even if training F falls. Read all metric components and diagnostics, timings, history, counts, line trials/restarts/nonfinite rejections and run.log before POST. Partial deadline evaluations count as attempted work and cannot update the checkpointed weights. Use only finite total L_val for ranking; numerical execution failures count without rerunning the ID. No claim of reference-solution accuracy or statistical significance.

## Observed results

Completed normally, return code 0. L_val 0.171914651398, physics 0.082777507043, IC relative MSE 0.089137144355, IC L2 0.298558443785. 85765 parameters, 738.956777 actual seconds within the 750-second budget. 30356 adaptive steps followed by 113 CG attempts, 108 accepted; 175 line-search values, 26 descent restarts and zero nonfinite proposals. Thus 288 complete full-pool evaluations used exactly 100000 PDE and 75000 IC points each. Arithmetic checks verify all owner counters: 59884544 PDE and 52684544 IC evaluations, 31184544 PDE and 31159544 IC draws, 37556 physics calls. Cached cycle sampling visited each full training pool once; subsequent evaluations reused that cache. No partial evaluation was needed to explain the counts, and no execution error occurred. All required result files and diagnostics were read. Full records follow.

```json
{
  "metrics": {
    "L_val": 0.17191465139780907,
    "physics_weighted": 0.08277750704265899,
    "ic_relative_l2": 0.29855844378471375,
    "ic_relative_mse": 0.08913714435515008,
    "windows": {
      "early": {
        "continuity": 0.19255918120891571,
        "momentum": 0.02546828398076027,
        "poisson": 0.010725352903837389,
        "total": 0.22875281809351336
      },
      "middle": {
        "continuity": 0.013898020422931754,
        "momentum": 0.013105434636113139,
        "poisson": 0.0068084468427731795,
        "total": 0.03381190190181807
      },
      "late": {
        "continuity": 0.019292320712303603,
        "momentum": 0.017051481539416644,
        "poisson": 0.017422943455101536,
        "total": 0.053766745706821786
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.994037389755249,
        "0.5": 0.9878190755844116,
        "0.8": 0.985995352268219
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.0059626102447509766,
        "0.5": -0.012180924415588379,
        "0.8": -0.014004647731781006
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11025422066450119,
        "0.5": 0.333914577960968,
        "0.8": 0.5849788188934326
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2624883651733398,
        "0.5": 1.9821120500564575,
        "0.8": 3.0877439975738525
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3632882535457611,
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
    "params": 85765,
    "training_seconds": 738.9567772920127,
    "optimizer_steps": 30469,
    "physics_calls": 37556,
    "pde_training_evaluations": 59884544,
    "ic_training_evaluations": 52684544,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9587,
      "loss": 0.4901161789894104,
      "elapsed_seconds": 187.5031158750062,
      "note": "AdaBelief before full PR+; PDE_eval=9817088; IC_eval=9817088"
    },
    {
      "step": 19058,
      "loss": 0.46056920289993286,
      "elapsed_seconds": 375.0148443750222,
      "note": "AdaBelief before full PR+; PDE_eval=19515392; IC_eval=19515392"
    },
    {
      "step": 28475,
      "loss": 0.4051913321018219,
      "elapsed_seconds": 562.5031690000324,
      "note": "AdaBelief before full PR+; PDE_eval=29158400; IC_eval=29158400"
    },
    {
      "step": 30469,
      "loss": 0.3809198415838182,
      "elapsed_seconds": 738.9565559590119,
      "note": "final full PR+; PDE_eval=59884544; IC_eval=52684544; PDE_draws=31184544; IC_draws=31159544; cg=113; accepted=108; full=100000/75000; micro=4096; lines=175; nf=0; restarts=26"
    }
  ]
}
```

## Decision and interpretation

The net-improvement hypothesis is supported in this single fit. L_val fell from Trial 003's 0.1791090870 to 0.1719146514, a decrease of 0.0071944356 (about 4.02%); it is about 6.23% below P. Physics fell 0.0073278339 while IC MSE rose only 0.0001333983. All three physics windows improved, to 0.2287528181/0.0338119019/0.0537667457. Total score, not the separate physics or IC diagnostics, makes this the current lowest finite method. Full-pool PR+ and the change from stochastic L-BFGS were tested together; this does not isolate batch size alone or prove that finite-pool overfitting caused W's earlier deterioration. Retain for further optimisation and eventual finalist consideration, without declaring a final winner or statistical significance. The full-pool exposure and acceptance accounting are verified, and the actual 738.9568 seconds reflect the documented reserve. No coordinates outside the training pools, parent checkpoints or numerical-reference feedback were used. An inherited module-docstring sentence about unchanged L-BFGS is stale; the frozen PRE and executable trainer correctly specify PR+. Preserve the locked source rather than repairing its annotation after execution. A distinct matrix-gradient preconditioner during the initial phase, with this PR+ finish retained, is a suitable next controlled hypothesis.
