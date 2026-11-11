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

