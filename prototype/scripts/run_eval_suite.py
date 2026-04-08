from __future__ import annotations

import json
import os
import sys
import hashlib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reconsolidation.baselines import (
    NoConsolidationBaseline,
    RecursiveSummarizationBaseline,
    RuleBasedConsolidationBaseline,
)
from reconsolidation.env_utils import load_env
from reconsolidation.judges import create_relation_judge
from reconsolidation.memory_store import VersionedMemoryStore
from reconsolidation.pipeline import ReconsolidationPipeline

load_env()
CACHE_PATH = ROOT / "data" / "processed" / "semantic_match_cache.json"


def _load_cache() -> Dict[str, bool]:
    if not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _save_cache(cache: Dict[str, bool]) -> None:
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _flatten_sessions(sessions: List[List[str]]) -> List[str]:
    turns: List[str] = []
    for session in sessions:
        turns.extend(session)
    return turns


def _new_store(name: str, case_id: str) -> VersionedMemoryStore:
    path = ROOT / "data" / "processed" / f"{name}_{case_id}_memory_store.json"
    if path.exists():
        path.unlink()
    return VersionedMemoryStore(path)


def _active_texts(result: dict) -> List[str]:
    return [item["text"] for item in result.get("active_memories", [])]


def _count_operation(result: dict, op: str) -> int:
    return sum(1 for item in result.get("events", []) if item.get("operation") == op)


def _contains_expected_memory(active_texts: List[str], expected: str) -> bool:
    if not active_texts:
        return False
    expected_terms = [term for term in expected.replace("，", " ").split() if term]
    if not expected_terms:
        return False
    joined = " ".join(active_texts)
    return any(term in joined for term in expected_terms[:2]) if len(expected_terms) >= 2 else expected_terms[0] in joined


def _llm_semantic_match(expected: str, active_texts: List[str], cache: Dict[str, bool]) -> bool:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_JUDGE_MODEL") or os.getenv("OPENAI_MODEL")
    base_url = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    if not api_key or not model or not active_texts:
        return _contains_expected_memory(active_texts, expected)

    cache_key = hashlib.sha256(
        json.dumps({"expected": expected, "active": active_texts}, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    if cache_key in cache:
        return cache[cache_key]

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You evaluate whether the active long-term memory satisfies the expected consolidated memory.\n"
                    "Return strict JSON with fields: match (true/false), explanation."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "expected_memory": expected,
                        "active_memories": active_texts,
                    },
                    ensure_ascii=False,
                ),
            },
        ],
        "temperature": 0,
    }
    request = urllib.request.Request(
        url=f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = json.loads(response.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            match = bool(parsed.get("match", False))
            cache[cache_key] = match
            return match
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        match = _contains_expected_memory(active_texts, expected)
        cache[cache_key] = match
        return match


def _render_markdown(summary: Dict[str, Dict[str, float]]) -> str:
    lines = [
        "| Runner | Cases | Behavior Hit | Memory Hit | Provenance Hit |",
        "|--------|-------|--------------|------------|----------------|",
    ]
    for runner, row in summary.items():
        lines.append(
            f"| {runner} | {int(row['cases'])} | {int(row['behavior_hit'])} | {int(row['memory_hit'])} | {int(row['provenance_hit'])} |"
        )
    return "\n".join(lines)


def _evaluate_case(case: dict, runner_name: str, result: dict, cache: Dict[str, bool]) -> dict:
    active_texts = _active_texts(result)
    expected_behavior = case.get("expected_behavior")
    behavior_hit = False

    if expected_behavior == "revise":
        behavior_hit = _count_operation(result, "REVISE") >= 1
    elif expected_behavior == "revise_or_split":
        behavior_hit = _count_operation(result, "REVISE") >= 1 or _count_operation(result, "SPLIT") >= 1
    elif expected_behavior == "revise_and_single_active":
        behavior_hit = _count_operation(result, "REVISE") >= 1 and len(active_texts) == 1
    elif expected_behavior == "traceable":
        behavior_hit = any(item.get("provenance_set") for item in result.get("active_memories", []))

    memory_hit = _llm_semantic_match(case.get("expected_active_memory", ""), active_texts, cache)

    provenance_expected = case.get("expected_provenance_count")
    provenance_hit = True
    if provenance_expected is not None:
        provenance_hit = any(len(item.get("provenance_set", [])) >= provenance_expected for item in result.get("active_memories", []))

    return {
        "case_id": case["case_id"],
        "task": case["task"],
        "runner": runner_name,
        "behavior_hit": behavior_hit,
        "memory_hit": memory_hit,
        "provenance_hit": provenance_hit,
        "active_count": len(active_texts),
        "revise_count": _count_operation(result, "REVISE"),
        "split_count": _count_operation(result, "SPLIT"),
    }


def main() -> None:
    judge_mode = os.getenv("JUDGE_MODE", "heuristic")
    dataset_path = ROOT / "data" / "eval" / "mini_reconsolidation_cases.jsonl"
    if not dataset_path.exists():
        raise SystemExit("Dataset not found. Run build_dataset.py first.")

    cases = [json.loads(line) for line in dataset_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    summary: Dict[str, Dict[str, float]] = {}
    detailed: List[dict] = []
    cache = _load_cache()

    for case in cases:
        turns = _flatten_sessions(case["sessions"])

        runners: Dict[str, Callable[[], dict]] = {
            "ours": lambda case_id=case["case_id"], turns=turns: ReconsolidationPipeline(
                store=_new_store("ours", case_id),
                judge=create_relation_judge(judge_mode),
            ).run_turns(turns, session_id=case_id),
            "no_consolidation": lambda case_id=case["case_id"], turns=turns: NoConsolidationBaseline(
                _new_store("no_consolidation", case_id)
            ).run_turns(turns, session_id=case_id),
            "rule_based": lambda case_id=case["case_id"], turns=turns: RuleBasedConsolidationBaseline(
                _new_store("rule_based", case_id)
            ).run_turns(turns, session_id=case_id),
            "recursive_summary": lambda case_id=case["case_id"], turns=turns: RecursiveSummarizationBaseline(
                _new_store("recursive_summary", case_id)
            ).run_turns(turns, session_id=case_id),
        }

        for name, run in runners.items():
            result = run()
            row = _evaluate_case(case, name, result, cache)
            detailed.append(row)
            if name not in summary:
                summary[name] = {
                    "cases": 0,
                    "behavior_hit": 0,
                    "memory_hit": 0,
                    "provenance_hit": 0,
                }
            summary[name]["cases"] += 1
            summary[name]["behavior_hit"] += int(row["behavior_hit"])
            summary[name]["memory_hit"] += int(row["memory_hit"])
            summary[name]["provenance_hit"] += int(row["provenance_hit"])

    _save_cache(cache)
    markdown = _render_markdown(summary)
    report = {"judge_mode": judge_mode, "summary": summary, "details": detailed, "markdown": markdown}
    out = ROOT / "data" / "processed" / "eval_summary.md"
    out.write_text(markdown, encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
