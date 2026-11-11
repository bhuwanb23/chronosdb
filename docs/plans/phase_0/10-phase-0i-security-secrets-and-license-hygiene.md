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
