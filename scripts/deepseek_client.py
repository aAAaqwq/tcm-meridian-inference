#!/usr/bin/env python3
"""DeepSeek API client for TCM meridian inference agent."""

from __future__ import annotations

import json
import os
import time
from typing import Any

import httpx

from logger import get_logger

log = get_logger("deepseek")

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
MAX_RETRIES = 2
TIMEOUT_S = 120  # 增加超时到 120 秒

# 全局复用的 HTTP Client（带连接池）
# limits: 最大保持 10 个连接，每个 host 最大 20 个连接
_http_client: httpx.Client | None = None


def _get_http_client() -> httpx.Client:
    """获取全局复用的 HTTP Client。"""
    global _http_client
    if _http_client is None:
        limits = httpx.Limits(
            max_keepalive_connections=10,
            max_connections=20,
        )
        # 分离连接超时和读取超时
        timeout = httpx.Timeout(
            connect=10.0,      # 建立连接超时
            read=TIMEOUT_S,    # 读取数据超时
            write=10.0,        # 写入超时
            pool=5.0,          # 从连接池获取连接超时
        )
        _http_client = httpx.Client(
            limits=limits,
            timeout=timeout,
            http2=False,  # 禁用 HTTP/2，避免兼容性问题
        )
        log.info("Initialized HTTP client with connection pooling")
    return _http_client


def close_http_client() -> None:
    """关闭 HTTP Client，释放资源。在程序退出时调用。"""
    global _http_client
    if _http_client is not None:
        try:
            _http_client.close()
            log.info("HTTP client closed")
        except Exception as e:
            log.warning("Error closing HTTP client: %s", e)
        finally:
            _http_client = None


class DeepSeekError(Exception):
    """Raised when the DeepSeek API call fails after retries."""


def _get_api_key() -> str:
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not key:
        raise DeepSeekError(
            "DEEPSEEK_API_KEY environment variable is not set. "
            "Set it in .env or export it before running."
        )
    return key


def chat(
    system: str,
    user: str,
    *,
    model: str | None = None,
    temperature: float = 1.0,
    max_tokens: int = 8192,
) -> dict[str, Any]:
    """Call DeepSeek chat completion and return parsed JSON dict.

    Uses deepseek-chat by default (fast, 2-5s).  For deepseek-reasoner,
    the system content is merged into the first user message because the
    reasoner model does not support system role or JSON mode.
    """
    api_key = _get_api_key()
    resolved_model = model or os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)
    is_reasoner = "reasoner" in resolved_model

    if is_reasoner:
        messages = [
            {"role": "user", "content": f"{system}\n\n---\n\n{user}"},
        ]
    else:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    body: dict[str, Any] = {
        "model": resolved_model,
        "messages": messages,
        "max_tokens": max_tokens,
    }

    if not is_reasoner:
        body["temperature"] = temperature
        body["response_format"] = {"type": "json_object"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_err: Exception | None = None
    t0 = time.time()
    log.info("DeepSeek call model=%s max_tokens=%d", resolved_model, max_tokens)

    client = _get_http_client()

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            resp = client.post(
                f"{DEEPSEEK_BASE_URL}/chat/completions",
                headers=headers,
                json=body,
            )
            if resp.status_code != 200:
                raise DeepSeekError(
                    f"DeepSeek API returned {resp.status_code}: {resp.text[:500]}"
                )
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            content = _extract_json_block(content)
            elapsed = time.time() - t0
            log.info("DeepSeek success model=%s latency=%.2fs", resolved_model, elapsed)
            return json.loads(content)
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            last_err = DeepSeekError(f"Failed to parse DeepSeek response: {e}")
            log.warning("DeepSeek parse error (attempt %d): %s", attempt, e)
        except httpx.TimeoutException:
            last_err = DeepSeekError(
                f"DeepSeek API timed out after {TIMEOUT_S}s (attempt {attempt})"
            )
            log.warning("DeepSeek timeout (attempt %d/%d)", attempt, MAX_RETRIES + 1)
        except httpx.HTTPError as e:
            last_err = DeepSeekError(f"HTTP error: {e}")
            log.warning("DeepSeek HTTP error (attempt %d): %s", attempt, e)

        if attempt <= MAX_RETRIES:
            wait = min(2 ** attempt, 8)
            log.info("DeepSeek retry %d/%d in %.1fs", attempt, MAX_RETRIES, wait)
            time.sleep(wait)

    elapsed = time.time() - t0
    log.error("DeepSeek failed after %d attempts (%.2fs): %s", MAX_RETRIES + 2, elapsed, last_err)
    raise last_err  # type: ignore[misc]


def _extract_json_block(text: str) -> str:
    """Extract JSON from markdown code fences if present."""
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        start = 1
        end = len(lines)
        for i in range(len(lines) - 1, 0, -1):
            if lines[i].strip() == "```":
                end = i
                break
        return "\n".join(lines[start:end])
    return stripped
