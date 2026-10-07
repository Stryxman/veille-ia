"""Complete missing excerpts with the start of the article text (D18).

Some feeds give no text at all (Hugging Face), and the description these pages publish for
social networks is generic ("A Blog post by … on Hugging Face"). For the retained stories
without an excerpt, the main text of the article page is extracted (trafilatura) and its start
becomes the excerpt. A page that cannot be read never stops the update: the story keeps an
empty excerpt.
"""

import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from dataclasses import replace

import trafilatura

from veille.collect import USER_AGENT
from veille.models import Source, Story
from veille.process import excerpt

MAX_PAGE_BYTES = 2 * 1024 * 1024  # enough for the start of the article text
TIMEOUT_SECONDS = 10
BUDGET_SECONDS = 120  # all article pages of one run; the remaining stories keep no excerpt
SPACES = re.compile(r"\s+")

logger = logging.getLogger(__name__)

PageFetcher = Callable[[str], bytes]


def _host(url: str) -> str:
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def _same_site(url: str, site_host: str) -> bool:
    host = _host(url)
    return bool(host) and (host == site_host or host.endswith("." + site_host))


class SameSiteRedirect(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only to http(s), on the host of the redirected request or a subdomain.

    Stricter than the source's site: a page on blog.example redirected to example is refused.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        scheme = urllib.parse.urlsplit(newurl).scheme.lower()
        if scheme not in {"http", "https"} or not _same_site(newurl, _host(req.full_url)):
            raise urllib.error.HTTPError(newurl, code, "redirect outside the site", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(SameSiteRedirect)


def fetch_page(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with _OPENER.open(request, timeout=TIMEOUT_SECONDS) as response:
        return response.read(MAX_PAGE_BYTES)


def _site_hosts(source: Source) -> set[str]:
    return {host for host in (_host(source.site_url), _host(source.feed_url)) if host}


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


def _excerpt_from_page(story: Story, fetch: PageFetcher) -> str:
    link = story.article.link
    if not any(_same_site(link, host) for host in _site_hosts(story.article.source)):
        logger.warning("%s: not on the source's site, page not read", link)
        return ""  # never read an address the source does not own (R13)
    try:
        text = _without_title(page_text(fetch(link)), story.article.title)
    except Exception as error:  # a page must never stop the update (CdC §6, D18)
        logger.warning("%s: article text not read (%s)", link, error)
        return ""
    # already plain text: only spaces are normalised, quoted tags and entities are kept
    return excerpt(SPACES.sub(" ", text).strip())


def enrich(
    stories: list[Story],
    fetch: PageFetcher | None = None,
    budget: float = BUDGET_SECONDS,
    clock: Callable[[], float] = time.monotonic,
) -> list[Story]:
    fetch = fetch or fetch_page  # looked up at call time, so tests can replace it
    start = clock()
    result = []
    for story in stories:
        if not story.article.summary and clock() - start < budget:
            summary = _excerpt_from_page(story, fetch)
            if summary:
                story = replace(story, article=replace(story.article, summary=summary))
        result.append(story)
    return result
