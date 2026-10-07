import re
from datetime import UTC, datetime

from veille import render as render_module
from veille.collect import CollectResult
from veille.config import OTHER_THEME
from veille.models import Article, Source, Story, Theme
from veille.render import french_date, render_page

GENERATED = datetime(2026, 10, 2, 4, 0, tzinfo=UTC)
S1 = Source("S1", "Hugging Face Blog", "https://hf.example/feed", "https://hf.example/", "en", 1)
S2 = Source("S2", "ActuIA", "https://actuia.example/feed", "https://actuia.example/", "fr", 2)
THEMES = [Theme("Modèles & recherche", ("model",)), Theme("Business & financement", ("funding",))]


def story(title, theme, source=S1, known=True, also=(), summary="Résumé.", link=None):
    article = Article(
        title,
        link or f"https://x.example/{abs(hash(title))}",
        source,
        GENERATED if known else None,
        summary,
        source.language,
    )
    return Story(article, GENERATED, known, tuple(also), theme)


def page(stories, unavailable=()):
    return render_page(stories, THEMES, [S1, S2], list(unavailable), GENERATED)


def test_french_dates_in_paris_time():
    assert french_date(GENERATED) == "2 octobre 2026"
    assert french_date(GENERATED, with_time=True) == "2 octobre 2026 à 06:00"
    assert french_date(datetime(2026, 10, 1, 12, tzinfo=UTC)) == "1er octobre 2026"
    assert (
        french_date(datetime(2026, 12, 1, 5, tzinfo=UTC), with_time=True)
        == "1er décembre 2026 à 06:00"
    )


def test_page_is_in_french_and_readable_on_mobile():
    html = page([story("A", "Modèles & recherche")])
    assert '<html lang="fr">' in html
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html
    assert (
        "body { overflow-wrap: anywhere;" in html
    )  # titles and pills wrap too, not only paragraphs


def test_header_shows_update_time_and_count():
    html = page([story("A", "Modèles & recherche"), story("B", OTHER_THEME)])
    assert "Mis à jour le 2 octobre 2026 à 06:00 (heure de Paris)" in html
    assert "2 articles" in html


def test_header_count_is_singular_for_one_article():
    assert "· 1 article sur les 7 derniers jours" in page([story("A", "Modèles & recherche")])
    assert "· 0 article sur les 7 derniers jours" in page([])


def test_themes_follow_configuration_order_and_empty_ones_are_hidden():
    html = page([story("Other", OTHER_THEME), story("Money", "Business & financement")])
    assert html.index("Business &amp; financement</h2>") < html.index(f"{OTHER_THEME}</h2>")
    assert "Modèles &amp; recherche</h2>" not in html
    assert "Modèles &amp; recherche <span" not in html


def test_theme_colours_follow_configuration_position():
    html = page([story("Money", "Business & financement"), story("Other", OTHER_THEME)])
    # anchors follow the configuration too, so a bookmark survives an empty theme
    assert '<section class="c2" aria-labelledby="theme-2">' in html
    assert '<section class="other" aria-labelledby="theme-autres">' in html
    pill = (
        '<a class="pill c2" href="#theme-2">Business &amp; financement <span class="count">1</span>'
    )
    assert pill in html


def test_theme_colours_start_again_after_the_sixth_theme():
    many = [Theme(f"T{index}", ("x",)) for index in range(1, 8)]
    html = render_page([story("A", "T7")], many, [S1], [], GENERATED)
    assert '<section class="c1" aria-labelledby="theme-7">' in html


def test_story_shows_title_link_source_date_and_excerpt():
    html = page(
        [
            story(
                "Gemini 4 released",
                "Modèles & recherche",
                link="https://g.example/4",
                summary="Google a présenté…",
            )
        ]
    )
    assert '<a href="https://g.example/4">Gemini 4 released</a>' in html
    assert "Hugging Face Blog · 2 octobre 2026" in html
    assert "Google a présenté…" in html


def test_undated_story_shows_collection_date_and_label():
    html = page([story("No date", "Modèles & recherche", known=False)])
    assert '2 octobre 2026 <span class="tag">Date de publication inconnue</span>' in html


def test_also_covered_lists_other_sources_with_links():
    other = Article("Same news", "https://actuia.example/same", S2, GENERATED, "", "fr")
    html = page([story("Same news", "Modèles & recherche", also=[other])])
    assert 'Aussi couvert par : <a href="https://actuia.example/same">ActuIA</a>' in html


def test_footer_lists_sources_and_unavailable_ones():
    html = page([story("A", "Modèles & recherche")], unavailable=[S2])
    assert "Source indisponible lors de la dernière mise à jour : ActuIA." in html
    html = page([story("A", "Modèles & recherche")], unavailable=[S1, S2])
    assert '<a href="https://hf.example/">Hugging Face Blog</a>' in html
    assert (
        "Sources indisponibles lors de la dernière mise à jour : Hugging Face Blog, ActuIA." in html
    )


def test_footer_says_when_all_sources_answered():
    assert "Toutes les sources ont répondu" in page([story("A", "Modèles & recherche")])


def test_special_characters_cannot_break_the_page():
    html = page([story('Use <script>alert(1)</script> & "quotes"', "Modèles & recherche")])
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt; &amp;" in html


def test_page_without_stories_says_so():
    assert "Aucun article sur les 7 derniers jours." in page([])


def test_main_writes_the_page(tmp_path, monkeypatch):
    article = Article("Live news about a model", "https://hf.example/news/1", S1, None, "x", "en")
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([article], []))
    assert render_module.main(["--output", str(tmp_path)]) == 0
    assert "Live news about a model" in (tmp_path / "index.html").read_text(encoding="utf-8")


