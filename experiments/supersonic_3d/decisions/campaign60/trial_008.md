# Trial 008

Research metadata (locked on preparation): research_area=optimisation; parents=trial:6; kind=mechanism; mechanism_id=soap_rotated_adam_preconditioning.

## Parent methods and evidence

Parent closed Trial 006, source only, remains lowest at L_val 0.1690991738, physics 0.0715177878 and IC relative MSE 0.0975813860. Trial 007 replaced its hidden matrix update with Adafactor and scored 0.1783725057: lower IC MSE (0.0892537606) did not offset higher physics (0.0891187452). Thus neither a smaller IC error nor factorisation alone justifies promotion. Trial 006's model/auxiliary partition and full-pool PR+ finish are retained as controls. Its all-window physics improvement motivates testing a different correlated preconditioner. No trained parent weights, moments, basis or checkpoints are imported; the entire fit starts fresh.

## Novelty claim

Optimisation mechanism: blockwise SOAP-style Adam in a rotating Kronecker eigenbasis for hidden matrices, replacing Muon's orientation normalisation. Credit Vyas et al., SOAP: Improving and Stabilizing Shampoo using Adam, https://arxiv.org/html/2409.11321v2 , Algorithm 3. The implemented method is an explicitly local blockwise variant: direct damped eigendecomposition, covariance refresh before the current update, and approximate diagonal variance transport. It is not a faithful copy of the package's power/QR basis update and no new-science claim is made. Four 64x64 blocks per hidden 128x128 matrix keep the decomposition native on MPS; global cross-block correlations are not represented. Auxiliary AdaBelief attribution/licence remains unchanged. Rotating coordinate preconditioning differs substantively from earlier diagonal/factored scales and Muon singular-direction updates, not just a scalar setting.

## Hypothesis and proposed change

Hypothesis: adapting hidden updates in correlated, periodically refreshed coordinates improves the IC/physics balance beyond Trial 006. Replace the hidden optimiser by BlockRotatedAdamSOAP(lr=0.001,betas=(0.9,0.99),frequency=50,eps=1e-8,block_size=64), no decay. For each tile gradient G, update L<-0.99L+0.01GG^T and R<-0.99R+0.01G^TG. At step 1 and every 50 steps, obtain eigenvectors from each symmetrised covariance plus (1e-6*trace/n+1e-12)*I. Keep first moments in original tile coordinates; project the gradient and first moment, maintain bias-corrected elementwise second moments in the current basis, then rotate the Adam update back. On refresh, approximate new diagonal variances by (Qnew_L^T Qold_L)^2 * V * (Qold_R^T Qnew_R)^2, where squares are elementwise; no full covariance transport is claimed. Synthetic identity/permutation transport, nonnegative variance, CPU tile-state and MPS native-block refresh/orthogonality checks passed. A 128x128 hardware-only check revealed library CPU fallback, so block size 64 was chosen before PRE or any PINN fit; native 64x64 tests showed no fallback warnings. All state remains float32 on MPS for these decompositions. Risks: block bias, approximate variance transport, unstable basis changes or excessive decomposition overhead.

## Training objective and setup

Fresh unchanged P sine model, seven Linear layers width 128, three spatial harmonics, 85765 parameters, Xavier/bias 0.01, startup_dt=0.05, density rho0*exp(clamp(max(t-0.05,0)*raw_rho,-4,4)). Objective = continuity + momentum_x + momentum_y + momentum_z + Poisson + IC_x + IC_y + IC_z, mean squared components weighted 1; frozen scorer remains unchanged. Initial 80% of 750 seconds: twenty hidden 64x64 SOAP-style tiles (covering 81920 matrix parameters); 3845 auxiliary input/output/bias parameters use unchanged UnrectifiedAdaBelief(lr=0.001,betas=(0.9,0.999),eps=1e-12). Both partitions consume the same backward pass after clearing all model gradients. Initial batches 1024 PDE/1024 IC with replacement, a control choice, not a total cap. Final phase caches all 100000 PDE and 75000 IC points by one cycle, with 25 exact-weight microbatches up to 4096 PDE/3072 IC. Every complete gradient and line-search value reuses all fixed points. Preserve PR+ conjugacy/descent restart, four Armijo trials c1=1e-4 with halving, alpha seed rules, >12-second iteration reserve, four-second chunk/eight-second proposal checks and rollback on deadline. No extra coordinates, perturbation, validation access or references. Count sampling draws, repeated evaluations, CG attempts/accepted steps/line trials/restarts/nonfinite proposals; return both initial states and CG state and record history. Eigensolver overhead is inside the same time budget. Only the locked owner runner checkpoints and scores; no PINN fit for this ID ran before PRE completion.

## Expected outcome

