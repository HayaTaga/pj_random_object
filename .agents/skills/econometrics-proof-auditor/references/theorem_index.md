# Theorem Index

This index gives compact theorem cards for proof auditing. It is drafted from
`corpus/extracted` using the local search scripts. Do not treat these cards as
verbatim textbook statements. Use them to locate source material, summarize
condition structures, and check proof dependencies.

Do not copy long passages from the corpus. No theorem number is listed unless it
was visible in the extracted text. If a standalone theorem location was not
clearly located, the source entry says `location uncertain`.

## Source Aliases

- `Hansen_2021_Econometrics`: `corpus/extracted/Hansen_2021_Econometrics.txt`
- `Hansen_2021_Probability_Statistics`: `corpus/extracted/Hansen_2021_Probability_Statistics.txt`
- `Hayashi_2000`: `corpus/extracted/Hayashi_2000.txt`
- `Newey_McFadden_1994`: `corpus/extracted/Newey_McFadden_1994.txt`
- `van_der_Vaart_1998`: `corpus/extracted/van_der_Vaart_1998.txt`
- `van_der_Vaart_Wellner_2023`: `corpus/extracted/van_der_Vaart_Wellner_2023.txt`
- `Amemiya_1985`: `corpus/extracted/Amemiya_1985.txt`
- `Arellano_2004`: `corpus/extracted/Arellano_2004.txt`
- `Cameron_Trivedi_2005`: `corpus/extracted/Cameron_Trivedi_2005.txt`
- `Hall_2005`: `corpus/extracted/Hall_2005.txt`
- `Hortacsu_Joo_2023`: `corpus/extracted/Hortacsu_Joo_2023.txt`
- `Kato_2019_STSCI6940`: `corpus/extracted/Kato_2019_STSCI6940.txt`
- `Vershynin_2020`: `corpus/extracted/Vershynin_2020.txt`
- `Handbook_Vol2_Ch15`: `corpus/extracted/Handbook of Econometrics/Vol2/Chapter-15-Approximating-the-distributions-of-econometr_1984_Handbook-of-Eco.txt`
- `Handbook_Vol4_Ch37`: `corpus/extracted/Handbook of Econometrics/Vol4/Chapter-37-Empirical-process-methods-in-economet_1994_Handbook-of-Econometri.txt`
- `Handbook_Vol4_Ch45`: `corpus/extracted/Handbook of Econometrics/Vol4/Chapter-45-Estimation-and-inference-for-dependent-_1994_Handbook-of-Economet.txt`

## 1. Law Of Large Numbers

- Topic: Law of large numbers for sample averages.
- Sources:
  - `Hansen_2021_Econometrics`, p.181, line 11600: `Theorem 6.1 Weak Law of Large Numbers (WLLN)`.
  - `Hansen_2021_Probability_Statistics`, p.169, line 10372: `Theorem 7.4 Weak Law of Large Numbers (WLLN)`.
  - `Hansen_2021_Probability_Statistics`, p.175, line 10894: `Theorem 7.12 Strong Law of Large Numbers (SLLN)`.
  - `van_der_Vaart_1998`, p.30, line 993: `2.16 Proposition (Weak law of large numbers)`.
  - `Vershynin_2020`, p.18, line 645: `Theorem 1.3.1 (Strong law of large numbers)`.
- Use case: Replace an average of random variables by its population mean.
- Sufficient conditions: A theorem-matched sampling scheme such as i.i.d.,
  independent, or stationary ergodic data; finite first moment or theorem-specific
  integrability; correct centering; componentwise handling for vectors.
- Conclusion: Sample averages converge to expectations, either in probability
  or almost surely depending on the invoked LLN.
- Common misuse: Applying an i.i.d. LLN under serial dependence, clustering, or
  triangular arrays; assuming finite variance when only finite mean is needed;
  treating a pointwise LLN as uniform in a parameter.
- Proof-check questions: What is the exact sample structure? Is the expectation
  finite? Is the target scalar, vector, or indexed by a parameter? Is the claimed
  mode in probability or almost sure?
- Related cards: Central limit theorem; Uniform law of large numbers; GMM
  consistency.

## 2. Central Limit Theorem

