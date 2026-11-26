"""Mermaid content invariant: reserved slot values must not leak into emitted content."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from src.grammar import RESERVED_SLOTS, load_grammar

PROJECT_ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


DIAGRAM_DIR = PROJECT_ROOT / "docs" / "manuscript" / "figures"


def _all_manuscript_mds() -> list[Path]:
    ms_dir = PROJECT_ROOT / "docs" / "manuscript"
    return sorted(ms_dir.glob("*.md"))


# ---------------------------------------------------------------------------
# Reserved slot values must not appear in Mermaid diagrams as data values
# (They can appear in comments or as labels, but not as raw slot option values
#  driving behavior)
# ---------------------------------------------------------------------------


RESERVED_SLOT_OPTIONS = {
    "figure_profile": ["mermaid_only", "mermaid_plus_plots", "full"],
    "qr_profile": ["figure", "page", "both", "full_encode"],
    "integrity_profile": ["sha256", "sha256_512", "sha512_merkle", "merkle_kmyth"],
}


def test_manuscript_mds_exist():
    mds = _all_manuscript_mds()
    assert len(mds) >= 5, f"Expected ≥5 manuscript md files, got {len(mds)}"


def test_mermaid_sources_and_rasters_are_present():
    manuscript = "\n".join(path.read_text() for path in _all_manuscript_mds())
    names = ("generation-pipeline", "grammar-product", "generation-methods")
    for name in names:
        assert (DIAGRAM_DIR / f"{name}.mmd").is_file()
        assert (DIAGRAM_DIR / f"{name}.png").is_file()
        assert f"output/figures/{name}.png" in manuscript


@pytest.mark.parametrize(
    "slot,options",
    [
        ("qr_profile", RESERVED_SLOT_OPTIONS["qr_profile"]),
        ("integrity_profile", RESERVED_SLOT_OPTIONS["integrity_profile"]),
    ],
)
def test_reserved_slot_options_not_in_mermaid(slot, options):
    """Reserved slot option strings should not appear as node labels in Mermaid blocks."""
    for source in DIAGRAM_DIR.glob("*.mmd"):
        for opt in options:
            pattern = rf"\[{re.escape(opt)}\]"
            assert not re.search(pattern, source.read_text()), (
                f"Reserved slot option '{opt}' appears as a node label in {source.name}"
            )


def test_grammar_reserved_slots_are_named():
    g = load_grammar(PROJECT_ROOT)
    reserved_names = {s.name for s in g.reserved_slots}
    for slot in RESERVED_SLOTS:
        assert slot in reserved_names


def test_grammar_loads_cleanly():
    g = load_grammar(PROJECT_ROOT)
    assert g.grammar_hash is not None
    assert len(g.grammar_hash) == 16
