# AGENTS: `scripts/` — Thin Orchestrators

## Thin-orchestrator contract

Every script in this directory is a thin orchestrator ONLY: path bootstrap,
logging, and delegated calls into `src/` entrypoints. Business, data, plot, and
analysis logic lives in `src/` (importable and covered by `tests/`). A script
that needs logic beyond bootstrap + delegation gets that logic moved into
`src/` first.

The analysis-stage allowlist in `docs/manuscript/config.yaml`
(`analysis.scripts`) is the pipeline's own ordering authority — the numeric
filename prefixes are cosmetic and do NOT define execution order.
`02_measure_test_coverage.py` intentionally runs first so the coverage data
consumed downstream by `01_generate_manuscript_assets.py` and
`z_generate_manuscript_variables.py` is fresh.

## Inventory

| Script | Role | Delegates to |
|--------|------|--------------|
| `01_generate_manuscript_assets.py` | Analysis stage: figures + registry | `src/manuscript_figures.py`, `src/project_paths.py`, shared `infrastructure.documentation.generated_figure_registry` |
| `02_measure_test_coverage.py` | Analysis stage: coverage measurement | `src/manuscript_variables.py::measure_test_summary`, `src/project_paths.py` |
| `04_seal.py` | Analysis stage: seal latest child | `scripts/seal_child.py::seal_child`, `src/project_paths.py` |
| `autopoiesis.py` | CLI entry point | `src/cli.py::main` |
| `generate_cover_art.py` | Analysis stage: cover art | `src/grammar.py`, `src/cover_art.py::render_cover` |
| `realize_archetypes.py` | Realization: one child per domain | `src/grammar.py`, `src/expand.py`, `src/materialize.py`, `src/realize.py` |
| `realize_child_full.py` | Realization: single full pipeline | `src/grammar.py`, `src/expand.py`, `src/materialize.py`, `src/realize.py` |
| `seal_child.py` | CLI/library helper: seal named child | `src/sealing.py::build_payload`, `src/verify.py::verify_child` |
| `z_generate_manuscript_variables.py` | Analysis stage: variable injection | `src/manuscript_variables.py`, shared `infrastructure.rendering.manuscript_injection` |

## Gotchas

- **Allowlist, not prefixes.** `docs/manuscript/config.yaml::analysis.scripts`
  lists exactly the seven argument-free analysis entry points in dependency
  order. `autopoiesis.py` (requires a subcommand) and `seal_child.py` (requires
  `<child_root>`) are deliberately excluded — analysis discovery would fail on
  them (see the comment block above `analysis:` in `config.yaml`).
- **Fail-closed inputs.** `01_generate_manuscript_assets.py` raises
  `FileNotFoundError` when `output/data/coverage_full.json` is missing and only
  writes `figure_registry.json` after every referenced PNG exists. Run
  `02_measure_test_coverage.py` first.
- **`04_seal.py` sys.path shadowing.** This directory has no `__init__.py`, so
  `from scripts.seal_child import ...` silently resolves to the repo-root
  `scripts` package found on `sys.path`. The script inserts its own directory
  and imports `seal_child` directly — keep it that way.
- **Shared `infrastructure` package.** `01_` and `z_` import `infrastructure.*`
  (bootstrap inserts the monorepo root via `parents[2]`/`parents[4]`). In a
  standalone checkout the package is absent, so those paths only run inside the
  template monorepo; `tests/test_manuscript_assets_script.py` skips with a
  matching reason.
- **`__pycache__/`.** Appears here when `04_seal.py` imports `seal_child`; it
  is local runtime state, gitignored, and never a source entry point.

## See also

- [`../AGENTS.md`](../AGENTS.md)
- [`README.md`](README.md)
- [`../docs/manuscript/config.yaml`](../docs/manuscript/config.yaml)
