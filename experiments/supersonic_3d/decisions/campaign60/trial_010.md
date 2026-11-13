# Trial 010

Research metadata (locked on preparation): research_area=optimisation; parents=trial:6; kind=mechanism; mechanism_id=lion_sign_momentum.

## Parent methods and evidence

Parent Trial 006 source only: lowest finite L_val 0.1690991738, physics 0.0715177878, IC MSE 0.0975813860. Trial 009 inverse roots scored 0.1750692811 (physics 0.0878342344, IC MSE 0.0872350467); like 007/008 its better IC did not compensate physics. Test a cheaper sign/momentum rule rather than covariance decomposition. Same model, auxiliary partition and full-pool PR+ finish; no trained states or weights reused.

## Novelty claim

Distinct optimisation mechanism: Lion sign-based updates with separate direction/momentum interpolation coefficients, replacing hidden Muon. Known method, no scientific novelty claim. Credit Chen et al., Symbolic Discovery of Optimization Algorithms, https://arxiv.org/abs/2302.06675 and official algorithm source https://raw.githubusercontent.com/google/automl/master/lion/lion_pytorch.py . This compact recurrence was independently expressed from the algorithm and checked against the official update order. Auxiliary AdaBelief attribution/licence retained. Sign quantisation is substantive, not a learning-rate-only refinement.

## Hypothesis and proposed change

Hypothesis: noise robustness and lower overhead of sign momentum improve total score versus Trial 006. For each of five 128x128 hidden matrices, m starts at zero, direction=sign(0.9m+0.1g), parameter-=1e-4*direction, then m=0.99m+0.01g. Zero weight decay; no bias correction, clipping, variance state or covariance. Input/output weights and biases retain AdaBelief. Syntax, unchanged model/auxiliary/PR+ AST and exact full-finish comparison passed. Three-step synthetic CPU and native MPS checks verified sign, momentum order and zero gradients. Initial local check could not access GPU in sandbox; authorised elevated check passed, no PINN fit or coordinate sampling occurred. A draft string replacement assertion was corrected before source was written/run; no research execution failure. Risks: sign removes magnitude information and fixed sign steps may stall or overfit.

## Training objective and setup

Fresh P sine model: seven Linear layers width 128, 85765 parameters, three spatial Fourier harmonics, Xavier weights/bias 0.01, density startup_dt=0.05. Objective continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z, all absolute-MSE weights one. First 80% of 750-second budget uses hidden Lion(lr=1e-4,betas=(0.9,0.99)), auxiliary UnrectifiedAdaBelief(lr=0.001,betas=(0.9,0.999),eps=1e-12), disjoint partitions from same backward, zero all gradients each step. Initial batches 1024 PDE/1024 IC with replacement from fixed pools, a controlled choice not a cap. Final phase caches all 100000 PDE and 75000 IC once by cycle, accumulates exact separately weighted full gradients/values in 25 microbatches max4096 PDE/3072 IC. Same PR+ descent restart, Armijo c1=1e-4, up to4 proposals halving, alpha seed min(1,1.5accepted_alpha), reset on rejection, deadline reserve >12 per attempt/4 per chunk/8 per proposal and rollback to last accepted state. All overhead within budget. Return both optimisers and CG state, record actual steps/draws/evaluations/search counts. No new coordinates, validation targets, references or post-checkpoint updates.

## Expected outcome

Expect total L_val below 0.1690991738, with physics near or below parent and enough IC preservation for net benefit. Higher total falsifies net hypothesis even if any component or throughput improves. Read all metric windows/IC/density/mass/periodicity/history/metadata/log and reconcile full-pool counts. Rank finite total only, no diagnostic gates. One matched-time fresh fit cannot establish significance or a universal Lion advantage. Full-pool point allowance remains explicit.

## Observed results

L_val 0.16823473026234562; physics 0.07803278266338856; IC MSE 0.09020194759895706; IC L2 0.30033639073371887. All metrics/metadata/history/log and diagnostics read. 30652 initial updates + 110 CG attempts (105 accepted), 172 line values, five restarts, zero nonfinite proposals. 282 complete full-pool evaluations reconcile exactly; no partial evaluations. Training 739.282283 seconds, 85765 parameters. No warnings/execution failure. Full records:

```json
{
  "metrics": {
    "L_val": 0.16823473026234562,
    "physics_weighted": 0.07803278266338856,
    "ic_relative_l2": 0.30033639073371887,
    "ic_relative_mse": 0.09020194759895706,
    "windows": {
      "early": {
        "continuity": 0.1887854455433942,
        "momentum": 0.02614560273028368,
        "poisson": 0.00896838511240115,
        "total": 0.223899433386079
      },
      "middle": {
        "continuity": 0.011644321600283636,
        "momentum": 0.012626734984558572,
        "poisson": 0.00567626824990962,
        "total": 0.029947324834751828
      },
      "late": {
        "continuity": 0.01932876839718765,
        "momentum": 0.017373384137506723,
        "poisson": 0.011835244536800049,
        "total": 0.048537397071494424
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.994337797164917,
        "0.5": 0.9890861511230469,
        "0.8": 0.9867829084396362
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.005662202835083008,
        "0.5": -0.010913848876953125,
        "0.8": -0.01321709156036377
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11342894285917282,
        "0.5": 0.34285953640937805,
        "0.8": 0.6041265726089478
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.280619740486145,
        "0.5": 2.0471105575561523,
        "0.8": 3.2142956256866455
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.44124457240104675,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.2649765014648438e-06
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
    "training_seconds": 739.2822825410403,
    "optimizer_steps": 30762,
    "physics_calls": 37702,
    "pde_training_evaluations": 59587648,
    "ic_training_evaluations": 52537648,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 9643,
      "loss": 0.4852904975414276,
      "elapsed_seconds": 187.51884966605576,
      "note": "Lion/AdaBelief before full PR+; PDE_eval=9874432; IC_eval=9874432"
    },
    {
      "step": 19209,
      "loss": 0.4312962293624878,
      "elapsed_seconds": 375.0104433330125,
      "note": "Lion/AdaBelief before full PR+; PDE_eval=19670016; IC_eval=19670016"
    },
    {
      "step": 28740,
      "loss": 0.41411739587783813,
      "elapsed_seconds": 562.5041667910409,
      "note": "Lion/AdaBelief before full PR+; PDE_eval=29429760; IC_eval=29429760"
    },
    {
      "step": 30762,
      "loss": 0.385402730666101,
      "elapsed_seconds": 739.2821509160567,
      "note": "final full PR+; PDE_eval=59587648; IC_eval=52537648; PDE_draws=31487648; IC_draws=31462648; cg=110; accepted=105; full=100000/75000; micro=4096; lines=172; nf=0; restarts=5"
    }
  ]
}
```

## Decision and interpretation

Total improved 0.0008644436 (0.51%) versus Trial 006: IC MSE fell 0.0073794384 while physics rose 0.0065149949. Early and late physics totals worsened, middle improved. Net hypothesis supported in one fresh matched-time run; retain Trial 010 as lowest finite score without diagnostic gates. Not statistical significance or a general Lion ranking. Full-pool finishing remains unchanged; no proof of W root cause.
