from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    store_path = root / "data" / "processed" / "memory_store.json"
    if not store_path.exists():
        raise SystemExit("memory_store.json not found. Run run_reconsolidation.py first.")

    payload = json.loads(store_path.read_text(encoding="utf-8"))
    active = []
    revised = 0
    retired = 0

    for versions in payload.values():
        for item in versions:
            status = item["status"]
            if status == "active":
                active.append(item)
            elif status == "revised":
                revised += 1
            elif status == "retired":
                retired += 1

    result = {
        "active_count": len(active),
        "revised_count": revised,
        "retired_count": retired,
        "traceable_active_count": sum(1 for item in active if item.get("provenance_set")),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