- Topic: Central limit theorem for normalized sums or sample moments.
- Sources:
  - `Hall_2005`, p.83, line 3773: central limit theorem for sample moments.
  - `Newey_McFadden_1994`, p.33, line 1357: CLT used for asymptotic normality
    of extremum estimators.
  - `Hortacsu_Joo_2023`, p.253, line 17261: `Theorem A.2.1` for a GMM estimator.
  - `van_der_Vaart_1998`, p.43, line 1493 and p.51, line 1781: CLT use in
    asymptotic distribution arguments.
- Use case: Derive a Gaussian limit for scores, sample moments, or centered
  estimators after `sqrt(n)` normalization.
- Sufficient conditions: Proper centering; theorem-matched dependence structure;
  finite second moments or Lindeberg-type conditions; limiting variance exists;
  for dependent data, long-run variance and mixing/martingale conditions as
  required by the invoked CLT.
- Conclusion: Normalized sums or sample moments converge in distribution to a
  mean-zero normal vector with the appropriate variance.
- Common misuse: Using an i.i.d. CLT for dependent or clustered data; ignoring
  long-run covariance; failing to verify Lindeberg or moment restrictions;
  claiming asymptotic normality when the limiting variance is singular.
- Proof-check questions: What is being centered? What normalization is used? Is
  the variance matrix finite and nonsingular where needed? Does the sample
  dependence match the theorem?
- Related cards: Slutsky theorem; Delta method; Extremum estimator asymptotic
  normality; GMM asymptotic normality; Sandwich variance.

## 3. Continuous Mapping Theorem

- Topic: Preservation of convergence under continuous maps.
- Sources:
  - `Hansen_2021_Econometrics`, p.182, line 11697: section on Continuous
    Mapping Theorem and Delta Method; p.182, line 11698 states the continuity
    principle.
  - `Hansen_2021_Probability_Statistics`, p.187, line 11854: CMT presented with
    Slutsky as a special case.
  - `van_der_Vaart_Wellner_2023`, p.49, line 2129: CMT combined with Slutsky's
    lemma.
- Use case: Transfer convergence of an estimator or process to a continuous
  transformation, such as sums, products, norms, or matrix functions.
- Sufficient conditions: Convergence in the relevant topology; map continuous at
  the limiting value or almost surely on the limit's support; measurable
  transformation or valid outer-probability formulation.
- Conclusion: The transformed sequence converges to the transformed limit.
- Common misuse: Applying CMT to discontinuous operations such as argmax without
  uniqueness, matrix inverse without nonsingularity, indicators at mass points,
  or suprema over nonmeasurable classes without outer probability.
- Proof-check questions: What topology is used? Is the mapping continuous at the
  limit? Is any inverse bounded away from singularity? Are measurability issues
  handled?
- Related cards: Slutsky theorem; Delta method; Argmax theorem; Rank and
  nonsingularity conditions.

## 4. Slutsky Theorem

- Topic: Combining distributional convergence with probability convergence.
- Sources:
  - `Hansen_2021_Probability_Statistics`, p.187, lines 11854-11855: Slutsky
    theorem location.
  - `Cameron_Trivedi_2005`, p.96, line 4046: Slutsky theorem used in an OLS
    asymptotic argument.
  - `van_der_Vaart_Wellner_2023`, p.49, line 2129 and p.427, line 29507:
    Slutsky lemma references in asymptotic arguments.
- Use case: Replace nuisance factors by probability limits inside an asymptotic
  distribution argument.
- Sufficient conditions: One component converges in distribution; the other
  component converges in probability to a constant or deterministic matrix; the
  algebraic operation is continuous at the limit; dimensions conform.
- Conclusion: Sums, products, and continuous combinations have the corresponding
  distributional limit.
- Common misuse: Replacing a random term that has only a distributional limit;
  inverting a matrix sequence without nonsingularity; using inconsistent
  variance estimators.
- Proof-check questions: Which factor is `o_p(1)` or converges in probability?
  Is the limiting matrix nonsingular? Is joint convergence needed and justified?
- Related cards: Central limit theorem; Continuous mapping theorem; Delta
  method; Sandwich variance.

## 5. Delta Method

