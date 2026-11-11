# Phase 2U: Adversarial Scenarios

## A. No impact

Sufficient inventory covers all demand across the horizon.

Expected: supply may be affected, but shortage is absent, SLA breaches are 0,
and revenue at risk is INR 0.

## B. No feasible intervention

No transfer is available, no approved alternate exists, the PO cannot be
expedited, and rescheduling cannot resolve the shortage.

Expected: `NO_FEASIBLE_INTERVENTION`; no least-invalid recommendation.

## C. Insufficient data

No valid inventory snapshot exists.

Expected: `INSUFFICIENT_DATA`, never zero inventory.

## D. Partial fulfilment

Half of an order line is delivered on time.

Expected: late quantity is half the order, one breached order, and proportional
revenue at risk.

## E. Cheaper but worse intervention

A candidate has the lowest cost but creates more SLA breaches.

Expected: it does not win `MINIMIZE_SLA_BREACHES`.

## F. Rescheduling externality

Moving one order earlier delays another order.

Expected: both helped and harmed orders appear in the result.

## G. Late correction

An inventory correction arrives after scenario completion.

Expected: completed scenario is unchanged; a new state version may use it.

## H. Identical candidates

Two candidates have identical metrics.

Expected: tie is reported; stable ID is used only if one recommendation is
required.

## I. Golden variant regression

Replace corrected Chennai on-hand 700 with the rejected 500 value.

Expected: validation catches transferable quantity 200 and rejects the locked
golden expected outputs rather than silently accepting a different ground
truth.
