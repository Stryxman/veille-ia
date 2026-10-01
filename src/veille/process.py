"""Process collected articles: clean, keep recent ones, group duplicates, classify by theme."""

import html
import re
from dataclasses import replace
from datetime import datetime, timedelta
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from veille.models import Article, Story

WINDOW = timedelta(days=7)
EXCERPT_LENGTH = 300

# Only real HTML markup is removed: quoted text such as "<think>" or "a < b" is kept.
HTML_TAG = re.compile(
    r"<!--.*?-->|<(script|style)\b[^>]*>.*?</\1\s*>"
    r"|</?(?:a|abbr|article|aside|audio|b|blockquote|br|button|caption|center|cite|code|dd|del"
    r"|details|div|dl|dt|em|figcaption|figure|font|footer|h[1-6]|header|hr|i|iframe|img|input|ins"
    r"|label|li|main|mark|nav|ol|p|picture|pre|q|s|section|small|source|span|strike|strong|sub"
    r"|summary|sup|svg|table|tbody|td|th|thead|time|tr|tt|u|ul|video)\b[^>]*>",
    re.IGNORECASE | re.DOTALL,
)
SPACES = re.compile(r"\s+")


def clean_text(raw: str) -> str:
    text = raw
    for _ in range(2):  # some feeds escape their HTML twice
        text = html.unescape(HTML_TAG.sub(" ", text))
    return SPACES.sub(" ", text).strip()


def excerpt(text: str, limit: int = EXCERPT_LENGTH) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit + 1]
    space = cut.rfind(" ")
    cut = cut[:space] if space > 0 else text[:limit]
    return cut.rstrip(" ,;:.-–—") + "…"


def clean_article(article: Article) -> Article:
    return replace(
        article,
        title=clean_text(article.title),
        summary=excerpt(clean_text(article.summary)),
    )


def select_recent(articles: list[Article], now: datetime) -> list[Story]:
    stories = []
    for article in articles:
        date_is_known = article.published is not None
        date = article.published if date_is_known else now  # collection time (D11)
        if date < now - WINDOW:
            continue
        stories.append(
            Story(article=clean_article(article), date=date, date_is_known=date_is_known)
        )
    return stories


TITLE_SIMILARITY = 0.9
PUNCTUATION = re.compile(r"[^\w\s]")


def normalize_link(link: str) -> str:
    parts = urlsplit(link.strip())
    query = urlencode(
        [
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_")
        ]
    )
    return urlunsplit(
        (parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), query, "")
    )


def normalize_title(title: str) -> str:
    return SPACES.sub(" ", PUNCTUATION.sub(" ", title.lower())).strip()


def _rank(story: Story) -> tuple[int, datetime]:
    # D10: best trust level first, then the earliest publication
    return (story.article.source.trust_level, story.date)


def group_duplicates(stories: list[Story]) -> list[Story]:
    links = [normalize_link(s.article.link) for s in stories]
    titles = [normalize_title(s.article.title) for s in stories]
    parent = list(range(len(stories)))

    def root(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(stories)):
        for j in range(i + 1, len(stories)):
            same_link = links[i] == links[j]
            if same_link or SequenceMatcher(None, titles[i], titles[j]).ratio() >= TITLE_SIMILARITY:
                parent[root(j)] = root(i)

    groups: dict[int, list[int]] = {}
    for i in range(len(stories)):
        groups.setdefault(root(i), []).append(i)

    result = []
    for members in groups.values():
        members.sort(key=lambda i: _rank(stories[i]))
        lead, *others = members
        others = [i for i in others if links[i] != links[lead]]  # same article, not a second source
        result.append(
            replace(stories[lead], also_covered=tuple(stories[i].article for i in others))
        )
    return result
