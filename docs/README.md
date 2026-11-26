# template_autopoiesis documentation

A seeded grammar selects a specification, materializes a runnable child tree,
and verifies that tree against its provenance before optional QR sealing.

- [Setup, usage, and verification](usage.md) covers the standalone CLI,
  vendoring boundaries, and the branch-coverage gate.
- [Grammar syntax](SYNTAX.md) describes slots, reserved options, seed, and
  dependency configuration. The [live configuration](manuscript/config.yaml)
  also defines the manuscript metadata and analysis order.
- [Source verification contract](SPEC.md) records the Phase 10 requirements.
- [Manuscript](manuscript/README.md) lists sections, references, and source
  assets. [Build the manuscript](manuscript-build.md) for PDF and HTML.
- [Historical records](archive/README.md) preserve prior audits and backlog.

See the [source](../src/), [script reference](../scripts/README.md),
and [tests](../tests/) for implementation details. Published records and
release identifiers are listed in the [repository README](../README.md).
