3. Phase 0B: Official-Source and Requirements Control
Goal

Create one traceable source of truth from conflicting public instructions.

## Source hierarchy

### Use this order:

Written organizer clarification
Devpost rules
Canonical repository instructions
Official event listing
Repository FAQ
Community messages
Personal interpretations
Important current requirements

### The official rules assign:

30% to Db2 integration and depth
25% to innovation and impact
20% to architecture and AI integration
15% to reproducibility and code quality
10% to documentation and presentation

### The canonical submission guide requires the project under:

submissions/<project-slug>/


### with the main implementation under src/, plus required metadata and documentation. It uses a feature branch named:

submission/<project-slug>


and requires lowercase alphanumeric characters and hyphens in the slug.

### Subphase 0B.1: Requirements register

### Create:

docs/project-control/requirements-register.csv


### Recommended fields:

requirement_id
requirement_text
category
source
source_date
mandatory
evidence_required
implementation_location
verification_method
status
conflict_id
notes


### Example:

SUB-001
Project must be submitted through a PR
Submission
Devpost rules
2026-11-10
Yes
PR URL
GitHub
Manual verification
Open
None

### Subphase 0B.2: Conflict register

### Create identifiers such as:

CONFLICT-001 Deadline mismatch
CONFLICT-002 Individual versus team eligibility
CONFLICT-003 AI framework required versus optional
CONFLICT-004 Correct official repository and current template
CONFLICT-005 Post-deadline update permission


### Each conflict needs:

Conflicting statements
Source references
Risk
Temporary conservative rule
Resolution owner
Final resolution
Conservative behavior

### Until clarified:

Treat participation as individual.
Include an approved framework.
Treat the earliest deadline as authoritative.
Use the canonical KunalGolaIBM repository.
Do not assume post-deadline changes are accepted.
Subphase 0B.3: Compliance matrix

### Create:

docs/project-control/compliance-matrix.md


### Each requirement must map to:

Requirement
→ Repository artifact
→ Verification command
→ Submission evidence

Benchmark
Requirement Coverage Ratio
RCR=mandatory requirements with verificationtotal mandatory requirementsRCR = \frac{\text{mandatory requirements with verification}}{\text{total mandatory requirements}}

### Target:

## RCR = 100%

Conflict Closure Ratio
CCR=resolved critical conflictstotal critical conflictsCCR = \frac{\text{resolved critical conflicts}}{\text{total critical conflicts}}

### Required to leave Phase 0:

## CCR = 100%


A conflict can remain open only if it is non-critical and the conservative interpretation prevents non-compliance.

