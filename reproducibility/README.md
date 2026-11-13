# Reproduce the evidence audit

## Lightweight checks — no training

From this repository root, Python 3.10+ and the standard library suffice:

```bash
python3 reproducibility/verify.py
```

This checks every imported artifact's SHA-256, curated Markdown/image paths, mean/SD arithmetic, Sitnikov per-case aggregation, historical Euler transfer aggregation, six new Euler full-grid results and finalist selection. Expected output is saved in [verification_results.json](../reports/verification_results.json). The script does not execute the historical trainers, invoke agents or access protected reference arrays.

For the original implementation history, use [sources.json](sources.json) and [the source map](../reports/SOURCE_MAP.md). Upstream links pin exact commits. [provenance.json](provenance.json) records original paths, bytes and hashes for copied files. Local-only KdV artifacts deliberately have no invented GitHub source URL; their reviewed copies and final checkpoints are available in this repository.

## Independently score the three KdV final checkpoints

Optional dependencies: NumPy, SciPy and PyTorch. Source runs used PyTorch 2.14.1/MPS; CPU inference can differ slightly. Obtain the original `kdv.mat` from the source project's protected evaluation/data path, subject to its dataset rights and access policy. Required SHA-256 is `0df03aee69597c8913f7120324303f663db617be3789b9ff35beb29303b1c087`.

```bash
python3 reproducibility/audit_kdv_checkpoints.py --reference /absolute/path/to/kdv.mat
```

This performs inference only, on all 201×512 pairs, for the three included final checkpoints. It checks the checkpoint hashes, source hash, grid, optimiser step counters and relative L2. It does not replace the saved official MPS metrics. [The curation-time audit](../experiments/kdv/evidence/corrected_three_seeds/curation_checkpoint_verification.json) additionally records direct comparison of the saved prediction arrays with the original reference; those combined reference arrays are omitted pending dataset-rights review.

Checkpoint deserialization uses `weights_only=True` and a small explicit allowlist for saved NumPy RNG/version metadata. The code first verifies expected file hashes. Do not substitute arbitrary checkpoints for these audited files.

## Optional KdV training reproduction

These commands are instructions for future reproduction, **not steps executed to assemble this repository**. Budget: approximately 2.4–2.5 hours per 200k fit on the original MPS setup, with no wall-clock cutoff. Other hardware changes timing and may change floating-point outcomes. Use fresh output folders. Keep references inaccessible during any new agent search.

1. Clone `akhilendra1811/agentic_pinns_KdV` into a new reproduction directory and check out the exact `75-exploratory-experiments` commit in `sources.json`. Do not run in an active research checkout.
2. Copy the contents of `reproducibility/kdv_overlay/` into that new checkout. This adds the local-only trainer and its exact frozen candidate/protocol; source paths are preserved.
3. Install the original `agent_workspace/requirements.txt` and the overlay provenance requirements in a dedicated environment. The source run configs record MPS/PyTorch 2.14.1, seed, source/reference/protocol hashes and all schedule parameters.
4. Make the required reference dataset available to this **post-selection** trainer. Source references are used only in diagnostics; they must not feed search or gradients.
5. From the new original-layout checkout, run each seed sequentially:

```bash
python3 comparison_study/runners/train_winner_b67_trapezoid.py --device mps --seed 99417 --output /absolute/path/to/fresh_99417
python3 comparison_study/runners/train_winner_b67_trapezoid.py --device mps --seed 99418 --output /absolute/path/to/fresh_99418
python3 comparison_study/runners/train_winner_b67_trapezoid.py --device mps --seed 99419 --output /absolute/path/to/fresh_99419
```

The trainer's default is 200,000 updates, no time cutoff, batch size 4,096, diagnostic interval 1,000, checkpoint interval 5,000. `finish_winner_b67_trapezoid.py` in the overlay performs original postprocessing. Its original main uses the default source output path; inspect its `main(out=..., console=...)` signature before using custom output folders. Do not assume the summary script automatically discovers arbitrary new directory names.

The method's trapezoidal integration followed benchmark diagnostics, so these reproductions remain evaluations of that benchmark-informed method. Fresh unused physical cases are needed for untouched-test claims.

## Sitnikov and Euler reproduction

Clone the respective original repositories at the pinned commits in `sources.json`, read their setup and rights documentation, and create dedicated environments. The curated frozen method snapshots are not standalone harness replacements.

- **Sitnikov:** `agent_workspace/experiment.py` exposes `inspect`, `smoke`, `run`, `select` and related commands. Original search: ten development IVPs, 90-second cap per case. The owner-only command from source root is `python3 protected_evaluation/evaluate.py --workspace agent_workspace`. It trains fresh held-out weights and generates DOP853 trajectories; it is not a lightweight audit. Keep `protected_evaluation` outside the agent's permitted filesystem during search, as the original README requires.
- **Historical Euler 069:** `agent_workspace/extra_seeds_after_experimentation/run_all.py` and `RESULTS.md` define the five physical transfer cases and local P comparison; Athena++ must be built and numerical references generated or obtained with matching provenance. This is substantial compute, not a verifier command. Do not confuse historical and new IC eligibility policies.
- **New Euler 056:** read `campaigns/supersonic_novelty60/RUN_OVERVIEW.md`, the campaign's locked `engine/`, and `agent_workspace/owner_evaluation/run.py`. Use frozen selected method, not the final attempted live `candidate.py`. Review the runner before use: its plan contains cancelled reused-case jobs. Reproduction must deliberately request the completed six-fit 104729/823001–823003 contract rather than interpret all planned jobs as completed. Numerical metrics require the full 256³ reference, not the displayed xy slices.

Exact access-control separation is an external responsibility: a folder named “protected” does not itself prevent an agent reading it. This curated collection contains post-selection evaluation records and should not be mounted into a supposedly blinded future agent search.

## Omitted reference/data artifacts

Third-party `kdv.mat`, native Athena VTK/restart/IC binaries, full-volume NPZ arrays and intermediate checkpoints are not bundled. Original source manifests, hashes and local paths identify them, but some remain local-only and have no permanent hosted download. This limits full independent Euler/Sitnikov recomputation from this repository alone. Resolve dataset rights and artifact hosting before public release; no result has been silently replaced to conceal that limit.
