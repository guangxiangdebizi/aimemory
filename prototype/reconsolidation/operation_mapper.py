from __future__ import annotations

from .types import OperationDecision, RelationDecision


class OperationMapper:
    """Map relation labels to reconsolidation operations."""

    def map(self, decision: RelationDecision) -> OperationDecision:
        relation = decision.relation
        if relation == "NEW":
            return OperationDecision("ADD", "Create a new long-term memory.")
        if relation == "SUPPORT":
            return OperationDecision("NOOP", "Retain the memory and attach support evidence.")
        if relation == "REFINE":
            return OperationDecision("REVISE", "Create a refined memory version.")
        if relation == "CONTRADICT":
            return OperationDecision("REVISE", "Create a corrected active version and preserve revision history.")
        if relation == "OVERGENERALIZED":
            return OperationDecision("SPLIT", "Replace a coarse abstraction with finer-grained memories.")
        return OperationDecision("NOOP", "No structural update needed.")

