from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reconsolidation.env_utils import load_env
from reconsolidation.judges import create_relation_judge
from reconsolidation.memory_store import VersionedMemoryStore
from reconsolidation.pipeline import ReconsolidationPipeline

load_env()


def main() -> None:
    judge_mode = os.getenv("JUDGE_MODE", "heuristic")
    store_path = ROOT / "data" / "processed" / "memory_store.json"
    if store_path.exists():
        store_path.unlink()
    store = VersionedMemoryStore(store_path)
    pipeline = ReconsolidationPipeline(store=store, judge=create_relation_judge(judge_mode))

    turns = [
        "用户说最近很喜欢蓝色界面，觉得蓝色很专业。",
        "用户说现在已经不喜欢蓝色界面了，因为会想到旧系统。",
        "用户说其实只接受深蓝色作为强调色，不喜欢大面积蓝色。",
    ]
    result = pipeline.run_turns(turns, session_id="demo")
    print(json.dumps({"judge_mode": judge_mode, **result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
