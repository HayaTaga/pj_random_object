# Test: Extremum Consistency

## User Prompt

Audit the following consistency proof for an extremum estimator. Identify the
target convergence mode and give the minimal repair.

## Theorem Or Proof Draft

Let `hat theta_n` maximize `Q_n(theta)` over `Theta`. For every fixed `theta`,
`Q_n(theta) ->p Q(theta)`. Also `Q(theta_0) >= Q(theta)` for all `theta`.
Therefore `hat theta_n ->p theta_0`.

## Expected Audit Behavior

- Verdict should be `incomplete`.
- Target convergence statement should be `hat theta_n ->p theta_0`.
- The audit should distinguish pointwise convergence from uniform convergence.
- The audit should catch missing identification because the draft states only
  weak maximization, not unique maximization or separation.
- The audit should catch missing compactness or localization.
- The audit should ask whether `hat theta_n` is an exact or approximate
  maximizer and whether the optimization error is negligible.
- The audit should not silently add assumptions.
- Minimal repair should add sufficient conditions such as compact or localized
  `Theta`, uniform convergence of `Q_n` to `Q`, unique separated maximum at
  `theta_0`, and exact or approximate maximization with `o_p(1)` error.
