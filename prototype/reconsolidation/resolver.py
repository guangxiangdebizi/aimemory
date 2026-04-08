from __future__ import annotations

from typing import List, Sequence

from .types import MemoryVersion


class RetrievalTimeResolver:
    """Resolve active memories for downstream answering."""

    def resolve_active(self, memories: Sequence[MemoryVersion]) -> List[MemoryVersion]:
        return [memory for memory in memories if memory.status == "active"]

