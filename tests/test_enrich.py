from datetime import UTC, datetime

from veille import enrich as enrich_module
from veille.enrich import SameSiteRedirect, enrich, page_text
from veille.models import Article, Source, Story

NOW = datetime(2026, 10, 3, 6, 0, tzinfo=UTC)
HF = Source("S1", "Hugging Face Blog", "https://hf.example/feed", "https://hf.example/", "en", 1)


def story(summary="", link="https://hf.example/blog/a", also=()):
    article = Article("Holo4", link, HF, NOW, summary, "en")
    return Story(article, NOW, True, tuple(also), "Modèles & recherche")


ARTICLE_TEXT = (
    "Holo4 is our new series of agentic models. It comes in two sizes and both are available "
    "today. Holo4 builds on our previous model and interacts with software through any "
    "available interface, with better accuracy on long tasks than before."
)


def page(paragraph=ARTICLE_TEXT):
    """A page shaped like a blog post: navigation, the article, then unrelated blocks."""
    return f"""<!doctype html><html><head><title>Holo4</title>
<meta property="og:description" content="A Blog post by H company on Hugging Face"></head>
<body><nav><a href="/">Home</a> <a href="/models">Models</a> <a href="/blog">Blog</a></nav>
<main><article><h1>Holo4</h1><p>{paragraph}</p>
<p>A second paragraph explains the training data and the evaluation in more detail.</p>
</article></main>
<aside><p>Trending models: Qwen3 • 2B • Updated Jul 22 • 356k downloads</p></aside>
<footer><p>© Company, all rights reserved.</p></footer></body></html>""".encode()


def test_article_text_is_kept_without_the_side_blocks():
    text = page_text(page())
    assert "Holo4 is our new series of agentic models." in text
    assert "Trending models" not in text and "all rights reserved" not in text


def test_generic_social_description_is_not_used():
    assert "A Blog post by" not in page_text(page())


def test_page_without_article_text_gives_nothing():
    assert page_text(b"<html><head><title>Empty</title></head><body></body></html>") == ""


def test_story_without_excerpt_gets_the_start_of_the_article():
    pages = {"https://hf.example/blog/a": page()}
    [result] = enrich([story()], fetch=pages.__getitem__)
    assert result.article.summary.startswith("Holo4 is our new series")
    assert result.article.title == "Holo4"  # nothing else changes, and the title is not repeated


def test_article_text_is_cleaned_and_shortened_like_other_excerpts():
    long = "<b>Bold</b> &amp; " + "word " * 100
    pages = {"https://hf.example/blog/a": page(long)}
    [result] = enrich([story()], fetch=pages.__getitem__)
    assert result.article.summary.startswith("Bold & word")
    assert len(result.article.summary) <= 301  # 300 characters at most, plus "…" (R6)


def test_story_with_an_excerpt_is_not_fetched():
    def fail(url):
        raise AssertionError(f"unexpected request to {url}")

    [result] = enrich([story(summary="From the feed")], fetch=fail)
    assert result.article.summary == "From the feed"


def test_unreachable_page_leaves_the_story_unchanged(caplog):
    def fail(url):
        raise OSError("timed out")

    with caplog.at_level("WARNING", logger="veille.enrich"):
        [result] = enrich([story()], fetch=fail)
    assert result.article.summary == ""
    assert "https://hf.example/blog/a" in caplog.text


def test_page_without_article_text_leaves_the_story_unchanged():
    empty = b"<html><head><title>x</title></head><body></body></html>"
    [result] = enrich([story()], fetch=lambda url: empty)
    assert result.article.summary == ""


def test_also_covered_articles_are_kept():
    other = Article("Same", "https://x.example/same", HF, NOW, "", "en")
    pages = {"https://hf.example/blog/a": page()}
    [result] = enrich([story(also=[other])], fetch=pages.__getitem__)
    assert result.also_covered == (other,)


def test_default_fetch_reads_the_page(monkeypatch):
    calls = []
    monkeypatch.setattr(enrich_module, "fetch_page", lambda url: calls.append(url) or page())
    enrich([story()])
    assert calls == ["https://hf.example/blog/a"]


def test_page_in_another_encoding_is_read_correctly():
    paragraph = "Le modèle est arrivé : « Holo4 » coûte 5 € de moins. " * 3
    html = (
        '<html><head><meta charset="iso-8859-15"></head><body><article>'
        f"<p>{paragraph}</p></article></body></html>"
    ).encode("iso-8859-15")
    assert "Le modèle est arrivé : « Holo4 » coûte 5 € de moins." in page_text(html)


def test_page_outside_the_source_site_is_not_fetched():
    def fail(url):
        raise AssertionError(f"unexpected request to {url}")

    [result] = enrich([story(link="http://169.254.169.254/latest")], fetch=fail)
    assert result.article.summary == ""


def test_page_on_a_subdomain_of_the_source_site_is_fetched():
    pages = {"https://blog.hf.example/a": page()}
    [result] = enrich([story(link="https://blog.hf.example/a")], fetch=pages.__getitem__)
    assert result.article.summary.startswith("Holo4 is our new series")


def test_redirects_leaving_the_site_or_the_web_are_refused():
    import urllib.error
    import urllib.request

    handler = SameSiteRedirect()
    request = urllib.request.Request("https://hf.example/blog/a")
    for target in ("https://evil.example/x", "ftp://hf.example/x", "http://127.0.0.1/x"):
        try:
            handler.redirect_request(request, None, 302, "Found", {}, target)
        except urllib.error.HTTPError:
            continue
        raise AssertionError(f"redirect to {target} was accepted")
    assert handler.redirect_request(request, None, 302, "Found", {}, "https://hf.example/b")


def test_page_text_keeps_quoted_tags():
    paragraph = "To wrap text in &lt;p&gt; tags, write AT&amp;T in full. " * 3
    pages = {"https://hf.example/blog/a": page(paragraph)}
    [result] = enrich([story()], fetch=pages.__getitem__)
    assert result.article.summary.startswith("To wrap text in <p> tags, write AT&T in full.")


def test_page_reading_stops_when_the_time_budget_is_spent():
    times = iter([0.0, 0.0, 100.0, 100.0, 100.0])
    pages = {"https://hf.example/blog/a": page(), "https://hf.example/blog/b": page()}
    stories = [story(), story(link="https://hf.example/blog/b")]
    first, second = enrich(stories, fetch=pages.__getitem__, budget=60, clock=lambda: next(times))
    assert first.article.summary and second.article.summary == ""


def test_spent_time_budget_is_logged(caplog):
    times = iter([0.0, 100.0, 100.0])
    with caplog.at_level("WARNING", logger="veille.enrich"):
        enrich([story()], fetch=lambda url: page(), budget=60, clock=lambda: next(times))
    assert "reading time budget spent" in caplog.text
