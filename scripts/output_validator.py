#!/usr/bin/env python3
"""Validate and fix DeepSeek output for the hybrid inference agent."""

from __future__ import annotations

import re
from typing import Any

from logger import MERIDIANS


# ---------------------------------------------------------------------------
# Post-processing: fix known LLM temperature-expression violations
# ---------------------------------------------------------------------------

_BAD_EXPR_FIXES: list[tuple[str, str]] = [
    # Order matters: more specific patterns first
    (r"温差扩大", "问题更突出"),
    (r"温差加重", "问题更突出"),
    (r"温差恶化", "问题更突出"),
    (r"且恶化", "且问题更突出"),
    (r"°C属([^于])", r"°C，\1"),                   # "°C属正常" → "°C，正常"
    (r"°C为有", "°C，"),                             # "°C为有" → "°C，"
    (r"属于有比较严重的问题", "存在严重失衡"),         # old → new
    (r"属于有健康问题", "存在明显失衡"),               # old → new
    (r"属于有一定亚健康", "存在轻度亚健康问题"),       # old → new
    (r"属于正常范围", "处于正常范围"),                  # old → new
    (r"属于较严重问题", "存在严重失衡"),
    (r"属于平衡(?!状|经|筋)", "处于正常范围"),
    (r"温差平衡", "温差正常"),
]


def _fix_temperature_expressions(text: str) -> str:
    """Apply regex fixes for known bad temperature expressions."""
    for pattern, replacement in _BAD_EXPR_FIXES:
        text = re.sub(pattern, replacement, text)
    # Fix double commas that may result from replacements
    text = text.replace("，，", "，")
    return text


def _fix_all_text_fields(result: dict[str, Any]) -> None:
    """Apply temperature expression fixes to all LLM-generated text fields."""
    # summary
    if isinstance(result.get("summary"), str):
        result["summary"] = _fix_temperature_expressions(result["summary"])
    if isinstance(result.get("reportSummary"), str):
        result["reportSummary"] = _fix_temperature_expressions(result["reportSummary"])

    # storefront
    sf = result.get("storefront", {})
    if isinstance(sf, dict):
        for key in ("focusHeadline", "clientExplanation", "retestPrompt"):
            if isinstance(sf.get(key), str):
                sf[key] = _fix_temperature_expressions(sf[key])
        for i, t in enumerate(sf.get("talkTrack", [])):
            if isinstance(t, str):
                sf["talkTrack"][i] = _fix_temperature_expressions(t)

    # meridianNarrative
    narrative = result.get("meridianNarrative", {})
    if isinstance(narrative, dict):
        for key in narrative:
            if isinstance(narrative[key], str):
                narrative[key] = _fix_temperature_expressions(narrative[key])

    # meridian_analysis narratives
    for ma in result.get("meridian_analysis", []):
        if isinstance(ma.get("narrative"), str):
            ma["narrative"] = _fix_temperature_expressions(ma["narrative"])

    # recommendations
    recs = result.get("recommendations", [])
    if isinstance(recs, list):
        result["recommendations"] = [
            _fix_temperature_expressions(r) if isinstance(r, str) else r
            for r in recs
        ]


