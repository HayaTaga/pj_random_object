# Test: Missing Rank Condition

## User Prompt

Audit the following estimating-equation asymptotic normality proof. Focus on
rank, nonsingularity, and hidden assumptions.

## Theorem Or Proof Draft

Let `hat theta_n` solve `psi_n(theta)=0`. Assume `hat theta_n ->p theta_0` and

```tex
sqrt(n) psi_n(theta_0) => N(0,S).
```

A Taylor expansion gives

```tex
0 = psi_n(theta_0)+A(hat theta_n-theta_0)+o_p(n^{-1/2}).
```

Therefore

```tex
sqrt(n)(hat theta_n-theta_0) => N(0,A^{-1}SA^{-1}).
```

## Expected Audit Behavior

- Verdict should be `incomplete`.
- Target convergence statement should be
  `sqrt(n)(hat theta_n-theta_0) => N(0,A^{-1}SA^{-1})`.
- The audit should catch missing nonsingularity of `A`; if `A` is not symmetric,
  it should also correct the covariance form to `A^{-1}S(A^{-1})'`.
- The audit should catch missing rank/full-column-rank conditions if `A` is a
  Jacobian rather than a square Hessian.
- The audit should ask whether Taylor expansion is valid locally and whether
  pointwise derivative convergence is enough at the random estimator.
- The audit should not silently assume `A` is invertible.
- Minimal repair should add the needed nonsingularity or full-rank condition,
  local derivative convergence, and the correct sandwich covariance formula.
