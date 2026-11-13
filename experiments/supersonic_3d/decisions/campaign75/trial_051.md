# Trial 051

Research metadata (locked on preparation): parents=trial:48,trial:50; kind=refinement; mechanism_id=accelerated_poisson_curriculum.

## Parent methods and evidence

Parents Trial 048 and Trial 050. Trial 048 reached full Poisson weight at f=0.25 and final IC weight 30, giving low L_val 0.14355815 but ineligible IC L2 0.25123018. Trial 050 kept that fast Poisson ramp and raised final IC weight to 33, crossing eligibility at IC L2 0.24891695 with L_val 0.15160360. Trial 030's slower Poisson ramp to f=0.40 remains slightly better by eligible score, L_val 0.15077613, but has narrower IC margin.

## Novelty claim

Refinement of the accelerated Poisson curriculum: interpolate its ramp endpoint between f=0.25 and the original f=0.40 while holding IC weight 33. Curriculum timing is a known method choice, not publication novelty.

## Hypothesis and proposed change

Hypothesis: reaching full Poisson weight at f=0.30 will retain Trial 050's IC eligibility while reducing its small score gap to Trial 030. Starting from Trial 050, change only the Poisson ramp denominator from 0.05 to 0.10, making b_P=min(1,(f-0.20)/0.10).

## Training objective and setup

B ResPINN, 664325 parameters, 256 width, ten sine residual blocks, three spatial harmonics. Fresh 750-second training. First 20% IC relative MSE only. From f=0.20 onward, loss is b(f)*(3.5 continuity+7.5 momentum)+5*b_P(f)*Poisson+(1+32*b(f))*IC relative MSE, where b reaches 1 by f=0.40 and b_P by f=0.30. Physics batch 1024 split 256 early/256 middle/512 late; IC batch 1024. Adam warmup 1e-4 to 1e-3 then cosine to 1e-5, clipping 0.5.

## Expected outcome

Expect IC L2 <=0.25 and L_val <Trial 030's 0.15077613, retaining late Poisson close to Trial 050's 0.01416380. Check all temporal residuals, mass drift, density spread, physical checks, steps and runtime. If ramp timing merely trades late Poisson for IC, retain Trial 050 or 030.

## Observed results

L_val 0.15605556; weighted physics 0.09474641; IC relative L2 0.24760684 and MSE 0.06130915, eligible true. Early/middle/late physics totals 0.19675067/0.09100377/0.05619029; late Poisson 0.01954494. Physical checks passed, rho0 error 0, periodic error 5.01e-6. At t=0.8 mean density 0.97460938, mass drift -0.02539063, density std 0.63587832, p99 3.28792143. 664325 parameters, 23574 steps, 748.0754 training seconds.

## Decision and interpretation

The gentler Poisson ramp improved IC L2 from Trial 050's 0.24891695 to 0.24760684 but raised late Poisson from 0.01416380 to 0.01954494 and L_val from 0.15160 to 0.15606. It did not beat Trial 030's 0.15078 eligible score. Trial 050 offers better physics with a somewhat narrower IC margin; Trial 051 is another eligible robustness alternative but not a priority finalist.
