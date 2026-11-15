"""Phase 7N: structured optimization event logging."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping


@dataclass
class OptimizationObservability:
    """Record events in memory and optionally as JSONL."""

    path: Path | None = None
    events: list[dict[str, Any]] = field(default_factory=list)

    def emit(self, event: str, **payload: Any) -> dict[str, Any]:
        entry = {"event": event, **payload}
        self.events.append(entry)
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, sort_keys=True, default=str) + "\n")
        return entry

    def clear(self) -> None:
        self.events.clear()

    def summary(self) -> dict[str, Any]:
        return {
            "event_count": len(self.events),
            "events": list(self.events),
        }
