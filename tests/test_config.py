from chronosdb.config import Settings


def test_db2_configuration_requires_all_connection_values() -> None:
    settings = Settings(
        DB2_DATABASE="CHRONOS",
        DB2_USERNAME="db2inst1",
        DB2_PASSWORD="secret",
        DB2_SCHEMA="CHRONOS",
    )

    assert settings.db2_configured is True
    assert "PWD" not in settings.connection_dsn()
    assert "DATABASE=CHRONOS" in settings.connection_dsn()


def test_incomplete_db2_configuration_is_detected() -> None:
    settings = Settings(DB2_DATABASE="CHRONOS")

    assert settings.db2_configured is False
