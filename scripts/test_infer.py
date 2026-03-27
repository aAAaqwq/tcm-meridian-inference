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


def test_c3_left_low_case_contract() -> None:
    data = run_case("fixtures/case_left_low.json")
    required = {"healthScore", "meridians", "combinations", "summary", "storefront"}
    missing = required - set(data.keys())
    assert not missing, f"missing top-level keys: {sorted(missing)}"
    assert data["meridians"]["liver"]["status"] == "left_low", data["meridians"]["liver"]
    assert isinstance(data["storefront"].get("talkTrack"), list), data["storefront"]


if __name__ == "__main__":
    test_c3_left_low_case_contract()
    print("PASS test_c3_left_low_case_contract")
