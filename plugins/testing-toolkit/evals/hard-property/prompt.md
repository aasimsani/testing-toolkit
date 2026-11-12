---
name: hard-property
tags: [hard, harness, python, runnable]
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add property-based tests for `busy/periods.py` with Hypothesis. Put them in `tests/test_periods_properties.py`. The README has the rules and the command that runs the tests.
