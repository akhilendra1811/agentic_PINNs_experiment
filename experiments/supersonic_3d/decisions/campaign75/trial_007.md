# Trial 007

Research metadata (locked on preparation): parents=B,trial:6; kind=mechanism; mechanism_id=anchored_initial_velocity_decomposition.

## Parent methods and evidence

Combined conceptual parents B and Trial 006: B supplies the ResPINN backbone/trainer; Trial 006 supplies a separate spatial velocity branch. B IC L2 0.28621542 and Trial 006 IC L2 0.29105055 were ineligible. Trial 006 branch added to unconstrained raw velocity, so both routes competed at t=0. Trial 003 had best score 0.12452034 and IC L2 0.27059138 but worse physics.

## Novelty claim

New campaign mechanism: anchored initial-velocity decomposition. Unlike Trial 006 additive branch, the time-dependent velocity backbone is multiplied by t so its contribution is exactly zero at t=0; only the periodic spatial branch determines initial velocity. This is architectural initial-time enforcement of a decomposition, but not an exact hard IC constraint because the spatial branch must still learn sampled targets. No global originality claim.

## Hypothesis and proposed change

Hypothesis: removing competition between a spatial IC representation and dynamic backbone at t=0 improves validation IC fit and allows the dynamic term to focus on evolution. Expand Trial 006 spatial branch to width 256 (18-256-256-3), and output velocity = spatial_branch(periodic_x) + t*raw_velocity. Keep B density and potential formulas and B training.

## Training objective and setup

B ResPINN width 256, ten sine residual blocks, three spatial Fourier harmonics plus width-256 SiLU spatial velocity branch, fresh weights. Parameter count must remain <=750000. Density rho=exp(t*raw_rho); potential raw_phi; velocity spatial(x)+t*raw_velocity(x,t). Loss 3.5 continuity + 7.5 mean momentum + 2.5 Poisson + 16 IC relative MSE. Fresh PDE and IC batches 1024. Adam 1e-4 to 1e-3 warmup 5% of 750 s, cosine to 1e-5; gradient clip 0.5. Locked validation.

## Expected outcome

Expect IC L2 below Trial 006 0.29105055 and B 0.28621542, ideally <=0.25. Compare L_val against B 0.12733444 and Trial 003 0.12452034. Check early momentum and continuity because t-scaled velocity changes their derivatives; monitor late physics, density spread and mass drift. Physical positivity and periodicity must pass.

## Observed results

L_val 0.15390302; weighted physics 0.01946885 (lowest so far); IC relative L2 0.36665267 (ineligible). Early/middle/late totals 0.02879733/0.01378695/0.01914659. Early continuity/momentum/Poisson 0.00599791/0.01620618/0.00659324; middle 0.00332981/0.00671346/0.00374367; late 0.00709991/0.00757236/0.00447432. Physical checks passed, rho0 error 0, periodic max error 2.03e-6. At t=0.8 mean rho 0.99406433, mass drift -0.00593567, density std 0.66815186, p99 3.50875163. 735752 parameters (under cap), 5438 steps, 748.061 s. Training loss 3.0243 at 187.6 s to 2.1669 at 748.1 s.

## Decision and interpretation

The IC hypothesis is rejected: IC L2 worsened to 0.36665 versus B 0.28622 and Trial 006 0.29105, so the model is far from eligibility. However, the architecture substantially lowered all physics windows and improved mass conservation relative to B. This appears to expose a strong physics/IC compromise, potentially a low-residual solution inconsistent with the turbulent initial field. The exact cause is uncertain from reference-free metrics. Do not select as a finalist while ineligible. A follow-up combining the anchored decomposition with IC-first optimisation is scientifically motivated, but must test whether physics remains good after IC fit improves.
