#!/usr/bin/env python3
"""Shared utilities for TCM Meridian Inference services.

Provides:
  - Logging configuration (stdout + daily-rotated file)
  - load_dotenv() for .env file loading
  - MERIDIANS constant
"""

from __future__ import annotations

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "tcm.log"

MERIDIANS = ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]

_FMT = logging.Formatter(
    fmt="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_initialized = False


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    gitignore = LOG_DIR / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text("*\n!.gitignore\n")


def _setup() -> None:
    global _initialized
    if _initialized:
        return
    _initialized = True

    _ensure_log_dir()

    root = logging.getLogger("tcm")
    root.setLevel(os.environ.get("TCM_LOG_LEVEL", "INFO").upper())

    if not root.handlers:
        # stdout
        sh = logging.StreamHandler()
        sh.setFormatter(_FMT)
        root.addHandler(sh)

        # file (rotate daily, keep 30 days)
        fh = TimedRotatingFileHandler(
            str(LOG_FILE),
            when="midnight",
            backupCount=30,
            encoding="utf-8",
        )
        fh.setFormatter(_FMT)
        root.addHandler(fh)


def get_logger(name: str) -> logging.Logger:
    """Return a logger under the 'tcm.' namespace."""
    _setup()
    if not name.startswith("tcm."):
        name = f"tcm.{name}"
    return logging.getLogger(name)


def load_dotenv(path: Path | None = None) -> None:
    """Load .env file into os.environ. Skips existing keys."""
    env_path = path or (PROJECT_DIR / ".env")
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value
