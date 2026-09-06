# Scripts

Thin orchestrators for `template_autopoiesis`: path bootstrap + logging +
delegated calls into `src/` entrypoints. See [`AGENTS.md`](AGENTS.md) for the
thin-orchestrator contract, gotchas, and the ordering authority.

| Script | Purpose | Delegates to | Run command |
|--------|---------|--------------|-------------|
| `01_generate_manuscript_assets.py` | Generate the four manuscript figures + fail-closed `figure_registry.json` | `src/manuscript_figures.py`, `src/project_paths.py`, shared `infrastructure.documentation.generated_figure_registry` | `uv run python scripts/01_generate_manuscript_assets.py` |
| `02_measure_test_coverage.py` | Run the test suite; cache TEST_COUNT/COVERAGE_PCT + per-module coverage | `src/manuscript_variables.py::measure_test_summary`, `src/project_paths.py` | `uv run python scripts/02_measure_test_coverage.py` |
| `04_seal.py` | Seal the most-recently materialized child | `scripts/seal_child.py::seal_child`, `src/project_paths.py` | `uv run python scripts/04_seal.py` |
| `autopoiesis.py` | Project CLI: expand/materialize/verify/honesty/enumerate/sample | `src/cli.py::main` | `uv run python scripts/autopoiesis.py <subcommand>` |
| `generate_cover_art.py` | Render the cover-art PNG from the grammar seed | `src/grammar.py`, `src/cover_art.py::render_cover` | `uv run python scripts/generate_cover_art.py` |
| `realize_archetypes.py` | Materialize + validate one child per primitive domain | `src/grammar.py`, `src/expand.py`, `src/materialize.py`, `src/realize.py` | `uv run python scripts/realize_archetypes.py` |
| `realize_child_full.py` | Full realize pipeline (spec → materialize → validate → analyze) for one child | `src/grammar.py`, `src/expand.py`, `src/materialize.py`, `src/realize.py` | `uv run python scripts/realize_child_full.py` |
| `seal_child.py` | Write `seal.json` (spec hash + payload) for a named child | `src/sealing.py::build_payload`, `src/verify.py::verify_child` | `uv run python scripts/seal_child.py output/children/<child>` |
| `z_generate_manuscript_variables.py` | Generate manuscript variables JSON + resolve `{{TOKEN}}` placeholders | `src/manuscript_variables.py`, shared `infrastructure.rendering.manuscript_injection` | `uv run python scripts/z_generate_manuscript_variables.py` |

Execution order is set by the `analysis.scripts` allowlist in
`docs/manuscript/config.yaml` — the numeric filename prefixes are cosmetic
(`02_measure_test_coverage.py` runs first by design, so downstream consumers
see fresh coverage data).
