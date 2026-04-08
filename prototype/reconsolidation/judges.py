from __future__ import annotations

from dataclasses import asdict
import json
import os
import re
import urllib.error
import urllib.request
from typing import Protocol, cast

from .env_utils import load_env
from .types import Episode, MemoryVersion, RelationDecision, RelationLabel

load_env()


class BaseRelationJudge(Protocol):
    def judge(self, episode: Episode, memory: MemoryVersion) -> RelationDecision: ...


class HeuristicRelationJudge:
    """
    Lightweight first-pass judge.

    This is not the research contribution. It is a replaceable component that
    lets the prototype validate the reconsolidation pipeline before we swap in
    an API-backed or learned judge.
    """

    NEGATION_CUES = ("不喜欢", "不再", "不想", "讨厌", "doesn't", "don't", "no longer", "not")
    REFINEMENT_CUES = ("只", "但是", "不过", "except", "only", "specifically", "更准确")

    def judge(self, episode: Episode, memory: MemoryVersion) -> RelationDecision:
        new_text = episode.content
        old_text = memory.text

        if new_text == old_text:
            return RelationDecision("SUPPORT", "New evidence matches the current memory.")

        if any(cue in new_text for cue in self.NEGATION_CUES) and not any(
            cue in old_text for cue in self.NEGATION_CUES
        ):
            return RelationDecision("CONTRADICT", "New evidence introduces a likely contradiction.")

        if any(cue in new_text for cue in self.REFINEMENT_CUES):
            return RelationDecision("REFINE", "New evidence appears to refine or condition the existing memory.")

        if len(new_text) > len(old_text) and old_text[:6] and old_text[:6] in new_text:
            return RelationDecision("REFINE", "New evidence is a more detailed version of the old memory.")

        if "喜欢" in old_text and ("热" in new_text or "冰" in new_text or "条件" in new_text):
            return RelationDecision("OVERGENERALIZED", "The old memory may be too coarse and needs splitting.")

        return RelationDecision("UNRELATED", "No strong relation detected.")


class PromptStubRelationJudge:
    """
    Placeholder for future API-backed judging.

    The prompt is made explicit here to show that prompts are only the
    implementation vehicle for the judge, not the research contribution.
    """

    def build_prompt(self, episode: Episode, memory: MemoryVersion) -> str:
        episode_json = asdict(episode)
        memory_json = asdict(memory)
        return (
            "You are a relation judge for reconsolidation.\n"
            "Classify the relation between new evidence and an existing long-term memory.\n"
            "Allowed labels: NEW, SUPPORT, REFINE, CONTRADICT, OVERGENERALIZED, UNRELATED.\n\n"
            f"New evidence:\n{episode_json}\n\n"
            f"Existing memory:\n{memory_json}\n\n"
            "Return a JSON object with fields: relation, explanation."
        )

    def judge(self, episode: Episode, memory: MemoryVersion) -> RelationDecision:
        explanation = self.build_prompt(episode, memory)
        return RelationDecision(
            "UNRELATED",
            "Prompt stub only. Replace with an API-backed judge in later experiments.\n" + explanation,
        )


