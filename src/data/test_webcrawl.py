import pytest
from .webcrawl import construct_url


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
