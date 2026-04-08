# Reconsolidation Prototype

This directory contains the first minimal prototype for
`provenance-preserving reconsolidation`.

Scope of v0:
- build episode-level evidence
- maintain versioned long-term memories
- retrieve candidate memories
- classify new evidence vs old memory relations
- execute `ADD / REVISE / SPLIT / RETIRE / NOOP`
- resolve active memory at retrieval time

This prototype is intentionally simple:
- rule-based storage and retrieval
- pluggable relation judge (`heuristic`, `prompt_stub`, `llm`)
- no RL
- no heavy training

Recommended first run:

```bash
python prototype/scripts/run_reconsolidation.py
python prototype/scripts/run_baselines.py
python prototype/scripts/build_dataset.py
python prototype/scripts/run_eval_suite.py
```

To use the LLM judge:

```bash
python prototype/scripts/run_reconsolidation.py
```

Environment variables:
- `OPENAI_API_KEY`
- optional `OPENAI_MODEL` or `OPENAI_JUDGE_MODEL`
- optional `OPENAI_BASE_URL`

Environment management:
- local secrets live in repository-root `.env`
- tracked template lives in `.env.example`
- `.env` is ignored by git
- `.env` values take precedence over inherited shell variables

What exists now:
- `reconsolidation/judges.py`: replaceable judge interface
- `reconsolidation/pipeline.py`: shared reconsolidation loop
- `reconsolidation/baselines.py`: minimal baseline runners
- `scripts/run_eval_suite.py`: minimal case-based evaluation
