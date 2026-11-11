# Phase 0 Deep Dive: Project Control, Submission Safety and Engineering Baseline

## Phase 0 is not a planning formality. Its purpose is to remove every administrative, environmental, repository and dependency risk that could invalidate ChronosDB before product development begins.

There is one immediate blocker: it is currently 11 November 2026 in Chennai, while the official IBM Db2Hack 2026 rules state a final submission deadline of 10 November 2026 at 5:00 PM IST. The header reportedly shows 7:00 PM, so the official page itself is inconsistent. The event listing also says results are scheduled for 11 November. Therefore, Phase 0A must be completed before writing new product code.

0. Phase Definition
0.1 Goal

Establish a verified and reproducible foundation from which every later phase can proceed safely.

### At the end of Phase 0, we must know:

Whether the project is eligible for evaluation.
Whether an existing submission can still be updated.
Which rules are authoritative.
Which repository, branch and project directory must be used.
Which exact technical environment will be used.
Whether the application can establish a real Db2 connection.
Whether the project can be installed, validated and tested from a clean checkout.
Whether secrets, licenses and dependencies are controlled.
Whether decisions, risks and evidence are being recorded consistently.
Whether Phase 1 can begin without unresolved critical ambiguity.
0.2 Required final result

## Phase 0 is complete only when we have a Foundation Release, tagged:

phase-0-foundation


### That release must include:

Verified eligibility and submission status
Official requirements register
Repository and branch baseline
Required submission files
Reproducible development environment
Real Db2 connectivity
Health-check command
Minimal automated tests
CI validation
Secret scanning
Dependency and license inventory
Risk register
Assumption register
Decision log
Phase 0 benchmark report
Phase 0 handoff package for Phase 1
1. Phase 0 Structure
Phase 0
├── 0A. Submission and eligibility control
├── 0B. Official-source and requirements control
├── 0C. Scope and project identity lock
├── 0D. Repository and submission workspace
├── 0E. Engineering environment baseline
├── 0F. IBM Db2 environment baseline
├── 0G. Application skeleton and connectivity
├── 0H. Quality automation and CI
├── 0I. Security, secrets and license hygiene
├── 0J. Project governance and traceability
├── 0K. Foundation benchmarking
├── 0L. Failure recovery and backup
└── 0M. Final acceptance and Phase 1 handoff

2. Phase 0A: Submission and Eligibility Control
Goal

Determine whether ChronosDB can still be submitted, evaluated or updated.

## Why this is the first gate

### The official IBM Db2Hack 2026 rules say:

Submission requires a Pull Request to the official GitHub repository.
The PR link must be submitted through the official Google Form.
Working code, setup instructions and documentation are required.
The project use case must be shared on LinkedIn.
Late or incomplete submissions may not qualify.

### The event listing adds that:

Participation is individual.
Both the GitHub PR and Google Form are mandatory.
Four files are mandatory: README.md, architecture.md, submission.json and .env.example.
At least one listed framework is mandatory according to that event listing.
The listed frameworks include LangChain, LlamaIndex, Haystack, CrewAI and Langflow.

However, the canonical GitHub FAQ says AI frameworks are optional and says teams may be eligible subject to official rules. That conflicts with the event listing, which says individual participation and framework use are mandatory.

### Subphase 0A.1: Submission-state inventory

### Record the status of each item:

| Item | Required evidence |
| --- | --- |
| Devpost registration | Screenshot or registration confirmation |
| Luma/Unstop registration | Confirmation or participant page |
| Official repository fork | Fork URL |
| Submission branch | Branch URL |
| Existing PR | PR URL and timestamp |
| Google Form | Confirmation screenshot or email |
| LinkedIn post | Public URL |
| Demo video | Accessible URL |
| Organizer permission | Message, email or announcement |

### Use statuses:

CONFIRMED
NOT COMPLETED
UNKNOWN
NOT APPLICABLE
BLOCKED

