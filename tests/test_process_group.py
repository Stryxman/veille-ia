from datetime import UTC, datetime, timedelta

from veille.models import Article, Source, Story
from veille.process import group_duplicates, normalize_link, normalize_title

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)


def src(id, level):
    return Source(
        id, f"Source {id}", f"https://{id}.example/feed", f"https://{id}.example/", "en", level
    )


def story(title, link, source, days_ago=0):
    date = NOW - timedelta(days=days_ago)
    article = Article(title, link, source, date, "", source.language)
    return Story(article=article, date=date, date_is_known=True)


def test_tracking_parameters_and_trailing_slash_are_ignored_in_links():
    assert normalize_link("https://X.example/news/?utm_source=rss&id=3#top") == (
        "https://x.example/news?id=3"
    )


def test_title_normalisation_ignores_case_and_punctuation():
    assert normalize_title("OpenAI unveils GPT-6!") == normalize_title("openai unveils gpt 6")


def test_same_link_from_another_source_is_listed():
    a, b = src("a", 2), src("b", 3)
    stories = [
        story("Title one", "https://n.example/x/?utm_medium=feed", a),
        story("Another wording", "https://n.example/x", b),
    ]
    [result] = group_duplicates(stories)
    assert result.article.source.id == "a"
    assert [x.source.id for x in result.also_covered] == ["b"]


def test_same_link_from_the_same_source_is_not_repeated():
    a = src("a", 2)
    stories = [
        story("Title one", "https://n.example/x", a),
        story("Title one", "https://n.example/x/?utm_source=rss", a, days_ago=1),
    ]
    [result] = group_duplicates(stories)
    assert result.also_covered == ()


def test_titles_with_different_numbers_are_kept_apart():
    # D16: versions, amounts or years that differ mean different news.
    a, b = src("a", 2), src("b", 2)
    stories = [
        story("OpenAI unveils GPT-5 with new reasoning mode", "https://a.example/1", a),
        story("OpenAI unveils GPT-6 with new reasoning mode", "https://b.example/1", b),
    ]
    assert len(group_duplicates(stories)) == 2


def test_articles_are_compared_to_the_retained_article_not_chained():
    # D16: A~B and B~C are similar enough, A~C is not: C stays a separate story.
    lead, b, c = src("lead", 1), src("b", 2), src("c", 2)
    stories = [
        story(
            "Anthropic opens a new research office in Paris to work on safety", "https://l/1", lead
        ),
        story(
            "Anthropic opens a new research office in Paris to work on AI safety", "https://b/1", b
        ),
        story(
            "Anthropic opens a new research office in Paris to work on AI safety policy rules",
            "https://c/1",
            c,
        ),
    ]
    results = group_duplicates(stories)
    assert len(results) == 2
    grouped = next(r for r in results if r.article.source.id == "lead")
    assert [x.source.id for x in grouped.also_covered] == ["b"]


def test_near_identical_titles_from_two_sources_are_grouped():
    a, b = src("a", 2), src("b", 2)
    stories = [
        story("OpenAI unveils GPT-6 with new reasoning mode", "https://a.example/1", a),
        story("OpenAI unveils GPT-6, with new reasoning mode", "https://b.example/2", b),
    ]
    [result] = group_duplicates(stories)
    assert [x.link for x in result.also_covered] == ["https://b.example/2"]


def test_more_trusted_source_is_retained_even_if_published_later():
    general, specialised = src("gen", 3), src("spec", 2)
    stories = [
        story("Mistral raises 2 billion euros", "https://gen.example/1", general, days_ago=2),
        story("Mistral raises 2 billion euros", "https://spec.example/1", specialised, days_ago=0),
    ]
    [result] = group_duplicates(stories)
    assert result.article.source.id == "spec"
    assert [x.source.id for x in result.also_covered] == ["gen"]


def test_same_level_keeps_the_earliest_article():
    a, b = src("a", 2), src("b", 2)
    stories = [
        story("Anthropic ships Claude 6", "https://a.example/1", a, days_ago=0),
        story("Anthropic ships Claude 6", "https://b.example/1", b, days_ago=1),
    ]
    [result] = group_duplicates(stories)
    assert result.article.source.id == "b"


def test_close_but_different_titles_are_kept_apart():
    a, b = src("a", 2), src("b", 2)
    stories = [
        story("OpenAI launches GPT-6 for developers", "https://a.example/1", a),
        story("Google launches Gemini 4 for developers", "https://b.example/1", b),
    ]
    assert len(group_duplicates(stories)) == 2


def test_also_covered_is_ordered_by_trust_then_date():
    lead, second, third = src("lead", 1), src("second", 2), src("third", 3)
    title = "Hugging Face releases a new open model"
    stories = [
        story(title, "https://third.example/1", third, days_ago=3),
        story(title, "https://second.example/1", second, days_ago=1),
        story(title, "https://lead.example/1", lead, days_ago=0),
    ]
    [result] = group_duplicates(stories)
    assert result.article.source.id == "lead"
    assert [x.source.id for x in result.also_covered] == ["second", "third"]


def test_same_link_as_any_member_joins_the_story():
    # B joins L by title; C shares B's link with another title: same story, not a new one.
    lead, b, c = src("l", 1), src("b", 2), src("c", 3)
    stories = [
        story("Anthropic opens a research office in Paris", "https://l.example/1", lead),
        story("Anthropic opens a research office in Paris!", "https://x.example/1", b),
        story("Paris gets a new AI lab", "https://x.example/1", c),
    ]
    [result] = group_duplicates(stories)
    assert [x.source.id for x in result.also_covered] == ["b", "c"]


def test_link_match_takes_priority_over_title_match():
    # C has A's title but B's link: the link decides (D16), so C joins B's story.
    a, b, c = src("a", 1), src("b", 2), src("c", 3)
    stories = [
        story("Anthropic opens a research office in Paris", "https://a.example/1", a),
        story("Unrelated headline about chips", "https://shared.example/1", b),
        story("Anthropic opens a research office in Paris.", "https://shared.example/1", c),
    ]
    results = {
        r.article.source.id: [x.source.id for x in r.also_covered]
        for r in group_duplicates(stories)
    }
    assert results == {"a": [], "b": ["c"]}


def test_a_source_is_never_listed_under_its_own_article():
    a = src("a", 2)
    stories = [
        story("Anthropic ships Claude 6", "https://a.example/1", a),
        story("Anthropic ships Claude 6", "https://a.example/2", a, days_ago=1),
    ]
    [result] = group_duplicates(stories)
    assert result.also_covered == ()


def test_long_titles_differing_by_one_entity_are_kept_apart():
    # D17: 0.94 similar, but "google" and "meta" each appear in one title only.
    a, b = src("a", 2), src("b", 2)
    stories = [
        story(
            "La CNIL inflige une amende record à Google pour ses cookies publicitaires",
            "https://a/1",
            a,
        ),
        story(
            "La CNIL inflige une amende record à Meta pour ses cookies publicitaires",
            "https://b/1",
            b,
        ),
    ]
    assert len(group_duplicates(stories)) == 2


def test_negated_title_is_kept_apart():
    a, b = src("a", 2), src("b", 2)
    stories = [
        story("Microsoft lance Copilot en Europe", "https://a/1", a),
        story("Microsoft ne lance pas Copilot en Europe", "https://b/1", b),
    ]
    assert len(group_duplicates(stories)) == 2
