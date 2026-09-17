# For employers and technical collaborators

[Overview](README.md) · [Products](PRODUCTS.md) · [Results](RESULTS.md)

**Benjamin Thomas Murphy · Basic Thoughts LLC**

This portfolio is organized around inspectable engineering work. It does not
claim employment history, credentials, customer deployments or production scale
that are not documented here. Projects span implemented software, measured
experiments and architecture still in development.

## Match the discussion to the evidence

| Engineering area | Relevant artifacts | Useful technical discussion |
| :--- | :--- | :--- |
| Backend applications | Monument Notes: FastAPI, SQLite, search and private-note encryption | API/storage boundaries, failure handling, tests and deployment requirements. |
| Systems integration | Factory/LISA, Sentinel and the local core verification receipt | Offline dependencies, supervision, observability, shutdown and target acceptance. |
| Performance analysis | HP15 CPU/OpenCL source and timing samples; expert-routing CSV | Baselines, allocation overhead, medians, output fidelity and limits of generalization. |
| AI orchestration | PAION/RIMAC, Omega X and fleet tooling | Routing, retrieval, explicit interfaces and the gap between architecture and deployed behavior. |
| Research engineering | MAR sequence comparison and NUMA placement scenarios | Measured versus reported versus modeled results, reproducing a method, and missing validation. |
| Evidence tooling | Recovery manifests, provenance and receipt workflows | Integrity, traceability and why file hashes do not establish functional correctness. |

## A ten-minute review

1. Scan the [catalog](PRODUCTS.md) to identify the relevant product and maturity.
2. Inspect the [results chart and tables](RESULTS.md), including unfavorable comparison rows.
3. Open the raw data and exact benchmark source linked beside the result.
4. Run the calculation checker below. It uses Python's standard library and does
   not install dependencies, invoke the GPU benchmark or start services.
5. Choose one artifact for a deeper code or architecture walkthrough. Main
   implementation sources remain private and require a separate authorized share.

```bash
python3 reproduce/verify_results.py
```

This checks published source/data hashes, 360 recorded timing samples across
two HP15 runs, summary statistics and all four expert-routing scenarios.
It does not independently rerun the hardware experiment or verify the MAR model.

## Results worth discussing

- Cached-topology routing records **1.128× reference execution rate** at cosine
  similarity **1.0**, for the specific recovered proxy—not full-model throughput.
- GPU buffer reuse records **1.97×–2.52×** improvement relative to fresh GPU
  buffers. CPU latency remains lower at the tested input sizes.
- The reported MAR control comparison separates sequence-gate fidelity
  (**1.000 vs 0.375**) despite similar final order. Original traces were not
  recovered; this remains a reported classical-model result.

## Authorship and evaluation

Basic Thoughts LLC and Benjamin Thomas Murphy identify the first-party product
work. Upstream libraries and third-party components retain their own authorship
and licenses. This profile does not imply exclusive manual authorship of every
line or conceal the distinction between original product design, recovered
artifacts, dependencies and AI-assisted implementation workflows.

For a technical interview or collaboration discussion, select a product and its
linked evidence first; evaluate the actual implementation and method rather than
inferring production readiness from presentation polish.
