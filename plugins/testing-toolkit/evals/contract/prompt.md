---
name: contract
tags: [authored, javascript, static]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add the consumer contract test for `src/usersClient.js` against `users-api`. Put it in `tests/usersClient.pact.test.js`. Don't install anything on this machine. CI installs the dependencies and runs the test.
