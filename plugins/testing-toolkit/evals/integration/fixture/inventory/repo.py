"""Stock levels in Postgres."""

import psycopg


class StockRepo:
    """Read and change stock levels through one psycopg connection."""

    def __init__(self, conn: psycopg.Connection) -> None:
        self._conn = conn

    def add_stock(self, sku: str, quantity: int) -> None:
        """Create the row for a new SKU, or add to an existing one."""
        self._conn.execute(
            """
            INSERT INTO stock (sku, quantity) VALUES (%s, %s)
            ON CONFLICT (sku) DO UPDATE SET quantity = stock.quantity + EXCLUDED.quantity
            """,
            (sku, quantity),
        )

    def reserve(self, sku: str, quantity: int) -> bool:
        """Take ``quantity`` out of stock, and say whether that worked."""
        cur = self._conn.execute(
            "UPDATE stock SET quantity = quantity - %s WHERE sku = %s AND quantity >= %s",
            (quantity, sku, quantity),
        )
        return cur.rowcount == 1

    def available(self, sku: str) -> int:
        """Return the quantity in stock, or 0 for an unknown SKU."""
        row = self._conn.execute("SELECT quantity FROM stock WHERE sku = %s", (sku,)).fetchone()
        return row[0] if row else 0
