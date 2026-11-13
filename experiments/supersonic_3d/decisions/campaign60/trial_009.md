# Trial 009

Research metadata (locked on preparation): research_area=optimisation; parents=trial:6; kind=mechanism; mechanism_id=shampoo_inverse_root_preconditioning.

## Parent methods and evidence

Parent closed Trial 006, source only, remains lowest at L_val 0.1690991738 (physics 0.0715177878, IC MSE 0.0975813860). Trial 008's blockwise rotated Adam improved IC MSE to 0.0861996959 but physics rose to 0.0863559452, giving the higher total 0.1725556411. Its initial updates fell to 26262 versus 28908 in Trial 006. The lower IC/training loss does not override total validation loss. Retain the parent's auxiliary partition, model and full-pool PR+ finish, while testing matrix inverse-root direction scaling. Fresh initial weights/state throughout; no trained parent weights, moments, preconditioners or checkpoints are imported.

## Novelty claim

Optimisation mechanism: blockwise Shampoo-inspired inverse-fourth-root covariance preconditioning with scalar Adam-norm grafting, replacing Muon's momentum orientation. Credit Gupta, Koren and Singer, Shampoo: Preconditioned Stochastic Tensor Optimization, https://arxiv.org/html/1802.09568v2 , matrix Algorithm 1. This is a disclosed local EMA/momentum/grafting variant, not the original cumulative-gradient algorithm or an exact released package. It differs from Trial 008's Adam coordinatewise normalisation in a rotating basis: here inverse covariance roots determine the direction and Adam supplies only its scalar Frobenius magnitude per tile. The mechanism is substantive, not learning-rate-only tuning, and no new scientific optimiser is claimed. Auxiliary AdaBelief retains its attribution/licence.

## Hypothesis and proposed change

Hypothesis: inverse-root correlations combined with controlled update magnitude improve the physics/IC balance enough to beat Trial 006. Use twenty 64x64 hidden tiles. Maintain momentum M=0.9M+0.1G, original-coordinate squared-gradient V=0.99V+0.01G^2, and L=0.99L+0.01GG^T, R=0.99R+0.01G^TG. At step 1/every 50, symmetrise each covariance, add delta*I with delta=1e-4*trace/n+1e-12, and form inverse fourth roots from eigenvalues clamped below at delta. Let U=L^(-1/4)*(M/(1-0.9^t))*R^(-1/4) and A=(M/(1-0.9^t))/(sqrt(V/(1-0.99^t))+1e-8). Update by -0.001*U*||A||F/max(||U||F,1e-12). No decay or extra clipping. Input/output weights and biases remain on the parent's AdaBelief. Model/auxiliary optimiser/PR+ AST equality and syntax passed; synthetic diagonal inverse-root, symmetry, graft-norm and native MPS four-tile refresh checks passed, without coordinate sampling or PINN fitting. Native checks emitted no fallback warnings. Risks: damped/blockwise covariance bias, graft magnitude obscuring useful scales, decomposition cost and IC/physics tradeoffs.

## Training objective and setup

Fresh unchanged P sine model, seven Linear layers width 128, three spatial harmonics, 85765 parameters, Xavier/bias 0.01, startup_dt=0.05; density rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)). Objective = continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, mean squared components weighted 1. First 80% of 750 seconds: hidden BlockShampoo(lr=0.001,betas=(0.9,0.99),frequency=50,eps=1e-8,block_size=64), settings above; auxiliary UnrectifiedAdaBelief(lr=0.001,betas=(0.9,0.999),eps=1e-12). Clear all model gradients and apply both disjoint partitions to the same backward pass. Initial 1024 PDE/1024 IC samples with replacement are a control choice, not a total cap. At the final phase, cache all 100000 PDE and 75000 IC points once by cycle sampling. Every complete gradient/value uses these fixed pools via 25 exact-weight microbatches up to 4096 PDE/3072 IC. No new/perturbed coordinates, validation access or reference targets. Preserve PR+ with descent restart, four-trial Armijo c1=1e-4/halving, alpha seed rules, >12-second attempt reserve, four-second chunk/eight-second proposal checks and rollback on interruption. Return both initial states plus CG state; log actual draws, repeated evaluations, updates/accepted steps/line trials/restarts/nonfinite proposals and timing. All decomposition/update overhead counts inside the budget; the owner alone checkpoints then scores. No PINN fit for this ID has preceded PRE completion.

