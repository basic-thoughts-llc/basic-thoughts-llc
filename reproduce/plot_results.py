"""Render the public figure directly from the published datasets (Matplotlib)."""
from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
with (root / "data/expert-routing.csv").open(encoding="utf-8-sig") as handle:
    routing = list(csv.DictReader(handle))
device = json.loads((root / "data/hp15-baseline.json").read_text())
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1.25, 1]})
fig.patch.set_facecolor("#f7f8fa")
for axis in (a, b):
    axis.set_facecolor("#f7f8fa")
    axis.spines["left"].set_visible(False)
    axis.spines["bottom"].set_color("#b9c3cc")
    axis.tick_params(axis="y", length=0)
    axis.set_axisbelow(True)
    axis.grid(axis="x", color="#dce1e6", linewidth=.65)
labels = ["Tokenwise reference", "Grouped · same math", "Grouped · cached topology", "Half-lane drop"]
values = [float(row["median_ms"]) for row in routing]
a.barh(labels, values, color=["#647588", "#497790", "#167569", "#b18165"], height=.52)
a.invert_yaxis()
for i, value in enumerate(values):
    a.text(value + .035, i, f"{value:.3f} ms", va="center", fontsize=10)
a.set_xlim(0, 2.16)
a.set_title("Expert-routing proxy", loc="left", fontweight="bold", pad=28)
a.text(0, 1.035, "Recorded median latency · lower is faster", transform=a.transAxes, fontsize=10, color="#54616d")
a.set_xlabel("Latency (ms)")
gains = [case["pooling_speedup"] for case in device["cases"]]
sizes = [f"{case['elements']:,} elements" for case in device["cases"]]
b.barh(sizes, gains, color="#497790", height=.52)
b.invert_yaxis()
for i, value in enumerate(gains):
    b.text(value + .055, i, f"{value:.3f}×", va="center", fontweight="bold", fontsize=10)
b.set_xlim(0, 3.12)
b.axvline(1, color="#71808e", linestyle="--", linewidth=1)
b.set_title("HP15 · GPU buffer reuse", loc="left", fontweight="bold", pad=28)
b.text(0, 1.035, "Fresh-buffer / pooled latency · baseline run", transform=b.transAxes, fontsize=10, color="#54616d")
b.set_xlabel("Relative GPU execution rate (×)")
fig.suptitle("BASIC THOUGHTS  /  ENGINEERING RECORD", x=.03, ha="left", fontsize=13, fontweight="bold", color="#172d42")
fig.text(.03, .025, "Separate workloads and baselines. Source: data/expert-routing.csv and data/hp15-baseline.json.\nHP15 ratios compare two GPU allocation paths; CPU comparisons and output fidelity are provided in RESULTS.md.", fontsize=9, color="#54616d")
fig.subplots_adjust(left=.21, right=.96, top=.79, bottom=.22, wspace=.92)
fig.savefig(root / "assets/engineering-results.png", dpi=180)
fig.savefig(root / "assets/engineering-results.pdf")
print("Rendered engineering-results.png and engineering-results.pdf from published data.")
