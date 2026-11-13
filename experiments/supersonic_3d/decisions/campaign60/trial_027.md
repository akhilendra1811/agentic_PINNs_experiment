# Trial 027

Research metadata (locked on preparation): research_area=activation_representation; parents=trial:25; kind=mechanism; mechanism_id=smooth_temporal_partition_experts.

## Parent methods and evidence

Closed025 source remains lowest finite total.1637461232,physics.0673056881,IC.0964404352. LearnedChebyshev026 total.1659302089 improved IC but worsened physics and reduced throughput. Test a different temporal representation:separate full space-time experts blended smoothly,without a low-rank raw-time constraint or per-layer conditioner. Main128-wide network source/seed map retained,but full mixed initial map is different. Fresh weights/state,no checkpoint reuse.

## Novelty claim

Representation mechanism normalized-Gaussian temporal partition-of-unity neural experts. Credit overlapping neural-basis precedent Moseley,Markham,Nissen-Meyer,FBPINNs,https://arxiv.org/html/2107.07871 Section4.2 equation13. Local design uses globally supported normalizedGaussian windows and all experts at every fixed-pool point,not compact sigmoid-window FBPINN,localcoordinate normalisation,parallel scheduling or new subdomain samples. Known mixture/domain-localisation idea,no scientific novelty. Unlike023 coarse/fine input bands,all experts have same harmonic inputs but specialise by time;unlike025 FiLM it blends independent raw networks.

## Hypothesis and proposed change

Hypothesis:overlapping temporal experts reduce conflicting early/late representation demands enough to lower total below025. Remove timeconditioner/FiLM,retain main19->128,five128->128,128->5 withsix Snake functions. Add two19->64,five64->64,64->5 experts,eachsix Snake. Same19axis Fourier+time features to all. Fixedcenters(.1,.35,.65),width.2;w_i(t)=softmax_i(-.5*((t-center_i)/.2)^2). Raw=sum_i w_i*raw_i,then shared parent density transform. AllLinear Xavier/bias.01;main initial tensors exactly match parent same seed,though mixed initial prediction differs.130575params. Apply existing Adan rule to all15 hidden matrices(122880params),auxiliary AdaBelief to7695remaining;this necessary partition extension and FiLM removal are explicit. Optimiser/PR+ AST unchanged;entire trainer equal except all-expert hidden collection. CPU/native MPS positive weights/partition unity,analytic first/second/third gate derivatives,finite all-expert parameter gradients,15hidden partition and mainseed check passed on synthetic features. No PDE coordinates/fitting. Risks:Gaussian-tail coupling/no strict localisation,window derivative stiffness,three-network overhead,smaller middle/late capacity and changed optimiser allocation/RNG stream confound pure gating causality.

## Training objective and setup

Fresh three temporal experts above,widths128/64/64,130575parameters,originalthree axis harmonics+time,SixSnake perexpert,shared density rho0*exp(clamp(max(t-.05,0)*mixed_raw_rho,-4,4)). F=continuity+momentum_x+momentum_y+momentum_z+Poisson+IC_x+IC_y+IC_z,absolute MSE weights1. First80% of750s:all15expert hidden matrices Adan(lr.001,betas .98/.92/.99,eps1e-8),allinput/outputweights+biases UnrectifiedAdaBelief(lr.001,betas .9/.999,eps1e-12),no decay/clipping. Initial1024PDE/1024IC pool replacement,a choice not total cap;all experts evaluated on same points. Final all100000PDE/75000IC cycle cache once,25 exact separately weighted microbatches max4096PDE/3072IC per complete gradient/value. Same PR+ restarts,4-trial Armijo c1=1e-4/halving,alpha seed rules,>12s attempt/4s chunk/8s proposal checks and rollback. All overhead within750s;return states/log draws,evaluations,steps,CG/search/restarts/nonfinite counts. No new/perturbed coordinates,validation/reference access or post-checkpoint updates.

## Expected outcome

Expect finite L_val below.1637461232,ideally lower early physics while preserving IC/late enough for net gain. Higher total falsifies net hypothesis irrespective of diagnostics/throughput. Read all actual metrics/windows/IC/density/mass/periodicity/history/metadata/log,reconcile counts. Finite total alone ranks,no eligibility gates. One fresh matched-time local temporal-expert fit cannot establish significance,general FBPINN/mixture superiority or numerical-reference accuracy;retain failures,no ID reruns.