- Topic: Asymptotic distribution of smooth transformations.
- Sources:
  - `Hansen_2021_Econometrics`, p.183, line 11718: `Theorem 6.8 Delta Method`.
  - `Hansen_2021_Econometrics`, p.182, line 11697: section on Continuous Mapping
    Theorem and Delta Method.
  - `van_der_Vaart_1998`, p.48, line 1664: delta method used with Slutsky.
  - `Handbook_Vol2_Ch15`, p.16, line 601: generalized delta method for
    higher-order expansions.
- Use case: Convert `sqrt(n)(T_n - \theta_0)` convergence into convergence of
  `sqrt(n)(g(T_n) - g(\theta_0))`.
- Sufficient conditions: Asymptotic normality or another distributional limit for
  the input estimator; differentiability of `g` at the true value, with
  Hadamard differentiability for functional parameters; derivative evaluated at
  the correct point; nondegenerate derivative unless a higher-order delta method
  is invoked.
- Conclusion: The transformed estimator has the linearized limiting distribution
  given by the derivative applied to the input limit.
- Common misuse: Applying the ordinary delta method at a nondifferentiable point,
  ignoring a zero first derivative, or using plug-in derivatives without showing
  consistency.
- Proof-check questions: What is the input convergence statement? Which
  derivative is used? Is the derivative continuous or consistently estimated?
  Does the first-order derivative vanish?
- Related cards: Continuous mapping theorem; Slutsky theorem; Sandwich
  variance; Rank and nonsingularity conditions.

## 6. Uniform Law Of Large Numbers

- Topic: Uniform convergence of sample criteria or indexed averages.
- Sources:
  - `Hansen_2021_Econometrics`, p.788, line 58388: `Theorem 22.2 Uniform Law of
    Large Numbers (ULLN)`.
  - `Hayashi_2000`, p.476, line 15410: `Lemma 7.2 (Uniform law of large numbers)`.
  - `Vershynin_2020`, p.205, line 10860: `Theorem 8.2.3 (Uniform law of large
    numbers)`.
  - `van_der_Vaart_Wellner_2023`, p.640, line 44820: `A.5.1 Proposition
    (Uniform law of large numbers)`.
- Use case: Show `sup_{\theta \in \Theta}|M_n(\theta)-M(\theta)|` converges to
  zero for consistency and uniform approximation arguments.
- Sufficient conditions: Parameter space compact or localized; continuity in the
  parameter; measurable/separable indexed class or outer-probability statement;
  integrable envelope; data structure matching the theorem, such as i.i.d. or
  stationary ergodic; entropy or Glivenko-Cantelli conditions when the class is
  large.
- Conclusion: The sample process converges uniformly to its population
  counterpart, in probability or almost surely depending on the theorem.
- Common misuse: Replacing ULLN with pointwise LLN; ignoring unbounded envelopes;
  using compactness without continuity; taking a supremum over a nonmeasurable
  class without outer probability.
- Proof-check questions: What is the index set? What envelope dominates the
  class? Is the supremum measurable? Is convergence global or only local?
- Related cards: Law of large numbers; Extremum estimator consistency;
  M-estimator consistency; GMM consistency; Stochastic equicontinuity.

## 7. Stochastic Equicontinuity

- Topic: Local uniform control of stochastic process increments.
- Sources:
  - `Handbook_Vol4_Ch37`, p.5, line 152: definition location for stochastic
    equicontinuity.
  - `Handbook_Vol4_Ch37`, p.29, line 1091: theorem application yielding
    stochastic equicontinuity under stated conditions.
  - `Handbook_Vol4_Ch37`, p.42, line 1605: stochastic equicontinuity follows
    from an assumption in a proof.
  - `Newey_McFadden_1994`, p.28, line 1147: proof step reduces to stochastic
    equicontinuity.
  - `Newey_McFadden_1994`, p.76, line 3055: stochastic equicontinuity assumption
    described for semiparametric conditions.
- Use case: Upgrade pointwise stochastic convergence to local uniform
  convergence around drifting or estimated parameter values.
- Sufficient conditions: A semimetric for the index set; shrinking neighborhoods;
  tightness or boundedness of local sequences; entropy/bracketing or Lipschitz
  plus moment envelope conditions; measurability or outer-probability handling.
- Conclusion: Supremum of process increments over small neighborhoods is
  `o_p(1)` or asymptotically negligible.