### Subphase 0A.2: Deadline reconciliation

### Create a deadline evidence table:

| Source | Displayed deadline | Authority level |
| --- | --- | --- |
| Devpost rules body | 10 Nov 2026, 5:00 PM IST | Highest available public rule |
| Devpost page header | 10 Nov 2026, 7:00 PM IST | Conflicting platform display |
| Luma listing | 10 Nov 2026, 5:00 PM IST | Organizer listing |
| User-provided display | 11 Nov 2026, 1:30 PM IST | Conflicting personalized display |
| Organizer message | To be captured | Final operational clarification |

The official public sources are inconsistent, so do not infer continued eligibility from the countdown alone.

### Subphase 0A.3: Organizer clarification

### Send one precise message through the official community or direct contacts:

I registered for IBM Db2Hack 2026 and am preparing ChronosDB. Devpost displays conflicting deadline information: the rules body lists 10 November 2026 at 5:00 PM IST, while another page display shows a different time. Please confirm whether a new submission is still accepted or whether an existing PR can still receive commits. I will follow the official decision immediately.

Do not expose project secrets or send code.

Decision states
State A: PR and form already submitted

Proceed, but establish whether additional commits are allowed.

The repository FAQ says an existing PR can be updated by pushing additional commits before the deadline. It does not authorize post-deadline commits.

## State B: PR exists, form not submitted

Treat eligibility as blocked until organizers explicitly approve.

## State C: Neither exists

### Treat official competition submission as blocked unless organizers grant an exception. Continue building only as:

Portfolio project
Open-source contribution candidate
Future IBM Db2 sample
Backup if submission is reopened
State D: Organizer permits late submission or update

Capture written proof and record exact constraints.

Required deliverable
docs/project-control/submission-status.md


### It must contain:

Status of every submission requirement
Deadline evidence
Organizer response
Allowed actions
Prohibited actions
Final Go, Conditional Go or No-Go decision
Acceptance criteria
No deadline assumption remains undocumented.
Existing PR and form status are evidenced.
Participation mode is known.
Permission to update after the deadline is explicit, if applicable.
We do not claim hackathon eligibility without evidence.
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

4. Phase 0C: Scope and Project Identity Lock
Goal

Prevent architecture drift, naming inconsistency and feature expansion.

Locked identity
Project name: ChronosDB
Descriptive name: ChronosDB: Auditable Counterfactual Intelligence
Domain: Supply-chain disruption decision intelligence
Primary scenario: Critical supplier outage
Database: IBM Db2
AI framework: LangChain
Backend: Python + FastAPI
Frontend: React-based web interface
Primary user: Supply-chain operations manager


LangChain is the recommended qualifying framework because it can support typed planning and retrieval without forcing the simulation engine into an agent framework. This lets deterministic Python and SQL retain authority over business calculations.

### Subphase 0C.1: Product charter

### Create:

docs/project-control/product-charter.md


### It must include:

## Problem

Operations teams can observe disruptions but struggle to trace cascading impacts and compare auditable recovery plans.

## Product promise

ChronosDB reconstructs supply-chain state, simulates alternative interventions and proves every recommendation using Db2 evidence.

In scope
Supplier outage
Inventory projection
BOM dependency propagation
Production delay
Customer SLA impact
Revenue at risk
Intervention comparison
Db2 evidence
Decision audit
Out of scope for MVP
Live ERP integration
Real-time external news
Multi-company collaboration
Autonomous purchasing
Monte Carlo forecasts
Geographic route optimization
Multiple LLM providers
Agent debate
Direct production actions
Subphase 0C.2: Terminology lock

### Define exact meanings:

revenue_at_risk, not revenue lost
projected_delay_days, not confirmed delay
recommended_intervention, not autonomous decision
simulation, not prediction unless a predictive model exists
confidence, only when mathematically defined
evidence, only when linked to a source record
Exit criterion

No major project description should use language that exceeds implemented capability.

