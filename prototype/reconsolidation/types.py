from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Literal, Optional


RelationLabel = Literal[
    "NEW",
    "SUPPORT",
    "REFINE",
    "CONTRADICT",
    "OVERGENERALIZED",
    "UNRELATED",
]

Operation = Literal["ADD", "REVISE", "SPLIT", "MERGE", "RETIRE", "NOOP"]
MemoryStatus = Literal["active", "revised", "retired"]


@dataclass
class Episode:
    episode_id: str
    content: str
    session_id: str
    timestamp: str
    entities: List[str] = field(default_factory=list)
    confidence: float = 1.0
    raw_span: Optional[List[int]] = None


@dataclass
class MemoryVersion:
    memory_id: str
    version: int
    text: str
    memory_type: str
    status: MemoryStatus
    provenance_set: List[str] = field(default_factory=list)
    support_set: List[str] = field(default_factory=list)
    contradiction_set: List[str] = field(default_factory=list)
    parent_versions: List[str] = field(default_factory=list)
    revision_history: List[str] = field(default_factory=list)
    confidence: float = 1.0
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def version_key(self) -> str:
        return f"{self.memory_id}_v{self.version}"


@dataclass
class RetrievalCandidate:
    memory: MemoryVersion
    score: float


@dataclass
class RelationDecision:
    relation: RelationLabel
    explanation: str


@dataclass
class OperationDecision:
    operation: Operation
    rationale: str

