# Common Proof Failures

Use this file as a diagnostic checklist. For each issue, identify the failed
step, state why it is not justified, and propose the smallest repair.

## Pointwise Used As Uniform

- Failure: `Q_n(theta)->Q(theta)` for fixed `theta` is used to prove consistency
  of an argmax.
- Why invalid: the optimizer is random and ranges over `Theta`.
- Check: find the line proving `sup_theta |Q_n(theta)-Q(theta)|=o_p(1)`.
- Minimal repair: add ULLN/GC conditions, stochastic equicontinuity plus
  compactness, or weaken the claim to fixed-parameter convergence.

## Identification Without Uniqueness

- Failure: the proof shows `Q(theta_0)` is an optimum or `g_0(theta_0)=0`, but
  not that it is unique.
- Why invalid: consistency targets the unique population optimizer or root.
- Check: require global uniqueness, local uniqueness plus localization, or a
  separation inequality outside every neighborhood.
- Minimal repair: add an identification assumption or weaken the conclusion to
  convergence to the identified set.

## Compactness Omitted

- Failure: an extremum consistency theorem is invoked on a noncompact parameter
  space with no replacement argument.
- Why invalid: the optimizer may escape to infinity even if local convergence
  holds.
- Check: look for compact `Theta`, coercivity, tightness, or a preliminary
  localization lemma.
- Minimal repair: assume compactness, prove coercive separation, or first prove
  the estimator lies in a compact neighborhood with probability approaching one.

## CLT Without Moment Or Dependence Assumptions

- Failure: a CLT is invoked without finite variance, Lindeberg, martingale,
  mixing, cluster, or triangular-array conditions.
- Why invalid: Gaussian limits and variance formulas depend on the sampling
  structure.
- Check: match the data structure to the cited CLT and identify the limit
  variance `S`.
- Minimal repair: add the correct CLT conditions and change `S` to iid,
  heteroskedastic, cluster, HAC, or long-run variance as appropriate.

## Slutsky With Wrong Convergence Mode

- Failure: a random factor is replaced because it is `O_p(1)` or because it has a
  distributional limit.
- Why invalid: Slutsky replacement needs convergence in probability to a
  constant, or joint convergence plus a continuous mapping argument.
- Check: identify exactly which term is `->p c`.
- Minimal repair: prove convergence in probability to a deterministic limit,
  establish joint convergence, or keep the random limit in the final
  distribution.

## Delta Method Without Differentiability

- Failure: `g(\hat theta)` is linearized without checking differentiability at
  `theta_0`.
- Why invalid: continuity alone gives CMT, not first-order distributional
  approximation.
- Check: derivative exists at `theta_0`; for functionals, Hadamard or tangential
  differentiability is stated.
- Minimal repair: add differentiability, use a higher-order delta method, or
  report only the CMT conclusion.

## Missing Rank Condition

- Failure: GMM, IV, or estimating-equation asymptotic normality is claimed
  without full-rank Jacobian.
- Why invalid: rank failure prevents local identification and inversion of the
  linear map.
- Check: dimensions of `G`, whether `rank(G)=p`, and whether `G'WG` is
  nonsingular.
- Minimal repair: add full-rank/local-identification assumption or switch to
  identified-set/weak-identification analysis.

## Missing Nonsingularity

- Failure: a matrix inverse appears after `A_n->A` without showing `A` is
  nonsingular.
- Why invalid: matrix inversion is continuous only on nonsingular matrices.
- Check: eigenvalues bounded away from zero, positive definiteness, or full rank.
- Minimal repair: assume/prove nonsingularity and then apply CMT to `A_n^{-1}`.

## Pointwise Hessian Convergence Used Locally

- Failure: `H_n(theta_0)->H` is used to replace `H_n(\bar theta_n)`, where
  `\bar theta_n` is random.
- Why invalid: pointwise convergence at `theta_0` does not control a random
  nearby point.
- Check: local uniform convergence, stochastic equicontinuity of Hessian, or
  deterministic continuity plus consistency.