5. Phase 0D: Repository and Submission Workspace
Goal

Create a repository structure that passes the official validator and remains maintainable.

## Canonical setup

### Use the canonical repository described in the submission guide:

git clone https://github.com/<username>/IBM_Db2_TechX_Project_Submission.git
cd IBM_Db2_TechX_Project_Submission
git remote add upstream https://github.com/KunalGolaIBM/IBM_Db2_TechX_Project_Submission.git
git fetch upstream main
git checkout -b submission/chronosdb upstream/main
cp -r submissions/_template submissions/chronosdb


The official guide specifies this fork, branch and template workflow.

Target structure
submissions/chronosdb/
├── README.md
├── architecture.md
├── submission.json
├── .env.example
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── package.json
├── src/
│   ├── backend/
│   │   └── chronosdb/
│   │       ├── api/
│   │       ├── core/
│   │       ├── db/
│   │       ├── domain/
│   │       ├── services/
│   │       └── main.py
│   └── frontend/
├── sql/
│   ├── migrations/
│   ├── seeds/
│   └── health/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── security/
├── benchmarks/
├── scripts/
├── docs/
│   ├── screenshots/
│   ├── project-control/
│   └── evidence/
└── artifacts/

Required initial files
submission.json

Populate all known fields with valid, honest values. Do not leave invalid placeholders that break JSON.

.env.example

### Only variable names and dummy values:

DB2_HOST=localhost
DB2_PORT=50000
DB2_DATABASE=CHRONOS
DB2_USERNAME=db2inst1
DB2_PASSWORD=replace-me
DB2_SCHEMA=CHRONOS
LLM_PROVIDER=disabled
LLM_API_KEY=replace-me
LOG_LEVEL=INFO
APP_ENV=development


Never commit .env.

.gitignore

### Include:

.env
.env.*
!.env.example
__pycache__/
*.pyc
.venv/
node_modules/
dist/
coverage/
.pytest_cache/
*.log
.DS_Store

## Local submission validation

### The repository provides:

python scripts/validate_submission.py submissions/chronosdb


Run this in Phase 0 and in CI. The submission guide explicitly recommends the local validator.

Benchmarks
| Test | Target |
| --- | --- |
| Official validator | 100% pass |
| Required files present | 4/4 |
| Invalid JSON | 0 |
| Files outside project folder changed | 0 |
| Broken internal documentation links | 0 |
| Untracked required source files | 0 |
Exit criterion

A clean branch containing only the foundation structure passes the official validator.

6. Phase 0E: Engineering Environment Baseline
Goal

Make developer behavior reproducible before building domain logic.

Recommended baseline
Backend
Python 3.11 or 3.12
FastAPI
Pydantic v2
ibm_db
SQLAlchemy plus ibm_db_sa, only if tested against the selected Db2 version
LangChain
pytest
Ruff
MyPy
Bandit
pip-audit
Frontend
Node.js 20 LTS or newer supported LTS
TypeScript
React
Vite or Next.js
ESLint
Vitest
General
Git
Make
Docker-compatible runtime if supported
Visual Studio Code
Java 17 for the Db2 Developer Extension

The official extension documentation currently lists Visual Studio Code 1.103.0 or newer and Java 17 or newer as prerequisites.

### Subphase 0E.1: Version manifest

### Create:

docs/project-control/version-matrix.md


### Include:

| Component | Required | Detected | Verification command |
| --- | --- | --- | --- |
| Python | 3.11.x or chosen version | Actual | python --version |
| Node.js | Chosen LTS | Actual | node --version |
| npm | Locked | Actual | npm --version |
| Java | 17+ | Actual | java -version |
| Git | Recorded | Actual | git --version |
| Db2 | Exact edition/version | Actual | Db2 version query |
| ibm_db | Locked | Actual | Package query |
Subphase 0E.2: Dependency locking

### Do not rely solely on broad ranges such as:

