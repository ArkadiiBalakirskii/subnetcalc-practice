import pytest

from subnetcalc import core


def test_aws_usable_ips_for_slash_24_returns_251():
    assert core.aws_usable_ips("10.0.0.0/24") == 251


def test_split_slash_20_into_slash_22():
    assert core.split("10.10.0.0/20", 22) == [
        "10.10.0.0/22",
        "10.10.4.0/22",
        "10.10.8.0/22",
        "10.10.12.0/22",
    ]


def test_split_rejects_bigger_prefix():
    with pytest.raises(ValueError):
        core.split("10.0.0.0/24", 16)


def test_parse_cidr_rejects_host_bits():
    with pytest.raises(ValueError):
        core.parse_cidr("10.0.0.1/24")


def test_overlaps_returns_empty_for_disjoint_cidrs():
    assert core.overlaps(["10.0.0.0/24", "10.0.1.0/24"]) == []


def test_overlaps_returns_pair_for_overlapping_cidrs():
    assert core.overlaps(["10.0.0.0/24", "10.0.0.128/25"]) == [
        ("10.0.0.0/24", "10.0.0.128/25")
    ]


def test_overlaps_returns_pair_for_identical_blocks():
    assert core.overlaps(["10.0.0.0/24", "10.0.0.0/24"]) == [
        ("10.0.0.0/24", "10.0.0.0/24")
    ]


def test_overlaps_rejects_invalid_cidr():
    with pytest.raises(ValueError):
        core.overlaps(["10.0.0.0/24", "not-a-cidr"])
