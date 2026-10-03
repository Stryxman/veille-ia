"""Complete missing excerpts with the start of the article text (D18).

Some feeds give no text at all (Hugging Face), and the description these pages publish for
social networks is generic ("A Blog post by … on Hugging Face"). For the retained stories
without an excerpt, the main text of the article page is extracted (trafilatura) and its start
becomes the excerpt. A page that cannot be read never stops the update: the story keeps an
empty excerpt.
"""

import logging
import urllib.request
from collections.abc import Callable
from dataclasses import replace

import trafilatura

from veille.collect import USER_AGENT
from veille.models import Story
from veille.process import clean_text, excerpt

MAX_PAGE_BYTES = 2 * 1024 * 1024  # enough for the start of the article text
TIMEOUT_SECONDS = 10

logger = logging.getLogger(__name__)

PageFetcher = Callable[[str], bytes]


def fetch_page(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return response.read(MAX_PAGE_BYTES)


def page_text(data: bytes) -> str:
    """Main text of an article page, without navigation, side blocks or comments."""
    text = trafilatura.extract(
        data,  # raw bytes: trafilatura reads the page's own encoding (e.g. ISO-8859-15)
        include_comments=False,
        include_tables=False,
        favor_precision=True,
    )
    return text or ""


def _without_title(text: str, title: str) -> str:
    """Drop the leading lines that only repeat the article title (already shown above)."""
    lines = text.splitlines()
    while lines and lines[0].strip().casefold() == title.strip().casefold():
        lines.pop(0)
    return "\n".join(lines)


def enrich(stories: list[Story], fetch: PageFetcher | None = None) -> list[Story]:
    fetch = fetch or fetch_page  # looked up at call time, so tests can replace it
    result = []
    for story in stories:
        if not story.article.summary:
            try:
                text = _without_title(page_text(fetch(story.article.link)), story.article.title)
                summary = excerpt(clean_text(text))
            except Exception as error:  # a page must never stop the update (CdC §6, D18)
                logger.warning("%s: article text not read (%s)", story.article.link, error)
                summary = ""
            if summary:
                story = replace(story, article=replace(story.article, summary=summary))
        result.append(story)
    return result