- Minimal repair: prove
  `sup_{||theta-theta_0||<=delta_n}||H_n(theta)-H||=o_p(1)` for a neighborhood
  containing `\bar theta_n`.

## Hidden Measurability Assumptions

- Failure: a supremum over an uncountable class is treated as an ordinary random
  variable.
- Why invalid: empirical-process suprema may be nonmeasurable.
- Check: separability, pointwise measurability, countable dense subclass, or
  outer probability notation.
- Minimal repair: state convergence in outer probability or add a measurability
  lemma.

## Necessary And Sufficient Confused

- Failure: a sufficient condition such as compactness, boundedness, or VC type is
  described as necessary.
- Why invalid: proof routes often use convenient sufficient conditions, while
  weaker alternatives may exist.
- Check: distinguish "needed for this proof" from "mathematically necessary for
  the theorem."
- Minimal repair: relabel as sufficient, or prove a necessity statement
  separately.

## Rate Arithmetic Error

- Failure: `R_n=o_p(1)` is multiplied by `sqrt(n)` and treated as negligible.
- Why invalid: after scaling, the proof needs `R_n=o_p(n^{-1/2})`.
- Check: every remainder after the final normalization.
- Minimal repair: strengthen the remainder bound, change the normalization, or
  keep the remainder in the limit.

## Boundary Or Constraint Ignored

- Failure: ordinary FOC is used for a constrained estimator or boundary true
  value.
- Why invalid: KKT conditions or directional derivatives replace the unconstrained
  score equation.
- Check: whether `theta_0` and `\hat theta_n` are interior with probability
  approaching one.
- Minimal repair: add an interiority assumption or use constrained asymptotic
  theory.

## False Positives And Overstatements To Avoid

- Do not say that separation is always an additional assumption. It may be
  derived from compactness, continuity, and unique maximization.
- Do not say compactness is always necessary. It is sufficient for a standard
  proof route, but noncompact proofs may use localization, tightness, coercivity,
  or sieve arguments.
- Do not say uniform convergence is always necessary. It is necessary for many
  standard argmax proof routes, but other convergence modes such as
  epi-convergence or hypi-convergence may be used in other settings.
- Do not treat measurability issues as the main gap unless the theorem involves
  uncountable parameter spaces, suprema, empirical processes, or outer
  probability.
- Do not conflate consistency of the criterion, consistency of the optimizer,
  and identification of the population optimizer.
- Do not silently strengthen the theorem. If the original theorem assumes
  pointwise convergence only, the audit must say the theorem is not proved as
  stated. Any uniform convergence condition must be labeled as an additional
  sufficient assumption.
- Do not confuse sufficient conditions with necessary conditions.

## Proof Audit Severity Levels

- Fatal gap: the conclusion does not follow under the stated assumptions.
- Major gap: a standard theorem is invoked but one or more main conditions are
  not verified.
- Technical gap: measurability, separability, outer probability, or existence of
  argmax is not handled.
- Expository gap: the proof is probably correct under stated assumptions, but
  the argument omits an intermediate step.
- No gap: the step is justified.

Use the severity label to prioritize the audit. Do not let a technical gap hide
a fatal or major mathematical gap.

## Required Language For Repairs

When proposing repairs, use precise repair language:

- "A sufficient repair is..."
- "This is not necessary in all possible proof routes."
- "This condition can be derived if..."
- "This condition must be added for the stated proof route."

Avoid vague phrases unless the assumptions are listed explicitly:

- "clearly"
- "obviously"
- "standard regularity conditions"
- "under suitable assumptions"

## Minimal Repair Policy

Prefer the smallest valid change:

1. clarify the target convergence mode,
2. weaken the conclusion to what is proved,
3. add the missing theorem conditions,
4. localize the argument,
5. add a short lemma for uniformity, rank, or measurability,
6. change the cited theorem,
7. rewrite the proof only after the dependency map is correct.

Audit questions Codex should always ask:

- Which exact proof step fails?
- Is the missing condition sufficient for this route or claimed necessary?
- Does the repair change the theorem statement?
- Does the repair alter the convergence mode, rate, or variance formula?
