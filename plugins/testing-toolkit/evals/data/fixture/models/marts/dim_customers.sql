with orders as (
    select * from {{ ref('stg_orders') }}
    where status != 'cancelled'
)

select
    customer_id,
    min(cast(ordered_at as date)) as first_order_date,
    count(*) as lifetime_orders,
    sum(amount_cents) as lifetime_value_cents
from orders
group by customer_id
