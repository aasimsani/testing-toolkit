---
type: llm
weight: 3
focus: trace
---

The agent wrote a promptfoo config and one or more dataset files for an eval suite.

Pass if the files the agent wrote put deterministic checks on the model's reply: an exact comparison of a field, a JSON or schema check, a regex, or a JavaScript or Python assertion.

Fail if every check the agent wrote is an LLM-judged rubric.
