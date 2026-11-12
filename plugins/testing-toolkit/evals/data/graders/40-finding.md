---
type: llm
weight: 2
---

The README says that a customer whose orders were all cancelled still gets a row in dim_customers, with zero totals. The SQL removes cancelled orders before it groups, so such a customer gets no row.

Pass if the final message reports this disagreement between the SQL and the README.

Fail if the message does not mention it.
