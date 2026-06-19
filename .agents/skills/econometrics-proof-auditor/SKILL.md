---
name: econometrics-proof-auditor
description: "Use for graduate-level econometric theory proof work: checking proofs, repairing incomplete proofs, constructing proofs from assumptions, auditing theorem invocations, and identifying missing assumptions. Covers consistency, asymptotic normality, extremum estimators, M-estimation, GMM, LLN, CLT, ULLN, stochastic equicontinuity, continuous mapping, Slutsky, delta method, identification, rank and nonsingularity, measurability, and outer probability."
---

# Econometrics Proof Auditor

Use this skill for econometric theory proof tasks: checking proofs, repairing incomplete proofs, constructing proofs from assumptions, auditing theorem invocations, and identifying missing assumptions.

Treat `corpus/pdfs/` as private source material: never move or copy PDFs into this skill, and do not reproduce long textbook passages. Use the corpus only to identify theorem locations, condition structures, and page references.

## Non-Negotiable Rules

- Do not say a proof is correct unless every nontrivial step is justified by stated assumptions or by a theorem whose conditions are verified.
- Do not introduce additional assumptions silently. Put them under `Additional Assumptions`.
- Classify every assumption or condition using the assumption taxonomy below.
- Do not change the target convergence mode silently. If the proof only supports a weaker mode, mark the gap and repair explicitly.
- Do not treat pointwise convergence as uniform convergence.
- Do not invoke CMT, Slutsky, delta method, LLN, CLT, ULLN, stochastic equicontinuity, argmax, GMM, or M-estimation theorems without checking their conditions.
- Do not call a condition necessary unless it is proved necessary for the stated conclusion. Otherwise call it sufficient for the proof.
- Do not list a condition as simply `missing` if it may be derived from stated assumptions. Say whether it is missing and must be added, derivable but not shown, sufficient but not necessary, or technical and convention-dependent.

## Assumption Taxonomy

Classify each assumption or condition into exactly one category:

1. `Stated assumption`: explicitly given in the theorem or proof.
2. `Derived condition`: not stated directly, but derivable from stated assumptions by a standard lemma.
3. `Additional sufficient assumption`: not stated and not derivable, but sufficient to repair the proof.
4. `Necessary for this proof route`: required by the theorem or argument currently being used, though not necessarily required by every possible proof.
5. `Technical measurability condition`: measurability, separability, or outer-probability condition needed to make a supremum, argmax, or stochastic statement well-defined.
6. `Not necessary`: convenient but not required for the claim or proposed proof route.

In the condition classification table, put the taxonomy category in `role in proof`. Use `status` only to record whether the condition is stated, derived, missing, a sufficient repair, or technical.

For extremum-estimator consistency, distinguish these objects explicitly:

- uniqueness of the population optimizer,
- separated maximum condition,
- compactness of the parameter space,
- continuity of the population criterion,
- uniform convergence of the sample criterion,
- approximate optimization error,
- localization or coercivity in noncompact parameter spaces.

Do not say `unique maximizer is insufficient` without explaining which additional conditions are needed to derive or replace separation. For example, separation may be derived from compactness, continuity, and unique maximization on a metric space; otherwise it may need to be assumed or replaced by a local/coercive argument.

## Verdict Standard

Use exactly one verdict:

- `correct`: every nontrivial step is justified and theorem conditions are verified.
- `correct with minor gaps`: the proof is essentially valid, but needs small clarifications, labels, or routine verifications.
- `incomplete`: the route may be valid, but important steps, assumptions, or theorem conditions are missing.
- `incorrect`: at least one step is false, uses an inapplicable theorem, proves the wrong convergence mode, or cannot be repaired without changing the claim substantially.

When uncertain between two verdicts, choose the stricter one and explain what would upgrade it.

## Required Output Order

Always use this order.

1. `Verdict`
   - One of: `correct`, `correct with minor gaps`, `incomplete`, `incorrect`.
   - Add one sentence giving the decisive reason.
2. `Restated Claim`
   - State the theorem or proof target precisely.