- Common misuse: Treating pointwise convergence as enough for random indices;
  omitting the metric; ignoring rate interactions between neighborhood size and
  empirical process fluctuations.
- Proof-check questions: What is the index metric? Is the index random? Is the
  neighborhood shrinking? Which entropy, envelope, or Lipschitz condition
  verifies equicontinuity?
- Related cards: Uniform law of large numbers; M-estimator asymptotic normality;
  Extremum estimator asymptotic normality; Argmax theorem.

## 8. Argmax Theorem

- Topic: Convergence of approximate maximizers or minimizers of stochastic
  criteria.
- Sources:
  - `van_der_Vaart_1998`, p.95, line 3455: `5.56 Theorem (Argmax theorem)`.
  - `van_der_Vaart_1998`, p.97, line 3533: argmax theorem used to prove
    consistency.
  - `van_der_Vaart_Wellner_2023`, p.403, line 27926: argmax continuous mapping
    theorem discussion.
  - `van_der_Vaart_Wellner_2023`, p.420, line 28990: tightness plus argmax
    continuous mapping theorem yields distributional convergence.
- Use case: Transfer convergence of objective functions to convergence of their
  maximizers.
- Sufficient conditions: Objective processes converge in the relevant function
  space or uniformly on compact/local sets; the limiting criterion has a unique
  and well-separated optimizer; the estimator is an exact or approximate
  optimizer; tightness/localization and measurability are handled.
- Conclusion: The optimizer converges in probability or distribution to the
  optimizer of the limiting criterion.
- Common misuse: Invoking argmax with nonunique limiting maximizers; relying only
  on pointwise convergence; failing to show the estimator is near-maximizing;
  ignoring boundary cases.
- Proof-check questions: Is the limit optimizer unique? Is convergence uniform
  or process-level? Is the estimator measurable and approximate optimal? Is the
  parameter space compact or localized?
- Related cards: Continuous mapping theorem; Extremum estimator consistency;
  M-estimator consistency; Stochastic equicontinuity.

## 9. Extremum Estimator Consistency

- Topic: Consistency of estimators defined by optimizing a sample criterion.
- Sources:
  - `Newey_McFadden_1994`, p.11, line 463: section on consistency of extremum
    estimators and sufficient conditions.
  - `Hayashi_2000`, p.473, line 15327: consistency theorem for extremum
    estimators.
  - `Hayashi_2000`, p.476, line 15430: ULLN combined with extremum consistency.
  - `Amemiya_1985`, p.123, line 4171: theorem covering local extremum
    estimators.
- Use case: Show an optimizer `\hat\theta_n` converges to the true parameter
  `\theta_0`.
- Sufficient conditions: Uniform convergence of the sample criterion to a
  deterministic population criterion; unique maximizer/minimizer or separation
  at `\theta_0`; compact parameter space or localization/tightness; continuity
  of the population criterion; approximate optimizer condition.
- Conclusion: The extremum estimator is consistent for the identified population
  optimizer.
- Common misuse: Proving only pointwise convergence of the criterion; assuming
  compactness without checking it; failing to show uniqueness or separation;
  ignoring approximate optimization error.
- Proof-check questions: What is the population criterion? Where is uniqueness
  verified? Is convergence uniform on the relevant set? Does the estimator
  actually nearly optimize?
- Related cards: Uniform law of large numbers; Argmax theorem; Identification
  and uniqueness of the population criterion; Extremum estimator asymptotic
  normality.

## 10. Extremum Estimator Asymptotic Normality

- Topic: Asymptotic normality for smooth extremum estimators.
- Sources:
  - `Arellano_2004`, p.198, line 5290: `Asymptotic Normality Theorem for
    Extremum Estimators`.
  - `Newey_McFadden_1994`, p.33, line 1357: CLT route for asymptotic normality
    of extremum estimators.
  - `Amemiya_1985`, p.123, line 4171: theorem covering consistency and
    asymptotic normality of local extremum estimators.
  - `Arellano_2004`, p.200, line 5356: discussion of differentiability
    conditions.
- Use case: Derive the limiting distribution of `\sqrt{n}(\hat\theta_n-\theta_0)`
  after consistency is known.
