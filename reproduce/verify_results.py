#!/usr/bin/env python3
"""Verify published data integrity and recompute recorded summary statistics."""
import csv
import hashlib
import json
import math
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def close(actual, expected, label):
    require(math.isfinite(actual) and math.isfinite(expected), f"Nonfinite: {label}")
    require(math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12),
            f"Mismatch: {label}: {actual} != {expected}")


def percentile95(samples):
    values = sorted(samples)
    index = (len(values) - 1) * 0.95
    lower = math.floor(index)
    upper = math.ceil(index)
    return values[lower] + (values[upper] - values[lower]) * (index - lower)


def main():
    manifest = json.loads((ROOT / "data/provenance.json").read_text())
    for entry in manifest["published_files"]:
        path = ROOT / entry["path"]
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == entry["sha256"], f"File integrity mismatch: {entry['path']}")

    checked_samples = 0
    for label in ("baseline", "performance"):
        data = json.loads((ROOT / f"data/hp15-{label}.json").read_text())
        require(len(data["cases"]) == 3, f"Unexpected case count: {label}")
        for case in data["cases"]:
            prefix = f"{label}/{case['elements']}"
            for method in ("cpu", "gpu_pooled_end_to_end", "gpu_fresh_buffers_end_to_end",
                           "gpu_resident_dispatch"):
                result = case[method]
                samples = result["samples_ms"]
                require(len(samples) == 15 and all(math.isfinite(x) and x > 0 for x in samples),
                        f"Invalid samples: {prefix}/{method}")
                close(statistics.median(samples), result["median_ms"], prefix + "/" + method)
                close(percentile95(samples), result["p95_ms"], prefix + "/" + method + "/p95")
                checked_samples += len(samples)
            pooled = case["gpu_pooled_end_to_end"]["median_ms"]
            close(case["gpu_fresh_buffers_end_to_end"]["median_ms"] / pooled,
                  case["pooling_speedup"], prefix + "/pooling")
            close(case["cpu"]["median_ms"] / pooled,
                  case["gpu_vs_cpu_end_to_end_speedup"], prefix + "/cpu-ratio")
    baseline = json.loads((ROOT / "data/hp15-baseline.json").read_text())
    source_hash = hashlib.sha256((ROOT / "reproduce/hp15-benchmark-tested.py").read_bytes()).hexdigest()
    require(source_hash == baseline["source_sha256"], "Baseline source hash mismatch")

    with (ROOT / "data/expert-routing.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) == 4, "Routing dataset must preserve all four scenarios")
    by_name = {row["scenario"]: row for row in rows}
    reference = float(by_name["reference_tokenwise"]["median_ms"])
    for row in rows:
        close(reference / float(row["median_ms"]), float(row["speedup_vs_reference"]), row["scenario"])
    cached = by_name["expert_grouped_cached_topology"]
    result = {
        "status": "PASS",
        "hashes_checked": len(manifest["published_files"]),
        "hp15_timing_samples_checked": checked_samples,
        "baseline_source_hash_matches": True,
        "routing_scenarios_checked": len(rows),
        "cached_topology_rate_increase_percent": (float(cached["speedup_vs_reference"]) - 1) * 100,
        "cached_topology_latency_reduction_percent": (1 - float(cached["median_ms"]) / reference) * 100,
        "scope": "Recorded data integrity and arithmetic; no new hardware or MAR simulation run."
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
