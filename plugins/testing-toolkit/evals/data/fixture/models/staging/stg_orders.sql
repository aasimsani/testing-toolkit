select
    order_id,
    customer_id,
    lower(status) as status,
    amount_cents,
    ordered_at,
    nullif(coupon_code, '') as coupon_code
from {{ source('shop', 'orders') }}
