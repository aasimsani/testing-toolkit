"""Messages to send, kept in Postgres so that a crash loses none."""

import psycopg


class Outbox:
    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn

    def enqueue(self, recipient: str, body: str, dedupe_key: str) -> bool:
        """Store one pending message, unless `dedupe_key` is already stored."""
        cur = self._conn.execute(
            "INSERT INTO outbox (recipient, body, dedupe_key) VALUES (%s, %s, %s) "
            "ON CONFLICT (dedupe_key) DO NOTHING",
            (recipient, body, dedupe_key),
        )
        return cur.rowcount == 1

    def claim(self, worker: str, limit: int) -> list[int]:
        """Mark up to `limit` pending messages as claimed by `worker`, oldest first."""
        rows = self._conn.execute(
            "UPDATE outbox SET status = 'claimed', claimed_by = %s "
            "WHERE id IN (SELECT id FROM outbox WHERE status = 'pending' "
            "ORDER BY id LIMIT %s FOR UPDATE SKIP LOCKED) RETURNING id",
            (worker, limit),
        ).fetchall()
        return sorted(row[0] for row in rows)

    def mark_sent(self, message_id: int) -> None:
        """Mark a claimed message as sent."""
        self._conn.execute(
            "UPDATE outbox SET status = 'sent' WHERE id = %s AND status = 'claimed'",
            (message_id,),
        )
