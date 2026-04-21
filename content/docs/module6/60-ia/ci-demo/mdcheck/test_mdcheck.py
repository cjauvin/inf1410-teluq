"""Tests pour mdcheck."""

from unittest.mock import Mock, patch

from main import check_url, extract_links


class TestExtractLinks:
    def test_single_link(self):
        text = "Voir [Google](https://google.com) pour plus d'info."
        links = extract_links(text)
        assert links == [("Google", "https://google.com")]

    def test_multiple_links(self):
        text = "[A](https://a.com) et [B](https://b.com)"
        links = extract_links(text)
        assert len(links) == 2

    def test_no_links(self):
        text = "Pas de liens ici."
        links = extract_links(text)
        assert links == []

    def test_link_with_anchor(self):
        text = "[Section](#installation)"
        links = extract_links(text)
        assert links == [("Section", "#installation")]

    def test_relative_link(self):
        text = "[Docs](./docs/guide.md)"
        links = extract_links(text)
        assert links == [("Docs", "./docs/guide.md")]

    def test_image_not_captured(self):
        text = "![Logo](https://example.com/logo.png)"
        links = extract_links(text)
        assert links == []

    def test_nested_brackets_ignored(self):
        text = "pas un lien [texte](pas une url avec espace)"
        links = extract_links(text)
        assert links == [("texte", "pas une url avec espace")]


class TestCheckUrl:
    @patch("main.requests.head")
    def test_url_ok(self, mock_head):
        mock_head.return_value = Mock(status_code=200)
        ok, msg = check_url("https://example.com")
        assert ok is True
        assert msg == "OK"

    @patch("main.requests.head")
    def test_url_redirect(self, mock_head):
        mock_head.return_value = Mock(status_code=301)
        ok, msg = check_url("https://example.com")
        assert ok is True

    @patch("main.requests.head")
    def test_url_not_found(self, mock_head):
        mock_head.return_value = Mock(status_code=404)
        ok, msg = check_url("https://example.com/missing")
        assert ok is False
        assert "404" in msg

    @patch("main.requests.head")
    def test_url_timeout(self, mock_head):
        import requests

        mock_head.side_effect = requests.Timeout()
        ok, msg = check_url("https://slow.example.com")
        assert ok is False
        assert "Timeout" in msg

    @patch("main.requests.head")
    def test_url_connection_error(self, mock_head):
        import requests

        mock_head.side_effect = requests.ConnectionError()
        ok, msg = check_url("https://doesnotexist.example.com")
        assert ok is False
        assert "Connexion" in msg
