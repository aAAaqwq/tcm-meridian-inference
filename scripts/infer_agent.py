#!/usr/bin/env python3
"""Hybrid inference agent: rule engine + DeepSeek natural language generation.

Flow:
  1. Run deterministic rule engine (infer.py) to get scores, statuses, symptoms
  2. Build prompts with rule context and engine results
  3. Call DeepSeek to generate natural language (summary, storefront, narrative)
  4. Validate and merge LLM output back into rule engine result
  5. Return enriched result

Falls back to pure rule engine output if DeepSeek is unavailable.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))

from infer import infer, load_rules  # noqa: E402
from deepseek_client import chat, DeepSeekError  # noqa: E402
from prompt_builder import build_system_prompt, build_user_prompt  # noqa: E402
from output_validator import validate_and_fix  # noqa: E402
from logger import get_logger, load_dotenv  # noqa: E402

log = get_logger("agent")


def run_hybrid(
    payload: dict[str, Any],
    *,
    rules_dir: Path | None = None,
    skip_llm: bool = False,
) -> dict[str, Any]:
    """Run hybrid inference: rule engine + optional DeepSeek enrichment.

    Args:
        payload: Input JSON with subject and measurements.
        rules_dir: Path to rules directory. Defaults to PROJECT_DIR/rules.
        skip_llm: If True, skip DeepSeek call and return pure rule engine output.

    Returns:
        Enriched inference result dict.
    """
    if rules_dir is None:
        rules_dir = PROJECT_DIR / "rules"

    thresholds, meridian_rules, combo_rules, score_rules, followup_policy = load_rules(rules_dir)

    # Step 1: deterministic rule engine
    t_rule = time.time()
    rule_result = infer(payload, thresholds, meridian_rules, combo_rules, score_rules, followup_policy)
    hs = rule_result.get("healthScore", {})
    score = hs.get("score", 0) if isinstance(hs, dict) else hs
    log.info(
        "rule engine done score=%.1f latency=%.2fs",
        score,
        time.time() - t_rule,
    )

    if skip_llm:
        rule_result["engine"]["mode"] = "rule-only"
        log.info("skipped LLM (rule-only mode)")
        return rule_result

    # Step 2: build prompts
    system_prompt = build_system_prompt(thresholds, meridian_rules, combo_rules)
    user_prompt = build_user_prompt(payload, rule_result)

    # Step 3: call DeepSeek
    t0 = time.time()
    try:
        llm_output = chat(system_prompt, user_prompt)
        elapsed = round(time.time() - t0, 2)
    except DeepSeekError as e:
        # Fallback to pure rule engine on LLM failure
        elapsed = round(time.time() - t0, 2)
        log.warning("DeepSeek failed (%.2fs), falling back to rule: %s", elapsed, e)
        rule_result["engine"]["mode"] = "rule-fallback"
        rule_result["engine"]["llmError"] = str(e)
        return rule_result

    # Step 4: validate and merge
    merged = validate_and_fix(llm_output, rule_result)
    merged["engine"] = {
        "mode": "hybrid",
        "version": rule_result["engine"]["version"],
        "llmModel": os.environ.get("DEEPSEEK_MODEL", "deepseek-reasoner"),
        "llmLatency": elapsed,
    }
    log.info("hybrid inference done score=%.1f llm_latency=%.2fs", merged.get("healthScoreValue", 0), elapsed)

    return merged


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        prog="infer_agent.py",
        description="TCM meridian hybrid inference agent (rule engine + DeepSeek)",
    )
    ap.add_argument("input", nargs="?", help="Input JSON file")
    ap.add_argument("--rules-dir", default="rules", help="Rules directory")
    ap.add_argument("--rule-only", action="store_true", help="Skip LLM, pure rule engine")
    ap.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    ap.add_argument("--out", help="Write output JSON to file")
    args = ap.parse_args()

    if not args.input:
        ap.print_help()
        return 0

    in_path = (PROJECT_DIR / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    rules_dir = (PROJECT_DIR / args.rules_dir).resolve()

    if not in_path.exists():
        print(f"Error: input not found: {in_path}", file=sys.stderr)
        return 1

    # Load .env if available
    load_dotenv(PROJECT_DIR / ".env")

    payload = json.loads(in_path.read_text(encoding="utf-8"))
    result = run_hybrid(payload, rules_dir=rules_dir, skip_llm=args.rule_only)

    text = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.out:
        out_path = (PROJECT_DIR / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