## Expected outcome

Expect L_val below Trial 006's 0.1690991738, potentially retaining low physics while recovering enough IC error for a net improvement. Any component can deteriorate; neither smaller IC error, lower training F nor higher throughput is an independent promotion rule. A larger total contradicts the net hypothesis. Read all metric components/windows, IC and density/mass/periodicity diagnostics, exact pool/update counts, history, timing and run.log including backend warnings. One fit cannot establish statistical significance or the general merit of Shampoo; this is a local blockwise variant. Use only finite total L_val, without IC/positivity/periodicity gates, post-validation updates, ID reruns or numerical-reference rewards. Document any execution failure honestly and count it.

## Observed results

L_val 0.17506928114564246; physics 0.08783423443403038; IC MSE 0.08723504671161209, L2 0.2953557968. All required files and diagnostics read. 27110 initial updates, 113 CG attempts/107 accepted, 175 line values, 16 restarts, zero nonfinite proposals. 288 full-pool evaluations reconcile exactly; no partial evaluations. Training 738.641500 seconds, 85765 parameters. No warning or execution error in run.log. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.17506928114564246,
    "physics_weighted": 0.08783423443403038,
    "ic_relative_l2": 0.29535579681396484,
    "ic_relative_mse": 0.08723504671161209,
    "windows": {
      "early": {
        "continuity": 0.19859728505036287,
        "momentum": 0.028042681244929733,
        "poisson": 0.012005066910467847,
        "total": 0.23864503320576044
      },
      "middle": {
        "continuity": 0.015125121972347194,
        "momentum": 0.01384057238341715,
        "poisson": 0.007331526969979906,
        "total": 0.03629722132574425
      },
      "late": {
        "continuity": 0.0206851772504954,
        "momentum": 0.01854293499761799,
        "poisson": 0.019204010542196632,
        "total": 0.05843212279031002
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9939340353012085,
        "0.5": 0.9872497320175171,
        "0.8": 0.9855844974517822
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.006065964698791504,
        "0.5": -0.01275026798248291,
        "0.8": -0.014415502548217773
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11163840442895889,
        "0.5": 0.33713072538375854,
        "0.8": 0.5889076590538025
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.269174575805664,
        "0.5": 2.002164125442505,
        "0.8": 3.0979089736938477
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.3999721109867096,
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
    "training_seconds": 738.6415004580049,
    "optimizer_steps": 27223,
    "physics_calls": 34310,
    "pde_training_evaluations": 56560640,
    "ic_training_evaluations": 49360640,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 8484,
      "loss": 0.44666188955307007,
      "elapsed_seconds": 187.5124974999926,
      "note": "BlockShampoo/AdaBelief before full PR+; PDE_eval=8687616; IC_eval=8687616"
    },
    {
      "step": 16928,
      "loss": 0.4309541583061218,
      "elapsed_seconds": 375.0031361669535,
      "note": "BlockShampoo/AdaBelief before full PR+; PDE_eval=17334272; IC_eval=17334272"
    },
    {
      "step": 25418,
      "loss": 0.42367255687713623,
      "elapsed_seconds": 562.5094577079872,
      "note": "BlockShampoo/AdaBelief before full PR+; PDE_eval=26028032; IC_eval=26028032"
    },
    {
      "step": 27223,
      "loss": 0.3732562535442412,
      "elapsed_seconds": 738.6412779999664,
      "note": "final full PR+; PDE_eval=56560640; IC_eval=49360640; PDE_draws=27860640; IC_draws=27835640; cg=113; accepted=107; full=100000/75000; micro=4096; lines=175; nf=0; restarts=16"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported: versus Trial 006 total increased 0.0059701073 (3.53%); physics rose 0.0163164466 while IC MSE improved 0.0103463393. Every physics window total increased. Retain finite result without diagnostic gates; Trial 006 still leads. This is one time-limited blockwise local variant, not evidence against Shampoo generally or a significance claim. Close normally; no rerun or trained-state reuse.
