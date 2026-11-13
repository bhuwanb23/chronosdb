from __future__ import annotations

from pathlib import Path

from .loader import load_rule_set
from .versions import RuleSet


class RuleRegistry:
    def __init__(self, root: Path) -> None:
        self._root = root
        self._cache: dict[str, RuleSet] = {}

    def load(self, version: str) -> RuleSet:
        if version not in self._cache:
            path = self._root / "config" / "rules" / f"{version}.yaml"
            self._cache[version] = load_rule_set(path)
        return self._cache[version]
