# Reproduce the result checks

[Results](../RESULTS.md) · [Source register](../data/provenance.json)

## Verify the published records

From the root of this repository, run:

```bash
python3 reproduce/verify_results.py
```

Python's standard library is sufficient. The checker verifies file hashes, recomputes the median and 95th percentile of every included HP15 timing series, checks the CPU and buffer-reuse ratios, matches the baseline to its exact benchmark-source hash, and recomputes the expert-routing speedup ratios.

Expected output is JSON with `status: PASS`. A failed check exits with an error. These checks validate the published records; they do not regenerate the original hardware measurements.

## Rerun the HP15 workload on compatible hardware

The preserved [benchmark source](hp15-benchmark-tested.py) uses NumPy and PyOpenCL. It requires a hardware GPU with a working OpenCL driver and chooses the first GPU device it finds. It measures three input sizes, including allocation, transfer, dispatch, and kernel timing paths. Your results will depend on the device, driver, and environment.

In a fresh directory, create a Python virtual environment, install `numpy` and `pyopencl`, then run the copied script with `--label baseline`. A working system OpenCL driver is also required. Preserve the printed device identity and generated JSON alongside your environment details.

The historical script writes relative to its own location. Run a copy to preserve the published evidence:

```bash
mkdir -p hp15-rerun/scripts
cp reproduce/hp15-benchmark-tested.py hp15-rerun/scripts/benchmark.py
python3 -m venv hp15-rerun/venv
hp15-rerun/venv/bin/python -m pip install numpy pyopencl
hp15-rerun/venv/bin/python hp15-rerun/scripts/benchmark.py --label baseline
```

The output is `hp15-rerun/evidence/benchmark-baseline.json`. The historical source is retained byte-for-byte to match the baseline receipt. This hardware rerun has not been executed as part of the public-profile revision.

## Other result families

- `expert-routing.csv` preserves the recovered scenario summaries. Raw per-repetition timing samples and the corresponding complete proxy harness are not included in this edition.
- `numa-scenarios.csv` contains modeled placement/controller scenarios, labeled in its `truth_state` column.
- `mar-reported-comparison.csv` is a transcription of the detailed run in the architecture paper. It is not a recovered original simulation-results file.

## Regenerate the figure

With Matplotlib installed in a Python environment, run `python3 reproduce/plot_results.py` from the repository root. The figure reads the published routing CSV and HP15 baseline JSON directly and writes PNG and PDF copies to `assets/`. This edition used Matplotlib 3.11.2.
