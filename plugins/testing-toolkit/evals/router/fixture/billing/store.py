"""Refund records in Postgres."""

import psycopg


class RefundStore:
    """Record refunds through one psycopg connection."""

    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn

    def record(self, payment_id: int, amount_cents: int, idempotency_key: str) -> bool:
        """Store one refund, and say whether this call stored it."""
        cur = self._conn.execute(
            """
            INSERT INTO refunds (payment_id, amount_cents, idempotency_key)
            VALUES (%s, %s, %s)
            ON CONFLICT (idempotency_key) DO NOTHING
            """,
            (payment_id, amount_cents, idempotency_key),
        )
        return cur.rowcount == 1

    def total_refunded(self, payment_id: int) -> int:
        """Return the sum of the refunds for one payment."""
        row = self._conn.execute(
            "SELECT COALESCE(SUM(amount_cents), 0) FROM refunds WHERE payment_id = %s",
            (payment_id,),
        ).fetchone()
        return int(row[0])
