---
type: regex
weight: 2
target: {source: file, path: tests/usersClient.pact.test.js}
match: contains
---

\b(like|string|regex|integer|eachLike|term)\(|MatchersV3|Matchers\.