- Sufficient conditions: Consistency; interior solution or valid treatment of
  constraints; first-order condition or subgradient condition; score/gradient
  CLT; Hessian or Jacobian convergence to nonsingular curvature; differentiability
  or a valid nonsmooth expansion; negligible remainder.
- Conclusion: The normalized estimation error is asymptotically normal with
  covariance determined by curvature and score variance.
- Common misuse: Using the first-order condition at a boundary solution; omitting
  Hessian nonsingularity; assuming differentiability where the criterion is
  nonsmooth; failing to prove the score CLT.
- Proof-check questions: Is the estimator in the interior with high probability?
  What expansion is used? Is the Hessian uniformly convergent? Is the curvature
  nonsingular? What variance matrix appears in the score CLT?
- Related cards: Central limit theorem; Slutsky theorem; Sandwich variance;
  Rank and nonsingularity conditions; M-estimator asymptotic normality.

## 11. M-Estimator Consistency

- Topic: Consistency of M-estimators as extremum estimators.
- Sources:
  - `Kato_2019_STSCI6940`, p.120, line 6484: example on consistency of
    M-estimators.
  - `Kato_2019_STSCI6940`, p.120, line 6485: uniform convergence of objective
    functions to a population criterion.
  - `van_der_Vaart_1998`, p.97, line 3533: argmax theorem applied to criterion
    functions.
  - `Newey_McFadden_1994`, p.11, line 463: extremum consistency conditions.
  - `Cameron_Trivedi_2005`, p.150, lines 6998 and 7015: consistency of global
    and local maxima.
- Use case: Prove consistency for maximum likelihood, least squares, quantile,
  or other criterion-based estimators.
- Sufficient conditions: The criterion class is Glivenko-Cantelli or satisfies a
  ULLN; population criterion uniquely optimizes at `\theta_0`; compactness or
  localization; approximate optimization; measurability or outer-probability
  formulation.
- Conclusion: The M-estimator converges to the population optimizer.
- Common misuse: Ignoring nonunique population optima under misspecification;
  treating local and global consistency as identical; failing to justify
  measurability of the criterion supremum.
- Proof-check questions: Is this global or local consistency? Does the objective
  class satisfy a ULLN? Is the optimizer unique? Is the estimator approximate or
  exact?
- Related cards: Extremum estimator consistency; Uniform law of large numbers;
  Argmax theorem; Identification and uniqueness of the population criterion.

## 12. M-Estimator Asymptotic Normality

- Topic: Asymptotic normality of smooth or locally quadratic M-estimators.
- Sources:
  - `van_der_Vaart_Wellner_2023`, p.423, line 29241: `3.2.16 Theorem
    (M-estimator-asymptotic normality)`.
  - `van_der_Vaart_Wellner_2023`, p.426, line 29461: `3.2.20 Theorem
    (M-estimator-asymptotic normality)`.
  - `van_der_Vaart_Wellner_2023`, p.427, line 29537: `3.2.22 Theorem
    (M-estimator-asymptotic normality)`.
  - `Newey_McFadden_1994`, p.33, line 1357: asymptotic normality route for
    extremum estimators.
  - `Amemiya_1985`, p.123, line 4171: local extremum estimator asymptotic
    normality location.
- Use case: Establish the limiting distribution for estimators obtained by
  minimizing empirical loss or maximizing empirical criterion.
- Sufficient conditions: Consistency and local parameterization; local quadratic
  expansion or differentiability of the criterion; empirical score process CLT;
  stochastic equicontinuity or remainder control; nonsingular Hessian or
  information matrix; valid variance estimator if inference is claimed.
- Conclusion: `\sqrt{n}(\hat\theta_n-\theta_0)` has a linear representation and
  converges to a normal distribution, often with sandwich covariance.
- Common misuse: Skipping the local expansion; using global ULLN as if it gives
  a `\sqrt{n}` rate; omitting stochastic equicontinuity for random local
  arguments; assuming information equality under misspecification.
- Proof-check questions: What is the asymptotic linear representation? Which
  score CLT is used? Is the Hessian/information matrix nonsingular? Is the
  remainder `o_p(n^{-1/2})` or negligible after normalization?
- Related cards: Stochastic equicontinuity; Central limit theorem; Sandwich
  variance; Rank and nonsingularity conditions; Extremum estimator asymptotic
  normality.

