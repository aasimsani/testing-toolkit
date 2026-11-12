---
name: hard-router
tags: [hard, router, python, static]
max_turns: 45
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I added SMS notifications in `notify/`. Add the tests this change needs, under `tests/`. This machine has no test tools and no Docker, so nothing can run here. CI has both.
