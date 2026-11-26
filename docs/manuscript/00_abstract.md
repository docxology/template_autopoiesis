## Abstract

`template_autopoiesis` is a combinatoric grammar that **deterministically generates
whole runnable projects** — not files or snippets, but complete, independently
testable child repositories with their own kernel source, tests, analysis
entry point, and manuscript. A single integer seed plus a grammar of orthogonal
slots (primitive domain, analytical track, section set, and three
presentation/provenance slots) selects one child from a combinatoric product
space of {{PRODUCT_SIZE}} nominal ({{EFFECTIVE_PRODUCT_SIZE}} content-distinct)
configurations, via a SHA-256 digest of the seed and slot identity — with no
random-number generator anywhere in the expansion path.

Project generators routinely claim completeness, determinism, and
traceability without making any of the three independently checkable. This
exemplar treats each claim as a structural property to verify rather than a
rhetorical one to assert: `verify_child()` recomputes a tree hash from the
files actually on disk and compares it against the recorded provenance,
rather than trusting a value the same run wrote down; an honesty manifest
inspects the live source AST to confirm every claim in this manuscript
resolves to a real function in a real file; and a per-domain mutation gate
checks that the acceptance tests reject a constant-success stub before
trusting that they accept the real kernel. The same discipline governs this
document itself — every number below is substituted at render time from a
live measurement rather than hand-typed as a literal.

Across {{DOMAIN_COUNT}} heterogeneous primitive domains
({{DOMAIN_BULLETS}}), {{TEST_COUNT}} tests exercise both fixed ground-truth
checks and Hypothesis-driven property invariants at {{COVERAGE_PCT}}% statement and branch
coverage, with an explicit negative control per domain distinguishing the
real kernel from a deliberately-wrong one.

### Generation pipeline

![Seeded grammar expansion produces a specification, then a child tree. Verification recomputes the tree hash before QR sealing.](../../output/figures/generation-pipeline.png){#fig:generation-pipeline width=85%}

### Grammar product space

![In the shipped grammar, five domains, three tracks, and three section sets yield 45 effective cells. The reserved slots expand the nominal space to 360 cells.](../../output/figures/grammar-product.png){#fig:grammar-product width=85%}

- **Domain count**: {{DOMAIN_COUNT}}
- **Effective product size**: {{EFFECTIVE_PRODUCT_SIZE}}
- **Total product size**: {{PRODUCT_SIZE}}
- **Reserved slots**: {{RESERVED_SLOT_COUNT}} (`{{RESERVED_SLOT_NAMES}}`)
- **Grammar hash**: `{{GRAMMAR_HASH}}`
- **Tests**: {{TEST_COUNT}} · **Coverage**: {{COVERAGE_PCT}}%
