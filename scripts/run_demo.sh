#!/bin/bash
# Phase 15J: Application Startup Automation (Run Demo Script)
# Phase 15K: Makefile Orchestration (make demo)

set -e

echo "Running ChronosDB Demo..."

# Check health
echo "Checking system health..."
python3 /home/user/chronosdb/scripts/health_check.py

# Print URLs
echo "========================================"
echo "ChronosDB Demo Ready!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:3000"
echo "Golden Scenario: SCN-GOLDEN-001"
echo "========================================"

# Phase 15J Status: ✅ COMPLETE
