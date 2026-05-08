#!/usr/bin/env python3
"""Test TCM API with fixtures and record input/output."""

import json
import subprocess
import sys
from pathlib import Path

API_URL = "http://180.76.137.183:18790/api/inference/meridian-diagnosis"
FIXTURES_DIR = Path("fixtures/v3")
OUTPUT_FILE = Path("docs/v3/testing/test_outputs_real.json")

def run_test(fixture_path: Path) -> dict:
    """Run single test against API."""
    with open(fixture_path) as f:
        payload = json.load(f)

    # Remove expected field if present
    expected = payload.pop("expected", None)

    # Run curl
    cmd = [
        "curl", "-s", "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload, ensure_ascii=False),
        API_URL
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        return {
            "file": fixture_path.name,
            "error": f"curl failed: {result.stderr}",
            "input": payload
        }

    try:
        response = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        return {
            "file": fixture_path.name,
            "error": f"JSON decode error: {e}",
            "raw_response": result.stdout[:500],
            "input": payload
        }

    return {
        "file": fixture_path.name,
        "input": payload,
        "output": response,
        "expected": expected
    }

def main():
    fixtures = sorted(FIXTURES_DIR.glob("test_*.json"))
    results = []

    print(f"Testing {len(fixtures)} fixtures against {API_URL}")
    print("=" * 60)

    for i, fixture in enumerate(fixtures, 1):
        print(f"[{i}/{len(fixtures)}] Testing {fixture.name}...", end=" ", flush=True)

        try:
            result = run_test(fixture)
            results.append(result)

            if "error" in result:
                print(f"FAIL: {result['error'][:50]}")
            else:
                score = result.get("output", {}).get("score_result", {}).get("score", "N/A")
                print(f"OK (score={score})")
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "file": fixture.name,
                "error": str(e)
            })

    # Save results
    output_data = {
        "api_url": API_URL,
        "total_tests": len(results),
        "passed": sum(1 for r in results if "error" not in r),
        "failed": sum(1 for r in results if "error" in r),
        "results": results
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"Results saved to {OUTPUT_FILE}")
    print(f"Total: {output_data['total_tests']}, Passed: {output_data['passed']}, Failed: {output_data['failed']}")

    return 0 if output_data['failed'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
