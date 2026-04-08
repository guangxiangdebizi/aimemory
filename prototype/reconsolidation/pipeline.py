from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List

from .episode_builder import EpisodeBuilder
from .judges import BaseRelationJudge, create_relation_judge
from .memory_store import VersionedMemoryStore
from .operation_mapper import OperationMapper
from .resolver import RetrievalTimeResolver
from .retriever import CandidateRetriever
from .types import Episode


class ReconsolidationPipeline:
    def __init__(
        self,
        store: VersionedMemoryStore,
        judge: BaseRelationJudge | None = None,
    ):
        self.store = store
        self.builder = EpisodeBuilder()
        self.retriever = CandidateRetriever()
        self.judge = judge or create_relation_judge("heuristic")
        self.mapper = OperationMapper()
        self.resolver = RetrievalTimeResolver()

    def run_turns(self, turns: Iterable[str], session_id: str) -> dict:
        episodes = self.builder.build_from_turns(turns, session_id=session_id)
        return self.run_episodes(episodes)

    def run_episodes(self, episodes: Iterable[Episode]) -> dict:
        log: List[dict] = []
        for episode in episodes:
            active_memories = self.resolver.resolve_active(self.store.list_active())
            candidates = self.retriever.retrieve(episode, active_memories, top_k=3)

            if not candidates:
                created = self.store.add_memory(episode, episode.content, memory_type="semantic_preference")
                log.append({"episode": episode.episode_id, "operation": "ADD", "memory": created.version_key})
                continue

            top = candidates[0].memory
            relation = self.judge.judge(episode, top)
            operation = self.mapper.map(relation)

            if operation.operation == "REVISE":
                revised = self.store.revise_memory(top, episode, episode.content, note=relation.explanation)
                if relation.relation == "CONTRADICT":
                    self.store.attach_contradiction(revised, episode.episode_id)
                else:
                    self.store.attach_support(revised, episode.episode_id)
                log.append(
                    {
                        "episode": episode.episode_id,
                        "operation": "REVISE",
                        "memory": revised.version_key,
                        "relation": relation.relation,
                    }
                )
            elif operation.operation == "SPLIT":
                self.store.retire_memory(top, note="Retired due to over-generalization evidence.")
                left = self.store.add_memory(episode, "用户喜欢热咖啡或条件化偏好。", memory_type="semantic_preference")
                right = self.store.add_memory(episode, episode.content, memory_type="semantic_preference")
                log.append(
                    {
                        "episode": episode.episode_id,
                        "operation": "SPLIT",
                        "memory": [left.version_key, right.version_key],
                        "relation": relation.relation,
                    }
                )
            elif operation.operation == "NOOP":
                self.store.attach_support(top, episode.episode_id)
                log.append(
                    {
                        "episode": episode.episode_id,
                        "operation": "NOOP",
                        "memory": top.version_key,
                        "relation": relation.relation,
                    }
                )
            else:
                created = self.store.add_memory(episode, episode.content, memory_type="semantic_preference")
                log.append(
                    {
                        "episode": episode.episode_id,
                        "operation": operation.operation,
                        "memory": created.version_key,
                        "relation": relation.relation,
                    }
                )

        self.store.save()
        return {
            "events": log,
            "active_memories": [asdict(memory) for memory in self.resolver.resolve_active(self.store.list_active())],
        }

