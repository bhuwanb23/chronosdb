# Data Quality and Partial Results

Critical missing data is isolated to the affected entity whenever possible.
For example, a customer line without a promised date is reported as
`INSUFFICIENT_DATA`, excluded from numerical SLA and revenue totals, and does
not make the line appear on time.

Runs distinguish complete, noncritical partial, critical partial,
insufficient, and invalid states. Machine-readable issue codes preserve the
entity, severity, message, and affected outputs.
