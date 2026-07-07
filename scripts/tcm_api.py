#!/usr/bin/env python3
"""TCM Meridian Inference HTTP API v3 - Mulinsen Report Edition.

Supports rule-only and hybrid (DeepSeek) modes.
Modes (set via TCM_INFER_MODE env var):
  - rule   : deterministic rule engine only (default, no API key needed)
  - agent  : hybrid = rule engine + DeepSeek natural language enrichment
  - auto   : use agent if DEEPSEEK_API_KEY is set, otherwise fall back to rule

Input format (v3):
  - measurement_type: "first_test" or "retest"
  - gender: "male", "female", or "unknown"
  - meridians: {stomach, gallbladder, bladder, liver, spleen, kidney}
    each with group1_left, group1_right, group2_left, group2_right

See docs/sources/mulinsen-report-inference-flow.md for full PRD.
"""
import json
import sys
import os
import signal
import threading
import time
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from importlib import util as importlib_util

from logger import get_logger, load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INFER_SCRIPT = os.path.join(SCRIPT_DIR, "infer_v3.py")  # v3 inference engine
AGENT_SCRIPT = os.path.join(SCRIPT_DIR, "infer_agent.py")
RULES_DIR = os.path.join(PROJECT_DIR, "rules")
PORT = int(os.environ.get("TCM_API_PORT", 18790))
INFER_MODE = os.environ.get("TCM_INFER_MODE", "auto").lower()
log = get_logger("api")

_shutting_down = False

_infer_mod = None
_agent_mod = None
_rules = None
_load_lock = threading.Lock()


def load_infer():
    """加载推理引擎模块（线程安全，双重检查锁定）。"""
    global _infer_mod
    if _infer_mod is not None:
        return _infer_mod
    with _load_lock:
        if _infer_mod is not None:
            return _infer_mod
        spec = importlib_util.spec_from_file_location("infer_v3", INFER_SCRIPT)
        _infer_mod = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(_infer_mod)
    return _infer_mod


def load_agent():
    """加载 agent 模块（线程安全，双重检查锁定）。"""
    global _agent_mod
    if _agent_mod is not None:
        return _agent_mod
    with _load_lock:
        if _agent_mod is not None:
            return _agent_mod
        spec = importlib_util.spec_from_file_location("infer_agent", AGENT_SCRIPT)
        _agent_mod = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(_agent_mod)
    return _agent_mod


def load_rules():
    """加载规则文件（线程安全，双重检查锁定）。"""
    global _rules
    if _rules is not None:
        return _rules
    with _load_lock:
        if _rules is not None:
            return _rules
        with open(os.path.join(RULES_DIR, "meridian_rules.json")) as f:
            meridian_rules = json.load(f)
        _rules = {"meridian_rules": meridian_rules}
    return _rules


def _resolve_mode():
    """Determine actual inference mode based on config and available keys."""
    if INFER_MODE == "agent":
        return "agent"
    if INFER_MODE == "rule":
        return "rule"
    # auto: use agent if API key is available
    if os.environ.get("DEEPSEEK_API_KEY", "").strip():
        return "agent"
    return "rule"


def run_inference(payload):
    mode = _resolve_mode()
    if mode == "agent":
        agent = load_agent()
        return agent.run_hybrid(
            payload,
            rules_dir=Path(RULES_DIR),
        )
    else:
        rules = load_rules()
        mod = load_infer()
        return mod.infer(payload, rules)


# v3 Sample data (Mulinsen format)
SAMPLE_DATA = {
    "measurement_type": "first_test",
    "gender": "female",
    "meridians": {
        "stomach": {
            "group1_left": 39.5,
            "group1_right": 40.5,
            "group2_left": 42.4,
            "group2_right": 42.5
        },
        "gallbladder": {
            "group1_left": 36.7,
            "group1_right": 36.7,
            "group2_left": 42.1,
            "group2_right": 42.1
        },
        "bladder": {
            "group1_left": 36.2,
            "group1_right": 36.5,
            "group2_left": 37.9,
            "group2_right": 41.1
        },
        "liver": {
            "group1_left": 36.7,
            "group1_right": 36.4,
            "group2_left": 39.6,
            "group2_right": 39.9
        },
        "spleen": {
            "group1_left": 36.6,
            "group1_right": 36.5,
            "group2_left": 39.1,
            "group2_right": 40.6
        },
        "kidney": {
            "group1_left": 36.6,
            "group1_right": 36.7,
            "group2_left": 40.5,
            "group2_right": 41.6
        }
    }
}


class TCMHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/health", "/healthz"):
            self._json({"status": "ok", "service": "tcm-meridian-api-v3", "python": sys.version})
        elif path == "/":
            self._json({
                "service": "TCM Meridian Inference API v3",
                "version": "3.0",
                "inferMode": _resolve_mode(),
                "endpoints": {
                    "POST /": "Run inference (legacy)",
                    "POST /test": "Run with sample data",
                    "GET /health": "Health check (legacy)",
                    "GET /healthz": "Health check",
                    "POST /api/inference/meridian-diagnosis": "Run inference"
                },
                "meridians": ["stomach", "gallbladder", "bladder", "liver", "spleen", "kidney"],
                "inputFormat": "v3 (group1/group2) - see PRD docs/sources/mulinsen-report-inference-flow.md"
            })
        else:
            self._json({"error": "not found"}, 404)
        log.debug("GET %s %s", path, 200 if path in ("/health", "/healthz", "/") else 404)

    def do_POST(self):
        path = urlparse(self.path).path
        t0 = time.time()
        try:
            if path == "/test":
                payload = SAMPLE_DATA
            elif path in ("/", "/api/inference/meridian-diagnosis"):
                length = int(self.headers.get("Content-Length", 0))
                if length > 10 * 1024 * 1024:  # 限制请求体 10MB
                    self._json({"error": "request body too large"}, 413)
                    log.warning("POST %s 413 body_too_large: %d bytes", path, length)
                    return
                body = self.rfile.read(length)
                payload = json.loads(body)
            else:
                self._json({"error": "not found"}, 404)
                return

            result = run_inference(payload)
            elapsed = time.time() - t0
            self._json(result)

            score_result = result.get("score_result", {})
            score = score_result.get("score", 0)
            problem_index = score_result.get("problem_index", 0)
            log.info(
                "POST %s mode=%s score=%s problem_index=%.1f latency=%.2fs",
                path,
                _resolve_mode(),
                score,
                problem_index,
                elapsed,
            )
            log.debug("response body: %s", json.dumps(result, ensure_ascii=False))
        except ValueError as e:
            self._json({"error": "invalid JSON: " + str(e)}, 400)
            log.warning("POST %s 400 invalid_json: %s", path, e)
        except Exception as e:
            elapsed = time.time() - t0
            self._json({"error": str(e)}, 500)
            log.error("POST %s 500 error (%.2fs): %s", path, elapsed, e)

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def log_message(self, fmt, *args):
        log.debug("http %s", fmt % args)


def main():
    global _shutting_down
    load_dotenv()
    mode = _resolve_mode()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), TCMHandler)
    log.info("TCM API v3 starting on 0.0.0.0:%d mode=%s", PORT, mode)

    def shutdown(sig, _frame):
        global _shutting_down
        if _shutting_down:
            log.info("Forced exit (second signal=%s)", sig)
            os._exit(1)
        _shutting_down = True
        log.info("TCM API shutting down (signal=%s)", sig)
        # 关闭 HTTP client 释放连接池
        try:
            from deepseek_client import close_http_client
            close_http_client()
        except Exception as e:
            log.warning("Error closing HTTP client during shutdown: %s", e)
        # Set the internal flag that serve_forever() polls every 0.5s
        # Cannot call server.shutdown() here — it deadlocks (tries to join itself)
        server._BaseServer__shutdown_request = True  # noqa: SLF001

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    try:
        server.serve_forever()
    except (KeyboardInterrupt, OSError):
        pass
    finally:
        try:
            server.server_close()
        except Exception:
            pass
        log.info("TCM API stopped")


if __name__ == "__main__":
    main()
