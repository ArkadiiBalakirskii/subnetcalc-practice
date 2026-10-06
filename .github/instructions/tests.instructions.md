---
applyTo: "tests/**/*.py"
---
- Use plain pytest functions (no classes) and `pytest.raises` for errors.
- One behaviour per test; name tests `test_<what>_<expected>`.
- Prefer real CIDR examples from AWS VPC layouts (e.g. 10.10.0.0/20, /24, /22).
