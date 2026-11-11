"""Small, explicit IBM Db2 access layer for the foundation slice."""

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import ibm_db

from chronosdb.config import Settings


class Db2UnavailableError(RuntimeError):
    """Raised when Db2 cannot be reached or queried."""


class Db2Client:
    """Owns short-lived Db2 connections and foundation queries."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @contextmanager
    def connection(self) -> Iterator[Any]:
        """Yield a connection and always close it after use."""

        if not self.settings.db2_configured:
            raise Db2UnavailableError("Db2 configuration is incomplete")

        connection = None
        try:
            connection = ibm_db.connect(
                self.settings.connection_dsn(),
                self.settings.db2_username,
                self.settings.db2_password,
            )
            yield connection
        except Exception as exc:
            raise Db2UnavailableError("Db2 connection or query failed") from exc
        finally:
            if connection is not None:
                ibm_db.close(connection)

    def readiness(self) -> dict[str, str]:
        """Run a read-only readiness query and return sanitized details."""

        with self.connection() as connection:
            statement = ibm_db.exec_immediate(
                connection,
                "VALUES CURRENT SERVER, CURRENT TIMESTAMP, CURRENT USER",
            )
            row = ibm_db.fetch_tuple(statement)
            if row is None:
                raise Db2UnavailableError("Db2 returned no readiness row")
            return {
                "server": str(row[0]),
                "checked_at": str(row[1]),
                "user": str(row[2]),
            }

    def ensure_health_table(self, sql_path: Path) -> None:
        """Create the health table when it does not already exist."""

        with self.connection() as connection:
            statement = ibm_db.prepare(
                connection,
                """
                SELECT 1
                FROM SYSCAT.TABLES
                WHERE TABSCHEMA = ? AND TABNAME = 'SYSTEM_HEALTH'
                """,
            )
            ibm_db.bind_param(statement, 1, self.settings.db2_schema.upper())
            ibm_db.execute(statement)
            if ibm_db.fetch_tuple(statement) is None:
                ibm_db.exec_immediate(connection, sql_path.read_text(encoding="utf-8"))

    def record_health_check(self, component: str, status: str, details: str) -> None:
        """Persist one health result using a parameterized statement."""

        with self.connection() as connection:
            statement = ibm_db.prepare(
                connection,
                """
                INSERT INTO SYSTEM_HEALTH (CHECK_ID, COMPONENT, STATUS, DETAILS)
                VALUES (GENERATE_UNIQUE(), ?, ?, ?)
                """,
            )
            for index, value in enumerate((component, status, details), start=1):
                ibm_db.bind_param(statement, index, value)
            ibm_db.execute(statement)

    def latest_health_check(self) -> dict[str, str] | None:
        """Read the latest persisted health result."""

        with self.connection() as connection:
            statement = ibm_db.exec_immediate(
                connection,
                """
                SELECT CHECK_ID, COMPONENT, STATUS, CHECKED_AT, DETAILS
                FROM SYSTEM_HEALTH
                ORDER BY CHECKED_AT DESC
                FETCH FIRST 1 ROW ONLY
                """,
            )
            row = ibm_db.fetch_assoc(statement)
            if row is None:
                return None
            return {str(key).lower(): str(value) for key, value in row.items()}
