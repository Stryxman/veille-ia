"""Render the processed stories as a single static HTML page."""

import argparse
import logging
import os
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from jinja2 import Environment, PackageLoader, select_autoescape

from veille.collect import CollectResult, collect
from veille.config import OTHER_THEME, load_sources, load_synthesis_config, load_themes
from veille.enrich import enrich
from veille.models import Source, Story, Synthesis, Theme
from veille.process import classify, process
from veille.synthesize import KEY_VARIABLE, segments, synthesize

PARIS = ZoneInfo("Europe/Paris")
MONTHS = (
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre",
)  # fmt: skip
REPOSITORY_URL = "https://github.com/Stryxman/veille-ia"
COLOURS = 6  # theme colours defined in the template (.c1 to .c6)


def french_date(moment: datetime, with_time: bool = False) -> str:
    local = moment.astimezone(PARIS)
    day = "1er" if local.day == 1 else str(local.day)
    text = f"{day} {MONTHS[local.month - 1]} {local.year}"
    return f"{text} à {local:%H:%M}" if with_time else text


def render_page(
    stories: list[Story],
    themes: list[Theme],
    sources: list[Source],
    unavailable: list[Source],
    generated_at: datetime,
    syntheses: dict[str, Synthesis] | None = None,
) -> str:
    env = Environment(
        loader=PackageLoader("veille", "templates"),
        autoescape=select_autoescape(enabled_extensions=("html", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["french_date"] = french_date
    env.filters["citations"] = segments
    # anchor and colour follow the position in the configuration, so they stay stable when a
    # theme is empty; beyond COLOURS themes, colours start again (themes configurable, O5)
    names = [
        (f"theme-{index + 1}", theme.name, f"c{index % COLOURS + 1}")
        for index, theme in enumerate(themes)
    ]
    names.append(("theme-autres", OTHER_THEME, "other"))
    sections = []
    for anchor, name, colour in names:
        items = [story for story in stories if story.theme == name]
        if items:  # no empty section nor table of contents entry
            sections.append((anchor, name, items, colour, (syntheses or {}).get(name)))
    return env.get_template("page.html.j2").render(
        sections=sections,
        count=len(stories),
        sources=sources,
        unavailable=unavailable,
        generated_at=generated_at,
        repository_url=REPOSITORY_URL,
    )


def source_lines(collected: CollectResult, sources: list[Source]) -> list[str]:
    unavailable = {source.id for source in collected.unavailable}
    per_source = Counter(article.source.id for article in collected.articles)
    return [
        f"{source.id} {source.name}: "
        + ("unavailable" if source.id in unavailable else f"{per_source[source.id]} article(s)")
        for source in sources
    ]


def durations_line(durations: dict[str, float]) -> str:
    return "Durations: " + ", ".join(f"{step} {secs:.1f} s" for step, secs in durations.items())


def _failed(
    message: str, collected: CollectResult, sources: list[Source], durations: dict[str, float]
) -> int:
    # a failed run still reports its sources and timings: that is when they matter most
    print("\n".join([*source_lines(collected, sources), durations_line(durations)]))
    logging.error(message)
    return 1  # the workflow stops here, the previous page stays online


def run_summary(
    collected: CollectResult,
    sources: list[Source],
    stories: list[Story],
    without_excerpt: int,
    durations: dict[str, float],
) -> str:
    """Run report printed in the workflow log (#39): what was read, kept and how long it took."""
    lines = source_lines(collected, sources)
    completed = without_excerpt - sum(1 for story in stories if not story.article.summary)
    classified = sum(1 for story in stories if story.theme != OTHER_THEME)
    lines += [
        f"Stories kept (7 days): {len(stories)}",
        f"Excerpts completed from article pages: {completed} of {without_excerpt}",
        f"Classified outside '{OTHER_THEME}': {100 * classified / len(stories):.0f} %",
        durations_line(durations),
    ]
    return "\n".join(lines)


def synthesis_line(
    syntheses: dict[str, Synthesis], stories: list[Story], themes: list[Theme]
) -> str:
    expected = sum(1 for theme in themes if any(story.theme == theme.name for story in stories))
    return f"Summaries: {len(syntheses)} of {expected}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Veille IA page.")
    parser.add_argument("--output", type=Path, default=Path("site"))
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    sources, themes = load_sources(), load_themes()
    durations: dict[str, float] = {}
    start = time.perf_counter()
    collected = collect(sources)
    durations["collect"] = time.perf_counter() - start
    if not collected.articles:
        return _failed(
            "No article collected: the page is not generated", collected, sources, durations
        )
    now = datetime.now(UTC)
    start = time.perf_counter()
    stories = process(collected.articles, now, themes)
    durations["process"] = time.perf_counter() - start
    if not stories:  # an empty page never replaces the previous one
        message = "No article in the last 7 days: the page is not generated"
        return _failed(message, collected, sources, durations)
    without_excerpt = sum(1 for story in stories if not story.article.summary)
    start = time.perf_counter()
    # missing excerpts read from the article pages (D18), then used for the themes like the others
    stories = classify(enrich(stories), themes)
    durations["enrich"] = time.perf_counter() - start
    start = time.perf_counter()
    # one summary per theme from a free model (V2, #43); no key or any failure: no summary
    key = os.environ.get(KEY_VARIABLE, "")
    syntheses = synthesize(stories, themes, load_synthesis_config(), key)
    durations["synthesize"] = time.perf_counter() - start
    start = time.perf_counter()
    args.output.mkdir(parents=True, exist_ok=True)
    page = render_page(stories, themes, sources, collected.unavailable, now, syntheses)
    (args.output / "index.html").write_text(page, encoding="utf-8")
    durations["render"] = time.perf_counter() - start
    print(run_summary(collected, sources, stories, without_excerpt, durations))
    print(synthesis_line(syntheses, stories, themes))
    print(f"Page written to {args.output / 'index.html'} ({len(stories)} stories)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
