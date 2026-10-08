"""Load and validate the configuration (sources, themes, summaries)."""

from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

from veille.models import Source, SynthesisConfig, Theme

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


DEFAULT_THEMES_PATH = Path("config/themes.yaml")
OTHER_THEME = "Autres"


def load_themes(path: Path = DEFAULT_THEMES_PATH) -> list[Theme]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    entries = data.get("themes") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise ConfigError(f"{path}: 'themes' must list at least one theme")
    themes: list[Theme] = []
    for position, entry in enumerate(entries, start=1):
        name = entry.get("name") if isinstance(entry, dict) else None
        if not isinstance(name, str) or not name.strip():
            raise ConfigError(f"{path}: theme #{position} needs a name")
        reserved = name.strip().casefold() == OTHER_THEME.casefold()
        if reserved or name in {t.name for t in themes}:
            raise ConfigError(f"{path}: theme name {name!r} is duplicated or reserved")
        keywords = entry.get("keywords")
        valid = isinstance(keywords, list) and keywords
        if not valid or not all(isinstance(k, str) and k.strip() for k in keywords):
            raise ConfigError(f"{path}: theme {name} needs a non-empty list of keywords")
        themes.append(Theme(name=name, keywords=tuple(keywords)))
    return themes


DEFAULT_SYNTHESIS_PATH = Path("config/synthesis.yaml")
SYNTHESIS_FIELDS = ("enabled", "provider", "base_url", "model", "timeout_seconds", "budget_seconds")


def load_synthesis_config(path: Path = DEFAULT_SYNTHESIS_PATH) -> SynthesisConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: expected a mapping")
    missing = [name for name in SYNTHESIS_FIELDS if name not in data]
    if missing:
        raise ConfigError(f"{path}: missing: {', '.join(missing)}")
    if not str(data["base_url"]).startswith("https://"):
        raise ConfigError(f"{path}: base_url must use https")  # the key travels in a header
    return SynthesisConfig(**{name: data[name] for name in SYNTHESIS_FIELDS})
