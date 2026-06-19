# GMM

Use this file to audit generalized method of moments proofs. Separate
identification, sample moment convergence, weighting, and rank conditions before
accepting any consistency or asymptotic normality claim.

## Objects

Require explicit definitions:

- moment function `g(Z_i,theta)` in `R^q`,
- sample moment `\hat g_n(theta)=n^{-1}\sum_i g(Z_i,theta)`,
- population moment `g_0(theta)=E g(Z_i,theta)`,
- parameter dimension `p` and moment dimension `q`,
- weighting matrix `\hat W_n`,
- criterion `Q_n(theta)=\hat g_n(theta)'\hat W_n\hat g_n(theta)`.

Audit questions:

- Is the model exactly identified, overidentified, or underidentified?
- Is `q>=p` stated where asymptotic normality uses rank?
- Are moments centered at the true parameter under the maintained assumptions?

## Moment Condition

Check:

- target moment: `g_0(theta_0)=0` or pseudo-true minimizer under
  misspecification,
- finite moments sufficient for LLN/CLT,
- dependence conditions match the variance estimator,
- instruments are valid where moment restrictions require exogeneity.

Do not accept `E[g(Z_i,theta_0)]=0` as identification by itself.

Audit questions:

- What economic/statistical assumption implies the moment condition?
- Are generated regressors or estimated nuisance parameters inside `g`?
- If the model is misspecified, what is the population target?

## Sample Moment Convergence

For consistency, verify:

- uniform convergence:
  `sup_{theta in Theta}||\hat g_n(theta)-g_0(theta)||=o_p(1)`,
- continuity of `g_0(theta)`,
- compactness or localization,
- measurability or outer probability for the supremum.

For asymptotic normality, verify:

- CLT for `sqrt(n)\hat g_n(theta_0)`,
- local expansion:
  `\hat g_n(\hat theta_n)=\hat g_n(theta_0)+G(\hat theta_n-theta_0)+remainder`,
- the remainder is negligible after `sqrt(n)` scaling.

Audit questions:

- Is convergence pointwise or uniform?
- What theorem handles serial correlation, clustering, or heteroskedasticity?
- Is the Jacobian sample-based, population-based, or both?

## Weighting Matrix Convergence

Check:

- `\hat W_n ->p W`,
- `\hat W_n` is symmetric or symmetrized when used in a quadratic form,
- `W` is positive semidefinite for consistency and positive definite where
  identification or optimality requires it,
- if `\hat W_n` is estimated in a first step, its estimation error is negligible
  for the stated result.

Audit questions:

- Is the weight matrix random but treated as fixed?
- Does singularity of `W` destroy identification?
- Is the same `W` used in the covariance formula?

## Identification

Consistency requires the population criterion

```tex
Q(theta)=g_0(theta)'Wg_0(theta)
```

to be uniquely minimized at `theta_0`.

Check:

- uniqueness is global or explicitly local,
- if `W` is singular, uniqueness is through the weighted norm, not just
  `g_0(theta)=0`,
- separation holds away from neighborhoods of `theta_0`,
- parameter restrictions or nuisance parameters do not introduce multiple
  minimizers.

Audit questions:

- Does `g_0(theta)=0` have multiple roots?
- Does the weighting matrix remove identifying directions?
- Is local rank being used as global identification?

## Jacobian Rank

Let

```tex
G = \partial g_0(theta_0)/\partial theta'.
```

For standard GMM asymptotic normality, verify:

- `G` is `q x p`,
- `rank(G)=p` under the relevant metric,
- `G'WG` is nonsingular,
- sample Jacobian converges to `G` if it is used,
- weak identification or near singularity is ruled out if Wald inference is
  claimed.

Audit questions:

- Which matrix is inverted?
- Are dimensions compatible?
- Are eigenvalues bounded away from zero in the limit?

## Asymptotic Normality

A standard linear representation is

```tex
sqrt(n)(\hat theta_n-theta_0)
= -(G'WG)^{-1}G'W sqrt(n)\hat g_n(theta_0)+o_p(1).
```

Check:

- consistency is already proved,
- first-order condition or argmin expansion is valid,
- `sqrt(n)\hat g_n(theta_0)=>N(0,S)`,
- `\hat W_n ->p W`,
- `G'WG` is nonsingular,
- local moment expansion remainder is negligible.

General asymptotic variance:

```tex
V = (G'WG)^{-1}G'WSWG(G'WG)^{-1}.
```

Audit questions:

- Is `S` a long-run, clustered, heteroskedastic, or iid variance?
- Is the sign irrelevant because the covariance squares the linear map?
- Is the proof claiming the optimal variance or just a valid variance?

## Optimal Weighting

For efficient two-step GMM:

- define `S = Var_limit(sqrt(n)\hat g_n(theta_0))`,
- require `S` nonsingular, or state a generalized inverse argument explicitly,
- show `\hat S ->p S`,
- use `W=S^{-1}`,
- covariance reduces to `(G'S^{-1}G)^{-1}`.

Audit questions:

- Does the estimated optimal weight use residuals from a consistent first step?
- Is HAC or cluster structure included in `\hat S` when needed?
- Is the model overidentified and are overidentification tests using the right
  weighting?

## Sandwich Variance

For non-optimal GMM or robust inference, audit:

- bread: `A=G'WG`,
- meat: `G'WSWG`,
- covariance: `A^{-1}(G'WSWG)A^{-1}`,
- plug-in estimators for `G`, `W`, and `S` are consistent,
- dependence and clustering are reflected in `S`.

Common failures:

- using `(G'WG)^{-1}` as if `W=S^{-1}`,
- omitting rank of `G`,
- using iid `S` under serial dependence,
- using a nonoptimal `J` test reference distribution without adjustment.
