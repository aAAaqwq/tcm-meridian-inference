#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_case(rel_path: str) -> dict:
    out = subprocess.check_output([
        "python3",
        str(ROOT / "scripts" / "infer.py"),
        rel_path,
    ], cwd=ROOT, text=True)
    return json.loads(out)


def _contains_any(items: list[str], keywords: list[str]) -> bool:
    blob = " ".join(items)
    return any(k in blob for k in keywords)


def test_c3_left_low_case_contract() -> None:
    data = run_case("fixtures/case_left_low.json")
    required = {"healthScore", "meridians", "combinations", "summary", "storefront"}
    missing = required - set(data.keys())
    assert not missing, f"missing top-level keys: {sorted(missing)}"
    assert data["meridians"]["liver"]["status"] == "left_low", data["meridians"]["liver"]
    assert isinstance(data["storefront"].get("talkTrack"), list), data["storefront"]


def test_c4_liver_left_low_symptoms() -> None:
    data = run_case("fixtures/case_left_low.json")
    liver = data["meridians"]["liver"]
    assert liver["status"] == "left_low", liver
    assert _contains_any(liver["symptoms"], ["代谢", "气虚"]), liver["symptoms"]


def test_c4_liver_right_low_symptoms() -> None:
    data = run_case("fixtures/case_right_low.json")
    liver = data["meridians"]["liver"]
    assert liver["status"] == "right_low", liver
    assert _contains_any(liver["symptoms"], ["血虚", "心脏供血"]), liver["symptoms"]


def test_c4_kidney_left_low_symptoms() -> None:
    data = run_case("fixtures/case_left_low.json")
    kidney = data["meridians"]["kidney"]
    assert kidney["status"] == "left_low", kidney
    assert _contains_any(kidney["symptoms"], ["尿酸", "耳鸣"]), kidney["symptoms"]


def test_c4_gallbladder_left_low_symptoms() -> None:
    data = run_case("fixtures/case_left_low.json")
    gallbladder = data["meridians"]["gallbladder"]
    assert gallbladder["status"] == "left_low", gallbladder
    assert _contains_any(gallbladder["symptoms"], ["胆红素", "偏头痛"]), gallbladder["symptoms"]


def test_c4_bladder_cross_symptoms() -> None:
    data = run_case("fixtures/case_cross.json")
    bladder = data["meridians"]["bladder"]
    # Current c3 design keeps directional low as primary status while retaining cross in tags.
    assert "cross" in bladder["tags"], bladder
    assert _contains_any(bladder["symptoms"], ["肠道息肉", "子宫", "肩颈腰"]), bladder["symptoms"]


def _combo_names(data: dict) -> list[str]:
    return [c.get("name", "") for c in data.get("combinations", [])]


def test_c5_combo_liver_gallbladder_transaminase() -> None:
    data = run_case("fixtures/case_left_low.json")
    names = _combo_names(data)
    assert any("转氨酶" in n for n in names), names


def test_c5_combo_kidney_bladder_opposite_low_cervical() -> None:
    data = run_case("fixtures/case_cross.json")
    names = _combo_names(data)
    assert any("颈椎" in n for n in names), names


def test_c5_combo_kidney_bladder_same_side_low_lumbar() -> None:
    data = run_case("fixtures/case_right_low.json")
    names = _combo_names(data)
    assert any("腰椎" in n for n in names), names


def test_c5_combo_right_side_four_plus_heart_supply() -> None:
    data = run_case("fixtures/case_right_low.json")
    names = _combo_names(data)
    assert any("心脏供血" in n for n in names), names


def test_c6_all_demo_cases_output_and_focusheadline() -> None:
    cases = {
        "fixtures/case_left_low.json": ["左侧偏低"],
        "fixtures/case_right_low.json": ["右侧偏低"],
        "fixtures/case_cross.json": ["交叉"],
        "fixtures/case_multi.json": ["多经络"],
        "fixtures/case_stable.json": ["整体相对平稳"],
    }

    for path, expected_any in cases.items():
        data = run_case(path)
        # required structure
        for k in ["healthScore", "meridians", "summary", "storefront"]:
            assert k in data, (path, k)
        sf = data["storefront"]
        assert isinstance(sf.get("talkTrack"), list) and len(sf["talkTrack"]) == 3, (path, sf)
        focus = sf.get("focusHeadline", "")
        assert any(x in focus for x in expected_any), (path, focus, expected_any)


if __name__ == "__main__":
    tests = [
        test_c3_left_low_case_contract,
        test_c4_liver_left_low_symptoms,
        test_c4_liver_right_low_symptoms,
        test_c4_kidney_left_low_symptoms,
        test_c4_gallbladder_left_low_symptoms,
        test_c4_bladder_cross_symptoms,
        test_c5_combo_liver_gallbladder_transaminase,
        test_c5_combo_kidney_bladder_opposite_low_cervical,
        test_c5_combo_kidney_bladder_same_side_low_lumbar,
        test_c5_combo_right_side_four_plus_heart_supply,
        test_c6_all_demo_cases_output_and_focusheadline,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
