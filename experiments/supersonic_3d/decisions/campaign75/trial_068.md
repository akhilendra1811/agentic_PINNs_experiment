# Trial 068

Research metadata (locked on preparation): parents=trial:57,trial:66; kind=refinement; mechanism_id=stronger_poisson_coupled_curriculum.

## Parent methods and evidence

Trial 057 at Poisson coefficient 5 has eligible L_val 0.15052786, physics 0.09003139, IC L2 0.24596031. Trial 066 at coefficient 6 improved to L_val 0.14634504, physics 0.08557238, IC L2 0.24652110. Trial 067 at coefficient 7 scored 0.14728625. The optimum in this small range may lie between 5 and 6.

## Novelty claim

Refinement of stronger-Poisson coupled curriculum: interpolate final Poisson coefficient to 5.5. This is scalar tuning of established PINN equation weighting, not publication novelty.

## Hypothesis and proposed change

Hypothesis: coefficient 5.5 retains the Poisson benefit of Trial 066 with slightly better IC fit and yields eligible L_val <0.14634504. Starting from Trial 066, change only the Poisson coefficient from 6.0 to 5.5.

## Training objective and setup

ResPINN width 256, ten 1.5-scaled sine residual blocks, three spatial harmonics, 664325 parameters; positive density rho0*exp(clamp(t*raw_rho,-4,4)). Fresh 750-second training. First 20% IC relative MSE only; afterward loss b(f)*(3.5 continuity+7.5 momentum)+5.5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, b full at f=0.40 and b_P full at f=0.25. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5; clip norm 0.5.

## Expected outcome

Expect IC L2 below Trial 066's 0.24652110, late Poisson near or below 0.01017608, and eligible L_val <0.14634504. Examine temporal residuals, mass drift, density spread, physical checks, steps and runtime. A worse score rejects the interpolation as leader.

## Observed results

L_val 0.15240351; weighted physics 0.09196804; IC relative L2 0.24583626 and MSE 0.06043547, eligible true. Early/middle/late physics totals 0.19528369/0.08944075/0.05215816; late Poisson 0.01502777. Physical checks passed, rho0 error 0, periodic error 2.95e-6. At t=0.8 mean density 0.97577256, mass drift -0.02422744, density std 0.63025856, p99 3.22221923. 664325 parameters, 21088 steps, 748.1002 training seconds.

## Decision and interpretation

Poisson coefficient 5.5 improved IC L2 slightly against Trial 066 (0.24583626 versus 0.24652110) but lost its Poisson and physics benefit: late Poisson 0.01502777 versus 0.01017608, weighted physics 0.09196804 versus 0.08557238. L_val 0.15240351 is above Trial 066's 0.14634504. The score hypothesis failed; reject as leader. This interpolation did not show a smooth score response under fixed-time optimization.
