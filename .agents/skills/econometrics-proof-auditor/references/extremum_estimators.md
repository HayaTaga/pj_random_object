# Extremum Estimators

Use this file as an internal proof-audit checklist for estimators defined by
maximizing or minimizing a sample criterion. Fix the sign convention first; the
statements below use maximization.

## Objects

Require explicit definitions:

- parameter space `Theta` and metric `d`,
- true value or target `theta_0`,
- sample criterion `Q_n(theta)`,
- population criterion `Q(theta)`,
- estimator `hat theta_n`,
- optimization error `r_n`,
- probability convention for suprema and argmax objects.

For maximization, approximate optimization means

```tex
Q_n(\hat\theta_n) >= \sup_{\theta\in\Theta} Q_n(\theta)-r_n.
```

For consistency, usually require `r_n=o_p(1)` on the unscaled criterion. For
local asymptotic normality, the optimization error must be negligible on the
local criterion scale.

## Consistency: compact parameter space route

Claim:
Let `\hat\theta_n` approximately maximize `Q_n(\theta)` over `\Theta`. Under
suitable conditions,

```tex
\hat\theta_n \to_p \theta_0.
```

Sufficient conditions:

1. `(\Theta,d)` is a compact metric space.
2. `Q:\Theta\to\mathbb R` is continuous.
3. `Q` has a unique maximizer at `\theta_0`.
4. Uniform convergence:

```tex
\sup_{\theta\in\Theta}|Q_n(\theta)-Q(\theta)|=o_p(1).
```

5. Approximate maximization:

```tex
Q_n(\hat\theta_n)\ge \sup_{\theta\in\Theta}Q_n(\theta)-r_n,
\qquad r_n=o_p(1).
```

6. Measurability or outer-probability convention is handled if needed.

Derived condition:
For every `\epsilon>0`,

```tex
\sup_{d(\theta,\theta_0)\ge \epsilon}Q(\theta)<Q(\theta_0).
```

This separated maximum condition follows from compactness, continuity, and
unique maximization, provided the complement of the `\epsilon`-ball is compact
and nonempty. If the complement is empty, the separation step is vacuous for
that `\epsilon`.

Audit questions:

- Is the convergence pointwise or uniform?
- Is the approximate maximization error defined?
- Is `\Theta` compact, or is there a localization/coercivity argument?
- Is separation assumed directly or derived?
- Is the convergence statement meaningful under the topology on `\Theta`?
- Are suprema and argmax objects measurable, or is outer probability used?

Condition classification:

- compactness, continuity, uniqueness, uniform convergence, and approximate
  optimization are additional sufficient assumptions if not stated.
- separated maximum is a derived condition when compactness, continuity, and
  unique maximization are stated and the complement set is compact.
- measurability or outer probability is a technical measurability condition.
- do not mark separation as simply missing until checking whether it is derived.

## Consistency: noncompact route

Compactness can be replaced by localization, tightness, coercivity, or sieve
restrictions. The proof must explicitly show why the estimator cannot escape to
regions where the population criterion is inferior.

Accepted replacements include:

- localization: `P(\hat\theta_n\in K)\to 1` for a compact `K`, followed by the
  compact-route argument on `K`,
- tightness: the estimator is shown to lie in bounded sets with high
  probability, and the criterion is controlled on those sets,
- coercivity: `Q(theta)` is uniformly below `Q(theta_0)` outside large compact
  sets,
- sieve restrictions: optimization over `Theta_n` is paired with approximation
  and no-escape conditions.

Audit questions:

- What prevents `\hat\theta_n` from leaving every compact set?
- Is the ULLN global, local, or only on the sieve?
- Is separation proved outside neighborhoods of `\theta_0` and outside large
  compact sets?
- Does the approximate optimization error remain negligible after localization?
- Is the limiting target still `theta_0`, or only a pseudo-true/sieve target?

## Common incorrect proof pattern

Pattern:
Pointwise convergence `Q_n(\theta)\to_p Q(\theta)` plus uniqueness of the
maximizer of `Q` is used to conclude

```tex
\hat\theta_n\to_p\theta_0.
```

Why invalid:
Pointwise convergence does not control the random criterion uniformly over
`\Theta`, so maximizers may behave discontinuously. The random maximizer can
move to values of `theta` where the pointwise LLN gives no simultaneous control.

Audit response:

- verdict is usually `incorrect` if the proof makes this transition directly,
  or `incomplete` if the intended route is clear but the uniformity/localization
  conditions are omitted,
- identify pointwise-versus-uniform convergence explicitly,
- classify uniqueness as stated if given,
- classify separation as derived only if compactness and continuity are also
  available,
- classify ULLN and compactness/localization as missing or sufficient repair
  conditions when not stated.

## Minimal repair template

Use this skeleton for the compact-route repair.

Fix `\epsilon>0` and define the outside set

```tex
A_\epsilon=\{\theta\in\Theta:d(\theta,\theta_0)\ge\epsilon\}.
```

By compactness, continuity, and unique maximization, if `A_\epsilon` is nonempty
there is a separated maximum gap: for some `eta_\epsilon>0`,

```tex
\sup_{\theta\in A_\epsilon}Q(\theta)\le Q(\theta_0)-2\eta_\epsilon.
```

Uniform convergence gives, with probability approaching one,

```tex
\sup_{\theta\in\Theta}|Q_n(\theta)-Q(\theta)|\le \eta_\epsilon/2.
```

Approximate maximization gives, with probability approaching one,

```tex
Q_n(\hat\theta_n)\ge Q_n(\theta_0)-\eta_\epsilon/2.
```

On these events, any `\hat\theta_n\in A_\epsilon` contradicts the separated
gap. Hence

```tex
P(d(\hat\theta_n,\theta_0)\ge\epsilon)\to 0.
```

Since `\epsilon>0` was arbitrary, `\hat\theta_n\to_p\theta_0`.

## Asymptotic normality checklist

To conclude

```tex
\sqrt n(\hat\theta_n-\theta_0) => N(0,V),
```

verify:

- consistency or local tightness at the required rate,
- interior solution or KKT conditions for constrained problems,
- first-order condition or valid argmax expansion,
- score or gradient CLT at `theta_0`,
- Hessian/Jacobian convergence to a nonsingular limit,
- local stochastic equicontinuity or uniform expansion of the derivative,
- scaled remainder is `o_p(1)`,
- variance formula matches the sampling scheme and misspecification status.

Audit questions:

- Does the proof establish a rate before using a local expansion?
- Is the first-order condition valid with probability approaching one?
- Is the Hessian limit negative definite for maximization or positive definite
  for minimization?
- Is the matrix being inverted nonsingular?
- Is the variance model-based, robust, clustered, or long-run?

## Local quadratic expansion

A common route is to define `h=\sqrt n(\theta-\theta_0)` and show, uniformly
over bounded `h`,

```tex
n\{Q_n(\theta_0+h/\sqrt n)-Q_n(\theta_0)\}
= h'Z_n - (1/2)h'Hh + o_p(1),
```

where `Z_n=>Z` and `H` is positive or negative definite according to the sign
convention.

Check:

- the expansion is uniform over compact `h` sets,
- `Z_n` has a CLT,
- `H` has the right definiteness,
- the maximizer of the limiting quadratic is unique,
- the approximate optimizer is tight on the `sqrt(n)` scale,
- behavior outside bounded local `h` sets is controlled.

Audit questions:

- Is the local criterion scaled correctly?
- Does the limiting quadratic have a unique optimizer?
- Does the proof control the stochastic remainder uniformly?
- Does local asymptotic normality rely on a compact-route consistency result or
  a separate rate/localization argument?
