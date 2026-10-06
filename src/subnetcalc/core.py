"""Core subnet calculations.

AWS reserves 5 addresses in every subnet: network, VPC router, DNS,
one reserved for future use, and broadcast.
"""

from __future__ import annotations

import ipaddress

AWS_RESERVED_IPS = 5


def parse_cidr(cidr: str) -> ipaddress.IPv4Network:
    """Parse an IPv4 CIDR string (strict: host bits must be zero)."""
    return ipaddress.IPv4Network(cidr, strict=True)


def total_ips(cidr: str) -> int:
    """Total number of addresses in the CIDR block."""
    return parse_cidr(cidr).num_addresses


def aws_usable_ips(cidr: str) -> int:
    """Addresses you can actually use in an AWS subnet."""
    # NOTE: practice bug lives here on purpose — see PRACTICE_GUIDE.md, task 3.
    return max(total_ips(cidr) - 4, 0)


def split(cidr: str, new_prefix: int) -> list[str]:
    """Split a CIDR block into equal subnets with the given prefix length."""
    network = parse_cidr(cidr)
    if new_prefix < network.prefixlen:
        raise ValueError(
            f"new prefix /{new_prefix} is larger than the network /{network.prefixlen}"
        )
    return [str(s) for s in network.subnets(new_prefix=new_prefix)]


def overlaps(cidrs: list[str]) -> list[tuple[str, str]]:
    """Return every pair of CIDR blocks that overlap.

    TODO: implement (practice task 4 — give this to Copilot as a GitHub issue).
    """
    raise NotImplementedError