fastapi>=0.100


Create deterministic locks or exact package versions.

### Subphase 0E.3: Standard commands

### The following command contract should exist:

make doctor
make install
make lint
make typecheck
make test
make validate-submission
make security
make db-health


## Phase 0 does not need make demo; that comes later.

## Environment benchmark

### On a clean checkout:

Environment diagnosis: under 30 seconds
Dependency installation: ideally under 10 minutes on normal broadband
Lint and foundation tests: under 2 minutes
No undocumented global Python or Node dependency
Same test result on two consecutive runs
7. Phase 0F: IBM Db2 Environment Baseline
Goal

Establish a real, stable and documented Db2 environment.

## Environment decision

Select one primary environment and one fallback.

## Recommended primary

IBM Db2 Community Edition, created through the official Db2 Developer Extension or documented container workflow.

The official extension can create a Community Edition instance, create databases and establish connection profiles. It can also browse schemas and execute SQL directly inside Visual Studio Code.

## Recommended fallback

Existing Db2 instance or approved IBM Cloud Db2 environment, if already available.

Do not use SQLite or PostgreSQL as a silent replacement. Those may support isolated unit tests, but the Phase 0 integration test must connect to actual Db2.

### Subphase 0F.1: Instance creation

### Record:

Edition
Version
Container or instance name
Host
Port
Database
Username
Schema
Memory limit
CPU allocation
Storage volume
Initialization time

Do not record passwords.

### Subphase 0F.2: Database creation

### Use a project-specific database where possible:

Database: CHRONOS
Schema: CHRONOS


If database naming is constrained, use a dedicated schema.

### Subphase 0F.3: Connection proof

### Run a minimal query:

VALUES CURRENT SERVER;
VALUES CURRENT TIMESTAMP;
VALUES CURRENT USER;


### Then create a Phase 0 health table:

CREATE TABLE CHRONOS.SYSTEM_HEALTH (
    CHECK_ID VARCHAR(36) NOT NULL PRIMARY KEY,
    COMPONENT VARCHAR(64) NOT NULL,
    STATUS VARCHAR(16) NOT NULL,
    CHECKED_AT TIMESTAMP NOT NULL DEFAULT CURRENT TIMESTAMP,
    DETAILS VARCHAR(512)
);


Insert and retrieve one record.

### Subphase 0F.4: Capability inventory

### Capture whether the selected Db2 environment supports:

Required SQL functionality
Vector data type
Vector distance operations
Vector indexing
Recursive CTEs
JSON features
Role and privilege controls
Explain plans
Required Python driver

Do not assume vector support merely because the project intends to use it. Record the actual Db2 edition and version.

## Db2 foundation benchmark

### Run at least 30 iterations after warm-up:

| Measurement | Phase 0 target |
| --- | --- |
| Connection success rate | 100% |
| SELECT 1 equivalent success | 100% |
| Median connection acquisition | <1 second locally |
| p95 health-query latency | <500 ms locally |
| Insert/read consistency | 100% |
| Restart recovery | <5 minutes |
| Credential leakage | 0 |

These are engineering thresholds, not hackathon performance claims.

Deliverable
artifacts/phase-0/db2-baseline.json


### Example:

{
  "runs": 30,
  "successful_runs": 30,
  "median_query_ms": 42.7,
  "p95_query_ms": 71.3,
  "db2_version": "record-actual-value",
  "vector_capability": "verified-or-unavailable",
  "timestamp": "record-actual-value"
}

8. Phase 0G: Application Skeleton and Connectivity
Goal

Prove that the actual application stack, not just a SQL editor, can connect to Db2.

Required vertical slice
HTTP request
→ FastAPI
→ Db2 connection
→ parameterized query
→ structured response
→ test

Minimum endpoints
Liveness
GET /health/live


### Response:

{
  "status": "alive"
}


This must not depend on Db2.

Readiness
GET /health/ready


### Successful response:

