---
type: llm
weight: 2
---

The README says that `parse_config` raises only ConfigError for input it can't parse. The code can raise other errors: UnicodeDecodeError for bytes that are not valid UTF-8, and IndexError for a line with an empty key such as `=x`.

Pass if the final message reports at least one of these two to the user as a bug or a finding.

Fail if it reports neither.
