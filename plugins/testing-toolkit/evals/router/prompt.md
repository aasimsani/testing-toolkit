---
name: router
tags: [router, python, static]
max_turns: 25
timeout_seconds: 480
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I added refunds in `billing/`. Add the tests this change needs, under `tests/`. This machine has no test tools and no Docker, so nothing can run here. CI has both.
