16. Phase 5L: Customer Fulfilment Engine
Goal

Map projected production output to customer-order fulfilment.

Fulfilment inputs
Customer-order lines
Unfulfilled quantities
Linked production orders
Finished inventory, if modelled
Product availability
Customer priority
Promised delivery
Delivery lead time
Allocation priority
Explicit customer priority
SLA class
Promised delivery time
Order time
Stable order-line ID
Product availability events

Each completed production batch creates:

Plain Text
product_id
quantity
availability_time
production_batch_id
facility_id
On-time quantity

Quantity available early enough to meet delivery commitment:

OnTimeQuantityl=min⁡(OpenQuantityl,EligibleQuantityAvailableByCutoffl)OnTimeQuantity_l = \min( OpenQuantity_l, EligibleQuantityAvailableByCutoff_l )OnTimeQuantityl​=min(OpenQuantityl​,EligibleQuantityAvailableByCutoffl​)
Late quantity
LateQuantityl=max⁡(0,OpenQuantityl−OnTimeQuantityl)LateQuantity_l = \max( 0, OpenQuantity_l - OnTimeQuantity_l )LateQuantityl​=max(0,OpenQuantityl​−OnTimeQuantityl​)
Projected delivery
ProjectedDeliveryl=ProductAvailabilityTimel+DeliveryLeadTimelProjectedDelivery_l = ProductAvailabilityTime_l + DeliveryLeadTime_lProjectedDeliveryl​=ProductAvailabilityTimel​+DeliveryLeadTimel​

For partial fulfilment, preserve multiple fulfilment segments:

JSON
{
"order_line_id": "COL-0704-01",
"segments": [
{
"quantity": 100,
"projected_delivery": "..."
},
{
"quantity": 100,
"projected_delivery": "..."
}
]
}
No double fulfilment
∑FulfilledQuantitysegments≤OpenOrderLineQuantity\sum FulfilledQuantity_{segments} \le OpenOrderLineQuantity∑FulfilledQuantitysegments​≤OpenOrderLineQuantity
Deliverables
Plain Text
src/backend/chronosdb/impact/fulfilment/
docs/impact-engine/customer-fulfilment.md
