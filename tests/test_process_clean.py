from datetime import UTC, datetime, timedelta

from veille.models import Article, Source
from veille.process import EXCERPT_LENGTH, clean_text, excerpt, select_recent

NOW = datetime(2026, 10, 1, 12, 0, tzinfo=UTC)
SOURCE = Source("T1", "Test", "https://t.example/feed", "https://t.example/", "en", 2)


def article(title="Title", summary="Summary", published=NOW, link="https://t.example/a"):
    return Article(
        title=title,
        link=link,
        source=SOURCE,
        published=published,
        summary=summary,
        language=SOURCE.language,
    )


def test_html_tags_and_entities_are_removed():
    assert clean_text("<p>Hello&nbsp;<b>world</b> &amp; co&#8217;s</p>") == "Hello world & co’s"


def test_double_escaped_html_is_cleaned():
    assert clean_text("&lt;p&gt;Here&amp;#8217;s news&lt;/p&gt;") == "Here’s news"


def test_whitespace_is_normalised():
    assert clean_text("  a\n\n b\t c  ") == "a b c"


def test_short_text_is_not_truncated():
    assert excerpt("Short text.") == "Short text."


def test_long_text_is_cut_at_a_word_boundary_with_ellipsis():
    text = " ".join(["alpha", "beta", "gamma"] * 40)
    result = excerpt(text)
    assert result.endswith("…")
    assert len(result) <= EXCERPT_LENGTH + 1
    assert set(result[:-1].split()) <= {"alpha", "beta", "gamma"}


def test_articles_older_than_seven_days_are_excluded():
    old = article(link="https://t.example/old", published=NOW - timedelta(days=7, minutes=1))
    edge = article(link="https://t.example/edge", published=NOW - timedelta(days=7))
    recent = article(link="https://t.example/new", published=NOW - timedelta(days=1))
    links = [s.article.link for s in select_recent([old, edge, recent], NOW)]
    assert links == ["https://t.example/edge", "https://t.example/new"]


def test_undated_article_is_kept_with_collection_date_and_flagged():
    [story] = select_recent([article(published=None)], NOW)
    assert story.date == NOW
    assert story.date_is_known is False


def test_dated_article_keeps_its_date():
    published = NOW - timedelta(hours=3)
    [story] = select_recent([article(published=published)], NOW)
    assert story.date == published
    assert story.date_is_known is True


def test_selected_articles_are_cleaned():
    [story] = select_recent([article(title="<b>Hi</b> &amp; bye", summary="<p>x</p>")], NOW)
    assert story.article.title == "Hi & bye"
    assert story.article.summary == "x"


def test_quoted_non_html_tag_is_kept():
    # AI news often quotes tags such as <think>: they are text, not markup.
    assert clean_text("How models use <think> tags") == "How models use <think> tags"


def test_escaped_tag_in_html_summary_is_kept_as_text():
    assert clean_text("<p>The &lt;think&gt; block</p>") == "The <think> block"


def test_comparison_signs_are_kept():
    assert clean_text("a < b and c > d") == "a < b and c > d"


def test_html5_markup_and_script_blocks_are_removed():
    raw = (
        "<article><header><time datetime='x'>Today</time></header><section>Body</section>"
        "<script>track()</script><style>p{}</style></article>"
    )
    assert clean_text(raw) == "Today Body"


def test_single_escaped_ampersand_is_not_decoded_twice():
    assert clean_text("Read more: https://x.example/?id=1&amp;section=ai") == (
        "Read more: https://x.example/?id=1&section=ai"
    )


def test_quoted_html_tag_in_html_summary_is_kept_as_text():
    assert clean_text("<p>Use the &lt;b&gt; tag</p>") == "Use the <b> tag"
