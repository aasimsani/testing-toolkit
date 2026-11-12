---
type: llm
weight: 2
focus: {source: file, path: e2e/signup.spec.ts}
---

A sign-up test that uses one fixed email passes once and fails on the next run, because the email is then taken.

Pass if the test avoids that: it builds a unique email for each run, or it removes its user through the API helper under /api/test/users before or after the test.

Fail if the test signs up with one fixed email and never removes that user.
