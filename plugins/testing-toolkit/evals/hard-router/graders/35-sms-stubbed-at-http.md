---
type: regex
weight: 2
target: {source: file, path: tests/test_sms_client.py}
match: contains
---

import responses|from responses|responses\.(activate|add|post|RequestsMock)|requests_mock|pytest_httpserver|HTTPServer|http\.server|wiremock|\b[Pp]act\b
