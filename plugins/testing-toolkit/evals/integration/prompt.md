---
name: integration
tags: [authored, python, static]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add tests for `inventory/repo.py`. Put the tests and their fixtures in `tests/test_repo.py`, and add no other test file. Docker isn't running on this machine, so nothing here can start a database. CI has Docker.
