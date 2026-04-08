from __future__ import annotations

import os
from pathlib import Path


def load_env(env_path: str | Path | None = None, override: bool = True) -> None:
    """
    Minimal `.env` loader to avoid adding a dependency at the prototype stage.

    Search order:
    1. Explicit `env_path`
    2. Repository root `.env`
    """

    candidate = Path(env_path) if env_path is not None else Path(__file__).resolve().parents[2] / ".env"
    if not candidate.exists():
        return

    for line in candidate.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if override or key not in os.environ:
            os.environ[key] = value
