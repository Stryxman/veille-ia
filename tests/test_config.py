from pathlib import Path

import pytest

from veille.config import (
    DEFAULT_SOURCES_PATH,
    DEFAULT_THEMES_PATH,
    OTHER_THEME,
    ConfigError,
    load_sources,
    load_themes,
)

ROOT = Path(__file__).resolve().parents[1]

VALID_ENTRY = """
  - id: X1
    name: Example
    feed_url: https://example.org/feed.xml
    site_url: https://example.org/
    language: en
    trust_level: 2
"""


def write(tmp_path, body):
    path = tmp_path / "sources.yaml"
    path.write_text("sources:\n" + body, encoding="utf-8")
    return path


def test_config_loads_the_six_project_sources():
    sources = load_sources(ROOT / DEFAULT_SOURCES_PATH)
    assert [s.id for s in sources] == ["S1", "S2", "S3", "S4", "S5", "S6"]
    assert [s.trust_level for s in sources] == [1, 1, 2, 2, 2, 2]
    assert {s.language for s in sources} == {"en", "fr"}
    assert {s.id: s.timezone for s in sources}["S6"] == "Europe/Paris"


def test_config_timezone_defaults_to_utc(tmp_path):
    [loaded] = load_sources(write(tmp_path, VALID_ENTRY))
    assert loaded.timezone == "UTC"


def test_config_rejects_unknown_timezone(tmp_path):
    path = write(tmp_path, VALID_ENTRY + "    timezone: Mars/Olympus\n")
    with pytest.raises(ConfigError, match="X1.*timezone"):
        load_sources(path)


def test_config_missing_field_names_the_source(tmp_path):
    path = write(tmp_path, VALID_ENTRY.replace("    language: en\n", ""))
    with pytest.raises(ConfigError, match="X1.*language"):
        load_sources(path)


def test_config_rejects_trust_level_outside_1_to_3(tmp_path):
    path = write(tmp_path, VALID_ENTRY.replace("trust_level: 2", "trust_level: 4"))
    with pytest.raises(ConfigError, match="X1.*trust_level"):
        load_sources(path)


def test_config_rejects_duplicate_ids(tmp_path):
    path = write(tmp_path, VALID_ENTRY + VALID_ENTRY)
    with pytest.raises(ConfigError, match="duplicate.*X1"):
        load_sources(path)


def test_config_requires_at_least_one_source(tmp_path):
    path = tmp_path / "sources.yaml"
    path.write_text("sources: []\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="at least one source"):
        load_sources(path)


def test_project_themes_follow_the_requirements():
    names = [t.name for t in load_themes(ROOT / DEFAULT_THEMES_PATH)]
    assert names == [
        "Modèles & recherche",
        "Produits & outils",
        "Business & financement",
        "Régulation & éthique",
    ]


def test_themes_require_keywords(tmp_path):
    path = tmp_path / "themes.yaml"
    path.write_text("themes:\n  - name: Vide\n    keywords: []\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="Vide.*keywords"):
        load_themes(path)


def test_other_theme_name_is_reserved(tmp_path):
    path = tmp_path / "themes.yaml"
    path.write_text(f"themes:\n  - name: {OTHER_THEME}\n    keywords: [x]\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="reserved"):
        load_themes(path)


def test_other_theme_name_is_reserved_whatever_the_case(tmp_path):
    path = tmp_path / "themes.yaml"
    path.write_text("themes:\n  - name: ' autres '\n    keywords: [x]\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="reserved"):
        load_themes(path)