Expect total L_val below Trial 006's 0.1690991738, possibly recovering part of its IC MSE increase while retaining low physics. The method can instead lose throughput or degrade both terms; an individual IC or PDE improvement cannot override a higher total. Read all PDE windows/components, IC and density/mass/periodicity diagnostics, timing, actual update/exposure counts, histories and run.log, including any backend warnings or failures. The small synthetic tests verify implementation/hardware capability, not scientific performance. Selection uses only finite total L_val, with no IC, density, mass or periodicity gate. Record execution failures without ID reruns; no reference-trajectory, statistical-significance or exact-published-implementation claim follows from this one fit.

## Observed results

Completed normally, return code 0. L_val 0.172555641064, physics 0.086355945170, IC relative MSE 0.086199695894, IC L2 0.293597847223. 85765 parameters, 738.602450 actual seconds. 26262 initial updates, 112 CG attempts/107 accepted, 175 line values, 17 restarts, zero nonfinite proposals. All 287 full-pool evaluations reconcile exactly: 55592288 PDE / 48417288 IC evaluations, 26992288 PDE / 26967288 IC draws and 33437 physics calls. No partial evaluation needed for counts. All required files/diagnostics read; run.log contains no backend warning or execution error. Full records follow.

```json
{
  "metrics": {
    "L_val": 0.1725556410640201,
    "physics_weighted": 0.08635594516987455,
    "ic_relative_l2": 0.29359784722328186,
    "ic_relative_mse": 0.08619969589414556,
    "windows": {
      "early": {
        "continuity": 0.2019969282172333,
        "momentum": 0.028885371206611554,
        "poisson": 0.011053710725756753,
        "total": 0.24193601014960162
      },
      "middle": {
        "continuity": 0.014610137192945545,
        "momentum": 0.013606425908595062,
        "poisson": 0.006575504071770569,
        "total": 0.034792067173311174
      },
      "late": {
        "continuity": 0.021114705455981445,
        "momentum": 0.01789933764663313,
        "poisson": 0.016048202873307174,
        "total": 0.05506224597592175
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9939666986465454,
        "0.5": 0.987844705581665,
        "0.8": 0.9860644936561584
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.00603330135345459,
        "0.5": -0.012155294418334961,
        "0.8": -0.013935506343841553
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.11321068555116653,
        "0.5": 0.34243229031562805,
        "0.8": 0.6015152335166931
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2709052562713623,
        "0.5": 2.0171642303466797,
        "0.8": 3.1590018272399902
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.5347554683685303,
      "rho0_max_abs_err": 0.0,
      "periodic_max_abs_err": 2.3543834686279297e-06
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
    "training_seconds": 738.6024502500077,
    "optimizer_steps": 26374,
    "physics_calls": 33437,
    "pde_training_evaluations": 55592288,
    "ic_training_evaluations": 48417288,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 8169,
      "loss": 0.4466339349746704,
      "elapsed_seconds": 187.51362487499136,
      "note": "BlockSOAP/AdaBelief before full PR+; PDE_eval=8365056; IC_eval=8365056"
    },
    {
      "step": 16350,
      "loss": 0.43320178985595703,
      "elapsed_seconds": 375.04295441601425,
      "note": "BlockSOAP/AdaBelief before full PR+; PDE_eval=16742400; IC_eval=16742400"
    },
    {
      "step": 24604,
      "loss": 0.4310026466846466,
      "elapsed_seconds": 562.5156763750128,
      "note": "BlockSOAP/AdaBelief before full PR+; PDE_eval=25194496; IC_eval=25194496"
    },
    {
      "step": 26374,
      "loss": 0.36668505799025297,
      "elapsed_seconds": 738.6023440409917,
      "note": "final full PR+; PDE_eval=55592288; IC_eval=48417288; PDE_draws=26992288; IC_draws=26967288; cg=112; accepted=107; full=100000/75000; micro=4096; lines=175; nf=0; restarts=17"
    }
  ]
}
```

## Decision and interpretation

The net-improvement hypothesis is not supported. L_val rose from Trial 006's 0.1690991738 to 0.1725556411, by 0.0034564672 (about 2.04%). IC MSE improved 0.0113816901 but physics worsened 0.0148381574; all three physics totals increased. The lowest IC error among these recent methods does not override the higher total, and no IC or physical diagnostic gate was applied. The finite result improves P but does not displace Trial 006 or Trial 005. The initial phase made 26262 versus the parent's 28908 updates, so decomposition overhead, block approximation and variance transport are inseparable parts of this matched-time configuration. A single fit cannot reject SOAP generally or validate the exact published implementation. The preflight-driven 64x64 adaptation ran without fallback warnings; preserve the locked source and complete record. Next test a distinct covariance inverse-root preconditioner with scalar Adam-norm grafting on the same hidden blocks, retaining Trial 006 as source parent. No trained-state reuse, data/engine changes, statistical-significance claim or numerical-reference feedback.
