---
type: llm
weight: 2
focus: {source: file, path: load/suggest.js}
---

Pass if the script supports at least two run sizes that are chosen without editing the file, for example through an environment variable: a short, small smoke run for pull requests, and a heavier or longer run for the nightly job.

Fail if the script has one fixed load shape.
