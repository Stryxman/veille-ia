import gzip
import io
import urllib.error
from datetime import UTC, datetime
from pathlib import Path

import pytest

import veille.collect as collect_module
from veille.collect import FeedError, collect, parse_feed
from veille.config import load_sources
from veille.models import Source

FIXTURES = Path(__file__).parent / "fixtures"


def source(id="T1", language="en", trust_level=2, timezone="UTC"):
    return Source(
        id=id,
        name=f"Source {id}",
        feed_url=f"https://example.org/{id}.xml",
        site_url="https://example.org/",
        language=language,
        trust_level=trust_level,
        timezone=timezone,
    )


def fixture(name):
    return (FIXTURES / name).read_bytes()


def test_rss2_articles_have_all_fields():
    articles = parse_feed(fixture("rss2.xml"), source())
    dated = articles[0]
    assert dated.title == "Dated article & more"
    assert dated.link == "https://example.org/dated"
    assert dated.source.id == "T1"
    assert dated.language == "en"
    assert "Summary of the dated article" in dated.summary
    assert dated.published == datetime(2026, 9, 29, 6, 30, tzinfo=UTC)


def test_undated_article_is_kept_with_empty_date():
    articles = parse_feed(fixture("rss2.xml"), source())
    undated = [a for a in articles if a.link == "https://example.org/undated"]
    assert len(undated) == 1
    assert undated[0].published is None


def test_item_without_link_is_skipped():
    articles = parse_feed(fixture("rss2.xml"), source())
    assert [a.link for a in articles] == [
        "https://example.org/dated",
        "https://example.org/undated",
    ]


def test_item_whose_link_is_not_a_web_address_is_skipped():
    feed = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>T</title>
<item><title>Script</title><link>javascript:alert(1)</link></item>
<item><title>Data</title><link>data:text/html,x</link></item>
<item><title>Web</title><link>HTTPS://example.org/ok</link></item>
</channel></rss>"""
    articles = parse_feed(feed, source())
    assert [a.title for a in articles] == ["Web"]  # a javascript: link would run code on click


def test_relative_link_is_completed_with_the_feed_address():
    feed = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>T</title>
<item><title>Relative</title><link>/blog/article-1</link></item>
<item><title>Scheme-relative</title><link>//cdn.example.org/a</link></item>
</channel></rss>"""
    articles = parse_feed(feed, source())  # feed address: https://example.org/T1.xml
    assert [a.link for a in articles] == [
        "https://example.org/blog/article-1",
        "https://cdn.example.org/a",
    ]


def test_skipped_items_are_logged(caplog):
    with caplog.at_level("WARNING", logger="veille.collect"):
        parse_feed(fixture("rss2.xml"), source())
    assert "T1: 1 entry skipped (missing title or web link)" in caplog.text


def test_atom_uses_updated_date():
    [article] = parse_feed(fixture("atom.xml"), source())
    assert article.link == "https://example.org/atom-entry"
    assert article.published == datetime(2026, 9, 29, 21, 31, tzinfo=UTC)


def test_rdf_iso_8859_15_uses_dc_date():
    # The real feed gives Paris local time without an offset (D15).
    feed_source = source(language="fr", timezone="Europe/Paris")
    [article] = parse_feed(fixture("rdf_iso_8859_15.xml"), feed_source)
    assert article.title == "Stratégie IA : l'été des éditeurs"
    assert article.language == "fr"
    assert article.published == datetime(2026, 9, 30, 7, 36, 48, tzinfo=UTC)


def test_date_without_timezone_defaults_to_utc():
    [article] = parse_feed(fixture("rdf_iso_8859_15.xml"), source(language="fr"))
    assert article.published == datetime(2026, 9, 30, 9, 36, 48, tzinfo=UTC)


def test_date_with_its_own_offset_ignores_source_timezone():
    articles = parse_feed(fixture("rss2.xml"), source(timezone="Europe/Paris"))
    assert articles[0].published == datetime(2026, 9, 29, 6, 30, tzinfo=UTC)


def test_gzip_compressed_feed_is_read():
    # Some servers send gzip even when the client did not ask for it.
    [article] = parse_feed(gzip.compress(fixture("atom.xml")), source())
    assert article.link == "https://example.org/atom-entry"


