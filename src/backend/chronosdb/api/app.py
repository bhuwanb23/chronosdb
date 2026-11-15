"""
Phase 11: Main Application
Backend and API Integration
"""

from fastapi import FastAPI, Request, Response
from datetime import datetime
from src.backend.chronosdb.routers.scenarios import router as scenarios_router
from src.backend.chronosdb.routers.impact import router as impact_router
from src.backend.chronosdb.routers.simulations import router as simulations_router
from src.backend.chronosdb.routers.optimization import router as optimization_router
from src.backend.chronosdb.routers.evidence import router as evidence_router
from src.backend.chronosdb.routers.ai import router as ai_router
from src.backend.chronosdb.routers.audit import router as audit_router
from src.backend.chronosdb.routers.health import router as health_router
from src.backend.chronosdb.middleware.correlation import CorrelationEngine
from src.backend.chronosdb.middleware.auditing import AuditingMiddleware

app = FastAPI(
    title="ChronosDB API Platform",
    description="Phase 11 Deep Dive: Backend and API Integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize middleware engines
correlation_engine = CorrelationEngine()
auditing_middleware = AuditingMiddleware()

# Include routers
app.include_router(scenarios_router)
app.include_router(impact_router)
app.include_router(simulations_router)
app.include_router(optimization_router)
app.include_router(evidence_router)
app.include_router(ai_router)
app.include_router(audit_router)
app.include_router(health_router)

@app.middleware("http")
async def correlation_and_auditing_middleware(request: Request, call_next):
    """
    Phase 11N & 11S: Correlation and Auditing Middleware
    """
    start_time = datetime.utcnow()
    
    # Generate Correlation ID
    correlation_id = correlation_engine.generate_correlation_id()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    # Log correlation
    correlation_engine.log_correlation(
        correlation_id=correlation_id,
        endpoint=str(request.url.path),
        duration_ms=duration_ms,
        data={"method": request.method, "status_code": response.status_code}
    )
    
    # Log audit
    auditing_middleware.log_request(
        correlation_id=correlation_id,
        endpoint=str(request.url.path),
        duration_ms=duration_ms,
        status="SUCCESS" if response.status_code < 400 else "ERROR"
    )
    
    # Add correlation ID to response headers
    response.headers["X-Correlation-ID"] = correlation_id
    
    return response

# Phase 11 Status: ✅ COMPLETE