def test_main_publishes_nothing_when_no_article_is_collected(tmp_path, monkeypatch):
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([], list(sources)))
    assert render_module.main(["--output", str(tmp_path)]) == 1
    assert not (tmp_path / "index.html").exists()


def test_english_story_is_marked_as_english():
    html = page([story("Model news", "Modèles & recherche", source=S1)])
    assert '<h3 lang="en"><a href=' in html  # WCAG 3.1.2: screen readers switch voice
    assert '<p lang="en">Résumé.</p>' in html


def test_french_story_keeps_the_page_language():
    html = page([story("Actualité", "Modèles & recherche", source=S2)])
    assert "<h3><a href=" in html


def test_each_section_links_back_to_the_themes():
    html = page([story("A", "Modèles & recherche"), story("B", OTHER_THEME)])
    assert '<nav id="themes" aria-label="Thèmes">' in html
    assert html.count('<a class="back" href="#themes">Retour aux thèmes</a>') == 2


def test_header_explains_the_page():
    html = page([story("A", "Modèles & recherche")])
    expected = "L'actualité de l'intelligence artificielle des 7 derniers jours"
    assert f'<p class="tagline">{expected}, dédoublonnée et classée par thème.</p>' in html


def test_main_publishes_nothing_when_no_story_is_recent(tmp_path, monkeypatch):
    old = Article(
        "Old news", "https://n.example/old", S1, datetime(2020, 1, 1, tzinfo=UTC), "x", "en"
    )
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([old], []))
    assert render_module.main(["--output", str(tmp_path)]) == 1  # previous page stays online
    assert not (tmp_path / "index.html").exists()


def test_main_completes_missing_excerpts_from_the_article_page(tmp_path, monkeypatch):
    article = Article("Live news about a model", "https://hf.example/news/1", S1, None, "", "en")
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([article], []))
    paragraph = "From the page: " + "a sentence about the model and its training data. " * 3
    html = f"<html><body><article><p>{paragraph}</p></article></body></html>".encode()
    monkeypatch.setattr("veille.enrich.fetch_page", lambda url: html)
    assert render_module.main(["--output", str(tmp_path)]) == 0
    assert "From the page" in (tmp_path / "index.html").read_text(encoding="utf-8")


def test_completed_excerpt_is_used_to_classify_the_story(tmp_path, monkeypatch):
    article = Article("Company news", "https://hf.example/news/2", S1, None, "", "en")
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([article], []))
    monkeypatch.setattr(render_module, "load_themes", lambda: THEMES)
    paragraph = "The startup announced new funding today. " * 4
    html = f"<html><body><article><p>{paragraph}</p></article></body></html>".encode()
    monkeypatch.setattr("veille.enrich.fetch_page", lambda url: html)
    assert render_module.main(["--output", str(tmp_path)]) == 0
    page_html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert '<section class="c2" aria-labelledby="theme-2">' in page_html  # Business, not Autres


def test_markup_in_the_article_page_is_escaped(tmp_path, monkeypatch):
    article = Article("Live news about a model", "https://hf.example/news/3", S1, None, "", "en")
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([article], []))
    paragraph = "The model writes &lt;think&gt; before answering, carefully. " * 3
    html = f"<html><body><article><p>{paragraph}</p></article></body></html>".encode()
    monkeypatch.setattr("veille.enrich.fetch_page", lambda url: html)
    assert render_module.main(["--output", str(tmp_path)]) == 0
    page_html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "The model writes &lt;think&gt; before answering" in page_html  # escaped, not dropped
    assert "<think>" not in page_html


def test_comparison_signs_in_the_article_page_are_escaped(tmp_path, monkeypatch):
    article = Article("Live news about a model", "https://hf.example/news/4", S1, None, "", "en")
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([article], []))
    paragraph = "The new model scores a &lt; b on one benchmark, which surprised the authors. " * 3
    html = f"<html><body><article><p>{paragraph}</p></article></body></html>".encode()
    monkeypatch.setattr("veille.enrich.fetch_page", lambda url: html)
    assert render_module.main(["--output", str(tmp_path)]) == 0
    page_html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "scores a &lt; b on one benchmark" in page_html  # escaped by the template (R13)


def test_main_prints_a_run_summary(tmp_path, monkeypatch, capsys):
    with_text = Article("Model news", "https://n.example/5", S1, None, "Model text.", "en")
    no_text = Article("Other news", "https://n.example/6", S2, None, "", "fr")
    monkeypatch.setattr(
        render_module, "collect", lambda sources: CollectResult([with_text, no_text], [S2])
    )
    monkeypatch.setattr(render_module, "load_sources", lambda: [S1, S2])
    monkeypatch.setattr(render_module, "load_themes", lambda: THEMES)
    monkeypatch.setattr("veille.enrich.fetch_page", lambda url: b"<html></html>")
    assert render_module.main(["--output", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "S1 Hugging Face Blog: 1 article(s)" in out
    assert "S2 ActuIA: unavailable" in out
    assert "Stories kept (7 days): 2" in out
    assert "Excerpts completed from article pages: 0 of 1" in out
    assert "Classified outside 'Autres': 50 %" in out
    for step in ("collect", "process", "enrich", "render"):
        assert re.search(rf"{step} \d+\.\d s", out)  # duration of each step, in seconds


def test_failed_run_still_prints_the_sources_and_durations(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(render_module, "collect", lambda sources: CollectResult([], [S1, S2]))
    monkeypatch.setattr(render_module, "load_sources", lambda: [S1, S2])
    assert render_module.main(["--output", str(tmp_path)]) == 1
    out = capsys.readouterr().out
    assert "S1 Hugging Face Blog: unavailable" in out and "S2 ActuIA: unavailable" in out
    assert re.search(r"Durations: collect \d+\.\d s", out)
