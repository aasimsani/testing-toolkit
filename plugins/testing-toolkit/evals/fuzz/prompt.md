---
name: fuzz
tags: [harness, python, static]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add a fuzz harness for `parse_config`. Put the harness in `fuzz/fuzz_parse_config.py` and its seed corpus in `fuzz/corpus/parse_config/`. Atheris isn't installed on this machine, so the fuzzer can't run here. CI runs it.
