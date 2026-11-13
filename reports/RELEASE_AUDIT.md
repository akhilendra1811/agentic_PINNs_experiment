# Inclusion, verification and release audit

## Included

The Euler–Poisson collection covers supersonic flow only: historical physical seeds 419/733/947 and the separate new Trial 056 campaign.

- Accessible main research narrative, explicit three-role framework status, scientific problems, comparison contracts and failure cases.
- Separate Sitnikov, historical cosine/exploratory/soliton KdV, historical Euler 069 and new Euler 056 experiment notes.
- Original selected figures, frozen method snapshots, selected decision logs, small quantitative tables and JSON metrics; all copied files have source paths and SHA-256 records.
- Locally discovered three-seed KdV evidence, final checkpoints only, source/protocol overlay and an independent curation-time CPU checkpoint audit. These were not in any current remote branch and are explicitly marked local in provenance.
- Reproduction commands, protected-evaluation access requirements, rights notes and a lightweight verifier.

`reproducibility/sources.json` pins every requested source branch. `reproducibility/provenance.json` enumerates every imported artifact. The new repository has a fresh history; source repository histories are not combined or modified.

## What was verified

Saved metric arithmetic supports the three application claims with the qualifications in `CLAIM_AUDIT.md`. Three KdV prediction arrays were independently scored against the original reference, then all three final checkpoints were reloaded on CPU for new inference; optimizer step counters and source/reference hashes were checked. No training or reference simulations were run. Sitnikov and Euler metrics were verified from saved files, not regenerated from checkpoints/full raw fields. The original PirateNet paper was checked directly for the benchmark value and problem definition.

All selected image files decode successfully and were visually inspected without editing. Markdown file/image targets are checked locally. Upstream GitHub file links are pinned to downloaded source commits and checked against their trees. Historical source documents may contain original local paths and wording; those are provenance records, not portable download links. The original source KdV aggregate README is retained verbatim with its referenced figures, not silently rewritten.

## Deliberately excluded

Private notes, fellowship forms, personal documents/photos, `document_update/`, expanded notes projects, ZIP archives, caches, credentials, API keys, environment files, native Athena VTK/restarts/IC binaries, large volume NPZs, the third-party KdV reference dataset, paper figure screenshots, vendor source and redundant/intermediate checkpoints. Only three necessary final KdV checkpoints are included. The original research checkout and its untracked evidence remain unchanged.

Oversized/unavailable raw references and historical checkpoints are identified through original manifests and source links, not represented as hosted here. Local absolute paths in original JSON identify historical inputs; they do not grant access or establish public availability. Dataset rights and permanent artifact hosting need owner review.

## Remaining issues before public release

1. Confirm licences/redistribution rights for original code adaptations, trained checkpoint publication and research-generated plots of third-party reference data. No blanket MIT/Apache licence has been invented. See `RIGHTS.md`.
2. Retain the short methods qualification that the newer KdV integration method follows benchmark diagnostics. Its valid three-run improvement is not untouched-holdout validation or equal-FLOP superiority over PirateNet.
3. Review any fellowship wording claiming a fully implemented three-agent system. Current archived implementation demonstrates an LLM-led loop and separate owner evaluation.
4. Choose permanent hosting and access instructions for raw numerical references and omitted artifacts, where redistribution is permitted; commit hashes alone do not make local-only files downloadable. The necessary local KdV final checkpoints and method overlay are preserved in this repository.
5. For stronger claims: fresh unused physical cases after method freeze, independently repeated searches, equal-compute held-out baselines, multiple physical/training seeds and grid-converged references. These are future experiments, not prerequisites that were secretly performed here.
6. Owner approval is required before changing visibility. The repository was created public by the owner and then made private before this upload; it remains private.

## Inconsistencies preserved rather than hidden

The root Euler README predates the new campaign; the new campaign overview and final selection take priority. The 60-search closure audit predates finalist completion and retains a historical “remaining” note. The soliton narrative mentions 039/075 while final selection chooses 022. The new Euler five-field and extended metrics differ slightly and use distinct aggregations. Original records and filenames remain unchanged; curated notes explain which is used.
