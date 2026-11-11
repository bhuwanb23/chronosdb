10. Phase 4F: Inventory-Ledger Production
Goal

Create a reconciled inventory history rather than independent random snapshots.

Inventory events

The release must include:

Plain Text
OPENING_BALANCE
PURCHASE_RECEIPT
PRODUCTION_RESERVATION
PRODUCTION_ISSUE
PRODUCTION_RETURN
TRANSFER_RESERVATION
TRANSFER_DISPATCH
TRANSFER_RECEIPT
QUARANTINE
RELEASE_FROM_QUARANTINE
POSITIVE_ADJUSTMENT
NEGATIVE_ADJUSTMENT
Ledger principle

Inventory snapshots must be derived from the transaction ledger.

For warehouse www, component ccc, and time ttt:

OnHandw,c,t=Openingw,c+Receipts+TransfersIn+PositiveAdjustments+ProductionReturns−ProductionIssues−TransfersOut−NegativeAdjustmentsOnHand_{w,c,t} = Opening_{w,c} + Receipts + TransfersIn + PositiveAdjustments + ProductionReturns - ProductionIssues - TransfersOut - NegativeAdjustmentsOnHandw,c,t​=Openingw,c​+Receipts+TransfersIn+PositiveAdjustments+ProductionReturns−ProductionIssues−TransfersOut−NegativeAdjustments
Inventory state fields
Plain Text
on_hand_quantity
reserved_quantity
quarantined_quantity
available_quantity
safety_stock_quantity
snapshot_time
Available quantity
Available=max⁡(0,OnHand−Reserved−Quarantined)Available = \max( 0, OnHand - Reserved - Quarantined )Available=max(0,OnHand−Reserved−Quarantined)
Transferable quantity
Transferable=max⁡(0,Available−ProtectedSafetyStock−CommittedFutureDemand)Transferable = \max( 0, Available - ProtectedSafetyStock - CommittedFutureDemand )Transferable=max(0,Available−ProtectedSafetyStock−CommittedFutureDemand)
Golden inventory
Pune
Plain Text
Component: CMP-MCU-42
On hand: 400
Reserved: 0
Quarantined: 0
Safety stock: 100
Chennai
Plain Text
Component: CMP-MCU-42
On hand: 700
Reserved or protected local demand: 180
Quarantined: 0
Safety stock: 120
Maximum transferable: 400

Validation:

700−180−120=400700 - 180 - 120 = 400700−180−120=400
Reconciliation requirements

For every warehouse-component pair:

Opening balance exists.
Every transaction has a valid sign and type.
Transfer dispatch has a corresponding receipt or open in-transit state.
Snapshots match the ledger.
Quantity cannot appear without a source transaction.
Inventory cannot be simultaneously allocated twice.
Deliverables
Plain Text
data/releases/v1.0.0/inventory/
├── inventory_opening_balances.csv
├── inventory_transactions.csv
├── inventory_reservations.csv
├── inventory_snapshots_daily.csv
├── inventory_snapshots_benchmark.csv
└── transfer_transactions.csv
Exit gate
Plain Text
Inventory reconciliation error = 0
Double allocations = 0
Negative unexplained balances = 0
Invalid transfer pairs = 0
