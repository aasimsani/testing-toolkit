---
type: llm
weight: 3
focus: {source: file, path: tests/usersClient.pact.test.js}
---

The consumer reads three fields from the response: displayName, avatarUrl and plan.

Pass if every response body that a Pact interaction expects holds only fields from that list.

Fail if an expected response body also lists any of these fields: id, email, createdAt, address, preferences, lastLoginAt.
