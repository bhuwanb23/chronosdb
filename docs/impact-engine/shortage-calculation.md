# Shortage Calculation

A shortage is evaluated at the requirement time, not by repeatedly summing
every later timeline point. Each requirement emits at most one shortage record
with required quantity, eligible quantity, unmet quantity, resolution time,
source receipt, and causal parents.

The engine distinguishes temporary, horizon, partial, and missing-data
shortages. A future receipt may resolve a temporary shortage; a receipt beyond
the horizon does not receive a fabricated completion time.
