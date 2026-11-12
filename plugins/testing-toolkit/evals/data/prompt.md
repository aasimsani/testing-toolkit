---
name: data
tags: [authored, dbt, static]
max_turns: 20
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Add tests for `dim_customers` and for the data that feeds it. Put them in `models/schema.yml`. There's no warehouse connection on this machine, so dbt can't run here.
