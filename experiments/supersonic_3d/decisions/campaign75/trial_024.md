# Trial 024

Research metadata (locked on preparation): parents=trial:23; kind=refinement; mechanism_id=frozen_ic_branch_evolution.

## Parent methods and evidence

Parent Trial 023 used a slowly adapting IC branch after 20% IC pretraining. It improved weighted physics from Trial 022's 0.71570144 to 0.09237855 and reduced t=0.8 mass drift, but IC L2 rose from 0.23181394 to 0.30172768, losing eligibility. Trial 022's frozen branch retained IC eligibility at a large physics cost.

## Novelty claim

Refinement of the two-branch initial-condition representation: increase the IC term during physics training to test whether it can hold the slow IC branch near its pretrained fit. Loss weighting is known; the campaign-specific test is its interaction with slow IC-branch adaptation.

## Hypothesis and proposed change

Hypothesis: raising the IC relative MSE coefficient from 16 to 64 while leaving Trial 023's architecture and optimizer unchanged will recover IC L2 <=0.25 with much lower weighted physics than the frozen Trial 022. The only functional source change is that coefficient.

## Training objective and setup

733192-parameter model with 128-wide four-block spatial IC branch and B-style 256-wide ten-block dynamic branch. First 20% of 750 seconds: IC relative MSE only, Adam 1e-3, 1024 IC samples. Remaining 80%: 3.5 continuity + 7.5 momentum + 2.5 Poisson + 64 IC relative MSE on 1024 fresh PDE and 1024 IC samples; Adam dynamic LR 1e-3 cosine to 1e-5, IC branch LR one tenth, gradient clipping 0.5. Fresh random weights.

## Expected outcome

Expect IC L2 below Trial 023's 0.30172768, ideally <=0.25, and weighted physics far below Trial 022's 0.71570144. Compare L_val, all three time windows, mass drift, density spread and physical checks. If the stronger IC term fails eligibility or recreates Trial 022's severe physics error, reject it.

## Observed results

L_val 0.32125230; weighted physics 0.25950807; IC relative L2 0.24848387 and MSE 0.06174423, eligible true. Early/middle/late physics totals 0.46861505/0.19537163/0.21434714. Early continuity/momentum 0.22697914/0.21816587, late Poisson 0.09110997. Physical checks passed, rho0 error 0, periodic error 3.22e-6. At t=0.8 mean density 0.92958927, mass drift -0.07041073, density std 0.53217816, p99 2.74563789. 733192 parameters, 22045 steps, 748.0646 training seconds.

## Decision and interpretation

The stronger IC term recovered eligibility while keeping weighted physics well below Trial 022 (0.25951 versus 0.71570). However it sacrificed much of Trial 023's physics gain (0.09238 to 0.25951), and L_val 0.32125 remains worse than eligible Trial 018's 0.21096. The trial establishes a tunable tradeoff rather than a superior candidate. A more selective treatment of IC and PDE gradients or a different representation is needed; do not promote this candidate now.
