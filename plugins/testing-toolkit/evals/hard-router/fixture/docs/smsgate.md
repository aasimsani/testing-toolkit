# SMSGate API, version 2

`POST /v2/messages` with the header `Authorization: Bearer <token>` and a JSON body:

```json
{ "to": "+4915112345678", "body": "Your booking is confirmed." }
```

| Status | Meaning | Body |
|---|---|---|
| 201 | The message is queued | `{ "id": "msg_01HZX", "status": "queued" }` |
| 400 | The number or the body is invalid | `{ "error": "invalid_number" }` |
| 401 | The token is wrong | `{ "error": "unauthorized" }` |
| 429 | Too many requests. The `Retry-After` header gives the seconds to wait | `{ "error": "rate_limited" }` |
| 503 | SMSGate is down for a short time | none |

SMSGate has no sandbox and no test numbers. Every accepted request sends a real message and costs money.
