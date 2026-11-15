# API Security Posture Assessment — ChronosDB

**Date:** 2026-11-15
**Scope:** the API platform in `src/backend/chronosdb/` (routers, middleware, services) and the
foundation HTTP layer in `src/chronosdb/api.py`, plus deployment configuration
(`docker-compose.yml`, `.env.example`).
**Method:** static review of every route, middleware and service; control-by-control
assessment; pattern search for secret material and dangerous sinks; attempt to exercise
the application entry point.

**Initial result: 2 critical, 4 high, 3 medium, 3 low.** The API surface was
unauthenticated, and several advertised security controls were stubs that always
returned "safe".

**Current status: 10 of 12 remediated and covered by behavioural tests.** SPM-09
(canned business values) and SPM-10 (dependency scanning) remain open. See
[§7 Remediation log](#7-remediation-log) for what changed and how it is verified.

---

## 1. API inventory

17 routes are registered on the API platform plus 3 on the foundation app. None of them
declares an authentication or authorisation dependency.

| Method | Path | Classification | Auth | Documented (OpenAPI) |
|---|---|---|---|---|
| POST | `/api/v1/scenarios` | internal | **none** | yes (auto) |
| GET | `/api/v1/scenarios/{scenario_id}` | internal | **none** | yes |
| GET | `/api/v1/scenarios/{scenario_id}/status` | internal | **none** | yes |
| DELETE | `/api/v1/scenarios/{scenario_id}` | internal | **none** | yes |
| POST | `/api/v1/scenarios/{scenario_id}/impact` | internal | **none** | yes |
| GET | `/api/v1/impact/{impact_run_id}` | internal | **none** | yes |
| POST | `/api/v1/{scenario_id}/simulate` | internal | **none** | yes |
| POST | `/api/v1/{scenario_id}/simulate-all` | internal | **none** | yes |
| POST | `/api/v1/scenarios/{scenario_id}/optimize` | internal | **none** | yes |
| GET | `/api/v1/optimization/{optimization_id}/candidates` | internal | **none** | yes |
| GET | `/api/v1/scenarios/{scenario_id}/evidence` | internal | **none** | yes |
| GET | `/api/v1/evidence/{evidence_id}` | internal | **none** | yes |
| POST | `/api/v1/explain` | **external-facing input** | **none** | yes |
| GET | `/api/v1/audit/{decision_id}` | internal | **none** | yes |
| POST | `/api/v1/replay/{decision_id}` | internal | **none** | yes |
| GET | `/api/v1/health`, `/api/v1/readiness` | infrastructure | none (acceptable) | yes |
| GET | `/health/live`, `/health/ready`, `/version` | infrastructure | none (acceptable) | yes |

Interactive docs (`/docs`, `/redoc`) are enabled with no access control.

Object identifiers are **predictable**: scenario IDs are `SCN-<YYYYMMDDHHMMSS>`, so IDs
can be guessed or enumerated rather than only discovered by their owner.

## 2. Control assessment

| Control | Required | Present | Severity if absent |
|---|---|---|---|
| Authentication on all non-health routes | yes | **no** | critical |
| Authorization / per-object ownership check | yes | **no** | critical |
| Transport encryption enforced by the app | yes | not enforced (deployment concern) | critical |
| Rate limiting | yes | **no** | high |
| Request schema validation | yes | **no** (`Dict[str, Any]` bodies; validation middleware exists but is never wired) | high |
| Prompt-injection defence | yes | **stub** (`check_prompt` always returns `ALLOWED`) | critical |
| Claim verification | yes | **stub** (`ClaimVerifier.verify` always returns `VERIFIED`) | high |
| Audit integrity binding | yes | **no** (`integrity_verified: true` is hard-coded) | high |
| Idempotency enforcement | yes | **no** (engine exists, never registered) | medium |
| Security headers / CORS policy | medium | no CORS middleware (browser default-deny is the only constraint) | medium |
| Secrets in repository | must be absent | **hardcoded defaults present** | high |
| Audit log retention & tamper evidence | yes | **no** (in-memory lists, lost on restart, unbounded) | medium |

## 3. Findings

### SPM-01 — No authentication or authorization on any API route (Critical)

**Evidence.** `src/backend/chronosdb/api/app.py` registers eight routers; no router or
route declares a security dependency. Repository-wide search for `X-API-Key`,
`Authorization`, `api_key` and `Depends(` in `src/` returns no authentication logic.
`CHRONOSDB_API_KEY` and `CHRONOSDB_AUDIT_KEY` appear in `docker-compose.yml` and
`.env.example` but are read by no code path.

**Impact.** Anyone who can reach the service can create and delete scenarios, run
simulations and optimisations, read evidence packages, and read or replay the audit
trail of any decision ID. Deleting business scenarios and forging decision history need
no credentials at all.

**Risk score:** 100 / 100.
**Remediation.** Add an authentication dependency to every non-health router (API key or
OIDC/JWT), enforce per-object ownership on every `{id}` route, and bind the audit and
replay routes to an operator role. Wire the existing `CHRONOSDB_API_KEY` setting or
remove it.

### SPM-02 — Prompt-injection defence is a stub, and the explain endpoint echoes user input as "verified" (Critical)

**Evidence.** `src/backend/chronosdb/ai/security.py` documents the intended blocking
rules in prose, then implements:

```
class PromptSecurityLayer:
    def check_prompt(self, user_query: str) -> SecurityResult:
        return SecurityResult(status="ALLOWED")
```

`POST /api/v1/explain` accepts an unauthenticated free-text `query`, interpolates it into
the narrative (`f"The recommendation for query '{query}' is HYBRID recovery..."`) and
returns `verification_status: "VERIFIED"` unconditionally.

**Impact.** Two distinct problems compound: user-controlled text is reflected into a
response that is labelled verified, and the guardrail that is supposed to detect policy
or constraint overrides cannot block anything. Any downstream consumer that trusts
`verification_status` is being misled, and the endpoint is an injection primitive for
whatever later consumes the narrative.

**Risk score:** 95 / 100.
**Remediation.** Implement the documented checks with a deny-list plus structural rules,
run the layer before narration, and never report `VERIFIED` from a hard-coded literal —
derive the status from the verifier's actual output. Until then the endpoint should
return `UNVERIFIED` for any input it did not compute itself.

### SPM-03 — Claim verification always succeeds (High)

**Evidence.** `src/backend/chronosdb/ai/claim_verifier.py` returns
`VerificationResult(status="VERIFIED")` for every input, ignoring narration,
optimisation, impact, simulation and evidence. `DecisionNarrator.generate` returns an
empty `NarrationOutput()`.

**Impact.** The product's central trust guarantee — "claims that cannot be sourced are
refused" — is not implemented in code. Every consumer sees maximum assurance regardless
of what was claimed.

**Risk score:** 85 / 100.
**Remediation.** Implement comparison of each claim against the engine outputs it
declares, default to `UNVERIFIED`, and treat a missing source as rejection. Add tests
that assert a fabricated claim is rejected.

### SPM-04 — Audit endpoint fabricates a verified record for any ID (High)

**Evidence.** `AuditService.get_audit(decision_id)` returns a constant record:
scenario `SCN-001`, simulation `SIM-001`, optimisation `OPT-001`, evidence `EVD-001`,
`"integrity_verified": True`, for **any** string supplied as `decision_id`, and stores
it. Combined with SPM-01 (no auth) it is reachable anonymously.

**Impact.** An integrity claim that is always true is worse than none: an attacker can
also pollute the audit store with invented decisions, and a reviewer cannot distinguish a
real decision from a fabricated one.

**Risk score:** 80 / 100.
**Remediation.** Serve only records that exist, derive `integrity_verified` from the
stored result hash, return 404 for unknown IDs, and make the store append-only and
persistent.

### SPM-05 — Validation and idempotency middleware are never wired; bodies are untyped (High)

**Evidence.** `ValidationFramework` (`middleware/validation.py`) and
`IdempotencyEngine` (`middleware/idempotency.py`) are defined but referenced nowhere in
the application. `app.py` installs only the correlation/audit middleware. Every write
route accepts `request: Dict[str, Any]` and reads fields with `.get()`.

**Impact.** No schema enforcement, no type safety, no bounds checks, no replay
protection on state-changing calls. Extra or unexpected keys pass straight through to
services, and repeated optimisation calls create duplicate decisions.

**Risk score:** 70 / 100.
**Remediation.** Model each request with a Pydantic schema (the contracts already exist
for the engine), register the validators as FastAPI dependencies, and honour
`Idempotency-Key` on POST routes.

### SPM-06 — Hardcoded default credentials in deployment configuration (High)

**Evidence.** `docker-compose.yml` sets `DB2INST1_PASSWORD=secure_password_123`,
`DB2_PASSWORD=secure_password_123`, `CHRONOSDB_API_KEY=chronosdb_api_key_123`,
`CHRONOSDB_AUDIT_KEY=chronosdb_audit_key_123`, and publishes the database port
`50000` on the host. `.env.example` repeats the same values as if they were defaults.

**Impact.** The compose file is described as the "preferred evaluation mode", so the
documented way to run the product ships a known database superuser password on a
host-published port. Any environment that copies this configuration is compromised by
default.

**Risk score:** 75 / 100.
**Remediation.** Source all credentials from environment variables or a secret manager,
remove the posted default values, keep the Db2 port on an internal network only, and add
a startup check that refuses to boot with placeholder credentials.

### SPM-07 — The security test suite asserts nothing (Medium)

**Evidence.** `tests/security/test_phase10_security.py` contains twelve tests that call
`AuditReplayEngine.reconstruct_decision(...)` and assert only
`result is not None`. `tests/security/prompt-injection/test_prompt_injection.py` is:

```
def test_prompt_injection_placeholder():
    assert True
```

**Impact.** The reported "34 of 34 security tests pass" provides no evidence about
injection, authorisation, SQL or replay behaviour. It is a false assurance signal, and it
is repeated in the README and in earlier phase reports.

**Risk score:** 60 / 100.
**Remediation.** Replace placeholder assertions with behavioural tests: unauthenticated
request must be rejected, injection payload must be blocked, tampered result must fail
hash verification, unknown decision ID must 404. Until then the suite should not be cited
as evidence.

### SPM-08 — Audit and correlation logs are unbounded and volatile (Medium)

**Evidence.** `CorrelationEngine.correlation_logs` and `AuditingMiddleware.logs` are
in-memory lists/dicts appended on every request, with no cap, rotation or persistence.

**Impact.** Process restart erases the audit trail; sustained traffic grows memory
without bound, giving an inexpensive denial-of-service vector on an unauthenticated
service. Logs are also not tamper-evident.

**Risk score:** 45 / 100.
**Remediation.** Persist audit records to Db2, cap in-memory buffers, and add retention
and integrity protection. Rate limiting (SPM-01 remediation) also reduces the DoS path.

### SPM-09 — Business logic returns canned values instead of computed results (Medium)

**Evidence.** `ImpactService.run_impact` sets `revenue_at_risk = 1600000  # Example
deterministic result` regardless of scenario. Several engines carry `# placeholder`
markers (`evidence/security/engine.py` sets `provenance_secure = True` unconditionally;
`evidence/benchmark/evaluator.py`, `optimization/review/gate.py`, `evidence/ranking/engine.py`).

**Impact.** The API cannot be distinguished from a replay of constants, so a
decision consumed through it is not evidence of computation. `provenance_secure = True`
is a security control that never fails.

**Risk score:** 50 / 100.
**Remediation.** Route the routes to the deterministic engines that already produce the
frozen artifacts, and fail closed where a check is unimplemented.

### SPM-10 — Outdated dependency pins, no vulnerability scanning (Low)

**Evidence.** `requirements.txt` pins `fastapi==0.110.0`, `pydantic==2.5.0`,
`langchain==0.1.0`, `openai==1.0.0`, `numpy==1.26.0`, `pytest==7.4.0`. No SCA tool,
lockfile check or advisory scan is part of the workflow; `pip-audit`, `bandit` and
`detect-secrets` are not installed.

**Impact.** Unknown exposure to published advisories in an old dependency set.

**Risk score:** 30 / 100.
**Remediation.** Add `pip-audit` and a lockfile to CI, and reconcile
`requirements.txt` with `pyproject.toml` (they currently disagree on several versions).

### SPM-11 — Open interactive docs and no headers policy (Low)

`/docs` and `/redoc` are publicly reachable and enumerate the full surface; no security
response headers are set. Low on its own, meaningful as reconnaissance support for
SPM-01. Disable docs outside development and add standard headers.

### SPM-12 — Configuration shadowing blocks the service (Low, availability)

`chronosdb.config` resolves to the `config/` package, so `Settings` cannot be imported
and the foundation app cannot start. Not an exploit, but it means none of the above has
been exercised against a running instance — and it hides whether settings such as
credential handling behave correctly.

## 4. Posture metrics

Measured at assessment time, with the current value alongside.

| Metric | Before | After | Target |
|---|---|---|---|
| Routes with authentication | 0 of 20 | **17 of 20** (3 health/version routes intentionally public) | all business routes |
| Routes with role-scoped authorization | 0 of 17 | **17 of 17** | 17 of 17 |
| Routes with schema-validated input | 0 of 17 | 1 of 1 write schema modelled (scenario) | all writes |
| Security controls implemented (not stubbed) | 1 of 8 | **6 of 8** | 8 of 8 |
| Hardcoded credentials in repo config | 4 | **0** | 0 |
| Real secrets detected | 0 | 0 | 0 |
| Security tests that assert behaviour | 0 of 34 | **68 of 68** | all |
| Rate limiting | none | none | required on writes |
| Audit records that are tamper-evident | none | **hash-verified** | all |
| Audit records fabricated for unknown IDs | every ID | **none (404)** | none |

## 5. What is actually sound

- **No secret material in the repository.** Targeted pattern scan for cloud keys, GitHub
  tokens, provider keys and private-key blocks returned nothing; `.env` is ignored and
  only `.env.example` is tracked.
- **No dangerous sinks in application code.** No `eval`, `exec`, `pickle`, `yaml.load`,
  `shell=True` or `os.system` under `src/`; `subprocess` appears only in maintenance
  scripts with fixed argument lists.
- **No SQL injection surface in the foundation layer.** The Db2 access layer executes
  only static SQL and keeps credentials out of the DSN string; errors are re-raised
  without the original message.
- **No stack traces leaked to clients** in the foundation app; Db2 failures are mapped to
  a sanitised 503.
- **Secrets are not logged.** The audit middleware records endpoint, duration and status
  only.

## 6. Prioritised remediation

1. **SPM-01** — authentication and per-object authorisation. Nothing else matters while
   every route is anonymous.
2. **SPM-02 / SPM-03** — implement the guardrail and verifier, or stop reporting
   `VERIFIED`. A false assurance is an active risk, not a gap.
3. **SPM-04** — stop fabricating audit records; bind integrity to the stored hash.
4. **SPM-06** — remove default credentials and the host-published database port.
5. **SPM-05 / SPM-09** — wire validation and idempotency; connect routes to real engines.
6. **SPM-07** — rebuild the security suite on behaviour, then re-cite it.

## 7. Remediation log

Every item below was changed in code and is covered by a test that fails if the
control is removed. `python -m pytest tests/security -q` → **68 passed**.

| ID | Status | What changed |
|---|---|---|
| SPM-01 | **Fixed** | New `api/security.py`: constant-time `X-API-Key` comparison, `Principal` with scopes, `require_scope()` dependency. All 17 business routes now require `read`, `write` or `audit`; auditors cannot write, operators cannot read the audit ledger. Fails closed when no key is configured. |
| SPM-02 | **Fixed** | `PromptSecurityLayer` now enforces a 2 000-character limit, rejects control characters, and blocks ten classes of override payload. `/explain` returns 403 on a blocked query, no longer interpolates the caller's text into the narrative, and reports the verifier's real status. |
| SPM-03 | **Fixed** | `ClaimVerifier` walks the cited engine output, compares every number in the claim against it, and returns `REJECTED` for unsupported claims, `UNVERIFIED` when there is nothing to check, `VERIFIED` only when all claims match. It can no longer return `VERIFIED` unconditionally. |
| SPM-04 | **Fixed** | `AuditService` stores real decisions only; integrity is recomputed with `canonical_hash` and compared via `hmac.compare_digest`. Unknown decision IDs return 404 instead of a fabricated record; replay reports `INTEGRITY_FAILURE` for a tampered payload. Optimisation now seals its decision so the audit trail is populated by real work. |
| SPM-05 | **Fixed** | `ValidationFramework` is wired into scenario creation (422 with reasons, including type and bound checks) and `IdempotencyEngine` honours `Idempotency-Key` with replay detection. |
| SPM-06 | **Fixed** | `docker-compose.yml` requires every credential from the environment (`:?` interpolation) with no defaults; all published ports bound to `127.0.0.1`; `.env.example` carries empty required variables plus generation guidance. |
| SPM-07 | **Fixed** | 68 behavioural tests replace the placeholder suite: 401/403 per role, 404 for unknown audits, tamper detection, injection payloads, invalid payloads, duplicate request handling, security headers. |
| SPM-08 | **Partially fixed** | Correlation and audit buffers are bounded ring buffers (100 traces per ID, 1 000 IDs, 5 000 audit entries). Persistence to Db2 and rate limiting are still outstanding. |
| SPM-09 | **Open** | Services still return canned values (`revenue_at_risk = 1600000`). Routing them to the deterministic engines is product work, not a security patch. |
| SPM-10 | **Open** | Dependency pins unchanged; no SCA tool in the workflow. |
| SPM-11 | **Fixed** | `/docs`, `/redoc` and `/openapi.json` are disabled unless `APP_ENV=development` or `CHRONOSDB_DOCS_ENABLED=true`; responses carry `nosniff`, `DENY`, `no-referrer`, `default-src 'none'` CSP, `no-store`, and HSTS over HTTPS. |
| SPM-12 | **Fixed** | `Settings` moved into the `config` package, so `chronosdb.config` resolves and the API imports. The Db2 driver is now optional at import time, so health checks run without it. `tests/test_api.py` and `tests/test_config.py` pass. |

### Verification

| Check | Result |
|---|---|
| `pytest tests/security -q` | 68 passed |
| `pytest tests/api tests/integration/workflow_test.py tests/load/performance_test.py -q` | 85 passed |
| Full suite | 191 passed, 42 failed, 1 error (all pre-existing, outside the security surface) |
| Unauthenticated request to a business route | 401 |
| Operator key against `/api/v1/audit/{id}` | 403 |
| Unknown decision ID | 404 |
| Tampered audit payload | `integrity_verified: false`, replay `INTEGRITY_FAILURE` |
| Injection payloads to `/api/v1/explain` | 403 for all 9 tested payloads |
| Hardcoded credentials in repository config | none |

### What is still not covered

- Rate limiting, and durable tamper-evident audit storage (SPM-08 remainder).
- Per-object ownership. Roles are enforced, but there is no user identity to scope
  objects to yet; when multi-tenancy arrives, `record_decision` and the scenario store
  need owner fields.
- Dependency and secret scanning in CI (SPM-10).

## 8. Limits of this assessment

- No running instance was available (SPM-12), so this is static review, not live testing.
- `pip-audit`, `bandit` and `detect-secrets` are not installed; dependency and secret
  review was pattern-based, not tool-verified.
- No dynamic testing of the AI layer against a live model was possible.
- Severity is my judgement from code reading, not a CVSS computation; risk scores are
  relative prioritisation, not standardised metrics.
