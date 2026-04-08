from __future__ import annotations

from typing import List, Sequence

from .types import Episode, MemoryVersion, RetrievalCandidate


def _overlap_score(left: Sequence[str], right: Sequence[str]) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)


def _char_ngrams(text: str, n: int = 2) -> List[str]:
    compact = "".join(text.lower().split())
    if len(compact) <= n:
        return [compact] if compact else []
    return [compact[index : index + n] for index in range(len(compact) - n + 1)]


def _extract_memory_entities(text: str) -> List[str]:
    items = []
    for token in text.replace("，", " ").replace("。", " ").split():
        token = token.strip()
        if len(token) >= 2 and token not in items:
            items.append(token)
    return items


class CandidateRetriever:
    """Very simple lexical/entity retriever for the first prototype."""

    def retrieve(self, episode: Episode, memories: Sequence[MemoryVersion], top_k: int = 5) -> List[RetrievalCandidate]:
        scored: List[RetrievalCandidate] = []
        episode_tokens = _char_ngrams(episode.content)
        for memory in memories:
            text_tokens = _char_ngrams(memory.text)
            lexical = _overlap_score(episode_tokens, text_tokens)
            entity = _overlap_score(episode.entities, _extract_memory_entities(memory.text))
            score = lexical * 0.7 + entity * 0.3
            if score > 0:
                scored.append(RetrievalCandidate(memory=memory, score=score))
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]
