# Quantitative claims audit — 13 November 2026

Verification levels: **metric arithmetic** checks original saved numbers and aggregation; **checkpoint inference** reloads weights and scores them without training; **independent training/reference replication** regenerates fits or references. This curation performed the first level for all main claims and the second level for the three local KdV runs. It performed no new training or numerical simulation.

| Application claim | Outcome | Traceable support and qualification |
|---|---|---|
| Sitnikov 43% position / 38% velocity reduction, ten cases | Supported as rounded mean-RMSE reductions | `experiments/sitnikov/evidence/benchmark_comparison.json`, held-out CSV and final summary. ≈43.33% / 38.37%; baseline ≈4.74 s vs winner ≈87.01 s/case. No matched-compute trajectory claim |
| KdV ≈1.8×10⁻⁴ over three runs; ≈2.4× below published 4.27×10⁻⁴ | Supported for the agent-discovered trapezoidal-quadrature follow-up | Local per-seed metrics, predictions and three final checkpoint reloads give mean 1.765196×10⁻⁴ ± sample SD 9.239126×10⁻⁶; published/mean≈2.419. Local files were untracked and absent from remote branches. Benchmark diagnostics informed the quadrature change; not untouched-holdout evidence |
| Historical supersonic 17.5% improvement over local published-method baseline, three physical seeds | Supported for full-volume density RMS log₂ ratio | `experiments/euler069/evidence/supersonic/seed_*/{trial_069,paper_P}/full_volume_256.json`. Ratio of three-seed means at t=.8, 256³; fresh ~30 min fits; seed 733 fails IC gate |
| New 60-trial research complete, Trial 056 chosen | Supported by closed-attempt and finalist records | 58 finite, 2 failed; six 1,800-second finalist/baseline fits; minimum finite total score. No old IC gate. Search-only winner 054 is not final winner 056 |
| New two-hour evaluation across three unseen physical seeds | Not supported | Completed: one physical seed 104729 × three training RNGs × two methods. Extra transfer pipeline cancelled. This wording must not appear |
| Three independent deployed specialist agents | Not established in code | LLM-led multi-role experiment loop and separate owner evaluation; no verified three-agent orchestrator or independently deployed critic |

## Do not combine these numbers

- KdV Trial 046's 200k result 6.47327×10⁻⁴ is a different source and schedule from the newer 067 trapezoidal result. Parent 067 with the prior quadrature has a separately archived 200k endpoint ≈2.05030×10⁻³.
- Three KdV development cases are not three random training seeds. The newer claim uses seeds 99417, 99418, 99419 on the cosine case.
- Sitnikov development loss, held-out in-interval RMSE and untrained extrapolation errors are distinct. Extrapolated velocity worsens relative to the short baseline.
- Euler density RMS log₂ ratio is not ordinary density relative L2, signed bias, a percentage density error or a plotted-slice metric.
- Historical 069's three physical transfer cases are not 056's three training RNGs on one IC. A 069 result on seed 419 cannot directly rank against 056 on 104729.
- New five-field records use one RNG and differ slightly from extended-summary metrics; original values are preserved. The three-RNG table uses extended full-grid outputs.

## Published comparator

The PirateNet relative-L2 endpoint 4.27×10⁻⁴ and PDE/IC are independently checked in [Wang et al., JMLR 2024, §5.2 / Table 3](https://www.jmlr.org/papers/volume25/24-0313/24-0313.pdf). The paper benchmark is context, not a matched hardware/FLOP comparison. No paper figures or vendor source were copied. The local 30-minute PirateNet port result must not be called the published paper result or assigned a speculative causal explanation without a controlled test.

Run `python3 reproducibility/verify.py` for an exact arithmetic report and provenance validation. See the independent KdV checkpoint audit JSON for device differences; official reported MPS errors were not replaced by CPU values.
