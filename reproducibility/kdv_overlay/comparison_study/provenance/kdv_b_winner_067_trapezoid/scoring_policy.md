# Two distinct decision criteria

## Hypothesis prioritization ONLY (never a leaderboard score)

For each proposed trial in `research_record.json`, record integer scores:

- **Novelty (0–3):** 0 = repeat/tuning; 1 = modest variant; 2 = substantive untested mechanism; 3 = distinct underexplored methodological family with a clear rationale.
- **Literature grounding (0–2):** 0 = no verified grounding; 1 = one relevant primary source; 2 = strong source plus checked implementation or mathematical argument.
- **Information gain (0–2):** 0 = redundant; 1 = useful comparison; 2 = a decisive test that could change the research direction.
- **Feasibility (0–2):** 0 = unlikely to work under the fixed derivative, step, hardware or time limits; 1 = significant risks addressed; 2 = realistic, reproducible within the fixed budget.

Total exploration priority is 0–9. This score rewards trying new ideas, not selecting a final model. Scores must be justified with actual evidence; do not invent literature, claims or method families. Prefer scientifically plausible proposals and preserve freedom to follow surprising results. The experiment runner records these fields but does not use them to select an incumbent or winner.

During trials 001–035, at least 15 distinct tests must be credited, with at least 5 activation-focused and 5 optimizer-focused. Only completed full three-case trials count toward the minimum quota. Every test should include a specific new mathematical or algorithmic mechanism, not merely another learning rate, weight decay, or a renamed old method. Methodologically unsound or incompatible ideas should be documented as screened out, not forced through training.

## Final winner selection ONLY

Use frozen validation: mean of full physics+IC validation losses across three development cases as the principal metric. Also consider the worst development case, strict IC/periodicity eligibility, reproducibility, numerical stability and parameter/computational efficiency. The full method is rerun independently per case. Use the **final weights**, not a cherry-picked checkpoint.

Novelty and literature citation scores have **zero coefficient** in final selection. Never look at test RMSE, relative L2 or numerical references while selecting a winner. If B cannot beat its frozen starting method under this criterion, retain the baseline.
