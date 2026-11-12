CREATE TABLE outbox (
    id bigserial PRIMARY KEY,
    recipient text NOT NULL,
    body text NOT NULL,
    dedupe_key text NOT NULL UNIQUE,
    status text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'claimed', 'sent')),
    claimed_by text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX outbox_pending ON outbox (id) WHERE status = 'pending';
