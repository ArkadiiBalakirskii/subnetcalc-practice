"""Command line interface: python -m subnetcalc <command> ..."""

from __future__ import annotations

import argparse
import sys

from . import __version__, core


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="subnetcalc", description="AWS subnet calculator")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    info = sub.add_parser("info", help="show total and AWS-usable IPs")
    info.add_argument("cidr")

    sp = sub.add_parser("split", help="split a block into smaller subnets")
    sp.add_argument("cidr")
    sp.add_argument("--prefix", type=int, required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "info":
            print(f"CIDR:        {core.parse_cidr(args.cidr)}")
            print(f"Total IPs:   {core.total_ips(args.cidr)}")
            print(f"AWS usable:  {core.aws_usable_ips(args.cidr)}")
        elif args.command == "split":
            for subnet in core.split(args.cidr, args.prefix):
                print(subnet)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
