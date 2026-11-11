"""HTTP API for the ChronosDB foundation."""

from dataclasses import dataclass
from importlib.resources import files
from importlib.resources.abc import Traversable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from chronosdb import __version__
from chronosdb.config import Settings, get_settings
from chronosdb.db2 import Db2Client, Db2UnavailableError


class HealthResponse(BaseModel):
    status: str


class ReadinessResponse(BaseModel):
    status: str
    checks: dict[str, str]


class VersionResponse(BaseModel):
    version: str
    environment: str
    schema_version: str


@dataclass(frozen=True)
class AppDependencies:
    settings: Settings
    db2: Db2Client


def create_app(
    settings: Settings | None = None,
    db2: Db2Client | None = None,
) -> FastAPI:
    """Build the API with injectable dependencies for tests."""

    resolved_settings = settings or get_settings()
    dependencies = AppDependencies(
        settings=resolved_settings,
        db2=db2 or Db2Client(resolved_settings),
    )
    app = FastAPI(title="ChronosDB", version=__version__)
    app.state.dependencies = dependencies

    @app.exception_handler(Db2UnavailableError)
    async def db2_error_handler(
        request: Request,
        exc: Db2UnavailableError,
    ) -> JSONResponse:
        del request
        del exc
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "checks": {"db2": "fail"}},
        )

    @app.get("/health/live", response_model=HealthResponse)
    async def liveness() -> HealthResponse:
        return HealthResponse(status="alive")

    @app.get("/health/ready", response_model=ReadinessResponse)
    def readiness() -> ReadinessResponse:
        if not dependencies.settings.db2_configured:
            return ReadinessResponse(
                status="not_ready",
                checks={"configuration": "fail", "db2": "not_checked"},
            )
        dependencies.db2.readiness()
        return ReadinessResponse(
            status="ready",
            checks={"configuration": "pass", "db2": "pass"},
        )

    @app.get("/version", response_model=VersionResponse)
    async def version() -> VersionResponse:
        return VersionResponse(
            version=dependencies.settings.app_version,
            environment=dependencies.settings.app_env,
            schema_version=dependencies.settings.schema_version,
        )

    return app


def health_sql_path() -> Traversable:
    """Return the packaged foundation health-table migration."""

    return files("chronosdb.sql").joinpath("001_system_health.sql")
