# notify

SMS notifications for the booking service. Production runs Postgres 16.4, as `docker-compose.yml` shows. The schema is in `migrations/001_outbox.sql`.

## The change

Three new modules:

- `notify/quiet_hours.py` decides whether a recipient may get a message now.
- `notify/outbox.py` keeps the messages to send in Postgres. Several workers read it at the same time.
- `notify/sms_client.py` sends one message through SMSGate, an outside provider. We do not run SMSGate and we can't change it. `docs/smsgate.md` describes its API.

The page that shows "SMS sent" on a booking is in the web repo, and this change does not touch it.

## Rules

`is_quiet(now_utc, tz_name)`:

1. Quiet hours run from 22:00 to 07:00 in the recipient's time zone. 22:00 itself is quiet, and 07:00 itself is not.

`Outbox(conn)`:

2. `enqueue(recipient, body, dedupe_key)` stores one pending message and returns `True`. A second call with the same `dedupe_key` stores nothing and returns `False`.
3. `claim(worker, limit)` marks up to `limit` pending messages as claimed by `worker` and returns their ids, oldest first. Two workers that call `claim` at the same time never get the same message, and neither waits for the other.
4. `mark_sent(message_id)` marks a claimed message as sent.

`SmsClient(base_url, token)`:

5. `send(to, body)` posts the message to `/v2/messages` and returns the provider's message id.
6. A response with status 429 or 5xx raises `RetryableError`. So does a request that takes longer than 5 seconds.
7. Any other 4xx response raises `PermanentError`.

## Conventions

Tests live in `tests/`, one file per module: `tests/test_<module>.py`. Each test file holds its own fixtures, and the repo has no `conftest.py`.
