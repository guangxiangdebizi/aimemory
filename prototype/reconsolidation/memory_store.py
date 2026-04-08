from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .types import Episode, MemoryVersion


class VersionedMemoryStore:
    """Simple JSON-backed versioned memory store."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.memories: Dict[str, List[MemoryVersion]] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        for memory_id, versions in raw.items():
            self.memories[memory_id] = [MemoryVersion(**item) for item in versions]

    def save(self) -> None:
        payload = {
            memory_id: [asdict(version) for version in versions]
            for memory_id, versions in self.memories.items()
        }
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_all(self) -> List[MemoryVersion]:
        return [version for versions in self.memories.values() for version in versions]

    def list_active(self) -> List[MemoryVersion]:
        items = []
        for versions in self.memories.values():
            active = [version for version in versions if version.status == "active"]
            items.extend(active)
        return items

    def latest(self, memory_id: str) -> Optional[MemoryVersion]:
        versions = self.memories.get(memory_id, [])
        if not versions:
            return None
        return sorted(versions, key=lambda item: item.version)[-1]

    def add_memory(self, episode: Episode, memory_text: str, memory_type: str = "episodic") -> MemoryVersion:
        memory_id = f"m_{len(self.memories) + 1:04d}"
        version = MemoryVersion(
            memory_id=memory_id,
            version=1,
            text=memory_text,
            memory_type=memory_type,
            status="active",
            provenance_set=[episode.episode_id],
            support_set=[episode.episode_id],
        )
        self.memories[memory_id] = [version]
        return version

    def revise_memory(self, target: MemoryVersion, episode: Episode, new_text: str, note: str) -> MemoryVersion:
        current = self.latest(target.memory_id)
        if current is None:
            raise KeyError(f"Memory {target.memory_id} not found")
        current.status = "revised"
        current.updated_at = episode.timestamp
        new_version = MemoryVersion(
            memory_id=current.memory_id,
            version=current.version + 1,
            text=new_text,
            memory_type=current.memory_type,
            status="active",
            provenance_set=sorted(set(current.provenance_set + [episode.episode_id])),
            support_set=sorted(set(current.support_set + [episode.episode_id])),
            contradiction_set=list(current.contradiction_set),
            parent_versions=[current.version_key],
            revision_history=current.revision_history + [note],
            confidence=current.confidence,
            created_at=current.created_at,
            updated_at=episode.timestamp,
        )
        self.memories[current.memory_id].append(new_version)
        return new_version

    def retire_memory(self, target: MemoryVersion, note: str) -> None:
        current = self.latest(target.memory_id)
        if current is None:
            return
        current.status = "retired"
        current.revision_history.append(note)

    def attach_support(self, target: MemoryVersion, episode_id: str) -> None:
        current = self.latest(target.memory_id)
        if current is None:
            return
        if episode_id not in current.support_set:
            current.support_set.append(episode_id)
        if episode_id not in current.provenance_set:
            current.provenance_set.append(episode_id)

    def attach_contradiction(self, target: MemoryVersion, episode_id: str) -> None:
        current = self.latest(target.memory_id)
        if current is None:
            return
        if episode_id not in current.contradiction_set:
            current.contradiction_set.append(episode_id)
        if episode_id not in current.provenance_set:
            current.provenance_set.append(episode_id)