## 13. GMM Consistency

- Topic: Consistency of generalized method of moments estimators.
- Sources:
  - `Handbook_Vol4_Ch45`, p.56, line 2128: `Theorem 7.1 (Consistency of GMM)`.
  - `Hayashi_2000`, p.484, line 15679: `Proposition 7.7 (Consistency of GMM with
    compact parameter space)`.
  - `Newey_McFadden_1994`, p.50, line 2033: consistency conditions applied to
    GMM.
  - `Hall_2005`, p.202, line 10208: consistency assumption for sub-sample GMM
    estimators.
- Use case: Show a GMM minimizer converges to the parameter satisfying population
  moment restrictions.
- Sufficient conditions: Uniform convergence of sample moments to population
  moments; weighting matrix converges to a deterministic positive semidefinite or
  positive definite limit; continuity of moments; compactness or localization;
  identification through unique minimization of the population GMM criterion.
- Conclusion: The GMM estimator converges to the identified population parameter.
- Common misuse: Assuming sample moments near zero imply identification; ignoring
  randomness or singularity of the weighting matrix; using pointwise convergence
  of moments where uniform convergence is needed.
- Proof-check questions: What is the population moment `g(\theta)`? Is
  `g(\theta)=0` unique at `\theta_0` or is the weighted criterion uniquely
  minimized? Does `W_n` converge? Is the minimization approximate?
- Related cards: Uniform law of large numbers; Identification and uniqueness of
  the population criterion; Rank and nonsingularity conditions; GMM asymptotic
  normality.

## 14. GMM Asymptotic Normality

- Topic: Asymptotic normality of GMM estimators.
- Sources:
  - `Handbook_Vol4_Ch45`, p.58, line 2194: `Theorem 7.2 (Asymptotic normality of
    GMM)`.
  - `Handbook_Vol4_Ch45`, p.58, lines 2204-2206: rank and positive-definite
    variance conditions for the theorem.
  - `Hayashi_2000`, p.497, line 16032: `Proposition 7.10 (Asymptotic normality
    of GMM)`.
  - `Newey_McFadden_1994`, p.68, line 2718: GMM asymptotic normality result
    applied to stacked moments.
  - `Arellano_2004`, p.199, line 5333: `Asymptotic Normality Theorem for GMM`.
- Use case: Derive the asymptotic distribution of a consistent GMM estimator.
- Sufficient conditions: GMM consistency; moment CLT at `\theta_0`; differentiable
  population moments with consistently estimated Jacobian; weighting matrix
  convergence; full column rank of the Jacobian under the relevant weighting;
  nonsingular long-run variance and bread matrix; negligible higher-order
  remainder.
- Conclusion: `\sqrt{n}(\hat\theta_n-\theta_0)` is asymptotically normal with
  covariance determined by the Jacobian, weighting matrix, and long-run variance.
- Common misuse: Treating optimal-weight and arbitrary-weight covariance formulas
  as identical; omitting rank verification; using homoskedastic variance under
  serial correlation; not proving the sample Jacobian converges.
- Proof-check questions: What CLT applies to the sample moments? What is the
  limiting weight matrix? Is `D' W D` nonsingular? Is the long-run variance
  consistently estimated? Is the model exactly or overidentified?
- Related cards: Central limit theorem; Slutsky theorem; Sandwich variance;
  Rank and nonsingularity conditions; GMM consistency.

## 15. Sandwich Variance

- Topic: Bread-meat-bread covariance for asymptotically linear estimators.
- Sources:
  - `Hansen_2021_Econometrics`, p.442, line 33881: GMM asymptotic variance in
    sandwich form.
  - `Handbook_Vol4_Ch45`, p.58, lines 2204-2206: positive-definite variance and
    rank conditions in GMM asymptotic normality.
  - `Handbook_Vol4_Ch45`, p.62, lines 2327-2328: optimal GMM asymptotic variance
    discussion.
  - `Cameron_Trivedi_2005`, p.185, line 9537: robust sandwich variance estimate.
  - location uncertain for a standalone general sandwich-variance theorem in the
    extracted corpus.
- Use case: State or estimate robust asymptotic variance for M-estimators, GMM,
  quasi-MLE, and misspecified likelihood estimators.
