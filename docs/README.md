# docs/ — template_autopoiesis

Human-facing documentation entry point. Agent-facing rules:
[`AGENTS.md`](AGENTS.md). Root overview: [`../README.md`](../README.md).

## What this repo is

`template_autopoiesis` (v1.0.1, MIT) is a combinatoric project generator:
a grammar deterministically emits complete child projects from a seeded
expansion. Architecture: grammar → spec → materialize → verify → seal
(from `../AGENTS.md`).

## Directory map

- `src/` — grammar parsing, expansion, materialization, verification,
  sealing, honesty manifest, integrity hashing, manuscript contract and
  figure writers (module inventory in `../AGENTS.md`; per-module notes in
  `src/README.md`)
- `scripts/` — thin orchestrators over `src/`
- `tests/` — pytest suite (`testpaths = ["tests"]`, `pythonpath = [".", "src"]`
  per `../pyproject.toml`)
- `manuscript/` — section sources for the PDF manuscript
- `data/`, `output/` — pipeline inputs and generated artifacts
- `docs/` — this documentation folder

## How to run / test

The CLI (`src/cli.py`) exposes: `enumerate`, `expand`, `sample`,
`materialize`, `verify`, `honesty`. Tests: `pytest` (configured in
`../pyproject.toml`; dev extras: pytest, pytest-cov, hypothesis). Exact
invocation of monorepo pipeline stages lives in the root monorepo
documentation; this standalone checkout carries its own `pyproject.toml`.

## Maintenance

Docs here are short and factual, derived from the repo's own files. Update
the map above when top-level layout changes.
