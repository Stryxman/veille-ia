"""docs/sources.md and config/sources.yaml must describe the same sources (R10)."""

import re
from pathlib import Path

from veille.config import DEFAULT_SOURCES_PATH, load_sources

ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\|\s*(S\d+)\s*\|")
LINK = re.compile(r"\((https?://[^)\s]+)\)")


def documented_sources(text):
    """Return {feed_url: (id, trust_level)} from the 'Liste des sources' table."""
    rows = {}
    for line in text.splitlines():
        if not ROW.match(line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        feed_url = LINK.search(cells[6]).group(1)
        rows[feed_url] = (cells[0], int(cells[4]))
    return rows


def load():
    documented = documented_sources((ROOT / "docs/sources.md").read_text(encoding="utf-8"))
    configured = {
        s.feed_url: (s.id, s.trust_level) for s in load_sources(ROOT / DEFAULT_SOURCES_PATH)
    }
    return documented, configured


def test_every_configured_source_is_documented():
    documented, configured = load()
    missing = sorted(
        f"{ident} ({url})" for url, (ident, _) in configured.items() if url not in documented
    )
    assert not missing, f"Configured but not documented in docs/sources.md: {', '.join(missing)}"


def test_every_documented_source_is_configured():
    documented, configured = load()
    missing = sorted(
        f"{ident} ({url})" for url, (ident, _) in documented.items() if url not in configured
    )
    assert not missing, (
        f"Documented but not configured in config/sources.yaml: {', '.join(missing)}"
    )


def test_ids_and_trust_levels_match():
    documented, configured = load()
    mismatches = sorted(
        f"{url}: doc {documented[url]} vs config {configured[url]}"
        for url in documented.keys() & configured.keys()
        if documented[url] != configured[url]
    )
    assert not mismatches, "Id or trust level differs: " + "; ".join(mismatches)


def test_parser_reads_a_documented_row():
    row = (
        "| S9 | Name | FR | Type | 3 "
        "| [site](https://s.example/) | [feed](https://s.example/rss) | Why |"
    )
    assert documented_sources(row) == {"https://s.example/rss": ("S9", 3)}
