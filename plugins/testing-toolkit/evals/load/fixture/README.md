# suggest-api

`GET /suggest?q=<prefix>` returns search suggestions while a shopper types. It is the busiest endpoint we have: about 40 requests per second on a normal day, and 3 times that during a sale.

## Targets, from the SLO

- p95 latency under 200 ms
- p99 latency under 500 ms
- Fewer than 0.5% of requests fail

## Environments

- Staging. The base URL is in `$BASE_URL`.
- `data/prefixes.json` holds prefixes that shoppers really typed.

We have no load test yet. We want one that runs on every PR and a heavier one that runs overnight. k6 is the tool the platform team supports.
