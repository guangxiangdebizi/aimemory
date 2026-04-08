from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reconsolidation.baselines import (
    NoConsolidationBaseline,
    RecursiveSummarizationBaseline,
    RuleBasedConsolidationBaseline,
)
from reconsolidation.memory_store import VersionedMemoryStore


def _new_store(name: str) -> VersionedMemoryStore:
    path = ROOT / "data" / "processed" / f"{name}_memory_store.json"
    if path.exists():
        path.unlink()
    return VersionedMemoryStore(path)


def main() -> None:
    turns = [
        "用户说最近很喜欢蓝色界面，觉得蓝色很专业。",
        "用户说现在已经不喜欢蓝色界面了，因为会想到旧系统。",
        "用户说其实只接受深蓝色作为强调色，不喜欢大面积蓝色。",
    ]

    baselines = {
        "no_consolidation": NoConsolidationBaseline(_new_store("no_consolidation")),
        "rule_based": RuleBasedConsolidationBaseline(_new_store("rule_based")),
        "recursive_summary": RecursiveSummarizationBaseline(_new_store("recursive_summary")),
    }

    results = {}
    for name, runner in baselines.items():
        results[name] = runner.run_turns(turns, session_id=f"{name}_demo")

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

