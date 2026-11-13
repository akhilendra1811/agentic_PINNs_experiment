# Trial 029 Decision Record: AdEMAMix Linear Alpha Mixture Warmup Schedule

## Hypothesis
In AdEMAMix with a fixed mixture weight $\alpha = 2.0$, the slow momentum buffer $\mathbf{m}_2$ ($\beta_3 = 0.999$, $\approx 1,000$-step memory) accumulates early stochastic gradients from initial collocation points before the physical wave profile has stabilized on the initial condition. Pagliardini et al. (Apple ML Research, arXiv:2409.03137) established that an $\alpha$-warmup schedule—linearly increasing $\alpha(t)$ from $0.0$ to $\alpha_{\max}$—significantly improves training stability by starting as standard AdamW ($\alpha=0$) and smoothly blending in the slow historical momentum buffer as confident trajectory direction develops. Aligning the $\alpha$-warmup duration with our 35% temporal curriculum expansion phase will provide pure local gradient descent during initial grounding and fully activate the deep historical momentum buffer for late-time multi-soliton interactions, lowering mean validation loss below our current 0.0007327 record.

## Proposed method change
In `candidate.py`:
1. Retain the winning targeted dual-harmonic SIREN architecture from Trial 027 ($k \in \{1, 2\}$, WIDTH=160, 8 layers, pure $\sin$ activations with additive residuals and unitary scaling).
2. Retain high-density Hamiltonian quadrature ($N_x=256$, $S=8$ time slices, $\lambda_{\mathrm{inv}} = 0.1$).
3. Retain 35% domain expansion temporal curriculum and cosine learning rate decay ($1.08 \times 10^{-3} \to 10^{-7}$).
4. In `train_model`, update the optimization loop to dynamically schedule `alpha`:
   - For `fraction < 0.35`: $\alpha(t) = 2.0 \times (\text{fraction} / 0.35)$
   - For `fraction >= 0.35`: $\alpha(t) = 2.0$
   - Update `param_group["alpha"] = alpha_curr` at each iteration alongside the learning rate.

## Training objective used
Augmented conservative physics-informed loss:
$$\mathcal{L} = \mathcal{L}_{\mathrm{PDE}} + \lambda_{\mathrm{IC}} \mathcal{L}_{\mathrm{IC}} + \lambda_{\mathrm{inv}} \mathcal{L}_{\mathrm{inv}}$$
with $\lambda_{\mathrm{IC}} = 1.0, \lambda_{\mathrm{inv}} = 0.1$, evaluated over $S=8$ time slices with $N_x=256$ spatial quadrature points per slice, alongside 4,096 fresh uniform collocation points and 512 IC points per step.

## Expected effect
Starting with $\alpha = 0$ avoids premature coupling to the uninitialized slow buffer during the first ~2,800 steps. As the domain expands and multi-soliton collisions begin, $\alpha$ smoothly rises to 2.0, providing persistent multi-thousand-step momentum that stabilizes the network across the second phase of training without transient shocks.

## Evidence from previous experiments
- In Trial 026, AdEMAMix with constant $\alpha = 2.0$ dropped mean loss by 30% to 0.0008031, demonstrating the immense value of slow historical momentum.
- In Trial 027, pairing AdEMAMix with $N_x = 256$ quadrature reached 0.0007327 across all cases.
- Literature shows that $\alpha$-warmup eliminates early training spikes and aligns momentum build-up with curriculum maturation.

## Literature and novelty assessment
- Category: optimizer
- Novelty credit: true
- Novelty key: ademamix_alpha_warmup_schedule
- Source: M. Pagliardini, P. Ablin, D. Grangier (Apple ML Research / EPFL, arXiv:2409.03137, Sep 2024), "The AdEMAMix Optimizer: Better, Faster, Older".
- Distinctness: Formulates scheduled slow-momentum activation dynamically synchronized with temporal domain expansion curricula in physics-informed neural networks.


## Observed results
- Validation loss:
  - Mean: 0.0006826 (**All-time best across all 29 trials**; previous best Trial 027: 0.0007327, baseline: 0.0030404; **4.45x reduction over baseline**)
  - dev_01: 3.3392e-07 (**All-time best across entire campaign**, dropping into sub-micro regime)
  - dev_02: 0.0019268 (**All-time best worst-case loss; breaks below 0.002 for the first time**, down from 0.0021435 in Trial 027 and baseline 0.007173; **3.72x reduction over baseline**)
  - dev_03: 0.0001208
- Eligibility: Fully eligible (IC = 0.0 <= 1e-3, BC total = 2.27e-6 <= 1e-3, params = 181,762 <= 250,000).
- Optimizer step throughput: Full speed maintained (~8,000 steps per case, 26.93 steps/sec).
- Comparison: Scheduling the AdEMAMix mixture parameter $\alpha$ to warm up linearly from 0.0 to 2.0 over the first 35% curriculum phase prevented early noisy gradients from polluting the slow momentum buffer. This allowed unhindered early initial condition convergence (yielding 3.34e-07 on `dev_01`) and provided stabilized long-term historical momentum that conquered the stiff two-soliton collision on `dev_02` (0.001927).

## Agent decision
Adopt Trial 029 as the **NEW ALL-TIME INCUMBENT WINNER**, decisively superseding Trial 027. Mark Trial 029 as completed and eligible, logging a breakthrough in optimizer curriculum scheduling.

## Reason for decision
Trial 029 establishes the strongest performance in the entire exploration research campaign:
1. Mean validation loss dropped to 0.0006826 (a 4.45x error reduction compared to baseline).
2. Worst-case validation loss broke through the 0.002 barrier to 0.0019268 (a 3.72x error reduction over baseline).
3. dev_01 set a new campaign record at 3.34e-07.
Aligning AdEMAMix momentum mixture warmup with the temporal domain curriculum combines pure early gradient descent for IC grounding with persistent multi-thousand-step momentum for long-horizon dispersive collisions.
