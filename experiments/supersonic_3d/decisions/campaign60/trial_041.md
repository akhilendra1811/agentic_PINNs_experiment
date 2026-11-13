# Trial 041

Research metadata (locked on preparation): research_area=combinations_refinements; parents=trial:28; kind=refinement; mechanism_id=zero_density_startup_hold.

## Parent methods and evidence

Trial 028 is the parent and current lowest finite score: L_val=0.16293784616066054, weighted physics=0.0682361379091252, IC relative MSE=0.09470170825153534. Early continuity contributes0.1791681846. Trial032 removed the hold as part of compatible jets and cut physics to0.0148955066, but its restricted initial Fourier velocity raised IC error. That does not isolate the hold. This trial makes a controlled refinement of028 instead. Fresh weights only.

## Novelty claim

Explicit refinement, not a new mechanism or publication novelty: change the density startup scalar from0.05 to0 and use the direct time gate t on the physical nonnegative-time domain. The old gate max(t-.05,0) forces uniform density throughout an initial interval; the fixed physics requires uniform density at t=0, not throughout that interval. No architecture, optimiser, loss-weight or sampling novelty is claimed. Frozen baselines and owner physics remain untouched.

## Hypothesis and proposed change

Primary hypothesis: allowing the density time derivative to learn immediately improves early continuity and the net IC/physics tradeoff. The only executable AST changes from028 are self.startup_dt=0.0 and dt=t; rho=rho0*exp(clamp(t*raw_rho,-4,4)). Retain every other executable node and identical fresh state dictionaries. A first disposable unit check found that clamp(t,min=0) gives zero derivative exactly at t=0 in this runtime, so that redundant clamp was removed before PRE/run. This was a pre-fit draft correction, not a failed numbered fit. CPU/native MPS tests then verified rho(0)=rho0, immediate positive-time evolution, correct first/second time derivatives for synthetic unsaturated logits, identical initial weights and148677parameters. No PDE fitting or new training coordinates in checks.

## Training objective and setup

Frozen score remains0.2early+0.3middle+0.5late+IC_relative_MSE. Entire028 trainer AST is identical: F=continuity+mom_x+mom_y+mom_z+poisson+ic_x+ic_y+ic_z absolute MSE, all coefficients1. Same seven-affine width128, six Snake activations, five original19-feature concatenations, bounded time-FiLM1->32->1536;148677parameters. Hidden94080weights use Adan lr.001, betas(.98,.92,.99),eps1e-8;54597auxiliary parameters use unrectified AdaBelief lr.001,betas(.9,.999),eps1e-12. First80% uses1024PDE/1024IC replacement-pool batches. Final20% uses canonical full-pool PR+/Armijo on100000PDE/75000IC via4096/3072microbatches and tail. No total points-per-step cap;8192 per context call.750seconds, fresh weights, physical seed82/training823001,MPS,750000parameter cap. Only frozen pools. Actual counts recorded after run.

## Expected outcome

Falsifiable target: L_val below0.16293784616066054 with lower early continuity and IC/late penalties small enough to preserve the gain. Removing the hold also changes the density training trajectory for all positive times; later residuals or IC error may worsen. Exponent saturation and shared-feature tradeoffs remain. Report all windows/components, throughput and density/mass/periodicity diagnostics without eligibility gates. One shared-seed fit does not establish statistical significance or numerical-reference accuracy.

## Observed results

The training process is absent after a session reset, and the retained status was stale running. No metrics, history, metadata or checkpoint were emitted. There is no usable score or measured training count/duration. Assigned budget was750seconds; source inspection/unit checks establish148677modelparameters, not a completed fit. The raw run.log contains only its starting marker.

Recovery evidence:
```json
{
  "observed_at": "2026-11-12T00:03:38.988260+00:00",
  "kind": "interrupted_worker_missing",
  "original_state": "running",
  "session_id": 47463,
  "session_observation": "write_stdin: Unknown process id47463",
  "process_observation": "Elevated ps inventory shows no experiment.py/_worker/training Python process; unrelated Python services only.",
  "artifacts": [
    "__pycache__",
    "candidate.py",
    "decision.md",
    "run.log",
    "status.json"
  ],
  "run_log_observation": "Only original starting marker; no completion or traceback.",
  "inference": "Training infrastructure/process was interrupted before it emitted a completed result. Exact cause,exit code,training duration,steps and evaluations unavailable.",
  "action": "Count041 as failed attempt; preserve source/PRE/rawlog; no rerun of ID041."
}
```

## Decision and interpretation

Execution/infrastructure interruption, not a scientific outcome or a demonstrated numerical failure. No performance conclusion about removing the density hold is supported. Count this attempt, preserve the frozen source and PRE, and do not rerun041. The best finite result remains028 at0.16293784616066054. Continue the amended60-trial campaign and, after all attempts, run exactly five finalist candidates plus P/B/W at1800seconds each as the user reiterated.
