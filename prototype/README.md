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
- prompt-style relation judge stub
- no RL
- no heavy training

Recommended first run:

```bash
python prototype/scripts/run_reconsolidation.py
```

