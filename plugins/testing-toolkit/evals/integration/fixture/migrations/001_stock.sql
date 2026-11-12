CREATE EXTENSION IF NOT EXISTS citext;

CREATE TABLE stock (
    sku citext PRIMARY KEY,
    quantity integer NOT NULL CHECK (quantity >= 0)
);
