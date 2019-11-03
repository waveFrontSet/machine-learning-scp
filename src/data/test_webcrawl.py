import pytest
from bs4 import BeautifulSoup
from .webcrawl import construct_url, filter_for_page_content, split_into_label_and_text


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