def validate_and_fix(
    llm_output: dict[str, Any],
    rule_engine_result: dict[str, Any],
) -> dict[str, Any]:
    """Merge LLM-generated natural language into the rule engine result.

    The rule engine provides the deterministic skeleton (scores, statuses,
    symptoms, combinations).  The LLM provides summary, storefront, narrative,
    and recommendations.  This function merges them and fixes any LLM issues.
    """
    result = dict(rule_engine_result)

    # --- summary / reportSummary ---
    summary = llm_output.get("summary")
    if isinstance(summary, str) and len(summary) > 5:
        result["summary"] = summary
        result["reportSummary"] = summary

    # --- healthScore enrichment ---
    hs = result.get("healthScore", {})
    if isinstance(hs, dict):
        llm_summary = llm_output.get("healthScoreSummary")
        if isinstance(llm_summary, str) and len(llm_summary) > 5:
            hs["summary"] = llm_summary

    # --- storefront (legacy compat) ---
    sf_llm = llm_output.get("storefront")
    if isinstance(sf_llm, dict):
        sf = dict(result.get("storefront", {}))

        headline = sf_llm.get("focusHeadline")
        if isinstance(headline, str) and len(headline) > 2:
            sf["focusHeadline"] = headline

        explanation = sf_llm.get("clientExplanation", "")
        if isinstance(explanation, str):
            if "不等同" not in explanation and "非诊断" not in explanation:
                explanation = explanation.rstrip("\u3002") + "\uff1b\u7ed3\u679c\u4e0d\u7b49\u540c\u4e8e\u533b\u7597\u8bca\u65ad\u3002"
            sf["clientExplanation"] = explanation

        talk = sf_llm.get("talkTrack")
        if isinstance(talk, list):
            talk = [t for t in talk if isinstance(t, str) and len(t) > 2]
            if len(talk) > 3:
                talk = talk[:3]
            elif len(talk) < 3:
                defaults = [
                    "这次结果更适合做状态追踪参考。",
                    "不等同于医疗诊断，主要看趋势和差异。",
                    "建议按周期复测，观察变化。",
                ]
                while len(talk) < 3:
                    talk.append(defaults[len(talk)])
            sf["talkTrack"] = talk

        retest = sf_llm.get("retestPrompt")
        if isinstance(retest, str) and len(retest) > 2:
            sf["retestPrompt"] = retest

        result["storefront"] = sf

    # --- meridianNarrative enrichment ---
    narrative = llm_output.get("meridianNarrative")
    if isinstance(narrative, dict) and len(narrative) > 0:
        # Add meridianNarrative as a top-level field for easy access
        result["meridianNarrative"] = narrative
        # Also enrich meridian_analysis with narrative if it exists
        meridian_analysis = result.get("meridian_analysis", [])
        for ma in meridian_analysis:
            mid = ma.get("meridian", "")
            if mid in narrative and isinstance(narrative[mid], str):
                ma["narrative"] = narrative[mid]
        # Also legacy meridianDetails enrichment
        details = result.get("meridianDetails", [])
        for md in details:
            mid = md.get("meridianId", "")
            if mid in narrative and isinstance(narrative[mid], str):
                md["narrative"] = narrative[mid]

    # --- recommendations ---
    recs = llm_output.get("recommendations")
    if isinstance(recs, list) and len(recs) > 0:
        result["recommendations"] = [r for r in recs if isinstance(r, str)]

    # --- final safety checks ---
    _fix_all_text_fields(result)
    _ensure_storefront_safety(result)

    return result


def _ensure_storefront_safety(result: dict[str, Any]) -> None:
    """Ensure storefront meets all acceptance criteria."""
    sf = result.get("storefront", {})

    ce = sf.get("clientExplanation", "")
    if "不等同" not in ce and "非诊断" not in ce:
        sf["clientExplanation"] = ce.rstrip("\u3002") + "\uff1b\u7ed3\u679c\u4e0d\u7b49\u540c\u4e8e\u533b\u7597\u8bca\u65ad\u3002"

    tt = sf.get("talkTrack", [])
    if not isinstance(tt, list) or len(tt) != 3:
        tt = list(tt) if isinstance(tt, list) else []
        defaults = [
            "这次结果更适合做状态追踪参考。",
            "不等同于医疗诊断，主要看趋势和差异。",
            "建议按周期复测，观察变化。",
        ]
        while len(tt) < 3:
            tt.append(defaults[min(len(tt), 2)])
        sf["talkTrack"] = tt[:3]

    risk_tags = result.get("adviceTags", [])
    if not risk_tags:
        blob = " ".join([
            sf.get("focusHeadline", ""),
            sf.get("clientExplanation", ""),
            *sf.get("talkTrack", []),
            sf.get("retestPrompt", ""),
        ])
        for bad_word in ["预警", "严重", "危险", "紧急"]:
            if bad_word in blob:
                sf["focusHeadline"] = "整体相对平稳"
                sf["clientExplanation"] = (
                    "整体相对平稳，本次结果更适合做状态追踪，不等同于医疗诊断。"
                )
                sf["talkTrack"] = [
                    "本次六经整体比较平稳，更像状态跟踪结果。",
                    "这不等同于医疗诊断，主要用于看趋势和左右差异。",
                    "建议保持作息，按周期复测即可。",
                ]
                break

    result["storefront"] = sf