{
  "status": "ready",
  "checks": {
    "db2": "pass",
    "configuration": "pass"
  }
}


Failure should return a non-success status and a sanitized reason.

Version
GET /version


### Return:

Application version
Git commit, when available
Environment
Schema migration version

Do not expose secrets, usernames or database passwords.

Connection rules
Centralize connection configuration.
Use parameterized statements.
Define connection timeouts.
Close connections safely.
Log correlation IDs.
Never log the password or full connection string.
Preserve the original error internally.
Expose only a sanitized error externally.
Minimum tests
Liveness passes without Db2.
Readiness passes with Db2.
Readiness fails correctly when Db2 is unavailable.
Missing required environment variable gives a clear startup error.
Health response contains no credentials.
Insert and read test succeeds.
Parameterized query test succeeds.
Connections are released after requests.
Benchmark

### Run readiness 50 times:

Success rate: 100%
Median latency: <250 ms locally
p95 latency: <500 ms locally
Credential exposure: 0
Unclosed connection warnings: 0

9. Phase 0H: Quality Automation and CI
Goal

Make regression detection automatic from the first commit.

Required pipelines
Pipeline 1: Submission validation
Required files
→ valid submission.json
→ no files outside allowed directory
→ template validation

Pipeline 2: Backend quality
Ruff
→ MyPy
→ pytest
→ Bandit
→ dependency audit

Pipeline 3: Frontend quality
ESLint
→ TypeScript check
→ unit tests
→ production build

## Pipeline 4: Secret detection

### Use:

Gitleaks or equivalent scanner
.env file detection
Common cloud/API key patterns
Branch protection target

### If repository permissions permit:

CI required before merge
No direct commits to protected release branch
No merge with failed validator
One final clean status before submission
Benchmark
| Metric | Target |
| --- | --- |
| CI pass rate on foundation commit | 100% |
| CI runtime | <8 minutes |
| Lint errors | 0 |
| Type errors in foundation code | 0 |
| Failed foundation tests | 0 |
| Critical dependency vulnerabilities | 0 |
| Secrets detected | 0 |

### If a dependency advisory has no immediate fix, document:

Package
Advisory
Exposure
Compensating control
Upgrade plan

Never simply suppress it.

10. Phase 0I: Security, Secrets and License Hygiene
Goal

Prevent disqualification, credential exposure and unusable third-party assets.

### Subphase 0I.1: Secrets policy

### Allowed:

.env.example
Dummy tokens
Environment-variable names
Local secret storage

### Forbidden:

.env
API keys
Db2 passwords
Personal access tokens
Cloud service credentials
Private URLs containing tokens
Credentials in screenshots

The repository guidance explicitly uses a zero-secrets policy and requires dummy placeholders in .env.example.

### Subphase 0I.2: Git-history scan

Scan the entire branch history, not only the current working tree.

### If a secret was committed:

Revoke it immediately.
Replace it.
Remove it from history.
Re-scan.
Record the incident without storing the secret.
Subphase 0I.3: Dependency inventory

### Generate:

artifacts/phase-0/backend-dependencies.txt
artifacts/phase-0/frontend-dependencies.json
artifacts/phase-0/licenses.csv


### Fields:

Package
Version
License
Usage
Source
Compatibility concern
Subphase 0I.4: Asset policy

### For future screenshots and diagrams:

Create original diagrams.
Use licensed icons.
Record third-party asset attribution.
Do not copy competitor screenshots.
Do not include private enterprise data.
Security acceptance
Zero valid secrets in repository and history.
Zero critical unresolved dependency advisories.
Every production dependency has an identified license.
No copied project code without attribution and license compatibility.
Health endpoints expose no sensitive configuration.
11. Phase 0J: Governance and Traceability
Goal

Prevent later design changes from becoming undocumented contradictions.

