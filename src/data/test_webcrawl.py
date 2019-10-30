import pytest
from .webcrawl import construct_url, filter_for_page_content


TEST_PAGE = """
    <html>
    <head>
    <title>Some scp</title>
    </head>
    <body>
    <div id="page-content">
        <p>Some paragraph.</p>
    </div></body></html>
    """


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
<p>Some paragraph.</p>
</div>
    """.strip()
    actual = str(filter_for_page_content(TEST_PAGE))
    assert expected == actual
