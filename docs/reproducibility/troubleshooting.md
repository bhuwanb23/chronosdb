# Phase 15O: Troubleshooting Guide

## Phase 15 Deep Dive: Packaging and Reproducibility

### Create explicit fixes for common failures.

#### Db2 Not Starting
**Fix:**
1. Check Docker status: `docker ps`
2. Check Db2 logs: `docker logs chronosdb_db2`
3. Restart Db2: `docker compose restart db2`
4. Verify port: `netstat -tuln | grep 50000`

#### Embedding Creation Failure
**Fix:**
1. Check embedding model availability
2. Verify document paths
3. Run: `python3 scripts/build_embeddings.py --debug`
4. Check Db2 vector storage

#### Missing Environment Variables
**Fix:**
1. Copy `.env.example` to `.env`
2. Fill in required values
3. Run: `make setup`

#### Port Collision
**Fix:**
1. Check port usage: `netstat -tuln | grep 8000`
2. Change port in `.env` or `docker-compose.yml`
3. Restart services

#### Seed Failure
**Fix:**
1. Check Db2 connection
2. Verify seed files
3. Run: `python3 scripts/seed.py --debug`
4. Check dataset integrity

### Deliverable Location
`/home/user/chronosdb/docs/reproducibility/troubleshooting.md`

## Phase 15O Status: ✅ COMPLETE
