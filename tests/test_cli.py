from subnetcalc.__main__ import main


def test_split_command_prints_subnets(capsys):
    assert main(["split", "10.0.0.0/23", "--prefix", "24"]) == 0
    assert capsys.readouterr().out.split() == ["10.0.0.0/24", "10.0.1.0/24"]


def test_invalid_cidr_returns_error_code():
    assert main(["info", "not-a-cidr"]) == 2


def test_overlaps_command_prints_overlapping_pairs(capsys):
    assert main(["overlaps", "10.0.0.0/24", "10.0.0.128/25"]) == 0
    assert capsys.readouterr().out == "10.0.0.0/24 overlaps with 10.0.0.128/25\n"


def test_overlaps_command_reports_no_overlaps(capsys):
    assert main(["overlaps", "10.0.0.0/24", "10.0.1.0/24"]) == 0
    assert capsys.readouterr().out == "No overlaps found\n"


def test_overlaps_command_reports_invalid_cidr(capsys):
    assert main(["overlaps", "10.0.0.0/24", "not-a-cidr"]) == 2
    error = capsys.readouterr().err
    assert error.startswith("error: ")
    assert "not-a-cidr" in error
