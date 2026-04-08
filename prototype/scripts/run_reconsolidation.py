from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from reconsolidation.episode_builder import EpisodeBuilder
from reconsolidation.memory_store import VersionedMemoryStore
from reconsolidation.operation_mapper import OperationMapper
from reconsolidation.relation_judge import RelationJudge
from reconsolidation.resolver import RetrievalTimeResolver
from reconsolidation.retriever import CandidateRetriever


def main() -> None:
    store_path = ROOT / "data" / "processed" / "memory_store.json"
    if store_path.exists():
        store_path.unlink()
    store = VersionedMemoryStore(store_path)
    builder = EpisodeBuilder()
    retriever = CandidateRetriever()
    judge = RelationJudge()
    mapper = OperationMapper()
    resolver = RetrievalTimeResolver()

    turns = [
        "用户说最近很喜欢蓝色界面，觉得蓝色很专业。",
        "用户说现在已经不喜欢蓝色界面了，因为会想到旧系统。",
        "用户说其实只接受深蓝色作为强调色，不喜欢大面积蓝色。",
    ]
    episodes = builder.build_from_turns(turns, session_id="demo")

    log = []
    for episode in episodes:
        active_memories = resolver.resolve_active(store.list_active())
        candidates = retriever.retrieve(episode, active_memories, top_k=3)

        if not candidates:
            created = store.add_memory(episode, episode.content, memory_type="semantic_preference")
            log.append({"episode": episode.episode_id, "operation": "ADD", "memory": created.version_key})
            continue

        top = candidates[0].memory
        relation = judge.judge(episode, top)
        operation = mapper.map(relation)

        if operation.operation == "REVISE":
            revised = store.revise_memory(top, episode, episode.content, note=relation.explanation)
            if relation.relation == "CONTRADICT":
                store.attach_contradiction(revised, episode.episode_id)
            else:
                store.attach_support(revised, episode.episode_id)
            log.append({"episode": episode.episode_id, "operation": "REVISE", "memory": revised.version_key})
        elif operation.operation == "SPLIT":
            store.retire_memory(top, note="Retired due to over-generalization evidence.")
            left = store.add_memory(episode, "用户喜欢热咖啡或条件化偏好。", memory_type="semantic_preference")
            right = store.add_memory(episode, episode.content, memory_type="semantic_preference")
            log.append({"episode": episode.episode_id, "operation": "SPLIT", "memory": [left.version_key, right.version_key]})
        elif operation.operation == "NOOP":
            store.attach_support(top, episode.episode_id)
            log.append({"episode": episode.episode_id, "operation": "NOOP", "memory": top.version_key})
        else:
            created = store.add_memory(episode, episode.content, memory_type="semantic_preference")
            log.append({"episode": episode.episode_id, "operation": operation.operation, "memory": created.version_key})

    store.save()
    print(json.dumps({"events": log, "active_memories": [m.text for m in resolver.resolve_active(store.list_active())]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
