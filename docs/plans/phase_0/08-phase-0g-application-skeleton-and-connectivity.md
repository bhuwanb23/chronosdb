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