## Observed results

All actual metrics,metadata,history,log and diagnostics read.14033 initial updates+46 CG attempts,44 accepted,77 line values,7 restarts,0 nonfinite proposals.123 complete full-pool evaluations exactly reconcile,no partial work or warning/execution failure. Full canonical records:

```json
{
  "metrics": {
    "L_val": 0.1801340132213194,
    "physics_weighted": 0.08174053912388367,
    "ic_relative_l2": 0.3136773407459259,
    "ic_relative_mse": 0.0983934740974357,
    "windows": {
      "early": {
        "continuity": 0.1834279107184176,
        "momentum": 0.05562428055835674,
        "poisson": 0.0021378257537520303,
        "total": 0.24119001703052637
      },
      "middle": {
        "continuity": 0.014454631501048747,
        "momentum": 0.022774716782867337,
        "poisson": 0.006697607449546827,
        "total": 0.04392695573346291
      },
      "late": {
        "continuity": 0.01626680224363268,
        "momentum": 0.016347682259934167,
        "poisson": 0.0080344134919122,
        "total": 0.04064889799547905
      }
    },
    "density_diagnostics": {
      "mean_density": {
        "0.0": 1.0,
        "0.2": 0.9921078681945801,
        "0.5": 0.9856961965560913,
        "0.8": 0.9836223721504211
      },
      "relative_mass_drift": {
        "0.0": 0.0,
        "0.2": -0.007892131805419922,
        "0.5": -0.014303803443908691,
        "0.8": -0.016377627849578857
      },
      "density_std": {
        "0.0": 0.0,
        "0.2": 0.10590110719203949,
        "0.5": 0.31504127383232117,
        "0.8": 0.5575275421142578
      },
      "density_p99": {
        "0.0": 1.0,
        "0.2": 1.2554166316986084,
        "0.5": 1.9108608961105347,
        "0.8": 2.9706671237945557
      },
      "grid": 32
    },
    "physical_checks": {
      "min_sampled_density": 0.26202449202537537,
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
    "params": 130575,
    "training_seconds": 739.9607435420039,
    "optimizer_steps": 14079,
    "physics_calls": 17108,
    "pde_training_evaluations": 26669792,
    "ic_training_evaluations": 23594792,
    "adaptive_probes": 0,
    "training_rng_seed": 823001,
    "startup_dt": 0.05,
    "torch_version": "2.15.0",
    "python_version": "3.13.16 (main, Oct 14 2026, 00:55:38) [Clang 23.1.3 ]",
    "host_os": "posix"
  },
  "history": [
    {
      "step": 4423,
      "loss": 0.5364594459533691,
      "elapsed_seconds": 187.51631420798367,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=4529152; IC_eval=4529152"
    },
    {
      "step": 8673,
      "loss": 0.5026528239250183,
      "elapsed_seconds": 375.03752516699024,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=8881152; IC_eval=8881152"
    },
    {
      "step": 13141,
      "loss": 0.4526122808456421,
      "elapsed_seconds": 562.5026662499877,
      "note": "Adan/AdaBelief before full PR+; PDE_eval=13456384; IC_eval=13456384"
    },
    {
      "step": 14079,
      "loss": 0.4305920172482729,
      "elapsed_seconds": 739.9603796249721,
      "note": "final full PR+; PDE_eval=26669792; IC_eval=23594792; PDE_draws=14469792; IC_draws=14444792; cg=46; accepted=44; full=100000/75000; micro=4096; lines=77; nf=0; restarts=7"
    }
  ]
}
```

## Decision and interpretation

Net hypothesis not supported:total rose0.0163878900 (10.01%) versus025,physics0.0144348511 and IC MSE0.0019530389 higher. All physics window totals worsen;early/middle momentum dominates the degradation.14033 initial updates/123 full evaluations reflect distinct expert overhead/allocation. No evidence isolates window derivatives,capacity allocation or FiLM removal. Retain finite result without diagnostic gates;no general temporal-mixture/FBPINN ranking or significance claim.
