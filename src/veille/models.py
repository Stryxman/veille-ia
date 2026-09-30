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


@dataclass(frozen=True)
class Article:
    title: str
    link: str
    source: Source
    published: datetime | None  # UTC; None when the feed gives no date
    summary: str
    language: str