def test_oversized_gzip_feed_is_rejected(monkeypatch):
    # A tiny compressed payload must not expand without limit (decompression bomb).
    monkeypatch.setattr(collect_module, "MAX_FEED_BYTES", 1_000)
    with pytest.raises(FeedError, match="larger than"):
        parse_feed(gzip.compress(b"x" * 5_000), source())


def test_oversized_download_is_rejected(monkeypatch):
    monkeypatch.setattr(collect_module, "MAX_FEED_BYTES", 1_000)
    with pytest.raises(FeedError, match="larger than"):
        collect_module.read_limited(io.BytesIO(b"x" * 5_000), "T1")


def test_two_digit_offset_is_not_shifted_twice():
    feed = (
        b'<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom"><title>x</title>'
        b'<entry><title>t</title><link href="https://example.org/a"/>'
        b"<updated>2026-09-30T09:36:48+02</updated></entry></feed>"
    )
    [article] = parse_feed(feed, source(timezone="Europe/Paris"))
    assert article.published == datetime(2026, 9, 30, 7, 36, 48, tzinfo=UTC)


def test_complete_feed_with_minor_xml_error_is_accepted():
    # Common real-world glitch (undefined entity): the feed is complete and readable.
    feed = (
        b'<?xml version="1.0"?><rss version="2.0"><channel><title>x</title>'
        b"<item><title>Caf&nbsp;IA</title><link>https://example.org/a</link></item>"
        b"</channel></rss>"
    )
    [article] = parse_feed(feed, source())
    assert article.link == "https://example.org/a"


EMPTY_FEED = b'<?xml version="1.0"?><rss version="2.0"><channel><title>x</title></channel></rss>'
UNUSABLE_FEED = (
    b'<?xml version="1.0"?><rss version="2.0"><channel><title>x</title>'
    b"<item><title>No link</title></item></channel></rss>"
)


def test_empty_feed_is_rejected():
    with pytest.raises(FeedError, match="no usable entries"):
        parse_feed(EMPTY_FEED, source())


def test_feed_with_only_unusable_entries_is_rejected():
    with pytest.raises(FeedError, match="no usable entries"):
        parse_feed(UNUSABLE_FEED, source())


def test_truncated_feed_is_rejected():
    data = fixture("rss2.xml")
    truncated = data[: data.index(b"<title>Undated") + 10]
    with pytest.raises(FeedError, match="malformed"):
        parse_feed(truncated, source())


def test_http_error_source_is_isolated():
    ok, down = source("OK"), source("DOWN")

    def fetch(url):
        if url == down.feed_url:
            raise urllib.error.HTTPError(url, 503, "Service Unavailable", None, None)
        return fixture("atom.xml")

    result = collect([down, ok], fetch=fetch)
    assert [a.source.id for a in result.articles] == ["OK"]
    assert [s.id for s in result.unavailable] == ["DOWN"]


def test_html_page_is_rejected():
    with pytest.raises(FeedError):
        parse_feed(fixture("not_a_feed.html"), source())


def test_failing_source_is_isolated():
    ok, broken, timeout = source("OK"), source("BROKEN"), source("SLOW")
    feeds = {ok.feed_url: fixture("atom.xml"), broken.feed_url: fixture("not_a_feed.html")}

    def fetch(url):
        if url == timeout.feed_url:
            raise TimeoutError("timed out")
        return feeds[url]

    result = collect([broken, ok, timeout], fetch=fetch)
    assert [a.source.id for a in result.articles] == ["OK"]
    assert [s.id for s in result.unavailable] == ["BROKEN", "SLOW"]


def test_new_source_needs_configuration_only(tmp_path):
    config = tmp_path / "sources.yaml"
    config.write_text(
        "sources:\n"
        "  - id: NEW\n"
        "    name: New source\n"
        "    feed_url: https://new.example/feed.xml\n"
        "    site_url: https://new.example/\n"
        "    language: fr\n"
        "    trust_level: 3\n",
        encoding="utf-8",
    )
    result = collect(load_sources(config), fetch=lambda url: fixture("rss2.xml"))
    assert {a.source.id for a in result.articles} == {"NEW"}
    assert result.unavailable == []
