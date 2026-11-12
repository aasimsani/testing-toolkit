# payroll (legacy)

`legacy/payslip.py` renders the payslip text for one employee. It was written in 2014. It has no tests and no spec, and the person who wrote it has left.

Next sprint we replace the string building with a template engine. The output must not change.

## Running tests

```bash
.venv/bin/python -m pytest -q
```
