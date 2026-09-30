"""Load and validate the source list (config/sources.yaml)."""

from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

from veille.models import Source

DEFAULT_SOURCES_PATH = Path("config/sources.yaml")
FIELDS = ("id", "name", "feed_url", "site_url", "language", "trust_level")


class ConfigError(ValueError):
    """The source configuration is invalid."""


def load_sources(path: Path = DEFAULT_SOURCES_PATH) -> list[Source]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    entries = data.get("sources")
    if not isinstance(entries, list) or not entries:
        raise ConfigError(f"{path}: 'sources' must list at least one source")

    sources: list[Source] = []
    seen: set[str] = set()
    for position, entry in enumerate(entries, start=1):
        label = entry.get("id", f"#{position}") if isinstance(entry, dict) else f"#{position}"
        if not isinstance(entry, dict):
            raise ConfigError(f"{path}: source {label} must be a mapping")
        missing = [name for name in FIELDS if name not in entry]
        if missing:
            raise ConfigError(f"{path}: source {label} is missing: {', '.join(missing)}")
        if entry["trust_level"] not in (1, 2, 3):
            level = entry["trust_level"]
            raise ConfigError(
                f"{path}: source {label} has trust_level {level!r}, expected 1, 2 or 3"
            )
        if entry["id"] in seen:
            raise ConfigError(f"{path}: duplicate source id {entry['id']}")
        seen.add(entry["id"])
        timezone = entry.get("timezone", "UTC")
        try:
            ZoneInfo(timezone)
        except (ZoneInfoNotFoundError, ValueError, TypeError):
            raise ConfigError(f"{path}: source {label} has unknown timezone {timezone!r}") from None
        sources.append(Source(**{name: entry[name] for name in FIELDS}, timezone=timezone))
    return sources
