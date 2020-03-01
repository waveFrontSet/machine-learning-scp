import pytest
from src.data.article_data import Article


@pytest.fixture
def article():
    return Article("SAFE", "", "", "")


@pytest.mark.parametrize("label", ["SAFE", "EUCLID", "KETER"])
def test_set_regular_label(article, label):
    article.label = label
    assert article.label == label
    article.label = label + "SOMETHING"
    assert article.label == label


def test_set_unknown_label(article):
    with pytest.raises(ValueError) as excinfo:
        article.label = "unknown"
    assert "unknown" in str(excinfo)


def test_from_text():
    procedures = [
        "Special Containment Procedures: Something...",
        "Something part two...",
    ]
    description = "Description: Something else..."
    article = Article.from_text(["SAFE", "Some name   ", *procedures, description])
    assert article.label == "SAFE"
    assert article.name == "Some name"
    assert article.procedures == "Something...Something part two..."
    assert article.desc == "Something else..."


def test_from_text_with_no_name():
    procedures = [
        "Special Containment Procedures: Something...",
        "Something part two...",
    ]
    description = "Description: Something else..."
    article = Article.from_text(["SAFE", *procedures, description])
    assert article.label == "SAFE"
    assert article.name == ""
    assert article.procedures == "Something...Something part two..."
    assert article.desc == "Something else..."


def test_from_text_with_summary():
    procedures = [
        "Special Containment Procedures: Something...",
        "Something part two...",
    ]
    description = "Summary: Something else..."
    article = Article.from_text(["SAFE", *procedures, description])
    assert article.label == "SAFE"
    assert article.name == ""
    assert article.procedures == "Something...Something part two..."
    assert article.desc == "Something else..."


def test_from_text_with_no_desc():
    procedures = [
        "Special Containment Procedures: Something...",
        "Something part two...",
    ]
    description = "Conclusion: Something else..."
    with pytest.raises(RuntimeError) as excinfo:
        Article.from_text(["SAFE", *procedures, description])
    assert "Description" in str(excinfo)


def test_from_text_with_no_special_containment_procedures():
    procedures = [
        "Object Containment Procedures: Something...",
        "Something part two...",
    ]
    description = "Description: Something else..."
    with pytest.raises(RuntimeError) as excinfo:
        Article.from_text(["SAFE", *procedures, description])
    assert "Procedures" in str(excinfo)


def test_to_dict_trivial_article(article):
    d = article.to_dict()
    assert "Label" in d
    assert d["Label"] == "SAFE"
    assert "Name" in d
    assert "Procedures" in d
    assert "Description" in d
    assert "Procedures_Length" in d
    assert d["Procedures_Length"] == 0
    assert "Description_Length" in d
    assert d["Description_Length"] == 0
    assert "Procedures_Description_Ratio" in d
    assert d["Procedures_Description_Ratio"] == 0


def test_to_dict(article):
    article.name = "Test"
    article.procedures = "TestTest"
    article.desc = "Test"
    d = article.to_dict()
    assert "Label" in d
    assert d["Label"] == "SAFE"
    assert "Name" in d
    assert d["Name"] == "Test"
    assert "Procedures" in d
    assert d["Procedures"] == "TestTest"
    assert "Description" in d
    assert d["Description"] == "Test"
    assert "Procedures_Length" in d
    assert d["Procedures_Length"] == 8
    assert "Description_Length" in d
    assert d["Description_Length"] == 4
    assert "Procedures_Description_Ratio" in d
    assert d["Procedures_Description_Ratio"] == 2
