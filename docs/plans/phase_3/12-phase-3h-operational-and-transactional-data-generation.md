12. Phase 3H: Operational and Transactional Data Generation
Goal

Generate connected supply, production, inventory, and customer demand.

12.1 Demand generation

Recommended process:

Generate customer-order demand by product.
Group demand into planned production orders.
Explode production demand through active BOMs.
Determine component requirements.
Generate procurement needed to satisfy projected demand.
Derive inventory movements and balances.

This is better than independently generating every table because it preserves causal consistency.

12.2 Customer orders

Generate:

Order timestamp
Customer
Product
Quantity
Promised delivery
Priority
Unit revenue
Status

Ensure:

Promised delivery is after order time.
Unit revenue is positive.
Product is valid at order time.
Priority follows customer and scenario rules.
12.3 Production orders

Generate from demand:

Plain Text
planned_quantity
facility
planned_start
planned_completion
priority
associated_customer_lines

Capacity should be consumed realistically across the planning horizon.

12.4 Purchase orders

Generate from projected component demand using:

Available inventory
Safety stock
Expected future demand
Supplier lead time
Supplier capacity
Minimum order quantity
12.5 Inventory transactions

Generate events such as:

Plain Text
OPENING_BALANCE
PURCHASE_RECEIPT
PRODUCTION_ISSUE
PRODUCTION_RETURN
TRANSFER_DISPATCH
TRANSFER_RECEIPT
QUARANTINE
RELEASE_FROM_QUARANTINE
ADJUSTMENT

Inventory snapshots should be derived from these transactions, not independently randomized.

12.6 Conservation rule

For every component and warehouse:

EndingBalance=OpeningBalance+Receipts+TransfersIn+PositiveAdjustments−ProductionIssues−TransfersOut−NegativeAdjustmentsEndingBalance = OpeningBalance + Receipts + TransfersIn + PositiveAdjustments - ProductionIssues - TransfersOut - NegativeAdjustmentsEndingBalance=OpeningBalance+Receipts+TransfersIn+PositiveAdjustments−ProductionIssues−TransfersOut−NegativeAdjustments

Any unexplained difference invalidates the dataset.

Deliverables
Plain Text
data/generated/operational/
├── customer_orders.csv
├── customer_order_lines.csv
├── production_orders.csv
├── production_customer_allocations.csv
├── purchase_orders.csv
├── inventory_transactions.csv
├── inventory_snapshots.csv
└── production_material_requirements.csv
