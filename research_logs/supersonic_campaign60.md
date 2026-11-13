# Internet use log

2026-11-10:

- Read all 75 prior numbered decision.md files through GitHub, under https://github.com/akhilendra1811/codex_iitr_3d/tree/main/agent_workspace/runs . Reference-free copy: prior_reference_free_decisions.md. No checkpoints or post-selection Athena++ outcomes accessed. Historical eligibility rules do not apply to this campaign.
- Searched PINN optimisation research. Primary source located: Rathore et al., Challenges in Training PINNs: A Loss Landscape Perspective, ICML 2024, https://proceedings.mlr.press/v235/rathore24a.html . Abstract discusses Adam/L-BFGS and NysNewton-CG for ill-conditioning; full method review remains pending.

- Opened the full Rathore et al. HTML: https://arxiv.org/html/2402.01868v2 . Motivation for a staged Adam/quasi-Newton experiment: residual-loss conditioning; this does not establish performance on 3D Euler–Poisson.
- Read SOAP method section: Vyas et al., https://arxiv.org/html/2409.11321v2 . Adam in a Kronecker preconditioner eigenbasis; periodic basis changes need second-moment transport. Potential implementation overhead must be included in the same wall-clock budget.
- Read primary abstracts for Lookahead (Zhang et al., https://arxiv.org/abs/1907.08610), stochastic weight averaging (Izmailov et al., https://arxiv.org/abs/1803.05407), Adan (Xie et al., https://arxiv.org/abs/2208.06677), AdaBelief (Zhuang et al., https://arxiv.org/abs/2010.07468), and Adafactor (Shazeer and Stern, https://arxiv.org/abs/1804.04235). These are known methods, not original campaign inventions.
- Consulted official installed-version PyTorch optimiser documentation: https://docs.pytorch.org/docs/2.15/generated/torch.optim.LBFGS.html , https://docs.pytorch.org/docs/2.15/generated/torch.optim.NAdam.html , https://docs.pytorch.org/docs/2.15/generated/torch.optim.RAdam.html .
- An attempted SOAP URL lookup at arXiv:2410.02446 resolved to an unrelated quantum-health review; discarded and not used as scientific evidence.

- Searched primary PINN methodology sources for later hypotheses: McClenny and Braga-Neto, self-adaptive point weights via minimax training, https://arxiv.org/abs/2009.04544 ; Wang, Teng and Perdikaris, gradient-statistic balancing, https://arxiv.org/abs/2001.04536 ; Wang et al., causal training, https://arxiv.org/abs/2203.07404 ; Gnanasambandam et al., self-scalable tanh, https://arxiv.org/abs/2204.12589 . Search/abstract-level review only at this stage; implementation must await full method review and the appropriate trial block.

- Read the gradient-conflict discussion in Wang et al., Gradient Alignment in Physics-informed Neural Networks: A Second-Order Optimization Perspective, https://arxiv.org/html/2502.00604v2 . It motivates comparing stochastic preconditioning against fixed-subset quasi-Newton finishing rather than assuming all curvature methods behave alike.
- Opened ConFIG and read the conflict-free direction and momentum sections: https://arxiv.org/html/2408.11104v2 . Also located MultiAdam, https://proceedings.mlr.press/v202/yao23c.html . Both are possible optimisation hypotheses distinct from the historical PCGrad experiment. No training or claim of faithful reproduction yet.
- Located primary Lion and SAM sources: https://arxiv.org/abs/2302.06675 and https://arxiv.org/abs/2010.01412 . Lion uses sign momentum; SAM perturbs weights, not coordinates. Their generalisation results on other tasks are not evidence of Euler–Poisson improvement.
- Read official Muon update and parameter restrictions: https://docs.pytorch.org/docs/2.15/generated/torch.optim.Muon.html . Installed torch.optim exposes Muon, Adafactor, RAdam, NAdam and LBFGS (verified signatures without executing training). A Muon hypothesis would use its matrix update with a separate bias optimiser and explicitly set weight decay, not accidentally inherit its nonzero default.
- Located separable PINN representation source: https://arxiv.org/abs/2306.15969 . Its original tensor-grid acceleration cannot be assumed for this campaign's random frozen point pools; any separable representation must work pointwise with the locked scorer.

- Located primary Shampoo source, Gupta, Koren and Singer, https://arxiv.org/abs/1802.09568 , and the RAdam source, Liu et al., https://arxiv.org/abs/1908.03265 . The reservoir in research_design.md distinguishes matrix preconditioning from diagonal variance rectification; specific implementations still require a documented PRE decision.

- Trial 002 draft: read the RAdam update equations in the installed-version official documentation (same URL above). The rectification factor and initial nonadaptive updates differ from Adam's rule; only this initial optimiser is changed in P, with its L-BFGS finish retained. No result is claimed before the recorded run.

- Read the upstream AdaBelief PyTorch implementation's moment update, bias correction, variance epsilon accumulation and rectification branches: https://github.com/juntang-zhuang/Adabelief-Optimizer/blob/update_0.2.0/pypi_packages/adabelief_pytorch0.2.1/adabelief_pytorch/AdaBelief.py . The repository uses the BSD 2-Clause licence. A future implementation must state whether rectification is disabled and specify epsilon explicitly; an unrectified belief-based update would be distinct from the RAdam draft. No third-party package installed and no additional training performed.

- Drafted a minimal unrectified AdaBelief variant in candidate.py, with the upstream BSD notice retained, beta=(0.9,0.999), epsilon=1e-12 accumulated into variance and added to the denominator, zero weight decay and no AMSGrad. This epsilon differs from the current package default and is explicitly chosen for damping. Two-step scalar-formula and zero-gradient CPU checks passed on two-element tensors. These are implementation unit checks, not PINN research fits; no field data or coordinates were used. P's model AST remains unchanged. Trial 003 has not yet been prepared or trained.

- Located the primary hard-constraint trial-solution source by Lagaris, Likas and Fotiadis, https://arxiv.org/abs/physics/9705023 (journal version 1998, DOI 10.1109/72.712178). Its abstract supports the established idea of embedding constraints in a trial solution. A separate Euler–Poisson initial-time cancellation was derived and symbolically checked locally; it is not attributed to that paper and has not been trained or scored.

- Subsequently Trial 003 was prepared and launched with the documented unrectified AdaBelief implementation and complete PRE sections, after Trial 002 was scored and closed. No further literature claims or unrecorded PINN fits were added.

- User-requested read-only W protocol investigation: fetched prior reference-free Trial 069 source, metrics, history and run_metadata; Trial 008 metrics; P/B benchmark metrics and run_metadata; public engine/core.py, engine/experiment.py and prepare_cases.py from https://github.com/akhilendra1811/codex_iitr_3d . No private validation arrays, checkpoints, protected evaluation outputs or Athena++ references accessed. Old W source equals the current W mirror after replacing its two `mode='fresh'` calls with `mode='pool'`. Governing residual implementation is byte-identical. W already used fresh initial weights, IC pretraining and the same declared training seed. Old W used CPU/PyTorch 2.14.1, 4930 physics calls; new W used MPS/PyTorch 2.15.0, 15731. IC pool changed 130000 to 75000, and validation sizes/coordinates changed. W physics loss rose 0.0788142814 to 0.5516820270 while IC MSE fell 0.0622452640 to 0.0493495093. Repeated finite-pool fitting with more updates is a leading hypothesis, not isolated causality. Old eligibility affected selection, not the arithmetic score; Trial 008's lower raw score was ineligible then. No experimental protocol changes were made in response.
- Read Lookahead Algorithm 1 and inner-state discussion in https://arxiv.org/html/1907.08610v2 for Trial 004. Implement k=5, alpha=0.5, preserve inner AdaBelief moments, and initialise the unchanged L-BFGS finish from the last completed slow state. Two synthetic CPU interpolation/reset checks passed; no unrecorded PINN fitting. The slow/fast mechanism is known work credited to Zhang et al.

- Trial 005: consulted official conjugate-gradient/Armijo documentation, https://docs.scipy.org/doc/scipy/reference/optimize.minimize-cg.html . Implemented a local restarted Polak–Ribiere-plus direction with bounded Armijo-only search, not SciPy's complete Wolfe method. It uses full fixed-pool gradients via exact microbatch weighting after the same fresh AdaBelief phase. Synthetic direction/restart and count/weight arithmetic checks passed, without PINN training. No novelty or convergence guarantee claimed. The PRE documents all choices and the limitations of finite-pool coverage.

- Trial 006: revisited official Muon documentation, https://docs.pytorch.org/docs/2.15/generated/torch.optim.Muon.html , and read installed torch/optim/_muon.py. inspect.getsource on the exported class was unavailable; reading the installed implementation resolved the update/dtype details without a research fit. The reference uses bfloat16 Newton–Schulz arithmetic; the local variant explicitly uses float32 and no weight decay. Five hidden square matrices use the momentum map, auxiliary parameters keep AdaBelief, and the full-pool PR+ finish is unchanged. Synthetic zero, scale, orthogonal-equivariance and one-step momentum checks passed; model/inner-AdaBelief/PR+ AST equality was verified. Credit Keller Jordan and the official implementation; no exact-package or novelty claim.

- Trial 007: read official Adafactor equations/options and precision deviations, https://docs.pytorch.org/docs/2.15/generated/torch.optim.Adafactor.html , with the installed torch/optim/_adafactor.py epsilon/relative-step implementation. Credit Shazeer and Stern, https://arxiv.org/abs/1804.04235 . Use the built-in PyTorch variant with lr=0.01, decay exponent -0.8, eps=(None,0.001), update clipping d=1, zero weight decay and foreach=False, on the same hidden matrices only. Default eps1 resolves to float32 machine epsilon, not the paper's squared-gradient stabiliser. Syntax, retained AST and installed signature checks passed without PINN fitting. No faithful-original-paper or novelty claim.

- Trial 008: reread Vyas et al.'s SOAP Algorithm 3 and basis-update details, https://arxiv.org/html/2409.11321v2 . Implemented a local blockwise rotating-Adam variant, direct eigendecomposition with damping, and approximate nonnegative diagonal-variance transport under basis changes. This differs from the reference power/QR update and is disclosed. Synthetic CPU transport/tile-state checks passed. MPS supported a 2x2 eigendecomposition, but the 128x128 synthetic check emitted a CPU-fallback warning. Before PRE or any PINN fit, revised to native 64x64 blocks; a two-refresh/four-tile MPS check passed with no fallback warnings. No coordinates, model targets or validation were used in these unit/capability checks. No scientific failure ID was consumed because Trial 008 had not run. Correlation/block limitations and all hyperparameters are in PRE.

- Trial 009: read Gupta, Koren and Singer's Shampoo matrix algorithm/inverse-root definition, https://arxiv.org/html/1802.09568v2 . Implemented a disclosed local blockwise EMA/momentum variant with inverse fourth roots and scalar Adam Frobenius-norm grafting, rather than the original cumulative update. Synthetic diagonal inverse-root, symmetry, tile-state and graft-norm checks passed; native MPS four-tile/two-refresh checks produced no fallback warning and relative graft-norm error about 8.4e-8. No PINN data/fit used for these implementation checks, and no novelty or exact-package claim. Model, auxiliary optimiser and PR+ AST remain controlled.


Trial 010: read official Google Research Lion implementation https://raw.githubusercontent.com/google/automl/master/lion/lion_pytorch.py (direction before momentum update, defaults lr1e-4/betas .9,.99/no decay), linked paper https://arxiv.org/abs/2302.06675. Recurrence drives hidden partition; known method credited, no reference solutions consulted. Trial 009 closed at L_val .1750692811; no further external source required for POST.

Trial 010 POST: all local exposed results read; no new sources needed. For Trial 011 read official Adan source https://raw.githubusercontent.com/sail-sg/Adan/main/adan.py , including first-step previous gradient initialisation, three bias corrections and zero-decay recurrence. Paper https://arxiv.org/abs/2208.06677 . No protected references used.

Trial 011 PRE: official Adan single-tensor algorithm read through update and previous-gradient save; explicit three bias corrections and zero first delta retained. Distinct gradient-difference mechanism, no new scientific novelty claimed. CPU/native MPS synthetic arithmetic checks passed before fitting.

Trial 011 POST read actual local records; no additional source required. Trial 012 literature: Foret et al. SAM https://arxiv.org/html/2010.01412v3 Section2/equations2-3/Algorithm1 and official https://github.com/google-research/sam . Read temporary weight-neighborhood ascent and second gradient; radius .05 documented as default. Also inspected community PyTorch implementation https://raw.githubusercontent.com/davda54/sam/main/sam.py but rely on paper/author code for algorithm. No coordinate perturbation or reference trajectories.

Trial012 PRE applies first-order L2 SAM as derived in paper Section2 (radius.05), keeping parent base optimisers and final PR+ controlled. Synthetic CPU/native MPS checks passed; no new coordinates or training outside numbered runner.

Trial012 POST all local records read, no new source required. Trial013 primary ConFIG paper https://arxiv.org/html/2408.11104v2 , Section3.1/3.2 two-loss closed form and gradient-length projection. Basic two-task ConFIG considered separately from adaptive M-ConFIG; no claim of conflict-free descent after arbitrary elementwise scaling.

Trial013 PRE: basic two-task ConFIG equal-weight pseudoinverse direction reduced algebraically to unit-vector bisector and projection-length scale;20 synthetic CPU equivalence checks and native MPS projection/degeneracy checks passed. Pure SGD chosen to preserve direction, explicitly not M-ConFIG. No protected outputs or off-pool fitting.

Trial013 POST actual records read,24305 conflicting task pairs observed,no source needed. Trial014 primary MultiAdam page https://proceedings.mlr.press/v202/yao23c.html and linked full paper. Task-wise moments considered to restore conditioning while addressing scale imbalance.

Trial014 full primary Algorithm2 and recommended(.99,.99)/lr.001 read. Implement two grouped tasks with mean normalised updates; paper recommends splitting PDEs further,this controlled grouping departure is explicit. Synthetic CPU/native MPS checks passed. No numerical-reference data accessed.

Trial014 POST actual records read,no new source needed. Trial015 primary algorithm research: Gorbunov,Loizou,Gidel,Extragradient Method: O(1/K) Last-Iterate Convergence for Monotone Variational Inequalities and Connections With Cocoercivity, https://arxiv.org/abs/2110.04261 , reviewing classical Korpelevich predictor-corrector. Nonconvex stochastic PINN setting is outside that convergence theorem.

Trial015 read primary EG recurrence in https://arxiv.org/html/2110.04261 ;predictor theta-etaF(theta),corrector from original theta at predicted operator. Implement classical two-step SGD on same sampled PINN objective,not a saddle-point theorem claim. CPU/native MPS quadratic and rollback checks passed before fitting. No reference trajectories or off-pool training.

Trial015 execution failure: actual traceback/status read,nonfinite residual at second predictor gradient,no emitted score/counts. Counted/no rerun. Activation block begins with known smooth tanh PINN alternative,primary Raissi et al. https://arxiv.org/abs/1711.10561 ;prior75 decision text contains no tanh/GELU/softplus/swish mentions (text search,not proof of source absence).

Trial016 primary full paper https://arxiv.org/html/1711.10561 Section2.1 explicitly describes hyperbolic tangent hidden activations. Initial guessed raw Github Burgers.py path returned404;no code obtained/reused from it. Primary paper supplies attribution. Tanh logits derivative checks CPU/native MPS through third order passed;trainer unchanged from011. No protected references or extra fitting.

Trial016 POST actual records read,no new source needed. Trial017 primary Ramachandran,Zoph,Le,Searching for Activation Functions,https://arxiv.org/abs/1710.05941 ,Swish f(x)=x sigmoid(beta*x). Use beta1 fixed,not learned;function change from sine/tanh is mechanism,not frequency tuning.

Trial017 PRE: beta1 Swish from primary Ramachandran et al. https://arxiv.org/abs/1710.05941 . Independent x*sigmoid(x) implementation;CPU/native MPS derivative formulas through third order and SiLU equivalence passed. No training/reference outcomes consulted beyond authorised frozen scores.

Trial017 POST actual results read,no extra source required. Representation research revisited SIREN primary https://arxiv.org/abs/2006.09661 (oscillatory functions and derivatives,not a claim to reproduce its initialisation). Consider local Gaussian-windowed sine to retain oscillation while changing support/derivative structure.

Trial018 primary WIRE Saragadam et al. https://arxiv.org/html/2301.05187 ,Gaussian localisation and continuous complex Gabor formulation read. Use disclosed real sin(x)*exp(-x^2/2) local variant on parent011,not complex WIRE reproduction. Synthetic CPU/native MPS analytic derivatives through third order/odd symmetry passed;no off-pool coordinates or training.

WIRE full Section3.4 Alternate forms explicitly includes real sine times Gaussian,matching this activation withomega1,s=1/sqrt2. It is a known published alternative,not newly invented here. Full complex architecture/initialisation not reproduced.

Trial018 POST actual results read,no extra source needed. Trial019 primary Liu Ziyin,Hartwig,Ueda,Neural Networks Fail to Learn Periodic Functions and How to Fix It,https://arxiv.org/abs/2006.08195 ;known Snake x+sin^2(x) activation. Linear-plus-periodic function is distinct from global sine/windowed sine/self-gating,not sine coefficient tuning.

Trial019 PRE applies known fixed-alpha1 Snake from primary https://arxiv.org/abs/2006.08195 . Synthetic CPU/native MPS analytic derivatives through third order and linear-periodic shift identity passed;entire011 trainer unchanged. No validation/reference coordinates or unrecorded fitting.

Trial019 POST actual records read,new lowest finite. Trial020 primary Tancik et al.,Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains,https://arxiv.org/abs/2006.10739 . Local deterministic integer oblique spatial modes considered for exact periodic input embedding,not a Gaussian random-feature reproduction or scalar harmonic count-only change.

Trial020 PRE historical decision text rechecked:old010/046 already use pairwise equal-harmonic oblique modes. New43-mode set explicitly includes18pairwise mixed modes+16three-axis modes+9axes,and differs from old k2equal pair cutoff. Not a claim oblique family absent before. Primary Fourier-feature attribution Tancik et al. https://arxiv.org/abs/2006.10739 . CPU/native MPS feature/periodicity/third-derivative checks passed without fitting/extra PDE coordinates.

Trial020 POST actual records read,no extra source needed. Trial021 primary MFN paper Fathony,Sahu,Willmott,Kolter https://openreview.net/pdf?id=OmtmcPkkhT and author presentation https://iclr.cc/media/iclr-2021/Slides/3198.pdf . Author repository discovered https://github.com/boschresearch/multiplicative-filter-networks ;AGPL code not copied,independent mathematical recurrence implementation planned from paper. Prior75 decision text search has no multiplicative-filter/FourierNet/GaborNet mention,not proof of every source absence.

Trial021 author ICLRslides https://iclr.cc/media/iclr-2021/Slides/3198.pdf ,recurrence page5,read. Direct OpenReview PDF fetch was browser-challenged,so not claimed read in full. Known MFN implemented independently,periodic input/local phase initialisation departures explicit;AGPL source not copied. Synthetic product-of-sines derivative checks CPU/native MPS passed without PDE fitting.

Trial021 POST actual records read,no additional source needed. Trial022 primary Cho et al.,Separable Physics-Informed Neural Networks,https://arxiv.org/abs/2306.15969 ,separable-product representation. Consider disclosed space-versus-time low-rank variant,not full per-axis SPINN/grid reuse/forward-AD algorithm;owner pointwise scorer and fixed random pools unchanged.

Trial022 full primary SPINN Section4.2 https://arxiv.org/html/2306.15969v4 equation5 read. Local space-versus-time product-sum raw representation,not per-axis/grid/forwardAD algorithm;density exponential breaks exact raw rank. No lattice-generated training points permitted or used. CPU/native MPS factor/mixed/third derivative/finite-parameter-gradient checks passed before fitting.

Trial022 POST actual records read,no extra source needed. Trial023 primary Wang,Wang,Perdikaris https://arxiv.org/abs/2012.10047 ,multiscale Fourier embedding principle. Local independently parameterised coarse/fine branches considered,not exact shared-MLP MFF reproduction.

Trial023 full primary MFF Section3.3 https://arxiv.org/html/2012.10047 read:published shared-MLP/concatenation differs from local independent additive branches. Historical decision text has harmonic expansions and dedicated spatial velocity branch,not claimed absent multiscale research. New branch allocation/zero-head architecture explicit. CPU/native MPS init/head/third angular derivative checks passed without fitting.

Trial023 POST actual records read. Preliminary guessed https://arxiv.org/abs/2110.11232 opened unrelated singular-SDE paper;not used as activation evidence or cited design basis. Trial024 ISRU primary source located by title search instead.

Trial024 primary Carlile et al. https://arxiv.org/html/1710.09967 Section5/equation2 read,symmetric smooth ISRU not piecewise ISRLU. Fixedalpha1 implementation and CPU/native MPS analytic derivatives through third order/odd symmetry passed. No paper CPU speed claim transferred to MPS/PINNs,no extra coordinates/fitting.

Trial024 POST actual records read,no additional source required. Trial025 primary Perez et al.,FiLM:Visual Reasoning with a General Conditioning Layer,https://arxiv.org/abs/1709.07871 ;feature-wise affine conditioning. Local time-conditioned hidden FiLM variant considered,not visual-reasoning architecture/results reproduction.

Trial025 primary FiLM Section2.1 https://arxiv.org/html/1709.07871 read,affine per-feature scale+shift;local time-only,bounded(.5,1.5)/(-.5,.5) variant explicitly cannot negate/shutoff features. Prior75 hidden-state residual-gate record acknowledged. CPU/native MPS identity/derivative checks passed without PDE coordinates/fitting.

Trial025 POST actual records read. User requested60 total and classical-theory optimisers,including Dogleg. Read official SciPy dogleg/trust-NCG source https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion_dogleg.py and https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion_ncg.py ;located primary Steihaug1983 https://epubs.siam.org/doi/10.1137/0720042 and Powell1970 hybrid-method attribution. Classical design reservoir to be documented;no such new fits yet.

Trial026 primary learned-basis activation literature https://arxiv.org/abs/2502.01247 (current2026v3) and adaptive blending https://arxiv.org/abs/1806.10064 read. Local degree3 Chebyshev-on-tanh/per-feature coefficients differs from their implementations;no exact-paper replication or KAN claim. CPU/native MPS polynomial/third-derivative/coefficient-gradient checks passed without PDE fitting.

Trial026 POST actual records read. Trial027 primary Moseley,Markham,Nissen-Meyer,FBPINNs https://arxiv.org/abs/2107.07871 ,overlapping local neural representations;consider smooth globally supported temporal partition-of-unity mixture,not exact compact-window FBPINN scheduling or coordinate generation.

Trial027 primary FBPINN https://arxiv.org/html/2107.07871 Section4.2/windowed sum read. Local globallysupported normalizedGaussian temporal mixture differs from published sigmoidwindows/localnormalisation/scheduling;allfixedpoints retained,no newcoordinates. CPU/native MPS partition/gate derivatives through third order/finite gradients passed.

Trial027 POST actual records read. Residual-network precedent https://arxiv.org/abs/1512.03385 consulted as background;next design chosen as input concatenation skips,not additive ResNet copying. Trial028 primary NeRF https://arxiv.org/abs/2003.08934 ,input skip precedent,local repeated periodic-feature injection with FiLM to be disclosed.

Trial028 PRE primary NeRF AppendixA https://arxiv.org/html/2003.08934v2 explicitly describes concatenating positional input at the fifth layer. Local repeated original-periodic-input skips are distinct, not a rendering reproduction. Independent implementation; CPU/native MPS initial-map/first-to-third-feature-derivative/finite-parameter-gradient checks passed, no PDE fitting or generated training coordinates.

Trial028 POST actual metrics/metadata/history/log and every physical diagnostic read;counts reconciled;no further source required. Small improvement is exploratory,not significance.

Trial029 primary Bai et al. PIRBN https://arxiv.org/pdf/2304.06234 Section3/eq17 Gaussian radial basis read. arXiv HTML v2 unavailable404;PDF text fetched successfully. Local deep scalar affine-ridge Gaussian units differ from singlelayer fixed-centre radial-distance PIRBN;no theorem transferred. Independent formula;CPU/native MPS evenness/analytic derivatives through third order/finite model gradients passed without PDE fitting or newcoordinates.

Trial029 POST actual metrics/metadata/history/log and every diagnostic read;counts reconciled,no extra source needed. Negative exploratory result,not a general Gaussian verdict.

Trial030 primary RWF Wang et al. https://arxiv.org/html/2210.01274v2 AppendixB Algorithm1 and AppendixC read. Independent log-scale parameterisation at five hidden maps;paper Algorithm1 exp(s) differs from its direct-scale JAX snippet,departure disclosed. No source copied. CPU/native MPS initial effective-map/third-feature-derivative/analytic parameter-chain-rule checks passed. Temporary AST-comparison index corrected before fitting,candidate unchanged;no extra coordinates or training.

Trial030 POST actual metrics/metadata/history/log and every diagnostic read;counts reconciled,no extra source needed. Close score-only contender,not significance or general RWF verdict. Activation/representation block complete.

Trial031 primary Lagaris,Likas,Fotiadis https://arxiv.org/abs/physics/9705023 hard-constraint ansatz principle read;own elementary Fourier inversion derived inresearch_design.md. Poisson/core source read-only verified sign and grav coefficient. Independent171integer-mode coupled density/potential,not a numerical solver/reference target. CPU/native MPS syntheticphase algebra checks passed at5.96e-8Poissonerror with nontrivial disposable coefficients;no off-pooltraining or modelupdates/fits. Scalar conversion warning onlyin temporarycheck,notbackendfallback;no sourcecodecopied.

Trial031 POST actual metrics/metadata/history/log and every diagnostic read;counts reconciled. Poisson hardconstraint numericallyverified in validation butnet score worse,no selectiongate. No additional source needed.

Trial032 applies independentlyderived Euler-Poisson initialjet algebra alreadydocumented inresearch_design.md. Knownhardconstraint precedent Lagaris et al. https://arxiv.org/abs/physics/9705023 previouslyread,reusedwithoutinventingnewsource. CPU/nativeMPS syntheticphase-variable cancellation checks passed withnonzero disposablecoefficients at1.79e-7/1.19e-7;periodicity/finite thirdderivatives/allparametergradients passed. No PDEcoordinategeneration/training/referenceaccess.

Trial032 POST actual metrics/metadata/history/log and every diagnostic read;counts reconciled. Largephysicsgain offsetbylargerICerror,not promotedbydiagnostics. No additionalsource needed.

Trial033 primary Wang,Sankaran,Perdikaris https://arxiv.org/pdf/2203.07404 Section3 eq3.2/Algorithm1 andstopgradientremarkread. HTMLv2unavailable404,PDFsuccessful. Local3window/fixedepsilon1/ICoutsideprefix/canonicalfinish adaptationexplicit. Prior75actual002decisionre-read:stagedsampling,notcurrentresidualgating. CPU/nativeMPS independentgate/gradient/windowchecks passed,noPDEfitsorcoordinatesgenerated.

Trial033 POST actual metrics/metadata/history/log and every diagnostic read;cc16539/counters reconciled. Causalgatesmoderate,implementationoverheadsubstantial,noisolatedcausalityverdict. No additionalsource needed.

Trial034 primaryWang,Teng,Perdikaris https://arxiv.org/html/2001.04536v1 Section2.5 Algorithm1eq40-41 read. Independenttwo-taskmax/mean gradientannealing,every32steps,alpha.1versuspaper.9,targetclip[.1,100],canonicalfinishdeparturesexplicit. CPU/nativeMPSstatistics/EMA/clipping/unusedgradient/combinedlossgradientchecks passed,noPDEfits/newcoordinates.

Trial034 POST actual metrics/metadata/history/log and every diagnosticread;443/443gradienttargetsclipped,countersreconciled. Intendedfeedbackdegeneratesnearconstant100,negativeconfigurationresult;no generalmethodverdict. No additionalsource needed.

Trial035 primaryKharazmi,Zhang,Karniadakis https://arxiv.org/html/1912.00873v1 Section4.1eq4.11/4.17andprojectiondiscussionread. IndependentfiniteFourierICresidualmoments,notweakPDEVPINN/integrationbyparts/newquadrature. Negative-orderweights1/|k|^2andMonteCarlobatchbiasdisclosed. CPU/nativeMPSanalyticgradient/nonnegative/equalMSEdistinctmomentchecks passed,noPDEfits/extraICpositions.

Trial035 POST actual metrics/metadata/history/log/everydiagnosticread;directICmomentforwards13804544addedtoowner18904544=>32709088fullICevaluations,countersreconciled. SmallphysicsgainoffsetbyICincrease,no momentmethodaccuracyclaim. Noadditionalsource needed.

Trial036 primaryMcClenny,Braga-Neto https://arxiv.org/html/2009.04544v2 Section3minimax/descent-ascentread. Independent8-taskboundedsoftmax/entropyadversarydiffersfrompointwiseincreasingpenaltySA-PINN;noauthorscodecopied. OwnentropyinnerproblemstationarityandgradientsverifiedCPU/nativeMPSwithsimplexbounds/modeldetach;noPDEfits/newcoordinates. Auxiliary8logitscountedseparatelyfromfieldmodel.

Trial036POSTactualmetrics/metadata/history/log/everydiagnosticread;model/auxstepsandpointcountsreconciled. ModerateentropyweightsimprovedICbutphysicsworse,no generalminimaxverdict. Noadditionalsource needed.

Trial037 classicalGolub,Pereyra https://doi.org/10.1137/0710036 publisherabstractread,fulltextpaywalled;Dong,Yang https://arxiv.org/abs/2201.09989 abstractread,guessedHTMLv2unavailable404. IndependentperiodicproximalIC-onlyreadoutsolve,noreducednonlinearPDEVarProclaim. CPU/nativeMPSexactparentmap/thirdderivativeandCPUfloat64normal-equation/proximaldecrease/rankdeficiencychecks passed,noPDEfits/newcoordinates. FullICfeaturequerieswillbecountedoutsideownercounters;CPU129x129solveintentional.

Trial037POSTactualmetrics/metadata/history/log/everydiagnosticread;55completeheadsolves/4125000featurequeries reconciled;fullIC24139808vsowner20014808. Trainingheadsubproblemimprovedbutnetvalidationworse,noisolatedVarProaccuracyclaim. Noadditionalsource needed.

Trial038 primaryYu,Lu,Meng,Karniadakis https://arxiv.org/html/2111.02801v1 Section2.2read. Independenttraining-onlyresidualderivativepenalty,ownerresidualalgebraread-onlymatched,nosubstitutescorer/RAR/newcoordinates. CPU/nativeMPSmanufacturedpolynomialr/grad r/parametergradientsofpenaltyandfourthfeaturederivatives passed;noPINNtraining/scoringatsynthetictestvariables. PDEsecondforwardpointcountsgewill supplementowner metadata.

Trial038POSTactualmetrics/metadata/history/log/everydiagnosticread;1780736extraPDEforwardsaddedtoowner8780736=>10561472fullPDEevaluations. Largehigher-derivativeoverhead1739initialupdates,notisolatedgPINNaccuracycomparison. Noadditionalsource needed.

Trial039 primaryClawpackRiemannbook https://www.clawpack.org/riemann_book/html/Euler.html mass/momentumfluxsectionsread. Onlygenericfluxformused;isothermalpressure+gravityremainownerphysics. cPINNDOIhttps://doi.org/10.1016/j.cma.2020.113028returned403,notclaimedread/reproduced. Prior75actual032decisionreread:momentumoutputparameterisationdiffersfromcurrentlossform. CPU/nativeMPSmanufacturedfluxidentity/parametergradient/C0equivalencechecks passed,nooffpooltraining/newcoordinates. Directsame-qPDEpasscountedce,nosubstitutescorer.

Trial039POSTactualmetrics/metadata/history/log/everydiagnosticread;10844160extraPDEforwardsaddedtoowner17744160=>28588320fullPDEevaluations. Cbetter,IC/momentum/Poissonworse,nonequivalence-of-optimisationclaim. Noadditionalsource needed.

Trial040 primaryLu etal. https://arxiv.org/html/2102.04626v1 Section2.6/Algorithm2read. Independent8signedmeanconstraintaugmentedLagrangian,fixedrho1/halfquadratic,projected64stepblockduals,notpointwiseinverse-designhPINNreproduction. CPU/nativeMPSanalyticmean-gradient/Jensenlowerbound/dualprojectionchecks passed;pointwiseresidualhelperASTidentical038,alreadymanufacturedverified. Nooffpooltraining/newcoordinates;bothdirectPDE/ICforwardswill supplementowner counts.

Trial040POSTactualmetrics/metadata/history/log/everydiagnosticread;7757824extraeachpooladdedtoownercounters=>22415648PDE/20690648ICfullqueries,118dualupdates0clipsreconciled. Smallmean/dualcorrectionswiththroughputcost,nonewfeasibilityclaim. Noadditionalsource needed.

Trial041 is an evidence-led startup refinement, not new literature novelty. No additional web source needed:028 source/metrics and032 metrics re-read; mathematical density derivative issue derived directly. Disposable pre-fit check found zero clamp derivative at t=0 on CPU/MPS; draft changed to direct t gate before any training. Executable AST differs only in startup scalar/gate, identical fresh weights and synthetic initial-density/time derivative checks passed. No extra training coordinates or hidden fits.

Trial041 recovery: no new research/source. Missing tool handle, elevated process inventory and absent result artifacts establish interrupted attempt; preserve source/PRE/rawlog and countfailure without rerun or invented metrics. Audit retained separately.

Trial042 is an evidence-led Fourier bandwidth refinement of closed032; no additional literature source needed.032 metrics/source re-read,cutoff3->5 explicitly labelled refinement. CPU/nativeMPS665mode/152667parameter/identicalinitialmap/initialPDEidentity/periodicity tests passed on synthetic phase variables;no extra training coordinates or fits. Interrupted041 provides no scientific outcome and is not rerun.

Trial042 POST actual metrics/metadata/history/log/every diagnostic read. New lowest total, without IC/physical gates. Counters reconcile42complete pool evaluations, including one full gradient in the final unfinished deadline-limited attempt; no invented update. No additional literature needed.

Trial043 is a controlled density-gate refinement of closed030 RWF, not a rerun of interrupted041. Previously read RWF primary source remains attribution; no additional lookup needed. Only two executable AST changes, identical fresh weights, CPU/nativeMPS initial-density/time derivative checks passed. No extra coordinates or unrecorded fits.

Trial043 POST actual metrics/metadata/history/log/every diagnostic read. New lowest total; both physics/IC improve versus direct030 parent. Counters reconcile68complete full-pool evaluations. No extrapolation to interrupted041 or general statistical significance. No additional literature needed.

Trial044 is an explicit main-width128->256 refinement of closed043, no new scientific novelty/source claim. Parent source/metrics re-read. Only14 width constants change, trainer identical; CPU/nativeMPS462405params/shapes/identityFiLM/zero input-skip columns/third derivatives/finite parameter gradients passed. No unrecorded fitting or added training coordinates.

Trial044 POST actual metrics/metadata/history/log/every diagnostic read. New lowest total from better IC despite higher physics;33complete pool evaluations include one full gradient in final unfinished attempt. Capacity/RNG/throughput confounds retained,no significance claim. No additional literature needed.

Trial045: numerical width192 refinement of044, retaining parent RWF/Snake/FiLM/input-skip sources; no new literature lookup or novelty claim.

Trial046: combines044 with032 initial potential gate phi=t*raw_phi. Known hard-constraint lineage credited in032; algebraic refinement, no new lookup or novelty claim.

Trial047: 80/20->50/50 time-budget refinement of044 stochastic/full-pool PR+ pipeline. No new literature lookup or novelty claim.

Trial048: numerical periodic spatial-feature cutoff3->5 refinement of047, motivated by042 bandwidth evidence in another representation. Parent encoding/RWF/Snake/FiLM sources retained; no new lookup or novelty claim.

Trial049: combination047 wide RWF/50-50 pipeline with037 full-IC proximal readout correction. Retain037 VarPro source attribution and limits; no new lookup or novelty claim.

Trial050: scalar training-component normalisation refinement of047: momentum mean and global training-target relative IC. Derived from existing component definitions, uniform time sampling retained; no new lookup or novelty claim.

Trial051: Read official SciPy Dogleg https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion_dogleg.py , trust-region controller https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion.py and BFGS https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_hessian_update_strategy.py . Used mathematical path/agreement/update formulas in independent Torch implementation with8-pair I-initialised BFGS; no dense/exact Hessian claim. Positive-curvature skip uses local angle threshold rather than SciPy normalisation.

Trial052: Read official SciPy Steihaug CG https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_trustregion_ncg.py ; SR1 update/safeguard in previously read https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_hessian_update_strategy.py . Implement independent8-pair SR1 model with20-step truncated CG,negative curvature boundary selection and common trust controller. Quasi-Newton actions,not true HVPs;initial radius.01 from051 evidence.

Trial053: Read Yuan author paper https://lsec.cc.ac.cn/pub/home/yyx/papers/p0504.pdf Section2 BB formulas2.5/2.6; credit original Barzilai/Borwein1988 DOI10.1093/imanum/8.1.141 (original Wisconsin PDF fetch timeout). SPG lineage from Birgin/Martinez/Raydan publisher abstract DOI10.1137/S1052623497330963; author bmr2.pdf extracted text garbled, bmr.pdf timeouts, so full algorithm not claimed read. Independent unconstrained alternateBB1/BB2,max5 nonmonotone Armijo,6halving variant;not exact SPG reproduction.

Trial054: Read Walker2011 author report https://users.wpi.edu/~walker/Papers/anderson_accn_algs_imps.pdf pages1-2 difference-form Anderson least squares/update; Scieur/dAspremont/Bach https://arxiv.org/html/1606.04133 Section3.2 Algorithm2 regularisation principle. Local ridge on difference coefficients plus descent/radius/Armijo safeguards;not exact RNA constrained coefficient algorithm.

Trial055: Read official Ceres https://ceres-solver.readthedocs.io/latest/nnls_solving.html Levenberg-Marquardt eq4-6 after main-domain timeout. Independent identity-damped Gauss-Newton dual8x8 solve on RMS pooled components;exact scalar objective/gradient,rank<=8compressed curvature,not full pointwise GN. Controller/normcap local;no new optimiser claim.

Trial056: Read Cartis/Gould/Toint2011 PartI author PDF https://www.numerical.rl.ac.uk/media/people/nick-gould/CartGoulToin11_mp.pdf Sections2.1,3.1,6.1 for cubic model/controller,shifted PSD stationarity and secular/hardcase characterisation. Local8-pair SR1,<=6-dimensional gradient Krylov projection,CPUdouble small cubic solve;no full Hessian/full-space minimiser/theorem claim.

Trial057: Read official SciPy https://raw.githubusercontent.com/scipy/scipy/main/scipy/optimize/_optimize.py _minimize_newtoncg and approx_fhess_p;independent finite-difference full-gradient Newton-CG with identity damping,max3products,L2forcing.5 and bounded Armijo. Parameter perturbations only,same fixed coordinates;not exact AD HVP or exact SciPy reproduction.

Trial058: Read Parikh/Boyd author monograph https://web.stanford.edu/~boyd/papers/pdf/prox_algs.pdf Section4.1/4.1.1 proximal iteration,shifted quadratic andinexact error caveats. Independent nonconvex3stepPR+ approximate subproblems,strength10,not exact/summable-error convex PPA theorem or weightdecay.

Trial059: Read Wright Coordinate Descent Algorithms https://arxiv.org/html/1502.04759 Section2 cyclic/block framework andSection3.1 nonconvex limitations. Combine local three-block Gauss-Seidel with051 BFGS action formulas;valid secants formed before otherblocks move,old models can become stale. No novelty/exact-minimisation/theorem claim.

Trial060: Read Fletcher/Powell1963 original paper https://galton.uchicago.edu/~lekheng/courses/302/classics/fletcher-powell.pdf Sections3-6 method/inverse-metric/secant/stability discussion. Independent limited-memory inverseDFP rank-two actions fromI,positivecurvature skip and bounded Armijo;not full-memory exact-line historical reproduction or a new optimiser.
