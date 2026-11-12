---
name: property
tags: [harness, python, runnable]
max_turns: 45
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add property-based tests for `textcodec/rle.py` with Hypothesis. Put them in `tests/test_rle_properties.py`. The README has the rules and the command that runs the tests.
