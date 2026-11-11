13. Phase 2I: Inventory Availability and Allocation Model
Goal

Define how material availability is calculated over time.

13.1 Inventory position

At warehouse www, component ccc, and time ttt:

AvailableInventoryw,c,t=OnHandw,c,t−Reservedw,c,t−Quarantinedw,c,tAvailableInventory_{w,c,t} = OnHand_{w,c,t} - Reserved_{w,c,t} - Quarantined_{w,c,t}AvailableInventoryw,c,t​=OnHandw,c,t​−Reservedw,c,t​−Quarantinedw,c,t​

For normal production use:

UsableInventory=max⁡(0,AvailableInventory)UsableInventory = \max(0, AvailableInventory)UsableInventory=max(0,AvailableInventory)
13.2 Projected inventory balance

For ordered event times t1…tnt_1 \dots t_nt1​…tn​:

Balancet=Balancet−1+Receiptst+TransfersInt−ProductionConsumptiont−TransfersOuttBalance_t = Balance_{t-1} + Receipts_t + TransfersIn_t - ProductionConsumption_t - TransfersOut_tBalancet​=Balancet−1​+Receiptst​+TransfersInt​−ProductionConsumptiont​−TransfersOutt​
13.3 Safety-stock distinction

Safety stock is not automatically unavailable for production in the MVP.

Recommended rule:

Production may consume below safety stock if required.
Optional warehouse transfers may not reduce the source warehouse below safety stock.
The resulting safety-stock breach is recorded as operational risk.

This prevents the model from declaring production impossible merely because inventory falls below a planning threshold.

13.4 Allocation priority

Recommended allocation sequence:

Already in-progress production orders
Released production orders
Higher-priority customer commitments
Earlier promised delivery
Earlier production-order creation
Stable identifier as deterministic tie-breaker
13.5 Reservation treatment

Avoid subtracting reservations twice.

Choose one authoritative approach.

Recommended model
Inventory snapshot stores physical on-hand and current reserved quantity.
Future simulation recalculates allocation from eligible demand.
The golden scenario explicitly identifies existing committed reservations.
13.6 Shortage definition

A shortage occurs when a material requirement cannot be fully allocated by the required consumption time.

ShortageQuantity=max⁡(0,RequiredQuantity−AllocatableQuantity)ShortageQuantity = \max(0, RequiredQuantity - AllocatableQuantity)ShortageQuantity=max(0,RequiredQuantity−AllocatableQuantity)
Shortage date

The earliest requirement time at which:

ProjectedBalancet<RequiredQuantitytProjectedBalance_t < RequiredQuantity_tProjectedBalancet​<RequiredQuantityt​
13.7 Warehouse-transfer availability

For a source warehouse:

TransferableQuantity=max⁡(0,ProjectedBalanceBeforeTransfer−SafetyStock−CommittedFutureDemand)TransferableQuantity = \max( 0, ProjectedBalanceBeforeTransfer - SafetyStock - CommittedFutureDemand )TransferableQuantity=max(0,ProjectedBalanceBeforeTransfer−SafetyStock−CommittedFutureDemand)

The planning window for committed demand must equal the scenario horizon or a defined transfer-protection window.

Deliverables
Plain Text
docs/domain/inventory-model.md
docs/domain/allocation-policy.md
Inventory invariants
Physical on-hand is never negative.
Allocated quantity never exceeds available eligible quantity.
Transfer quantity never exceeds transferable quantity.
The same inventory unit cannot be allocated to two production orders.
Reserved inventory is not subtracted twice.
Receipts cannot be consumed before arrival.
