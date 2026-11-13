# New 60-trial Euler–Poisson campaign: Trial 056

Source: `codex_iitr_3d/codex/supersonic60-twohour-plots-20261113`, under `campaigns/supersonic_novelty60/`. The old root README still describes an earlier experiment; the campaign overview, closure and final-selection records define this experiment.

## Search and selection

Sixty attempts closed: 58 finite and failures 015/041. Search uses physical seed 82, training RNG 823001, a 750-second fit budget, fixed pools and fixed residual scoring. At the short budget Trial 054 scores best; the saved `search_closure_audit.json` is a pre-finalist checkpoint and its “remaining” field is historical.

After search, three candidate finalists 054/053/056 and fresh baselines P/B/W each receive 1,800 seconds. The six scores are P 0.19061710, B 0.55461895, W 1.06084077, 054 0.10604834, 053 0.10566741, 056 0.10566120. The minimum finite total score selects 056. The ≈6.21×10⁻⁶ gap to 053 is not statistical evidence of superiority. No earlier 0.25 IC eligibility gate is imposed: selected 056 has IC relative L2≈0.28452 at this stage.

The source selection has `trial: null` and `selected_method: trial_056`; the latter is authoritative. We preserve the JSON unchanged. The immutable selected source hash is c17b898b69142be7552e5a23cd44d508f14ef102664878cfb419910fdedb9aea.

## Completed post-selection two-hour fits

One physical seed 104729, paired training RNGs 823001/823002/823003, methods P and 056, 7,200 seconds each: six completed fits, twelve hours of prior neural training. The seed differs from known development and prior transfer cases but is not claimed globally unseen. No new training was conducted for this curated repository.

All errors below visit 16,777,216 cell centres of the same Athena++ 256³ reference at t=0.8. Mean ± sample SD across three training RNGs:

| Metric | Trial 056 | Local P |
|---|---:|---:|
| Density relative L2 | 0.34196878 ± 0.00035263 | 0.37281346 ± 0.00226713 |
| Density RMS log₂ ratio | 0.41136184 ± 0.00130544 | 0.46541947 ± 0.00111805 |
| Velocity-vector relative L2 | 0.26796783 ± 0.00051144 | 0.29767638 ± 0.00058410 |

These are training-seed variations conditional on one physical IC, not population generalisation. `extended_summary.json` also includes top/bottom 0.1% density/speed groups (16,778 cells/group), chosen using the reference fields, not the predictions. Groups can overlap. Global means do not establish accurate extremes or shocks.

`five_field_errors.json` is a separate one-RNG, five-field view, and includes historical 069 on physical seed 419. Do not rank 056 versus 069 across different ICs. It also differs slightly from extended-summary reductions: for RNG 823001, density RMS log₂ values are about 0.409914/0.466177 there, versus 0.409918/0.466180 in the extended outputs. Preserve both; use the extended outputs for the three-RNG table. Full-volume potential is gauge-aligned; signed components and potential do not have meaningful log-ratio metrics across sign changes.

## Pictures and cancellations

The selected heatmaps show a 256×256 xy plane at z=7 over five physical times, using one fixed final two-hour checkpoint per model. Potential is slice-mean-centred for display; numerical potential evaluation removes a volume mean. A picture of that plane is not a full-volume assessment.

The planned extra 30-minute reused-case stage was cancelled after P/419 completed and during W/419. The runner/README still contain plans for additional fits; those plans are not completed results. No three-physical-seed Trial 056 transfer conclusion is claimed.
