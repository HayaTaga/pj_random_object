# Test: GMM Asymptotic Normality

## User Prompt

Audit the following GMM asymptotic normality proof. Check theorem invocations,
rank conditions, and variance formula.

## Theorem Or Proof Draft

Let `hat theta_n` minimize
`hat g_n(theta)' W_n hat g_n(theta)`. Assume `hat theta_n ->p theta_0`,
`sqrt(n) hat g_n(theta_0) => N(0,S)`, and `W_n ->p W`. A Taylor expansion gives
`hat g_n(hat theta_n)=hat g_n(theta_0)+G(hat theta_n-theta_0)+o_p(n^{-1/2})`.
Therefore

```tex
sqrt(n)(hat theta_n-theta_0)
=-(G'WG)^{-1}G'W sqrt(n)hat g_n(theta_0)+o_p(1),
```

so the estimator is asymptotically normal.

## Expected Audit Behavior

- Verdict should be `incomplete`.
- Target convergence statement should be
  `sqrt(n)(hat theta_n-theta_0) => N(0,V)`.
- The audit should verify the moment CLT, weighting matrix convergence, local
  expansion, and Slutsky step.
- The audit should catch missing rank and nonsingularity conditions:
  `rank(G)=p`, `G'WG` nonsingular, and any positive definiteness needed for `W`
  or `S`.
- The audit should ask whether the first-order condition or argmin expansion is
  justified.
- The audit should not silently assume optimal weighting.
- Minimal repair should state the additional sufficient rank, nonsingularity,
  moment differentiability, and variance conditions, then give the sandwich
  variance `V=(G'WG)^{-1}G'WSWG(G'WG)^{-1}` unless `W=S^{-1}` is verified.
