"""Process collected articles: clean, keep recent ones, group duplicates, classify by theme."""

import html
import re
from dataclasses import replace
from datetime import datetime, timedelta

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
