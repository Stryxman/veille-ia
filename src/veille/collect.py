"""Collect articles from the configured RSS/Atom feeds.

A failing source never stops the collection: it is reported as unavailable (R1).
"""

import calendar
import logging
import sys
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime

import feedparser

from veille.config import load_sources
from veille.models import Article, Source

USER_AGENT = "Mozilla/5.0 (compatible; veille-ia/0.1; +https://github.com/Stryxman/veille-ia)"
TIMEOUT_SECONDS = 20

logger = logging.getLogger(__name__)

Fetcher = Callable[[str], bytes]


class FeedError(Exception):
    """The downloaded document is not a usable RSS/Atom feed."""


@dataclass
class CollectResult:
    articles: list[Article] = field(default_factory=list)
    unavailable: list[Source] = field(default_factory=list)


def fetch_feed(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return response.read()


def _entry_date(entry) -> datetime | None:
    # RSS 2.0 uses pubDate (published); Atom and RSS 1.0 dc:date end up in "updated".
    for key in ("published_parsed", "updated_parsed"):
        value = entry.get(key)
        if value:
            return datetime.fromtimestamp(calendar.timegm(value), tz=UTC)
    return None


def parse_feed(data: bytes, source: Source) -> list[Article]:
    parsed = feedparser.parse(data)
    if not parsed.version:
        raise FeedError(f"{source.id}: not an RSS/Atom feed")
    articles = []
    for entry in parsed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        if not title or not link:
            continue
        articles.append(
            Article(
                title=title,
                link=link,
                source=source,
                published=_entry_date(entry),
                summary=entry.get("summary", ""),
                language=source.language,
            )
        )
    return articles


def collect(sources: list[Source], fetch: Fetcher = fetch_feed) -> CollectResult:
    result = CollectResult()
    for source in sources:
        try:
            result.articles.extend(parse_feed(fetch(source.feed_url), source))
        except Exception as error:  # any failure isolates this source only (R1)
            logger.warning("Source %s unavailable: %s", source.id, error)
            result.unavailable.append(source)
    return result


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    sources = load_sources()
    result = collect(sources)
    unavailable = {s.id for s in result.unavailable}
    for source in sources:
        if source.id in unavailable:
            print(f"{source.id} {source.name}: UNAVAILABLE")
        else:
            count = sum(1 for a in result.articles if a.source.id == source.id)
            print(f"{source.id} {source.name}: {count} articles")
    print(f"Total: {len(result.articles)} articles, {len(unavailable)} unavailable source(s)")
    return 0 if result.articles else 1


if __name__ == "__main__":
    sys.exit(main())
