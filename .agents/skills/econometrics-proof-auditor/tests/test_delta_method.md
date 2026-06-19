# Test: Delta Method

## User Prompt

Audit the following delta method argument. Decide whether the stated conclusion
is justified and give the smallest repair.

## Theorem Or Proof Draft

Suppose `sqrt(n)(hat theta_n-theta_0) => N(0,V)`. Let
`g(theta)=abs(theta)` and suppose `theta_0=0`. Since `g` is continuous,

```tex
sqrt(n)(g(hat theta_n)-g(theta_0)) => N(0,V).
```

## Expected Audit Behavior

- Verdict should be `incorrect` or `incomplete` with a clear reason; the
  ordinary delta method does not apply at the kink.
- Target convergence statement should be the claimed distributional convergence
  of `sqrt(n)(abs(hat theta_n)-0)`.
- The audit should distinguish CMT from the delta method: continuity gives
  `abs(hat theta_n) ->p 0`, not the stated normal limit.
- The audit should catch missing differentiability at `theta_0=0`.
- The audit should avoid adding differentiability silently.
- Minimal repair should either change the conclusion to
  `sqrt(n)abs(hat theta_n) => abs(Z)` for `Z ~ N(0,V)` in the scalar case, or
  add a differentiability condition by changing the example to a point where
  `g` is differentiable.