Required registers
docs/project-control/
├── project-charter.md
├── submission-status.md
├── requirements-register.csv
├── compliance-matrix.md
├── conflict-register.md
├── decision-log.md
├── assumption-register.md
├── risk-register.md
├── version-matrix.md
├── scope-register.md
└── phase-0-report.md

Decision log format
ADR-0001: Use LangChain as mandatory AI framework
Status: Accepted
Context:
Decision:
Alternatives:
Consequences:
Evidence:
Revisit condition:


### Initial architectural decision records:

ADR-0001 Use LangChain for typed planning and retrieval
ADR-0002 Use deterministic Python/SQL for all business calculations
ADR-0003 Use Db2 as system of record and evidence store
ADR-0004 Use FastAPI for backend APIs
ADR-0005 Lock supplier-outage as the first vertical slice
ADR-0006 Separate liveness from Db2 readiness
ADR-0007 Use synthetic data with explicit disclosure
ADR-0008 Never allow LLM-generated numerical business truth

## Risk scoring

### Use:

Risk Score=Likelihood(1−5)×Impact(1−5)\text{Risk Score} = \text{Likelihood}(1-5) \times \text{Impact}(1-5)

### Priority:

20–25: Critical
12–19: High
6–11: Medium
1–5: Low
Initial Phase 0 risks
| ID | Risk | Likelihood | Impact | Score | Treatment |
| --- | --- | --- | --- | --- | --- |
| R-001 | Submission deadline passed | 5 | 5 | 25 | Organizer confirmation |
| R-002 | Post-deadline commits rejected | 4 | 5 | 20 | Freeze or obtain permission |
| R-003 | Db2 vector feature unavailable | 3 | 5 | 15 | Verify version immediately |
| R-004 | Db2 setup unstable | 3 | 5 | 15 | Test restart and clean setup |
| R-005 | Secret committed | 2 | 5 | 10 | Gitleaks and protected config |
| R-006 | Scope expands beyond time | 4 | 4 | 16 | Lock MVP |
| R-007 | Repository validator fails | 2 | 5 | 10 | Run locally and in CI |
| R-008 | Framework-rule conflict | 3 | 4 | 12 | Include LangChain conservatively |
Acceptance criterion

### Every Critical and High risk must have:

Owner
Mitigation
Trigger
Contingency
Current status

No Critical Phase 0 risk may remain untreated.

12. Phase 0K: Foundation Benchmarking
Goal

Prove that the project foundation is stable enough for Phase 1.

This is not the product benchmark. It measures setup, compliance, connectivity and engineering health.

Benchmark suite
B0-01 Submission validation
Input: submissions/chronosdb
Runs: 3
Target: 3/3 passes

### B0-02 Clean-install reproducibility

Perform from a clean checkout.

### Measure:

Installation success
Time to ready
Manual interventions
Missing instructions
Package conflicts

### Target:

Success: 100%
Undocumented manual steps: 0
Package conflicts: 0

B0-03 Db2 connectivity reliability
Warm-up: 5 calls
Measured calls: 50
Target success rate: 100%
Target p95: <500 ms locally

B0-04 Restart recovery
Stop Db2.
Confirm readiness fails.
Restart Db2.
Confirm readiness recovers.
Run read/write verification.

### Target:

Correct failure detection: 100%
Correct recovery detection: 100%
Data loss: 0
Manual code changes: 0

### B0-05 Secret scan

### Run against:

Working tree
Git history
Config files
Documentation
Screenshot folder

### Target:

## Verified secrets: 0

### B0-06 CI repeatability

Run the full foundation pipeline three times.

### Target:

Passes: 3/3
Flaky tests: 0
Result differences: 0

### B0-07 Error-quality test

### Trigger:

Missing DB2_HOST
Invalid credentials
Db2 unavailable
Invalid port

### Target:

Clear actionable internal logs
Sanitized user response
No password exposure
Correct non-zero command exit or non-ready status
Phase 0 Foundation Score

Use a strict gate, not a vanity score.

