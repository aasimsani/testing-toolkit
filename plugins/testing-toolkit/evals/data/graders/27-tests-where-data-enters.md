---
type: llm
weight: 2
focus: {source: file, path: models/schema.yml}
---

Pass if the file puts data tests on the source table `orders` or on the staging model `stg_orders`, for example unique and not_null on order_id.

Fail if every data test is on `dim_customers`.
