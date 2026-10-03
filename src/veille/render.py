"""Render the processed stories as a single static HTML page."""

import argparse
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from jinja2 import Environment, PackageLoader, select_autoescape

from veille.collect import collect
from veille.config import OTHER_THEME, load_sources, load_themes
from veille.enrich import enrich
from veille.models import Source, Story, Theme
from veille.process import classify, process

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
) -> str:
    env = Environment(
        loader=PackageLoader("veille", "templates"),
        autoescape=select_autoescape(enabled_extensions=("html", "j2")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["french_date"] = french_date
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
            sections.append((anchor, name, items, colour))
    return env.get_template("page.html.j2").render(
        sections=sections,
        count=len(stories),
        sources=sources,
        unavailable=unavailable,
        generated_at=generated_at,
        repository_url=REPOSITORY_URL,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Veille IA page.")
    parser.add_argument("--output", type=Path, default=Path("site"))
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    sources, themes = load_sources(), load_themes()
    collected = collect(sources)
    if not collected.articles:
        logging.error("No article collected: the page is not generated")
        return 1  # the workflow stops here, the previous page stays online
    now = datetime.now(UTC)
    stories = process(collected.articles, now, themes)
    if not stories:
        logging.error("No article in the last 7 days: the page is not generated")
        return 1  # same as above: an empty page never replaces the previous one
    # missing excerpts read from the article pages (D18), then used for the themes like the others
    stories = classify(enrich(stories), themes)
    args.output.mkdir(parents=True, exist_ok=True)
    page = render_page(stories, themes, sources, collected.unavailable, now)
    (args.output / "index.html").write_text(page, encoding="utf-8")
    print(f"Page written to {args.output / 'index.html'} ({len(stories)} stories)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
