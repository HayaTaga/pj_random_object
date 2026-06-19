# M-Estimation

Use this file to audit likelihood, quasi-likelihood, least squares, LAD,
quantile, and general criterion-based estimators. For consistency, use the
extremum-estimator checklist. For asymptotic normality, audit the score,
Taylor expansion, Hessian, rank, and variance.

## Objects

Require explicit definitions:

- criterion `M_n(theta)` and population target `M(theta)`,
- estimator as max, min, zero of score, or approximate optimizer,
- score `S_n(theta)=\dot M_n(theta)` when differentiable,
- Hessian `H_n(theta)=\ddot M_n(theta)` or derivative of the score,
- target `theta_0`, parameter space, and neighborhood.

Audit questions:

- Is the proof maximizing log likelihood or minimizing negative log likelihood?
- Is the estimator defined by an optimizer, a first-order condition, or both?
- Are constraints or boundary points present?

## Score Equation

For a score-based proof, verify:

- `S_n(theta_0)` is centered or has a known mean,
- `sqrt(n)S_n(theta_0)` satisfies a CLT,
- if observations are dependent, the score variance is long-run or clustered,
- any nuisance parameter in the score is controlled by rate or orthogonality.

Audit questions:

- Is the score evaluated at `theta_0` or at `\hat theta_n`?
- Is the score normalized by `n^{-1}` or by a sum? Track this before applying a
  CLT.
- Is the score measurable and finite with the stated moments?

## First-Order Condition

Do not accept `S_n(\hat theta_n)=0` unless:

- the estimator is interior with probability approaching one,
- the criterion is differentiable at the estimator,
- optimization error is small enough for an approximate FOC, or
- KKT/subgradient conditions are stated for constrained or nonsmooth problems.

Audit questions:

- Does the proof justify moving from argmax to FOC?
- If the solution is on the boundary, what replaces the ordinary FOC?
- Is the FOC exact or approximate?

## Taylor Expansion

Canonical smooth expansion:

```tex
0=S_n(\hat theta_n)
=S_n(theta_0)+H_n(\bar theta_n)(\hat theta_n-theta_0),
```

where `\bar theta_n` lies between `\hat theta_n` and `theta_0`.

Check:

- consistency ensures `\bar theta_n` is in the differentiability neighborhood,
- expansion is valid for vector-valued scores,
- if a remainder form is used, the scaled remainder is `o_p(1)`,
- random intermediate-point arguments require local or uniform Hessian control.

Audit questions:

- Does the proof prove consistency before using the Taylor expansion?
- Is pointwise differentiability enough for the random point?
- What is the exact order of the remainder?

## Hessian Convergence

To replace `H_n(\bar theta_n)` by `H`, verify:

- local uniform convergence:
  `sup_{||theta-theta_0||<=delta_n}||H_n(theta)-H(theta)||=o_p(1)` or a
  deterministic continuity plus ULLN argument,
- `H(theta)` is continuous at `theta_0`,
- `H_n(theta_0)->p H` alone is enough only when the proof separately controls
  `H_n(\bar theta_n)-H_n(theta_0)`,
- normalization of `H_n` matches the score normalization.

Audit questions:

- Is convergence pointwise, uniform on fixed neighborhoods, or local on shrinking
  neighborhoods?
- Does `\bar theta_n` depend on data?
- Are second moments or envelope conditions enough for Hessian LLN?

## Nonsingularity

Check:

- limiting Hessian or information matrix `A` is nonsingular,
- signs match the criterion: negative definite for a maximum, positive definite
  for a minimum,
- eigenvalues are bounded away from zero when sample inverse is used,
- singular or nearly singular cases are treated as weak identification or
  nonstandard asymptotics, not ordinary root-`n` normality.

Audit questions:

- Which matrix is inverted?
- Is nonsingularity stated as an assumption or proved from identification?
- Does the covariance formula require positive definiteness or only full rank?

## Asymptotic Linear Representation

After the previous checks, the standard representation is

```tex
sqrt(n)(\hat theta_n-theta_0)
= -A^{-1}sqrt(n)S_n(theta_0)+o_p(1),
```

where `A` is the limit of the Hessian or derivative of the score.

Check:

- `sqrt(n)S_n(theta_0)=>N(0,B)`,
- `A^{-1}` exists,
- Slutsky applies to replace the random Hessian by `A`,
- all remainders are negligible after `sqrt(n)` scaling.

Audit questions:

- Is the displayed linear representation explicitly derived?
- Are signs consistent with max/min convention?
- Does the claimed covariance follow from this representation?

## Sandwich Variance

For quasi-likelihood, misspecification, heteroskedasticity, clustering, or serial
dependence:

- bread: `A` is the Hessian or derivative limit,
- meat: `B` is the variance limit of `sqrt(n)S_n(theta_0)`,
- covariance: `A^{-1}BA^{-1}` or `A^{-1}B(A^{-1})'` when not symmetric,
- information equality `B=-A` is allowed only under verified correct
  specification and regularity,
- plug-in estimators for `A` and `B` must be consistent.

Audit questions:

- Is the proof using model-based or robust variance?
- Does the data structure require HAC or cluster meat?
- Are nuisance-parameter effects included in `B`?

## Nonsmooth M-Estimators

For LAD, quantile, maximum score, kinked loss, or boundary parameters:

- ordinary Taylor expansion may be invalid,
- use convexity, subgradients, directional derivatives, Knight identity, or an
  argmax process theorem as appropriate,
- rates may be nonstandard,
- asymptotic variance may depend on conditional density or contact sets.

Audit questions:

- Is differentiability actually available?
- Is the claimed `sqrt(n)` rate justified?
- Does the proof need stochastic equicontinuity of a nonsmooth score class?
