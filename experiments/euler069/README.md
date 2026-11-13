# Historical Euler–Poisson Trial 069

This is the original 75-trial research line in `codex_iitr_3d/main`, not the newer 60-trial campaign. The comparison baseline P is an equal-budget locally trained paper-style method, not a published checkpoint or independently exact reproduction of its published accuracy.

After selection, both frozen methods were fitted from fresh weights for approximately 1,800 seconds on three supersonic physical seeds 419, 733, 947 (amplitude a=1.1). Each is one training fit, not multiple RNG replications. The evaluated interval is [0,0.8].

For t=0.8 and all 256³ cell centres, δρ=log₂(ρ_PINN/ρ_Athena), with RMSδρ=sqrt(mean(δρ²)). Trial 069's supersonic mean is approximately 0.3957 and P's 0.4799. The reported reduction is the ratio of the means, about 17.5%, rather than a generic density percentage error or relative L2 reduction. `evidence/` retains all three cases' exact metrics, full-volume records and run metadata.

The fixed reference-free eligibility condition IC relative L2≤0.25 is failed by Trial 069 on seed 733 (≈0.2731); it passes seeds 419 and 947. P fails that gate on all three supersonic transfer cases. These failures remain visible and do not erase the measured numerical comparisons.

Athena++ 128³ and 256³ comparisons are grid sensitive; neither is established converged. Density/speed pictures display sampled faces or slices, while `full_volume_256.json` visits the full native grid. Do not confuse sampled velocity errors with full-volume density aggregation. The original longer-budget seed-419 Trial 069 checkpoint used in newer illustrative plots belongs to this historical campaign; it is not a Trial 056 fit.
