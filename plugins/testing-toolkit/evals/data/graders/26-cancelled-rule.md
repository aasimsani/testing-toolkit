---
type: llm
weight: 3
focus: {source: file, path: models/schema.yml}
---

Pass if a dbt unit test gives mock input rows that include a cancelled order, and expects output in which that cancelled order is not counted.

Fail if no unit test has a cancelled order among its input rows.