| Category | Weight | Passing condition |
| --- | --- | --- |
| Submission certainty | 25 | Eligibility and update permission documented |
| Compliance | 15 | 100% mandatory requirement coverage |
| Repository validity | 10 | Validator passes 3/3 |
| Environment reproducibility | 15 | Clean install succeeds |
| Db2 reliability | 15 | Connectivity and restart tests pass |
| CI and quality | 10 | Pipeline passes 3/3 |
| Security and licensing | 10 | No secrets or critical vulnerabilities |
| Total | 100 |  |
Required result
90–100: Phase 0 passes
80–89: Conditional pass; no critical defect permitted
Below 80: Phase 0 fails


### However, the following are automatic failures regardless of score:

Eligibility remains unknown.
A real secret exists in Git history.
Official validator fails.
Application cannot connect to actual Db2.
Required submission files are missing.
Clean checkout cannot run.
Critical dependency vulnerability is ignored.
Organizer explicitly rejects continued participation.
13. Phase 0L: Failure Recovery and Backup
Goal

Make sure a machine, database or branch failure cannot destroy the project.

Required recovery controls
Source control
Push foundation branch to remote.
Confirm remote branch contains all committed files.
Record the foundation commit hash.
Do not depend on uncommitted local changes.
Database

## Phase 0 database contains little data, but validate:

Schema recreation script
Seed script
Health-table recreation
Database reset procedure

The system must be reconstructible from code. A database backup alone is not enough.

## Configuration

### Store:

.env.example
Configuration documentation
No real credentials
Recovery drill

### Simulate:

New project directory
Clean clone
Checkout foundation commit
Install dependencies
Configure from .env.example
Start or connect to Db2
Apply Phase 0 SQL
Run health check
Run tests
Run official validator
Target
Full foundation recovery: <30 minutes after dependencies/Db2 image are available
Data required outside repository: 0, apart from credentials
Unrecorded commands: 0

14. Phase 0M: Final Acceptance and Phase 1 Handoff
Goal

Freeze a known-good foundation and give Phase 1 exact inputs.

Required final artifacts
submissions/chronosdb/
├── README.md
├── architecture.md
├── submission.json
├── .env.example
├── Makefile
├── src/
├── sql/
├── tests/
├── scripts/
├── docs/project-control/
│   ├── product-charter.md
│   ├── submission-status.md
│   ├── requirements-register.csv
│   ├── compliance-matrix.md
│   ├── conflict-register.md
│   ├── decision-log.md
│   ├── assumption-register.md
│   ├── risk-register.md
│   ├── version-matrix.md
│   └── phase-0-report.md
└── artifacts/phase-0/
    ├── db2-baseline.json
    ├── foundation-benchmark.json
    ├── ci-summary.md
    ├── security-summary.md
    └── recovery-drill.md

## Phase 1 handoff inputs

## Phase 1 will receive:

Locked product name
Locked problem domain
Primary user
Primary scenario
Confirmed hackathon requirements
Confirmed technical stack
Measured environment baseline
Db2 capability inventory
Risk register
Assumptions requiring product validation
Available time and resource constraints
Repository commit hash
Release procedure
make doctor
make validate-submission
make lint
make typecheck
make test
make security
make db-health


### If all pass:

git add submissions/chronosdb
git commit -m "chore(chronosdb): complete phase 0 foundation"
git tag phase-0-foundation
git push origin submission/chronosdb
git push origin phase-0-foundation


Only push if doing so is allowed under the confirmed submission status. A post-deadline commit must not be made on the assumption that it is accepted.

## 15. Phase 0 Work Order

Execute Phase 0 in this exact order.

Block 1: Eligibility control
0A.1 Inventory submission state
0A.2 Capture conflicting deadline evidence
0A.3 Ask organizer for authoritative clarification
0A.4 Decide Go / Conditional Go / No-Go


Do not skip this block.

