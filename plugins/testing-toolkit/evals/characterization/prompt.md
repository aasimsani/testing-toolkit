---
name: characterization
tags: [authored, python, runnable]
max_turns: 45
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I'm about to refactor `legacy/payslip.py`. Pin its current behaviour first, so that I can tell if the refactor changes anything. Put the tests in `tests/test_payslip_characterization.py`. Don't change what `render_payslip` does.
