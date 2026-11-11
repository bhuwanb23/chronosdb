7. Phase 3C: Synthetic Enterprise Blueprint
Goal

Create a coherent fictional manufacturer rather than disconnected random tables.

Enterprise identity

Use a clearly synthetic organization:

Plain Text
Company:
Asterion Control Systems
 
Industry:
Industrial electronics manufacturing
 
Primary products:
Industrial controllers and monitoring units
 
Primary regions:
India
 
Planning currency:
INR
 
Planning timezone:
Asia/Kolkata
 
Canonical timestamp storage:
UTC

Add this disclaimer everywhere required:

Asterion Control Systems and all suppliers, customers, transactions, incidents, prices, and operational records in this repository are synthetic and created solely for demonstration and evaluation.

Operational network
Facilities
Plain Text
FAC-PUNE
FAC-CHENNAI
Warehouses
Plain Text
WH-PUNE
WH-CHENNAI
WH-GURUGRAM
Supplier regions
India
Southeast Asia
East Asia
Europe

Regional diversity should affect lead time, not introduce unsupported geopolitical inference.

Product families

Recommended:

Plain Text
Controller-X
Controller-Pro
Sensor-Hub
Gateway-Edge
Monitor-Lite
Component families
Microcontrollers
Memory modules
Power units
Sensors
Connectors
Printed circuit boards
Casings
Cables
Displays
Communication modules
Customer classes
Plain Text
STRATEGIC
ENTERPRISE
STANDARD

Possible SLA patterns:

Class	Expected treatment
Strategic	Highest allocation priority
Enterprise	Medium priority
Standard	Standard priority

Do not use real customer names.

Deliverables
Plain Text
docs/data/synthetic-enterprise-blueprint.md
config/enterprise.yaml
