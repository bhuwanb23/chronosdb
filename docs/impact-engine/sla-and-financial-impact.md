# SLA and Financial Impact

For every complete customer line:

`delay_hours = max(0, projected_delivery - promised_delivery)`

`revenue_at_risk = late_quantity * unit_revenue`

The engine reports line and customer breach counts, late quantity, maximum
and average delay, quantity-weighted delay, and INR revenue at risk. Revenue
at risk is bounded by the open quantity times unit revenue and never includes
on-time quantity.

Missing promised dates produce `INSUFFICIENT_DATA`; they are not treated as
on-time and are excluded from numeric financial totals.
