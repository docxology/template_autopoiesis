# AGENTS.md — docs/ (template_autopoiesis)

## Layout

- `README.md` — human entry point (what this repo is, directory map, run/test)
- `AGENTS.md` — this file: conventions for maintaining docs/

## Key modules (pointer, not duplication)

The full module inventory lives in `../AGENTS.md`. See
[the documentation index](README.md), [grammar syntax](SYNTAX.md), and
[the source contract](SPEC.md).

## Conventions observed in this repo

- Pipeline stages: grammar → spec → materialize → verify → seal; each stage
  is recompute-verified (see `src/verify.py`, `src/sealing.py`).
- Honesty manifest: structural evidence is declared and checked
  (`src/honesty.py`); do not weaken it when editing docs or content.
- Integrity hashing: `sha256_text()` / `sha256_bytes()` / Merkle root
  (`src/integrity.py`).
- Business logic in `src/`; `scripts/` are thin orchestrators.
- Decision memory and verifier hardening follow the monorepo rule
  referenced at the top of `../AGENTS.md`.

## Maintaining these docs

Keep current guides concise and grounded in repository files. Do not duplicate module-level rules here.
