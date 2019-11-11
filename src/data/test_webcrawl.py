import pytest
import io
from unittest.mock import Mock, mock_open, patch
from click.testing import CliRunner
from bs4 import BeautifulSoup
from .webcrawl import (
    construct_url,
    filter_for_page_content,
    split_into_label_and_text,
    write_to,
    crawl_for,
)


TEST_PAGE = """
    <html>
    <head>
    <title>Some scp</title>
    </head>
    <body>
    <div id="page-content">
        <p><strong>Object Class:</strong> Safe</p>
        <p>Some paragraph.</p>
    </div></body></html>
    """

response_mock = Mock()
response_mock.text = TEST_PAGE


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1, "http://scp-wiki.net/scp-001"),
        (11, "http://scp-wiki.net/scp-011"),
        (111, "http://scp-wiki.net/scp-111"),
        (1111, "http://scp-wiki.net/scp-1111"),
    ],
)
def test_construct_url(test_input, expected):
    assert construct_url(test_input) == expected


def test_filter_for_page_content():
    expected = """
<div id="page-content">
<p><strong>Object Class:</strong> Safe</p>
<p>Some paragraph.</p>
</div>
    """.strip()
    actual = str(filter_for_page_content(TEST_PAGE))
    assert expected == actual


def test_split():
    test_content = BeautifulSoup(
        """
        <div class="image-content">
            <p>Some caption</p>
        </div>
        <p><strong>Item #:</strong> SCP-xxx</p>
        <p><strong>Object Class:</strong> Safe</p>
        <p><strong>Special Containment Procedures:</strong> ...</p>
        <p><strong>Description:</strong> ...</p>
        <p>Other...</p>
        <div class="footer">
            <p>Links to other SCPs...</p>
        </div>
        """,
        features="html.parser",
    )
    actual_label, actual_content = split_into_label_and_text(test_content)
    expected_label = "SAFE"
    expected_content = [
        "<p><strong>Item #:</strong> SCP-xxx</p>",
        "<p><strong>Special Containment Procedures:</strong> ...</p>",
        "<p><strong>Description:</strong> ...</p>",
        "<p>Other...</p>",
    ]
    assert expected_label == actual_label
    assert expected_content == [str(p) for p in actual_content]


def test_write_to():
    label = "EUCLID"
    expected = ["p1", "p2"]
    paragraphs = [BeautifulSoup(f"<p>{p}</p>", "html.parser") for p in expected]
    f = io.StringIO()
    write_to(f, label, paragraphs)
    lines = f.getvalue().split("\n")
    assert 4 == len(lines)
    assert label == lines[0]
    for i, p in enumerate(expected):
        assert p == lines[i + 1]


@patch("requests.get", side_effect=lambda *args, **kwargs: response_mock)
@patch("builtins.open", side_effect=mock_open)
def test_crawl_for(mock_file, mock_requests):
    runner = CliRunner()
    result = runner.invoke(crawl_for, ["--lower", "2", "--upper", "3", "data/raw/"])
    print(result.output)
    print(result.exception)
    mock_requests.assert_called_once_with("http://scp-wiki.net/scp-002")
    mock_file.assert_called_once_with("data/raw/scp-002.txt", "w")