Block 2: Compliance foundation
0B.1 Build source hierarchy
0B.2 Build requirements register
0B.3 Record conflicts
0B.4 Produce compliance matrix

Block 3: Identity and scope
0C.1 Lock name and pitch
0C.2 Lock MVP
0C.3 Lock terminology
0C.4 Record rejected features

Block 4: Repository
0D.1 Fork canonical repository
0D.2 Create submission branch
0D.3 Copy official template
0D.4 Create baseline structure
0D.5 Run validator

Block 5: Environment
0E.1 Record machine and tool versions
0E.2 Create Python environment
0E.3 Create frontend environment
0E.4 Lock dependencies
0E.5 Implement Make targets

Block 6: Db2
0F.1 Install or connect to Db2
0F.2 Record exact version
0F.3 Create database/schema
0F.4 Run health SQL
0F.5 Verify vector capabilities
0F.6 Run reliability benchmark

Block 7: Application baseline
0G.1 Create FastAPI skeleton
0G.2 Implement configuration
0G.3 Implement Db2 connector
0G.4 Implement liveness
0G.5 Implement readiness
0G.6 Add integration tests

Block 8: Quality and security
0H.1 Configure linting
0H.2 Configure typing
0H.3 Configure tests
0H.4 Configure CI
0I.1 Configure secret scanner
0I.2 Scan history
0I.3 Audit dependencies
0I.4 Build license inventory

Block 9: Governance
0J.1 Complete ADRs
0J.2 Complete risk register
0J.3 Complete assumption register
0J.4 Complete scope register

Block 10: Acceptance
0K.1 Run all benchmarks
0L.1 Run clean recovery drill
0M.1 Write Phase 0 report
0M.2 Run final gate
0M.3 Create foundation tag
0M.4 Hand off to Phase 1

16. Final Phase 0 Gate Checklist
Submission safety
 Registration status documented
 Existing PR status documented
 Google Form status documented
 LinkedIn requirement documented
 Deadline conflict resolved
 Post-deadline update permission resolved
 Participation mode resolved
 Framework requirement resolved
Repository
 Canonical repository used
 submission/chronosdb branch exists
 submissions/chronosdb directory exists
 Required four files exist
 submission.json is valid
 Official validator passes three times
 No unrelated files changed
Environment
 Versions are recorded
 Dependencies are locked
 Clean installation succeeds
 Make targets work
 No undocumented global dependency exists
Db2
 Actual Db2 instance is available
 Exact version is recorded
 Application connects successfully
 Health table write/read works
 Restart recovery works
 Vector capability is explicitly verified
 Baseline performance is recorded
Application
 Liveness endpoint works
 Readiness endpoint works
 Db2 failure is detected
 Configuration failure is clear
 No credential appears in responses or logs
Quality
 Linter passes
 Type checker passes
 Foundation tests pass
 CI passes three times
 No flaky foundation test remains
Security
 .env is ignored
 .env.example contains dummy values
 Working tree has no secrets
 Git history has no secrets
 No critical vulnerability is ignored
 Dependency licenses are inventoried
Governance
 Product charter complete
 Requirements register complete
 Conflict register complete
 Decision log complete
 Risk register complete
 Assumption register complete
 Phase 0 report complete
Handoff
 Foundation benchmark score is at least 90
 No automatic-failure condition exists
 Foundation commit is recorded
 Foundation tag is created when allowed
 Phase 1 inputs are complete
Phase 0 Definition of Done

## Phase 0 passes only when this statement is true:

From a clean checkout, an evaluator can identify the official requirements, install the foundation, connect the application to a real IBM Db2 instance, run the health checks and tests, pass the repository validator, verify that no secrets are exposed, and understand exactly what ChronosDB will build in Phase 1.

The immediate first action is Phase 0A: verify whether you already submitted the PR and Google Form, and obtain written confirmation about post-deadline commits. Until that is resolved, the correct project status is Conditional Go, not full Go.