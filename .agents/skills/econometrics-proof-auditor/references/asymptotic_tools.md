# Asymptotic Tools

Use this file to audit limit arguments. The goal is not to summarize limit
theory; it is to force every asymptotic transition to name its object,
normalization, convergence mode, and theorem conditions.

## First Pass

For each asymptotic line, identify:

- object: scalar, vector, matrix, process, supremum, or random function,
- normalization: none, `sqrt(n)`, `a_n`, local parameter `h`,
- mode: a.s., `->p`, `=>`, stable, conditional, outer probability,
- index set: fixed, growing, compact, local, random, or function class,
- probability law: fixed law, triangular array, bootstrap, conditional law.

Do not accept a line that changes any of these silently.

## Stochastic Order

Check definitions against the proof's norm and probability law:

- `X_n=o_p(1)`: `X_n ->p 0`.
- `X_n=O_p(1)`: `{X_n}` is tight.
- `X_n=o_p(a_n)`: `X_n/a_n=o_p(1)`.
- `X_n=O_p(a_n)`: `X_n/a_n=O_p(1)`.
- vector or matrix statements need a stated norm; finite-dimensional norms are
  equivalent, but infinite-dimensional norms are not.
- uniform `o_p(1)` over `T`: `sup_{t in T}|X_n(t)|=o_p(1)`.
- local uniform `o_p(1)`: the supremum is over a shrinking or bounded local set;
  the set must be stated.

Useful algebra, only when products are well-defined:

- `o_p(1)+o_p(1)=o_p(1)`.
- `O_p(1)+O_p(1)=O_p(1)`.
- `o_p(1)O_p(1)=o_p(1)`.
- `O_p(a_n)O_p(b_n)=O_p(a_nb_n)`.
- `o_p(a_n)+O_p(a_n)=O_p(a_n)`, not `o_p(a_n)`.

Audit questions:

- Is the stochastic order scalar, vector, matrix, or uniform?
- Is the same probability law used on both sides?
- After multiplying by `sqrt(n)` or `a_n`, is the remainder still negligible?

## LLN

Use LLN only after verifying:

- sample structure: iid, independent non-identical, martingale difference,
  mixing, stationary ergodic, panel, cluster, spatial, or triangular array,
- centering: the population expectation exists and is the claimed limit,
- moments: integrability, uniform integrability, or envelope moment condition,
- indexing: fixed function, finite vector, parameter-indexed class, or growing
  dimension,
- mode: pointwise, uniform, a.s., in probability, or outer probability.

Common invalid move: fixed-`theta` LLN implies
`sup_theta |P_n f_theta-P f_theta|=o_p(1)`. It does not without a ULLN or a
separate finite-grid plus continuity argument.

Audit questions:

- Which LLN matches the dependence structure?
- Is the expectation finite under the stated assumptions?
- Is the claimed conclusion pointwise or uniform?

## CLT

Use CLT only after verifying:

- centering: `E X_i` or conditional mean is correctly removed,
- normalization: usually `sqrt(n)`, but may differ under dependence or weak
  identification,
- variance: finite limit exists; nonsingularity is checked if inversion or Wald
  inference follows,
- dependence: iid, martingale, mixing, cluster, HAC, spatial, or triangular
  array conditions match the theorem,
- moment condition: finite second moment, Lindeberg, Lyapunov, envelope, or
  theorem-specific condition,
- covariance estimator: homoskedastic, heteroskedastic, cluster, or long-run
  form matches the sampling scheme.

Audit questions:

- What is the exact random vector satisfying the CLT?
- Is the variance matrix `S` positive definite or only semidefinite?
- Does the proof need joint CLT with another statistic?

## Continuous Mapping

Check:

- input convergence mode and topology are stated,
- map is continuous at the limiting value with probability one,
- discontinuities are excluded: indicators at mass points, argmax without
  uniqueness, inverse at singular matrices, projections at boundary points,
- measurability is handled for random maps or suprema.

Audit questions:

- What is the map `g` and what is its domain topology?
- Is the limiting point in the continuity set?
- Is any matrix inverse justified by nonsingularity?

## Slutsky

Check:

- one term has a distributional limit,
- the replacing term converges in probability to a constant or deterministic
  matrix,
- the combined operation is continuous at the limit,
- joint convergence is available when both terms are random limits.

Invalid Slutsky uses:

- replacing a term with only `O_p(1)`,
- replacing a term that converges in distribution to a nonconstant random
  variable without joint convergence,
- inverting `A_n` from `A_n ->p A` without checking `A` nonsingular.

Audit questions:

- Which term is `o_p(1)` or `->p c`?
- Is the limiting multiplier deterministic?
- Is the dimension of every product conformable?

## Delta Method

Check:

- input statement: `r_n(T_n-theta_0) => Z`,
- map: `g` is differentiable at `theta_0` in the needed sense,
- derivative: `Dg(theta_0)` is the derivative used in the limit,
- nonzero derivative: if `Dg(theta_0)=0`, use a higher-order delta method or
  change the rate,
- functional setting: Hadamard or tangential differentiability is verified when
  the object is infinite-dimensional.

Conclusion form:

```tex
r_n\{g(T_n)-g(\theta_0)\} => Dg(\theta_0)Z.
```

Audit questions:

- Is ordinary differentiability enough, or is a functional delta method needed?
- Does the proof estimate the derivative, and if so is it consistent?
- Does the target rate survive the transformation?

## Taylor Expansion With Stochastic Remainder

For scalar or vector estimating equations, a valid expansion must state the
neighborhood and the remainder:

```tex
S_n(\hat\theta_n)
= S_n(\theta_0)+H_n(\theta_0)(\hat\theta_n-\theta_0)+R_n,
```

or

```tex
0 = S_n(\theta_0)+H_n(\bar\theta_n)(\hat\theta_n-\theta_0).
```

Check:

- `\hat\theta_n` is in the expansion neighborhood with probability approaching
  one,
- differentiability holds on that neighborhood,
- `H_n(\bar\theta_n) ->p H` or locally uniformly approaches `H`,
- `H` is nonsingular when solving for `\hat\theta_n-\theta_0`,
- scaled remainder is negligible: e.g. `sqrt(n)R_n=o_p(1)` or the exact
  normalization required by the proof.

Audit questions:

- Is the expansion deterministic, stochastic, pointwise, or uniform?
- Does pointwise Hessian convergence suffice for the random intermediate point?
- Is the remainder small after the proof's normalization?

## Invalid Convergence Transitions

Flag these immediately:

- `->p` used as a.s. convergence.
- pointwise convergence used as uniform convergence.
- `=>` to a nonconstant limit treated as `->p`.
- `O_p(1)` treated as `o_p(1)`.
- `o_p(1)` multiplied by an unbounded `O_p(a_n)` without rate control.
- componentwise convergence used for growing dimension without dimension
  control.
- convergence of `A_n` used to invert `A_n` without nonsingularity of the limit.
- weak convergence in a function space used without tightness or measurability.
- ordinary probability statements used for nonmeasurable suprema where outer
  probability is required.
