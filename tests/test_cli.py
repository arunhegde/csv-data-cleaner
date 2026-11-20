from csv_cleaner.cli import main


def test_cli_success(tmp_path, capsys):
    source = tmp_path / "input.csv"
    output = tmp_path / "output.csv"
    source.write_text("id,name\n1, Ada \n", encoding="utf-8")
    assert main([str(source), str(output), "--required", "id"]) == 0
    assert "Wrote 1 rows" in capsys.readouterr().out


def test_cli_error(tmp_path, capsys):
    assert main([str(tmp_path / "missing.csv"), str(tmp_path / "out.csv")]) == 1
    assert "Error:" in capsys.readouterr().err
