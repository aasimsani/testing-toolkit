# inventory

`inventory/repo.py` stores stock levels in Postgres. Production runs Postgres 15.6, as `docker-compose.yml` shows. The schema is in `migrations/001_stock.sql`.

## Rules

`StockRepo(conn)` wraps a psycopg connection.

1. `add_stock(sku, quantity)` creates the row for a new SKU, or adds to the quantity of an existing one.
2. `reserve(sku, quantity)` takes the quantity out of stock and returns `True`. When the stock is too low, it changes nothing and returns `False`.
3. Stock never goes below 0. The database enforces this with a check constraint.
4. SKUs are case-insensitive: `ab-1` and `AB-1` are the same SKU.
5. `available(sku)` returns the quantity in stock, or 0 for an unknown SKU.