- Sufficient conditions: Asymptotic linear representation; score or moment CLT
  with finite covariance; consistent estimators of the bread and meat matrices;
  nonsingular bread; dependence-robust meat when data are serially correlated or
  clustered.
- Conclusion: The estimator's asymptotic covariance is a bread-inverse, meat,
  bread-inverse transpose expression; plug-in versions are consistent when their
  components are consistent.
- Common misuse: Using information equality under misspecification; ignoring
  clustering or serial dependence; inverting a nearly singular bread matrix;
  dropping finite-sample scaling conventions without tracking normalization.
- Proof-check questions: What is the influence function? What is the meat under
  the actual sampling scheme? Is the bread nonsingular? Are all plug-in pieces
  consistent?
- Related cards: M-estimator asymptotic normality; GMM asymptotic normality;
  Slutsky theorem; Rank and nonsingularity conditions.

## 16. Identification And Uniqueness Of The Population Criterion

- Topic: Population-level uniqueness needed for consistency.
- Sources:
  - `Newey_McFadden_1994`, p.14, lines 577-579: identification condition based
    on a unique maximum of the limit objective.
  - `Hall_2005`, p.133, lines 6296-6298: population GMM criterion has a unique
    minimum at the true parameter under an assumption.
  - `Cameron_Trivedi_2005`, p.150, lines 6998 and 7015: consistency for global
    and local maxima.
  - `Amemiya_1985`, p.119, lines 4038-4039: population criterion uniquely
    maximized at the true value in a consistency result.
- Use case: Verify that the limit objective or moment restrictions identify the
  target parameter before applying an extremum consistency theorem.
- Sufficient conditions: Population objective has a unique maximizer/minimizer at
  `\theta_0`; for global consistency, separation away from neighborhoods of
  `\theta_0`; for GMM, population moments or weighted criterion uniquely identify
  `\theta_0`; parameter space and topology match the consistency theorem.
- Conclusion: The population target is well defined, allowing uniform convergence
  of the criterion to imply estimator consistency.
- Common misuse: Confusing local identification with global uniqueness; assuming
  moment equations identify when there are multiple roots; failing to prove
  separation on noncompact parameter spaces.
- Proof-check questions: Is uniqueness global or local? Is there a separation
  inequality outside every neighborhood? Does the weighting matrix preserve
  identification? Are there nuisance parameters or observational equivalence?
- Related cards: Extremum estimator consistency; M-estimator consistency; GMM
  consistency; Rank and nonsingularity conditions.

## 17. Rank And Nonsingularity Conditions

- Topic: Full-rank and invertibility conditions used in identification and
  asymptotic normality.
- Sources:
  - `Handbook_Vol4_Ch45`, p.58, line 2204: rank condition in GMM asymptotic
    normality.
  - `Handbook_Vol4_Ch45`, p.58, lines 2205-2206: positive-definite asymptotic
    variance condition.
  - `Hayashi_2000`, p.373, lines 12616-12618: identification and nonsingularity
    discussion for matrix invertibility.
  - `Newey_McFadden_1994`, p.108, lines 4244-4245: full-rank matrix condition
    used in an asymptotic argument.
  - location uncertain for a standalone general rank/nonsingularity theorem in
    the extracted corpus.
- Use case: Justify matrix inversion, local identification, nonsingular limiting
  covariance, and valid linearization.
- Sufficient conditions: Jacobian or derivative matrix has full column rank;
  Hessian or bread matrix is nonsingular; variance or weighting matrix is
  positive definite on the relevant subspace; eigenvalues are bounded away from
  zero in the limit; sample matrices converge to those nonsingular limits.
- Conclusion: Inverses exist with probability approaching one, continuous
  mapping applies to inverses, and asymptotic covariance formulas are well
  defined.
- Common misuse: Assuming sample full rank proves limiting full rank; ignoring
  weak identification or near singularity; inverting positive semidefinite
  matrices as if positive definite; failing to check dimensions.
- Proof-check questions: Which matrix is inverted? Is rank full at the population
  value? Are eigenvalues bounded away from zero? Is the sample matrix converging
  uniformly or pointwise to the nonsingular limit?
- Related cards: Continuous mapping theorem; Delta method; Sandwich variance;
  Extremum estimator asymptotic normality; GMM asymptotic normality.
