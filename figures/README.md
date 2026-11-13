# Selected figures

All selected PNGs are copied without pixel/axis manipulation. Source URLs and SHA-256 values are in [the provenance manifest](../reproducibility/provenance.json). The figures were decoded and visually inspected; full-size originals are retained.

| Figure | Scientific meaning and comparison limit |
|---|---|
| [sitnikov_position.png](sitnikov_position.png) | Trial 049 position vs DOP853; ten held-out IVPs, trained interval only. |
| [sitnikov_velocity.png](sitnikov_velocity.png) | Same cases and interval, velocity; not forecast performance. |
| [sitnikov_search.png](sitnikov_search.png) | 50-trial development physics-loss progression; includes failures and historical descriptive annotations. |
| [sitnikov_residual_error.png](sitnikov_residual_error.png) | Held-out physics loss versus trajectory RMSE; lower residual need not imply lower error. |
| [sitnikov_equal_compute.png](sitnikov_equal_compute.png) | Separate 87-second development follow-up; residuals, not equal-budget held-out trajectory errors. |
| [kdv_200k_solution_error.png](kdv_200k_solution_error.png) | Earlier Trial 046, 200k steps, cosine benchmark; relative L2 6.47e-4. |
| [kdv_equal_time.png](kdv_equal_time.png) | One seed, 30 minutes each; local PirateNet port, not published endpoint. |
| [kdv_equal_steps.png](kdv_equal_steps.png) | One seed, 51,573 updates each; different wall times and parameter counts. |
| [kdv067_three_seed_fields.png](kdv067_three_seed_fields.png) | Three individual 067 trapezoidal-method fits, one cosine case, 200k updates; full grid predictions/errors. |
| [kdv067_three_seed_curves.png](kdv067_three_seed_curves.png) | Mean/sample SD of individual diagnostic errors; final endpoint remains the scored model. |
| [kdv067_three_seed_final_errors.png](kdv067_three_seed_final_errors.png) | Individual-run errors and mean/sample SD; not ensemble error or confidence interval. |
| [euler056_density_potential.png](euler056_density_potential.png) | One RNG and IC, 2h checkpoint across time; xy slice at z=7, raw density and slice-centred potential. |
| [euler056_velocity.png](euler056_velocity.png) | Same 2h checkpoint/IC/RNG and xy slice; signed components, not log-ratios or full-volume metric. |

Archived KdV aggregate figures retain common field ranges and per-seed error scales. Density/potential 056 slice views do not establish full-volume accuracy; read the numerical tables separately. No new experimental figures or scientific data were fabricated for this repository.
