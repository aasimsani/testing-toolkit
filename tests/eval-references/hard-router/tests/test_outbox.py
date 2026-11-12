"""Reference result for the hard-router case: integration tests on the production Postgres.

The rules depend on the unique constraint and on FOR UPDATE SKIP LOCKED, which
only the real database implements.
"""

from pathlib import Path

import psycopg
import pytest
from testcontainers.postgres import PostgresContainer

from notify.outbox import Outbox

MIGRATION = Path(__file__).parent.parent / "migrations" / "001_outbox.sql"


@pytest.fixture(scope="module")
def dsn():
    with PostgresContainer("postgres:16.4", driver=None) as postgres:
        url = postgres.get_connection_url()
        with psycopg.connect(url, autocommit=True) as conn:
            conn.execute(MIGRATION.read_text())
        yield url


@pytest.fixture
def connect(dsn):
    opened = []

    def _connect():
        opened.append(psycopg.connect(dsn))
        return opened[-1]

    yield _connect
    for conn in opened:
        conn.rollback()
        conn.close()
    with psycopg.connect(dsn, autocommit=True) as conn:
        conn.execute("TRUNCATE outbox RESTART IDENTITY")


def enqueue_four(connect):
    conn = connect()
    for n in range(4):
        Outbox(conn).enqueue("+4915112345678", f"message {n}", f"key-{n}")
    conn.commit()


def test_second_enqueue_with_the_same_dedupe_key_stores_nothing(connect):
    conn = connect()
    assert Outbox(conn).enqueue("+4915112345678", "hello", "booking-7") is True
    assert Outbox(conn).enqueue("+4915112345678", "hello", "booking-7") is False
    assert conn.execute("SELECT count(*) FROM outbox").fetchone() == (1,)


def test_two_workers_that_claim_at_the_same_time_get_different_messages(connect):
    enqueue_four(connect)
    first, second = connect(), connect()
    # The first worker's transaction stays open while the second worker claims.
    assert Outbox(first).claim("worker-a", 2) == [1, 2]
    assert Outbox(second).claim("worker-b", 2) == [3, 4]


def test_mark_sent_changes_only_a_claimed_message(connect):
    enqueue_four(connect)
    conn = connect()
    Outbox(conn).claim("worker-a", 1)
    Outbox(conn).mark_sent(1)
    Outbox(conn).mark_sent(2)
    assert conn.execute("SELECT status FROM outbox ORDER BY id LIMIT 2").fetchall() == [("sent",), ("pending",)]
