from __future__ import annotations

import re
from dataclasses import asdict
from datetime import datetime
from typing import Iterable, List

from .types import Episode


ENTITY_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]+|[\u4e00-\u9fff]{2,8}")


class EpisodeBuilder:
    """Turn raw dialogue turns into episode-level evidence."""

    def build_from_turns(self, turns: Iterable[str], session_id: str) -> List[Episode]:
        episodes: List[Episode] = []
        for index, turn in enumerate(turns, start=1):
            content = turn.strip()
            if not content:
                continue
            episodes.append(
                Episode(
                    episode_id=f"{session_id}_e{index:03d}",
                    content=content,
                    session_id=session_id,
                    timestamp=datetime.utcnow().isoformat(),
                    entities=self._extract_entities(content),
                    raw_span=[index - 1, index - 1],
                )
            )
        return episodes

    def _extract_entities(self, text: str) -> List[str]:
        seen = []
        for token in ENTITY_PATTERN.findall(text):
            if len(token) < 2:
                continue
            if token not in seen:
                seen.append(token)
        return seen[:8]

    def as_dicts(self, episodes: Iterable[Episode]) -> List[dict]:
        return [asdict(item) for item in episodes]