class LLMRelationJudge:
    """
    OpenAI-compatible relation judge.

    This keeps the pipeline unchanged while replacing heuristic label decisions
    with a model-based classifier. The research claim is still about
    reconsolidation, not about prompt design.
    """

    VALID_LABELS = {
        "NEW",
        "SUPPORT",
        "REFINE",
        "CONTRADICT",
        "OVERGENERALIZED",
        "UNRELATED",
    }
    JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", re.DOTALL)

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        timeout: int = 60,
        fallback: BaseRelationJudge | None = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("OPENAI_JUDGE_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
        self.base_url = (base_url or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.timeout = timeout
        self.fallback = fallback or HeuristicRelationJudge()

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for LLMRelationJudge.")

    def build_messages(self, episode: Episode, memory: MemoryVersion) -> list[dict]:
        system = (
            "You are a relation judge for a reconsolidation memory system.\n"
            "Your task is to classify how a new episodic evidence item relates to an existing long-term memory.\n"
            "Allowed labels: NEW, SUPPORT, REFINE, CONTRADICT, OVERGENERALIZED, UNRELATED.\n"
            "Return strict JSON with fields: relation, explanation.\n"
            "Use OVERGENERALIZED only when the old memory is too coarse and should be split or re-grounded.\n"
            "Use REFINE when the new evidence adds conditions, exceptions, or more precise detail.\n"
            "Use CONTRADICT when the new evidence reverses or invalidates the old memory."
        )

        examples = [
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "new_evidence": "用户说现在已经不喜欢蓝色界面了，因为会想到旧系统。",
                        "existing_memory": "用户喜欢蓝色界面。",
                    },
                    ensure_ascii=False,
                ),
            },
            {
                "role": "assistant",
                "content": json.dumps(
                    {
                        "relation": "CONTRADICT",
                        "explanation": "The new evidence reverses the old preference and provides a reason.",
                    },
                    ensure_ascii=False,
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "new_evidence": "用户说只喜欢热咖啡，不喜欢冰咖啡。",
                        "existing_memory": "用户喜欢咖啡。",
                    },
                    ensure_ascii=False,
                ),
            },
            {
                "role": "assistant",
                "content": json.dumps(
                    {
                        "relation": "OVERGENERALIZED",
                        "explanation": "The old memory is too coarse and misses crucial conditional preference details.",
                    },
                    ensure_ascii=False,
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "new_evidence": "用户说深蓝色做强调色还能接受。",
                        "existing_memory": "用户现在不喜欢蓝色界面。",
                    },
                    ensure_ascii=False,
                ),
            },
            {
                "role": "assistant",
                "content": json.dumps(
                    {
                        "relation": "REFINE",
                        "explanation": "The new evidence adds a condition and exception to the current memory.",
                    },
                    ensure_ascii=False,
                ),
            },
        ]

        task = {
            "new_evidence": asdict(episode),
            "existing_memory": asdict(memory),
            "instruction": "Return strict JSON only.",
        }
        return [{"role": "system", "content": system}, *examples, {"role": "user", "content": json.dumps(task, ensure_ascii=False)}]

    def judge(self, episode: Episode, memory: MemoryVersion) -> RelationDecision:
        payload = {
            "model": self.model,
            "messages": self.build_messages(episode, memory),
            "temperature": 0,
        }
        request = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            fallback = self.fallback.judge(episode, memory)
            return RelationDecision(
                fallback.relation,
                f"Fallback to heuristic due to LLM judge HTTPError {exc.code}: {body[:300]} | {fallback.explanation}",
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            fallback = self.fallback.judge(episode, memory)
            return RelationDecision(
                fallback.relation,
                f"Fallback to heuristic due to LLM judge error: {type(exc).__name__}: {exc}. {fallback.explanation}",
            )

        content = raw["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            match = self.JSON_BLOCK_PATTERN.search(content)
            if match:
                try:
                    parsed = json.loads(match.group(0))
                except json.JSONDecodeError:
                    parsed = None
            else:
                parsed = None
        if parsed is None:
            fallback = self.fallback.judge(episode, memory)
            return RelationDecision(
                fallback.relation,
                f"Fallback to heuristic due to non-JSON LLM output: {content[:200]} | {fallback.explanation}",
            )

        relation = str(parsed.get("relation", "UNRELATED")).strip().upper()
        explanation = str(parsed.get("explanation", "")).strip() or "LLM judge returned no explanation."
        if relation not in self.VALID_LABELS:
            fallback = self.fallback.judge(episode, memory)
            return RelationDecision(
                fallback.relation,
                f"Fallback to heuristic due to invalid label {relation!r}. {fallback.explanation}",
            )

        return RelationDecision(cast(RelationLabel, relation), explanation)


def create_relation_judge(mode: str = "heuristic") -> BaseRelationJudge:
    if mode == "heuristic":
        return HeuristicRelationJudge()
    if mode == "prompt_stub":
        return PromptStubRelationJudge()
    if mode == "llm":
        return LLMRelationJudge()
    raise ValueError(f"Unsupported judge mode: {mode}")
