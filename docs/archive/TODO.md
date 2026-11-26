# template_autopoiesis TODO

This backlog is future-only. Completed validation and dated review evidence are preserved in
`docs/maintenance/exemplar-backlog-history.md` (monorepo-only path)
or in source-owned generated receipts. Each active row must retain a stable ID, size, dependency,
next action, proving artifact, acceptance command, and negative control; absence of an owner or external receipt
keeps a capability blocked rather than silently promoting it.

## Backlog operating rules

- Keep deterministic and offline defaults unchanged unless an upcoming row explicitly scopes an opt-in.
- Do not close a row until its producer, artifact, consumer, gate, and failing negative control are present.
- Treat unavailable network, LLM, container, formal-tool, and publication paths as explicit skips
  or blockers.
- Re-derive counts and receipts from live source data; never copy measurements into this planning file.

## Integrity and template-status gaps

- Keep the grammar the single source of truth in `docs/manuscript/config.yaml` (`autopoiesis:` block) and all generation logic in `src/` (`grammar.py`, `expand.py`, `materialize.py`, `realize.py`, `sealing.py`, `verify.py`, `honesty.py`) — scripts stay thin orchestrators.
- Keep materialization routed through `src/emit_templates.py::emit_all` for
  every child-facing analysis, test, project, and manuscript file so standalone
  emitters and generated children cannot drift silently.
- Keep provenance recompute-based: verification must re-derive the tree hash from disk at check time and never trust a recorded manifest hash.

## Configurable-surface gaps

- Keep the placeholder-safe `docs/manuscript/config.yaml.example` synchronized with the live config shape, including the list-form slot and dependency syntax.
- The optional `archetype_filters` mapping is the fork-owned selector for materializing a subset of the combinatoric product space; keep its values schema-validated and included in the grammar digest.

## Documentation and signposting gaps

- Keep README and `SYNTAX.md` clear that Stage 02 expands the grammar and materializes/verifies children, while Stage 03 renders the descriptive manuscript PDF.
- `SPEC.md` Phase 10 and `docs/manuscript/preamble.md` are source-owned inputs to the deterministic manuscript contract; keep the checklist, explicit fences, and renderer-qualified receipt synchronized.

## Dependency-mode gaps

- `dep_mode="template"` remains intentionally loud (`NotImplementedError`) until a seam contract is defined that does not require parent infrastructure at child runtime.

## Test and validator gaps

- Keep figure fallback handling explicit for empty arrays, and require
  malformed or under-specified grammar shapes to fail before expansion with real
  negative controls.
- Keep mutation coverage per domain and permit an explicit skip only when a domain has no negative-control primitive; a second primitive must be used when available so the meta-gate cannot become green-by-construction.

## Minor upcoming

| ID | Status | Size | Dependency | Next action / unblock condition | Proving artifact | Acceptance command | Negative control |
| --- | --- | --- | --- | --- | --- | --- | --- |
No active rows are currently scoped at this size.

## Medium upcoming

| ID | Status | Size | Dependency | Next action / unblock condition | Proving artifact | Acceptance command | Negative control |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AUTOPOIESIS-SPEC-1` | blocked-tool | Medium | Pinned renderer and visual QA toolchain | Install or pin the renderer, or record its unavailable receipt; run the explicit Phase 10 visual gate and attach the tool-qualified receipt. | `SPEC.md` Phase 10 checklist + renderer receipt | `uv run pytest projects/templates/template_autopoiesis/tests -q --no-cov --timeout=120` | missing renderer must report blocked-tool; fenced preamble/spec mismatch must fail |

## Major upcoming

| ID | Status | Size | Dependency | Next action / unblock condition | Proving artifact | Acceptance command | Negative control |
| --- | --- | --- | --- | --- | --- | --- | --- |
No active rows are currently scoped at this size.

## Backlog status

Rows remain active until the acceptance command and negative control pass in the same source revision.
A blocked row is a deliberate boundary, not a skipped success.

## Workflowz review — 2026-11-10

Source review at base `eff704e8` (bounded packet; no code executed). Rows follow the backlog rules
above: deterministic/offline defaults stay unchanged, unavailable optional decoders are explicit
skips, and no row closes without its acceptance probe and negative control passing together.

- [ ] `WFZ-20261110-1` · P1 · Make the QR seal fail loudly when `qrcode` is unavailable instead of silently emitting a non-decodable 5×5 checkerboard.
  - Outcome: a missing required `qrcode` dependency raises a clear error at seal time (or produces a seal that verification rejects); a generated `seal.json` QR is always a real, decodable encoding of the payload, matching the "Seal — embeds spec hash + tree hash as a QR code" contract. No silent production substitute.
  - Evidence: `src/sealing.py:21-34` (docstring fallback + `except ImportError` returning a 5×5 checkerboard), `pyproject.toml:14-20` (`qrcode` is a required dependency, not optional), `tests/test_seal_child.py:84-87` (`qr_size >= 5  # at minimum the fallback 5x5` accepts the stub as a passing seal), `README.md:67`, `README.md:69-73` (anti green-by-construction stance this fallback undercuts).
  - Acceptance (from repo root):
    ```bash
    uv run python - <<'PY'
    import sys
    sys.modules["qrcode"] = None  # force ImportError for the required dep
    from src.sealing import qr_matrix
    try:
        m = qr_matrix("payload")
    except ImportError:
        print("loud: missing qrcode surfaces as ImportError")
    else:
        raise SystemExit(f"still silently substituting: returned {len(m)}x{len(m)} matrix")
    PY
    uv run pytest tests/test_seal_child.py tests/test_cover_art.py -q
    ```
    With `qrcode` installed, the seal path still passes; with it blocked, the old 5×5 checkerboard is no longer returned and no `seal.json` verifying clean can be produced from it.
  - Negative control: blocking `qrcode` must not yield a 5×5 matrix that `tests/test_seal_child.py` accepts as a valid seal; remove the "at minimum the fallback 5x5" allowance or convert it to an explicit opt-in test mark.
  - Dependencies/constraints: `qrcode` stays a required dependency per `pyproject.toml:18`; do not weaken the manifest. If a minimal/no-qrcode test mode is wanted it must be an explicit opt-in per TODO.md "Backlog operating rules" (TODO.md:11-14), never the silent default. Coordinate with `read_qr_matrix`/`verify_seal` so a rejected seal fails verification rather than passing.

