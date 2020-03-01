import pandas as pd
from click.testing import CliRunner
from src.data.make_dataset import main

TEST_DATA = {
    "scp-002.txt": """EUCLID\n
Item #: 002\n
Special Containment Procedures: Something something...\n
Description: Something else...\n
""",
    "scp-003.txt": """UNKNOWN\n
Item #: 003\n
Special Containment Procedures: Something something...\n
Description: Something else...\n
""",
    "scp-004.txt": """SAFE\n
Item #: 004\n
Special Containment Procedures: Something something...\n
Conclusion: Something else...\n
""",
}


def test_main():
    runner = CliRunner()
    with runner.isolated_filesystem():
        for filename, text in TEST_DATA.items():
            with open(filename, "w") as f:
                f.write(text)
        result = runner.invoke(main, [".", "."])
        assert result.exit_code == 0
        df = pd.read_json("data.json")
        assert len(df.index) == 1
        data = df.loc[0]
        assert "Label" in data
        assert data["Label"] == "EUCLID"
        assert "Name" in data
        assert data["Name"] == "Item #: 002"
        assert "Procedures" in data
        assert data["Procedures"] == "Something something..."
        assert "Description" in data
        assert data["Description"] == "Something else..."
