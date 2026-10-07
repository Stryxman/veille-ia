"""Data model shared by the collection, processing and rendering steps."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Source:
    id: str
    name: str
    feed_url: str
    site_url: str
    language: str
    trust_level: int
    timezone: str = "UTC"  # used for feed dates that carry no offset (D15)


@dataclass(frozen=True)
class Article:
    title: str
    link: str
    source: Source
    published: datetime | None  # UTC; None when the feed gives no date
    summary: str
    language: str


@dataclass(frozen=True)
class Story:
    """One piece of news: the retained article plus the duplicates grouped under it."""

    article: Article
    date: datetime  # publication date, or collection time when unknown (D11)
    date_is_known: bool
    also_covered: tuple[Article, ...] = ()
    theme: str = "Autres"


@dataclass(frozen=True)
class Theme:
    name: str
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class Synthesis:
    """Summary of one theme, checked: every sentence cites the theme's cards ([n])."""

    text: str
    model: str  # shown under the summary, e.g. "Mistral, mistral-small-latest"


@dataclass(frozen=True)
class SynthesisConfig:
    enabled: bool
    provider: str  # shown on the page, e.g. "Mistral"
    base_url: str  # OpenAI-compatible API, https only
    model: str
    timeout_seconds: float  # one request
    budget_seconds: float  # all themes of one run
