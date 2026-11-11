"""Bootstrap and verify the ChronosDB foundation health table."""

import argparse
import sys

from chronosdb.api import health_sql_path
from chronosdb.config import get_settings
from chronosdb.db2 import Db2Client, Db2UnavailableError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="Create the system health table when it is missing.",
    )
    args = parser.parse_args()

    client = Db2Client(get_settings())
    try:
        if args.bootstrap:
            client.ensure_health_table(health_sql_path())
        readiness = client.readiness()
        client.record_health_check("db2", "pass", "Foundation readiness check passed")
        latest = client.latest_health_check()
    except Db2UnavailableError as exc:
        print(f"Db2 health check failed: {exc}", file=sys.stderr)
        return 1

    print(f"Db2 server: {readiness['server']}")
    print(f"Checked at: {readiness['checked_at']}")
    if latest:
        print(f"Latest health record: {latest['status']} ({latest['component']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
