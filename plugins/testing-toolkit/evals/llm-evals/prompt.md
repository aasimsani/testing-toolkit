---
name: llm-evals
tags: [harness, promptfoo, static]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add the regression eval suite for the extraction prompt. Put the promptfoo config in `evals/promptfooconfig.yaml` and the dataset under `evals/datasets/`. There's no API key on this machine, so the suite can't run here.
