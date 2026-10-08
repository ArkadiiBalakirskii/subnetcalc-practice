# subnetcalc

Tiny new subnet calculator (offline, no AWS account needed — it only does math with Python's `ipaddress`). **Practice project** for Git Flow, GitHub and AI tools (GitHub Copilot, Claude).

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q

python -m subnetcalc info 10.10.0.0/22
python -m subnetcalc split 10.10.0.0/20 --prefix 22
```

AWS reserves 5 IP addresses in every subnet, so a /24 has 251 usable addresses.

See `PRACTICE_GUIDE.md` for the exercises.
