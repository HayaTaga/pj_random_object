# Test: Bad Proof Uniform Convergence

## User Prompt

Audit the following proof that claims uniform convergence. Focus on pointwise
versus uniform arguments and measurability.

## Theorem Or Proof Draft

For every fixed `theta in Theta`, the law of large numbers gives

```tex
P_n f_theta ->p P f_theta.
```

Taking the supremum over `theta`, it follows that

```tex
sup_{theta in Theta}|P_n f_theta-P f_theta| ->p 0.
```

This proves the uniform law of large numbers for the class
`{f_theta: theta in Theta}`.

## Expected Audit Behavior

- Verdict should be `incorrect`.
- Target convergence statement should be
  `sup_{theta in Theta}|P_n f_theta-P f_theta| ->p 0`.
- The audit should flag the invalid transition from pointwise convergence to
  uniform convergence.
- The audit should ask for a function-class condition such as finite class, VC
  type, entropy/bracketing, compact parametric Lipschitz class with envelope, or
  stochastic equicontinuity plus finite-net control.
- The audit should ask whether the supremum is measurable or whether outer
  probability is needed.
- Minimal repair should add a valid ULLN route and state the required envelope,
  measurability, and dependence conditions.
