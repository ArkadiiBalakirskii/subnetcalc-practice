from subnetcalc.__main__ import main


def test_split_command_prints_subnets(capsys):
    assert main(["split", "10.0.0.0/23", "--prefix", "24"]) == 0
    assert capsys.readouterr().out.split() == ["10.0.0.0/24", "10.0.1.0/24"]


def test_invalid_cidr_returns_error_code():
    assert main(["info", "not-a-cidr"]) == 2