3. `Notation and Assumptions`
   - Define objects, sample structure, parameter spaces, metrics, norms, filtrations, sigma fields, nuisance parameters, and stated assumptions.
   - List candidate assumptions and conditions; classify them fully in the condition classification table.
4. `Target Convergence Statement`
   - Specify the exact mode: a.s., in probability, distribution, stable, outer probability, weak convergence in a function space, stochastic equicontinuity, uniform convergence, or rate.
   - Specify normalization and limiting object.
5. `Step-by-Step Proof Audit`
   - Decompose the proof into atomic nontrivial steps.
   - For each step, state whether it is valid, unsupported, too strong, or false.
6. `Dependency Map`
   - For each nontrivial step, include:
     - proof step,
     - theorem or lemma used,
     - required conditions,
     - where each condition is verified,
     - whether the step is justified.
7. `Critical Gaps`
   - List missing assumptions, invalid theorem invocations, wrong convergence modes, measurability gaps, rate errors, or identification failures.
8. `Condition Classification Table`
   - Include columns:
     - condition,
     - status: `stated`, `derived`, `missing`, `sufficient repair`, or `technical`,
     - role in proof,
     - whether it is necessary for this proof route,
     - comment.
   - The comment must say if a condition is derivable but not shown, missing and must be added, sufficient but not necessary, technical and convention-dependent, or not necessary.
9. `Additional Assumptions`
   - State only assumptions needed for the repair.
   - Distinguish sufficient assumptions from necessary assumptions.
   - If no additional assumptions are needed, say so.
10. `Minimal Repair`
   - Give the smallest fix: add an assumption, weaken the conclusion, localize the argument, change the theorem, correct normalization, add a lemma, or revise the proof structure.
11. `Optional Polished Proof in LaTeX`
   - Include only if requested or clearly useful after the audit.

## Audit Checklist

Check these before giving the verdict:

- Consistency: identification, compactness/localization, continuity, ULLN, approximate optimizer.
- Asymptotic normality: expansion, score CLT, Hessian/Jacobian convergence, nonsingularity, remainder rate.
- Extremum estimators: argmax/argmin theorem, separation, stochastic equicontinuity, measurability of optimizer.
- M-estimation: differentiability or valid nonsmooth argument, sandwich variance, misspecification, nuisance effects.
- GMM: moment identification, weighting matrix limit, rank of Jacobian, long-run variance, overidentification distribution.
- LLN/CLT/ULLN: sample structure, dependence, triangular arrays, moments, envelopes, entropy, clustering or serial correlation.
- Stochastic equicontinuity: metric, local neighborhood, random indexing, empirical-process conditions.
- CMT/Slutsky/delta method: continuity set, tightness, differentiability, matrix inversion, normalization.
- Identification: uniqueness, local versus global identification, weighted identification, separation.
- Rank and nonsingularity: full rank, eigenvalues bounded away from zero, continuous inverse.
- Measurability and outer probability: uncountable suprema, separability, pointwise measurability, outer probability statements.

## References

Load only the relevant reference file:

- `references/theorem_index.md`: local theorem-card and corpus index conventions.
- `references/asymptotic_tools.md`: convergence, CLT, LLN, Slutsky, delta method, stochastic order.
- `references/extremum_estimators.md`: consistency and argmax/argmin proof audits.
- `references/gmm.md`: GMM consistency, asymptotic normality, weighting matrices, overidentification.
- `references/m_estimation.md`: score expansion, information matrices, sandwich variance, misspecification.
- `references/empirical_process.md`: GC/Donsker, entropy, stochastic equicontinuity, outer probability.
- `references/common_failures.md`: frequent proof gaps and minimal repairs.

## Scripts

- Extract text: `python3 .agents/skills/econometrics-proof-auditor/scripts/extract_pdf_text.py`
- Search extracted corpus: `python3 .agents/skills/econometrics-proof-auditor/scripts/search_corpus.py "uniform convergence"`
- Locate theorem candidates: `python3 .agents/skills/econometrics-proof-auditor/scripts/locate_theorem.py "argmax theorem"`
- Build theorem cards: `python3 .agents/skills/econometrics-proof-auditor/scripts/build_theorem_cards.py`