- [ ] `WFZ-20261110-2` · P1 · Stop `materialize()` from silently writing an empty vendored stub module (plus a stub test) when the real infrastructure source is absent; fail loudly or record provenance that verification rejects.
  - Outcome: when the vendored source file cannot be found at build time, `materialize()` raises an error naming the missing module/path (or marks the child so `verify_child_full` fails), instead of emitting `vendored/<module>.py` containing only "Vendored stub … # Source not found at build time." Children can no longer ship non-functional vendored modules backed by placeholder `test_<module>_stub` tests while materialization/verification report success.
  - Evidence: `src/materialize.py:120-127` (path arithmetic at 122; silent stub fallback at 125-127), `src/materialize.py:155-161` (`_vendor_test_file` generates "Stub tests for vendored {module}" with `def test_{module}_stub():`), and the anti-test-theater / provenance invariants this bypasses at `TODO.md:19-23`, `AGENTS.md:49-50`, `README.md:69-73`.
  - Acceptance (from repo root), using the vendoring dep_mode literal and fixtures already exercised in `tests/test_deps_vendoring.py`:
    ```bash
    uv run python - <<'PY'
    import pathlib, tempfile
    from tests.test_deps_vendoring import _make_grammar  # same helper as tests/test_deps_vendoring.py:145-146
    from src.expand import expand
    from src.materialize import materialize
    from src.verify import verify_child_full
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        # vendoring dep_mode exactly as used in tests/test_deps_vendoring.py fixtures
        spec = expand(_make_grammar(domain="optimization", dep_mode="vendor", deps=["glossary_gen"]))
        # template_root whose parent.parent.parent has no infra source (src/materialize.py:122)
        template_root = root / "a" / "b" / "c"
        template_root.mkdir(parents=True)
        try:
            result = materialize(spec, out_root=root / "children", template_root=template_root)
        except Exception as exc:
            print("loud: missing vendored source ->", type(exc).__name__)
        else:
            report = verify_child_full(result.root)
            assert not report.all_passed, "child with stubbed vendored module must not verify clean"
    PY
    uv run pytest tests/test_deps_vendoring.py tests/test_materialize.py -q
    ```
    Add a regression test capturing this and keep the happy path (real source present) vendoring actual bytes.
  - Negative control: an unresolvable vendored source must not produce a child that passes `verify_child_full`; the previous behavior (successful materialize + `vendored/<module>.py` stub + generated stub test) must now fail.
  - Dependencies/constraints: preserve the intentional `dep_mode="template"` `NotImplementedError` boundary (`TODO.md:37`; `tests/test_deps_vendoring.py:145-172`) and keep monorepo path resolution at `src/materialize.py:122` working for the standalone and monorepo layouts (standalone absence should surface as a blocker/skip per `TODO.md:11-14`, not a stub). Do not break routing through `src/emit_templates.py::emit_all` (`TODO.md:20-22`). Substitute the vendoring dep_mode literal from the test fixtures if it differs from `"vendor"`.

- [ ] `WFZ-20261110-3` · P2 · Make `read_qr_matrix` distinguish "decoder unavailable / decode error" from "no QR payload found" instead of collapsing every exception to `""`.
  - Outcome: a missing optional `pyzbar` decoder or an unexpected decode error raises (or returns a distinct status) so callers and seal verification can tell an undecodable-environment failure apart from a genuinely absent/invalid payload; only a real "no data" decode returns the empty result.
  - Evidence: `src/sealing.py:44-51` (`except Exception:  # noqa: BLE001 … pass` then `return ""`), with the decode call at `src/sealing.py:44-48`.
  - Acceptance (from repo root):
    ```bash
    uv run python - <<'PY'
    import sys
    sys.modules["pyzbar"] = None        # simulate optional decoder being unavailable
    sys.modules["pyzbar.pyzbar"] = None
    from src.sealing import read_qr_matrix, qr_matrix
    m = qr_matrix("seal-payload")
    try:
        out = read_qr_matrix(m)
    except Exception as exc:
        print("decoder-unavailable surfaced:", type(exc).__name__)
    else:
        assert out != "" or out is None, "no-data sentinel is fine only when a decoder ran"
        raise SystemExit("decoder-unavailable still collapsed to the no-data sentinel")
    PY
    uv run pytest tests/test_seal_child.py -q
    ```
    When `pyzbar` is installed, a real `qr_matrix`/`read_qr_matrix` roundtrip still decodes the payload; when absent, that roundtrip is an explicit skip, not a silent pass.
  - Negative control: with the decoder import blocked, the result must not equal the value returned for a valid-image-but-undecodable matrix when a decoder is present.
  - Dependencies/constraints: `pyzbar` is optional and deliberately absent from `pyproject.toml:14-20`; do not add it as a hard dependency and do not change offline/deterministic defaults (`TODO.md:11-14`). Keep the change scoped to error signalling so `verify_seal` can report an unavailable decoder distinctly from a failed seal.
