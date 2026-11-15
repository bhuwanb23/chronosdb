15. Phase 15K: Makefile Orchestration

This becomes the heart of reproducibility.

Required Commands
make setup

make db-up

make migrate

make seed

make embeddings

make app

make benchmark

make test

make demo

make clean

Most Important Command
make demo

Required Behavior
Start Db2

Run migrations

Load seed data

Prepare embeddings

Start backend

Start frontend

Run health checks

Print URLs

Deliverable
Makefile

