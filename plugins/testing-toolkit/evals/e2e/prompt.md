---
name: e2e
tags: [authored, typescript, static]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add the E2E test for sign-up. Put it in `e2e/signup.spec.ts`. No browser is installed on this machine, so the test can't run here. CI runs Playwright.
