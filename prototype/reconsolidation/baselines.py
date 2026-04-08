from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List

from .episode_builder import EpisodeBuilder
from .memory_store import VersionedMemoryStore
from .resolver import RetrievalTimeResolver
from .retriever import score_memory_match
from .types import Episode


class NoConsolidationBaseline:
    def __init__(self, store: VersionedMemoryStore):
        self.store = store
        self.builder = EpisodeBuilder()
        self.resolver = RetrievalTimeResolver()

    def run_turns(self, turns: Iterable[str], session_id: str) -> dict:
        episodes = self.builder.build_from_turns(turns, session_id=session_id)
        events = []
        for episode in episodes:
            created = self.store.add_memory(episode, episode.content, memory_type="semantic_preference")
            events.append({"episode": episode.episode_id, "operation": "ADD", "memory": created.version_key})
        self.store.save()
        return {
            "events": events,
            "active_memories": [asdict(memory) for memory in self.resolver.resolve_active(self.store.list_active())],
        }


class RuleBasedConsolidationBaseline:
    def __init__(self, store: VersionedMemoryStore):
        self.store = store
        self.builder = EpisodeBuilder()
        self.resolver = RetrievalTimeResolver()

    def run_turns(self, turns: Iterable[str], session_id: str) -> dict:
        episodes = self.builder.build_from_turns(turns, session_id=session_id)
        events = []
        for episode in episodes:
            matched = None
            best_score = 0.0
            for memory in self.store.list_active():
                score = score_memory_match(episode, memory)
                if score > best_score:
                    best_score = score
                    matched = memory
            if matched is None or best_score < 0.05:
                created = self.store.add_memory(episode, episode.content, memory_type="semantic_preference")
                events.append({"episode": episode.episode_id, "operation": "ADD", "memory": created.version_key})
            else:
                merged = self.store.revise_memory(
                    matched,
                    episode,
                    f"{matched.text} {episode.content}",
                    note="Rule-based merge on entity overlap.",
                )
                events.append({"episode": episode.episode_id, "operation": "MERGE", "memory": merged.version_key})
        self.store.save()
        return {
            "events": events,
            "active_memories": [asdict(memory) for memory in self.resolver.resolve_active(self.store.list_active())],
        }


class RecursiveSummarizationBaseline:
    def __init__(self, store: VersionedMemoryStore):
        self.store = store
        self.builder = EpisodeBuilder()
        self.resolver = RetrievalTimeResolver()

    def run_turns(self, turns: Iterable[str], session_id: str) -> dict:
        episodes = self.builder.build_from_turns(turns, session_id=session_id)
        events = []
        if not episodes:
            return {"events": events, "active_memories": []}

        summary_text = "；".join(episode.content for episode in episodes)
        created = self.store.add_memory(episodes[-1], summary_text, memory_type="session_summary")
        events.append({"episode": episodes[-1].episode_id, "operation": "SUMMARY", "memory": created.version_key})
        self.store.save()
        return {
            "events": events,
            "active_memories": [asdict(memory) for memory in self.resolver.resolve_active(self.store.list_active())],
        }
