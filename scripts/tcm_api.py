#!/usr/bin/env python3
"""TCM Meridian Inference HTTP API - supports rule-only and hybrid (DeepSeek) modes.

Modes (set via TCM_INFER_MODE env var):
  - rule   : deterministic rule engine only (default, no API key needed)
  - agent  : hybrid = rule engine + DeepSeek natural language enrichment
  - auto   : use agent if DEEPSEEK_API_KEY is set, otherwise fall back to rule
"""
import json, sys, os, signal, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from importlib import util as importlib_util

from logger import get_logger, load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
INFER_SCRIPT = os.path.join(SCRIPT_DIR, "infer.py")
AGENT_SCRIPT = os.path.join(SCRIPT_DIR, "infer_agent.py")
RULES_DIR = os.path.join(PROJECT_DIR, "rules")
PORT = int(os.environ.get("TCM_API_PORT", 18790))
INFER_MODE = os.environ.get("TCM_INFER_MODE", "auto").lower()
log = get_logger("api")

_shutting_down = False

_infer_mod = None
_agent_mod = None
_thresholds = None
_meridian_rules = None
_combo_rules = None
_score_rules = None
_followup_policy = None


def load_infer():
    global _infer_mod
    if _infer_mod is not None:
        return _infer_mod
    spec = importlib_util.spec_from_file_location("infer", INFER_SCRIPT)
    _infer_mod = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(_infer_mod)
    return _infer_mod


def load_agent():
    global _agent_mod
    if _agent_mod is not None:
        return _agent_mod
    spec = importlib_util.spec_from_file_location("infer_agent", AGENT_SCRIPT)
    _agent_mod = importlib_util.module_from_spec(spec)
    spec.loader.exec_module(_agent_mod)
    return _agent_mod


def load_rules():
    global _thresholds, _meridian_rules, _combo_rules, _score_rules, _followup_policy
    if _thresholds is not None:
        return
    with open(os.path.join(RULES_DIR, "thresholds.json")) as f:
        _thresholds = json.load(f)
    with open(os.path.join(RULES_DIR, "meridian_rules.json")) as f:
        _meridian_rules = json.load(f)
    with open(os.path.join(RULES_DIR, "combination_rules.json")) as f:
        _combo_rules = json.load(f)
    with open(os.path.join(RULES_DIR, "score_rules.json")) as f:
        _score_rules = json.load(f)
    with open(os.path.join(RULES_DIR, "followup_policy_rules.json")) as f:
        _followup_policy = json.load(f)


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
        load_rules()
        mod = load_infer()
        return mod.infer(payload, _thresholds, _meridian_rules, _combo_rules, _score_rules, _followup_policy)


SAMPLE_DATA = {
    "measurements": {
        "liver": {"left": 34.5, "right": 34.3},
        "heart": {"left": 35.0, "right": 34.8},
        "spleen": {"left": 34.8, "right": 34.6},
        "kidney": {"left": 33.5, "right": 34.2},
        "stomach": {"left": 34.0, "right": 34.5},
        "gallbladder": {"left": 34.2, "right": 34.0},
        "bladder": {"left": 33.8, "right": 34.8}
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
            self._json({"status": "ok", "service": "tcm-meridian-api", "python": sys.version})
        elif path == "/":
            self._json({
                "service": "TCM Meridian Inference API",
                "version": "2.0",
                "inferMode": _resolve_mode(),
                "endpoints": {
                    "POST /": "Run inference (legacy)",
                    "POST /test": "Run with sample data",
                    "GET /health": "Health check (legacy)",
                    "GET /healthz": "Health check",
                    "POST /api/inference/meridian-diagnosis": "Run inference"
                },
                "meridians": ["liver", "spleen", "kidney", "stomach", "gallbladder", "bladder"]
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
                body = self.rfile.read(length)
                payload = json.loads(body)
            else:
                self._json({"error": "not found"}, 404)
                return

            result = run_inference(payload)
            elapsed = time.time() - t0
            self._json(result)

            engine = result.get("engine", {})
            hs = result.get("healthScore", {})
            score = hs.get("score", 0) if isinstance(hs, dict) else hs
            log.info(
                "POST %s mode=%s score=%.1f latency=%.2fs",
                path,
                engine.get("mode", "?"),
                score,
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
    server = HTTPServer(("0.0.0.0", PORT), TCMHandler)
    log.info("TCM API starting on 0.0.0.0:%d mode=%s", PORT, mode)

    def shutdown(sig, _frame):
        global _shutting_down
        if _shutting_down:
            log.info("Forced exit (second signal=%s)", sig)
            os._exit(1)
        _shutting_down = True
        log.info("TCM API shutting down (signal=%s)", sig)
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
