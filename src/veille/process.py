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
NUMBER = re.compile(r"\d+")


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


def _similar_titles(title: str, lead_title: str) -> bool:
    if NUMBER.findall(title) != NUMBER.findall(lead_title):
        return False  # D16: different versions, amounts or years are different news
    matcher = SequenceMatcher(None, title, lead_title)
    return (  # cheap upper bounds first: most pairs are far apart
        matcher.real_quick_ratio() >= TITLE_SIMILARITY
        and matcher.quick_ratio() >= TITLE_SIMILARITY
        and matcher.ratio() >= TITLE_SIMILARITY
    )


def group_duplicates(stories: list[Story]) -> list[Story]:
    # Stories are built in rank order, so the first member is the retained article (D10).
    # D16: a link already present in a story always joins it (checked first, in every story);
    # otherwise the title is compared with each story's retained article (no chaining).
    groups: list[tuple[set[str], str, list[Story]]] = []
    for story in sorted(stories, key=_rank):
        link = normalize_link(story.article.link)
        title = normalize_title(story.article.title)
        target = next((g for g in groups if link in g[0]), None)
        if target is None:
            target = next((g for g in groups if _similar_titles(title, g[1])), None)
        if target is None:
            groups.append(({link}, title, [story]))
        else:
            target[0].add(link)
            target[2].append(story)

    result = []
    for _, _, (lead, *others) in groups:
        listed = {lead.article.source.id}
        also_covered = []
        for other in others:
            if other.article.source.id not in listed:  # each other source once, never its own
                listed.add(other.article.source.id)
                also_covered.append(other.article)
        result.append(replace(lead, also_covered=tuple(also_covered)))
    return result
