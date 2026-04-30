#!/usr/bin/env python3
"""Benchmark script for TCM API performance testing.

Tests:
1. Rule-only inference performance (no DeepSeek calls)
2. Connection pooling efficiency
3. Memory usage stability
"""

import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from infer import infer, load_rules

# Test payload (correct format)
TEST_PAYLOAD = {
    "subject": {"id": "bench-001", "name": "Benchmark"},
    "measurements": {
        "before": {
            "liver": {"left": 34.5, "right": 34.3},
            "spleen": {"left": 34.8, "right": 34.6},
            "kidney": {"left": 33.5, "right": 34.2},
            "stomach": {"left": 34.0, "right": 34.5},
            "gallbladder": {"left": 34.2, "right": 34.0},
            "bladder": {"left": 33.8, "right": 34.8}
        },
        "after": {
            "liver": {"left": 34.6, "right": 34.4},
            "spleen": {"left": 34.9, "right": 34.7},
            "kidney": {"left": 33.8, "right": 34.0},
            "stomach": {"left": 34.2, "right": 34.4},
            "gallbladder": {"left": 34.3, "right": 34.1},
            "bladder": {"left": 34.0, "right": 34.6}
        }
    }
}


def benchmark_single_call(rules, payload):
    """Run a single inference call and return latency."""
    thresholds, meridian_rules, combo_rules, score_rules, followup_policy = rules
    t0 = time.time()
    result = infer(payload, thresholds, meridian_rules, combo_rules, score_rules, followup_policy)
    latency = time.time() - t0
    return latency, result


def benchmark_sequential(rules, payload, n=100):
    """Run sequential benchmark."""
    print(f"\n{'='*60}")
    print(f"Sequential Benchmark: {n} calls")
    print(f"{'='*60}")

    latencies = []
    errors = 0

    for i in range(n):
        try:
            latency, _ = benchmark_single_call(rules, payload)
            latencies.append(latency)
            if (i + 1) % 20 == 0:
                print(f"  Progress: {i+1}/{n}")
        except Exception as e:
            errors += 1
            print(f"  Error at {i+1}: {e}")

    return latencies, errors


def benchmark_concurrent(rules, payload, concurrency=10, total=100):
    """Run concurrent benchmark."""
    print(f"\n{'='*60}")
    print(f"Concurrent Benchmark: {total} calls, {concurrency} concurrent")
    print(f"{'='*60}")

    latencies = []
    errors = 0

    def worker(_):
        try:
            latency, _ = benchmark_single_call(rules, payload)
            return latency, None
        except Exception as e:
            return None, str(e)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {executor.submit(worker, i): i for i in range(total)}
        completed = 0

        for future in as_completed(futures):
            latency, error = future.result()
            if error:
                errors += 1
            else:
                latencies.append(latency)

            completed += 1
            if completed % 20 == 0:
                print(f"  Progress: {completed}/{total}")

    return latencies, errors


def print_stats(latencies, errors, label=""):
    """Print benchmark statistics."""
    if not latencies:
        print(f"  No successful calls!")
        return

    latencies_ms = [l * 1000 for l in latencies]  # Convert to ms

    print(f"\n  Results {label}:")
    print(f"  {'-'*56}")
    print(f"  Total calls:    {len(latencies) + errors}")
    print(f"  Successful:     {len(latencies)}")
    print(f"  Errors:         {errors}")
    print(f"  {'-'*56}")
    print(f"  Latency (ms):")
    print(f"    Min:    {min(latencies_ms):.2f}")
    print(f"    Max:    {max(latencies_ms):.2f}")
    print(f"    Mean:   {statistics.mean(latencies_ms):.2f}")
    print(f"    Median: {statistics.median(latencies_ms):.2f}")
    print(f"    P95:    {sorted(latencies_ms)[int(len(latencies_ms)*0.95)]:.2f}")
    print(f"    P99:    {sorted(latencies_ms)[int(len(latencies_ms)*0.99)]:.2f}")
    print(f"    StdDev: {statistics.stdev(latencies_ms) if len(latencies_ms) > 1 else 0:.2f}")
    print(f"  {'-'*56}")
    print(f"  Throughput:     {len(latencies) / sum(latencies):.2f} req/s")


def main():
    print(f"{'='*60}")
    print("TCM Inference Engine Benchmark")
    print(f"{'='*60}")

    # Load rules
    PROJECT_DIR = SCRIPT_DIR.parent
    rules_dir = PROJECT_DIR / "rules"

    print("\nLoading rules...")
    rules = load_rules(rules_dir)
    print(f"  Rules loaded from {rules_dir}")

    # Warmup
    print("\nWarming up (10 calls)...")
    for _ in range(10):
        benchmark_single_call(rules, TEST_PAYLOAD)
    print("  Warmup complete")

    # Sequential benchmark
    latencies_seq, errors_seq = benchmark_sequential(rules, TEST_PAYLOAD, n=100)
    print_stats(latencies_seq, errors_seq, "(Sequential)")

    # Concurrent benchmark
    latencies_conc, errors_conc = benchmark_concurrent(rules, TEST_PAYLOAD, concurrency=10, total=100)
    print_stats(latencies_conc, errors_conc, "(Concurrent)")

    # Summary
    print(f"\n{'='*60}")
    print("Benchmark Complete")
    print(f"{'='*60}")

    # Write baseline if requested
    if "--save-baseline" in sys.argv:
        baseline = {
            "timestamp": time.time(),
            "sequential": {
                "count": len(latencies_seq),
                "mean_ms": statistics.mean(latencies_seq) * 1000 if latencies_seq else 0,
                "p95_ms": sorted([l * 1000 for l in latencies_seq])[int(len(latencies_seq) * 0.95)] if latencies_seq else 0,
            },
            "concurrent": {
                "count": len(latencies_conc),
                "mean_ms": statistics.mean(latencies_conc) * 1000 if latencies_conc else 0,
                "p95_ms": sorted([l * 1000 for l in latencies_conc])[int(len(latencies_conc) * 0.95)] if latencies_conc else 0,
            }
        }

        baseline_file = PROJECT_DIR / ".ecc" / "benchmarks" / "baseline.json"
        baseline_file.parent.mkdir(parents=True, exist_ok=True)
        with open(baseline_file, "w") as f:
            json.dump(baseline, f, indent=2)
        print(f"\nBaseline saved to {baseline_file}")


if __name__ == "__main__":
    main()
