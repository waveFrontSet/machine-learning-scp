from .webcrawl import construct_url


def test_construct_url():
    assert "http://scp-wiki.net/scp-001" == construct_url(1)
    assert "http://scp-wiki.net/scp-011" == construct_url(11)
    assert "http://scp-wiki.net/scp-111" == construct_url(111)
    assert "http://scp-wiki.net/scp-1111" == construct_url(1111)
