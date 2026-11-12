CREATE TABLE refunds (
    id bigserial PRIMARY KEY,
    payment_id bigint NOT NULL,
    amount_cents integer NOT NULL CHECK (amount_cents > 0),
    idempotency_key text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX refunds_payment_id ON refunds (payment_id);
