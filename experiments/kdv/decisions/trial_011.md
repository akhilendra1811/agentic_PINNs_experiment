# Trial 011 Decision Record: Schedule-Free AdamW with Iterate Averaging

## Hypothesis
Replacing predetermined cosine learning rate decay with Schedule-Free AdamW (Defazio et al., 2024) will prevent premature learning rate decay, allowing continuous descent on late-emerging wave packet dynamics while online Polyak iterate averaging naturally filters out stochastic collocation noise.

## Proposed method change
Retain the top-performing SIREN sinusoidal architecture from Trial 004. In `train_model`, replace scheduled AdamW with `ScheduleFreeAdamW`:
$$v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$$
$$\hat{g}_t = \frac{g_t}{\sqrt{v_t} + \epsilon} + \lambda \theta_{t-1}$$
$$z_t = z_{t-1} - \eta \hat{g}_t$$
$$\theta_t = (1 - c_t) \theta_{t-1} + c_t z_t$$
where $c_t = \frac{1}{t+1}$, with constant base learning rate $\eta = 1.0\times 10^{-3}$, $\beta_2 = 0.99$, weight decay $\lambda = 5\times 10^{-5}$, and remove the cosine learning rate decay loop while preserving the linear temporal curriculum.

## Training objective used
Identical to baseline:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}}$$
with $\lambda_{\mathrm{IC}} = 1.0$, using 4,096 fresh uniform $(t, x)$ collocation points sampled dynamically each step, alongside 512 spatial IC points at $t=0$.

## Expected effect
In standard scheduled training, the learning rate drops to $10^{-7}$ during the final 65% of the budget. If the temporal curriculum is still introducing new time intervals $[0, 1.0]$, small learning rates cannot make meaningful parameter progress. Schedule-Free AdamW maintains active gradient updates throughout the entire 300 seconds, with iterate averaging finding flatter, more generalizable minima.

## Evidence from previous experiments
Trial 004 established the sinusoidal network as the best architecture (mean val 0.001260). However, examination of the training logs showed that the loss plateaued as the learning rate decayed past $t = 150\text{s}$. Schedule-Free optimization directly tests whether constant-rate iterate averaging can unlock further descent on multi-frequency cases.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: schedule_free_adamw
- Source: Defazio et al. (NeurIPS 2024), "The Road Less Scheduled", arXiv:2405.15682.
- Distinctness: Genuinely distinct optimization approach that eliminates the need for predetermined learning rate schedules (like cosine decay) by unifying momentum acceleration with online Polyak iterate averaging.

## Observed results
Trial 011 completed all three cases in 891.04 seconds (~8,500 steps per case).
- Mean validation loss: 0.0151959 (worse than Trial 004's 0.0012602)
- Case dev_01 validation: 0.0001928
- Case dev_02 validation: 0.0361070
- Case dev_03 validation: 0.0092879
- Eligibility: Fully eligible ($L_{\mathrm{IC}} = 0.0 \le 10^{-3}$, periodic mismatch $1.57\times 10^{-6} \le 10^{-3}$).
- Step throughput: ~28.6 steps/sec, maintaining high optimizer efficiency on MPS.

## Agent decision
Do not promote Trial 011. Retain Trial 004 as the active validation incumbent. Mark `schedule_free_adamw` as credited novelty in the optimizer category.

## Reason for decision
The experiment reveals an incompatibility between unweighted Polyak iterate averaging ($c_t = 1/(t+1)$) and progressive temporal curriculum training. In early training (first 35% of steps), the temporal domain is restricted to $[0, 0.05]$. Averaging early iterates into the final model weight sequence $\theta_t$ biases the network towards early-time dynamics, impeding subsequent adaptation as the domain expands to $t \in [0, 1.0]$. In contrast, scheduled cosine decay allows the parameters to track the changing curriculum freely before annealing into the final minimum.
