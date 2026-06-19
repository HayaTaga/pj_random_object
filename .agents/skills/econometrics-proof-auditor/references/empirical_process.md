# Empirical Process

Use this file to audit uniform laws, stochastic equicontinuity, and weak
convergence for indexed function classes. The main proof risk is replacing
pointwise statements with uniform or random-index statements without the needed
function-class conditions.

## Objects

Require explicit definitions:

- function class `Fcal={f_theta: theta in Theta}` or local class,
- envelope `F` such that `|f|<=F` for all `f in Fcal`,
- empirical measure `P_n` and population measure `P`,
- empirical process `G_n f=sqrt(n)(P_n-P)f`,
- metric or semimetric, often `L_2(P)`,
- measurability convention: ordinary probability or outer probability.

Audit questions:

- What exactly is indexed by `theta`?
- Is the class deterministic or random?
- What norm is used for the supremum?

## ULLN

To justify

```tex
sup_{f in Fcal}|(P_n-P)f|=o_p(1),
```

verify at least one valid route:

- finite class plus LLN for each element,
- VC, monotone, Lipschitz-parametric, or other manageable class,
- entropy or bracketing condition with integrable envelope,
- compact parameter space plus stochastic equicontinuity and pointwise LLN,
- local ULLN on a shrinking neighborhood after localization.

Check:

- envelope moment is finite,
- dependence structure matches the theorem,
- supremum is measurable or the result is stated in outer probability.

Audit questions:

- Which theorem gives the supremum convergence?
- Does pointwise convergence appear where ULLN is needed?
- Is the envelope integrable under the same distribution?

## Stochastic Equicontinuity

A typical target is

```tex
sup_{d(s,t)<=delta_n}|G_n(f_s-f_t)|=o_p(1)
```

for `delta_n -> 0`, or an analogous unscaled version.

Check:

- metric `d` is stated,
- random index satisfies `d(\hat t,t_0)=o_p(1)`,
- local entropy, bracketing, Lipschitz, or moment condition controls increments,
- envelope for increments is integrable or square-integrable as required,
- the rate of the neighborhood and process fluctuation is compatible.

Audit questions:

- Is the proof replacing `f_{\hat theta}` by `f_{theta_0}`?
- Is the empirical process equicontinuous under the metric used by consistency?
- Does the local class shrink fast enough?

## Function Class Conditions

Common sufficient routes:

- finite-dimensional smooth parametric class with compact parameter space and
  integrable Lipschitz envelope,
- VC-subgraph or VC-type class with appropriate envelope moments,
- entropy integral finite for Donsker claims,
- bracketing entropy small enough for GC or Donsker target,
- monotone or bounded-variation class where a known class theorem applies.

Do not label these as necessary unless the proof proves necessity. They are
sufficient conditions for the chosen route.

Audit questions:

- Is the class GC, Donsker, or only pointwise LLN/CLT?
- Is the class changing with `n`?
- Are indicators discontinuous in a way that requires boundary probability
  control?

## Envelope Functions

For an envelope `F`, check:

- `|f|<=F` for every function in the class,
- moment condition matches the theorem: `PF<infty`, `PF^2<infty`, or stronger,
- for local differences, use an increment envelope if needed,
- unbounded envelopes require explicit integrability or tail control,
- under dependence, envelope conditions alone do not replace mixing or other
  dependence assumptions.

Audit questions:

- Is the envelope deterministic and measurable?
- Does the proof use boundedness when only integrability is assumed?
- Is the envelope valid uniformly over the whole parameter set?

## Measurability

For uncountable classes, verify one of:

- the supremum is measurable,
- the class is pointwise measurable/separable,
- results are stated using outer probability or outer expectation,
- the proof restricts to a countable dense subclass with a valid approximation.

Audit questions:

- Is `sup_{f in Fcal}` a random variable?
- Does the cited theorem use outer probability notation?
- Has the proof silently converted outer convergence into ordinary convergence?

## Outer Probability

Use outer probability when measurability is not established:

- `X_n=o_{P^*}(1)` means outer probability convergence to zero,
- avoid applying ordinary expectation or conditioning to nonmeasurable objects,
- when moving back to ordinary probability, state the separability or
  measurability argument.

Audit questions:

- Is the final theorem stated in ordinary probability while the proof only gives
  outer probability?
- Is that acceptable for the estimator, which may be measurable even if a
  supremum used in the proof is not?

## Pointwise Versus Uniform

Flag these as gaps:

- `P_n f_theta -> P f_theta` for each fixed `theta` used to control
  `sup_theta`,
- CLT for each fixed `theta` used as weak convergence in `ell^\infty(Theta)`,
- continuity of `f_theta` in `theta` used without an integrable modulus,
- consistency of `\hat theta` used to replace random-index empirical processes
  without stochastic equicontinuity.

Audit questions:

- What step needs uniformity?
- Is the index fixed before seeing the data?
- Would the proof still work if `theta` were replaced by a random
  `\hat theta_n`?
