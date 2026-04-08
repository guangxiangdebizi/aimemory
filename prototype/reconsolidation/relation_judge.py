from __future__ import annotations

from .types import Episode, MemoryVersion, RelationDecision


class RelationJudge:
    """
    First-pass relation judge.

    This is intentionally lightweight and heuristic. In later iterations this
    can be swapped with an API-backed LLM judge without changing the rest of
    the pipeline.
    """

    NEGATION_CUES = ("不喜欢", "不再", "不想", "讨厌", "doesn't", "don't", "no longer", "not")
    REFINEMENT_CUES = ("只", "但是", "不过", "except", "only", "specifically", "更准确")

    def judge(self, episode: Episode, memory: MemoryVersion) -> RelationDecision:
        new_text = episode.content
        old_text = memory.text

        if new_text == old_text:
            return RelationDecision("SUPPORT", "New evidence matches the current memory.")

        if any(cue in new_text for cue in self.NEGATION_CUES) and not any(cue in old_text for cue in self.NEGATION_CUES):
            return RelationDecision("CONTRADICT", "New evidence introduces a likely contradiction.")

        if any(cue in new_text for cue in self.REFINEMENT_CUES):
            return RelationDecision("REFINE", "New evidence appears to refine or condition the existing memory.")

        if len(new_text) > len(old_text) and old_text[:6] and old_text[:6] in new_text:
            return RelationDecision("REFINE", "New evidence is a more detailed version of the old memory.")

        if "喜欢" in old_text and ("热" in new_text or "冰" in new_text or "条件" in new_text):
            return RelationDecision("OVERGENERALIZED", "The old memory may be too coarse and needs splitting.")

        return RelationDecision("UNRELATED", "No strong relation detected.")

