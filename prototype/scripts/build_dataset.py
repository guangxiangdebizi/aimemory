from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "eval" / "mini_reconsolidation_cases.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)

    records = [
        {
            "case_id": "delayed_contradiction_001",
            "task": "delayed_contradiction",
            "sessions": [
                ["用户说最近很喜欢蓝色界面。", "用户说蓝色显得专业。"],
                ["用户说现在已经不喜欢蓝色界面了。", "用户说蓝色会让他想到旧系统。"],
            ],
            "expected_active_memory": "用户现在不喜欢蓝色界面",
        },
        {
            "case_id": "refinement_001",
            "task": "refinement",
            "sessions": [
                ["用户说喜欢咖啡。", "用户经常点拿铁。"],
                ["用户说只喜欢热咖啡。", "用户不喜欢冰咖啡。"],
            ],
            "expected_active_memory": "用户对咖啡偏好具有条件限制",
        },
    ]

    with out.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Wrote {len(records)} records to {out}")


if __name__ == "__main__":
    main()

