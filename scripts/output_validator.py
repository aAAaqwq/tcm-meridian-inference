#!/usr/bin/env python3
"""Validate and fix DeepSeek output for the hybrid inference agent."""

from __future__ import annotations

from typing import Any

from logger import MERIDIANS


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
    if isinstance(narrative, dict):
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
