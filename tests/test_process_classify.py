from datetime import UTC, datetime, timedelta

from veille.config import OTHER_THEME, load_themes
from veille.models import Article, Source, Story, Theme
from veille.process import classify, process

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)
SOURCE = Source("T1", "Test", "https://t.example/feed", "https://t.example/", "fr", 2)
THEMES = [
    Theme("Business", ("funding", "levée de fonds")),
    Theme("Régulation", ("loi", "ai act")),
]


def story(title, summary=""):
    article = Article(
        title, "https://t.example/" + str(abs(hash(title))), SOURCE, NOW, summary, "fr"
    )
    return Story(article=article, date=NOW, date_is_known=True)


def theme(title, summary="", themes=THEMES):
    [result] = classify([story(title, summary)], themes)
    return result.theme


def test_keyword_match_ignores_case_and_accents():
    assert theme("Record de LEVEE DE FONDS pour une startup") == "Business"


def test_keywords_match_whole_words_only():
    assert theme("Les lois et exploits du marché") == OTHER_THEME


def test_summary_is_searched_too():
    assert theme("Une annonce", summary="Le Parlement adopte la loi") == "Régulation"


def test_theme_with_most_matches_wins():
    assert theme("Funding talks stall as the AI Act and a new loi arrive") == "Régulation"


def test_tie_goes_to_first_theme_in_file_order():
    assert theme("Funding announced while the AI Act applies") == "Business"


def test_no_keyword_means_other_theme():
    assert theme("Une journée ordinaire") == OTHER_THEME


def test_new_theme_needs_configuration_only(tmp_path):
    path = tmp_path / "themes.yaml"
    path.write_text("themes:\n  - name: Santé\n    keywords: [hôpital, santé]\n", encoding="utf-8")
    assert theme("L'IA à l'hôpital", themes=load_themes(path)) == "Santé"


def test_process_cleans_groups_classifies_and_sorts():
    def art(title, link, hours_ago, source=SOURCE):
        return Article(title, link, source, NOW - timedelta(hours=hours_ago), "<p>x</p>", "fr")

    other = Source("T2", "Other", "https://o.example/feed", "https://o.example/", "fr", 3)
    articles = [
        art("Vieille loi", "https://t.example/old", 24 * 8),
        art("Levée de fonds record", "https://t.example/1", 5),
        art("Levée de fonds record", "https://o.example/1", 1, other),
        art("Nouvelle loi sur l'IA", "https://t.example/2", 2),
    ]
    stories = process(articles, NOW, THEMES)
    assert [s.article.title for s in stories] == ["Nouvelle loi sur l'IA", "Levée de fonds record"]
    assert [s.theme for s in stories] == ["Régulation", "Business"]
    assert [a.source.id for a in stories[1].also_covered] == ["T2"]
    assert stories[1].article.summary == "x"


def test_typographic_apostrophe_matches_keyword():
    themes = [Theme("Business", ("chiffre d'affaires",))]
    assert theme("Hausse du chiffre d’affaires de Mistral", themes=themes) == "Business"
