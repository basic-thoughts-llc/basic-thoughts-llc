# For employers and technical collaborators

[Overview](README.md) · [Products](PRODUCTS.md) · [Results](RESULTS.md)

**Benjamin Thomas Murphy · Basic Thoughts LLC**

This profile presents a curated selection of inspectable engineering work. Basic Thoughts LLC's full product, connector, application and device portfolio is broader than the public examples here. Each linked artifact retains its exact test context and authorship/source attribution.

## Match the discussion to the evidence

| Engineering area | Relevant artifacts | Useful technical discussion |
| :--- | :--- | :--- |
| Backend applications | Monument Notes: FastAPI, SQLite, search and private-note encryption | API/storage boundaries, failure handling, tests and deployment requirements. |
| Systems integration | Factory/LISA, Sentinel and the local core verification receipt | Offline dependencies, supervision, observability, shutdown and target acceptance. |
| Performance analysis | HP15 CPU/OpenCL source and timing samples; expert-routing CSV | Baselines, allocation overhead, medians, output fidelity and limits of generalization. |
| AI orchestration | PAION/RIMAC, Omega X and fleet tooling | Routing, retrieval, explicit interfaces and the gap between architecture and deployed behavior. |
| Research engineering | MAR sequence comparison and NUMA placement scenarios | Research design, measured workloads, reproducible methods and evidence traceability. |
| Evidence tooling | Recovery manifests, provenance and receipt workflows | Artifact integrity, traceability, provenance and runtime verification workflows. |

## A ten-minute review

1. Scan the [catalog](PRODUCTS.md) to identify the relevant product and maturity.
2. Inspect the [results chart and tables](RESULTS.md), using each named workload, host and baseline to understand its scope.
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
The checker validates published record consistency; the related experimental and architecture receipts have their own provenance.

## Results worth discussing

- Cached-topology routing records **1.128× reference execution rate** at cosine
  similarity **1.0** in its recorded routing workload.
- GPU buffer reuse records **1.97×–2.52×** improvement relative to fresh GPU buffers in three HP15 test cases.
- The reported MAR control comparison separates sequence-gate fidelity
  (**1.000 vs 0.375**) despite similar final order. Original traces were not
  published in the linked research record; it is a distinct staged-control comparison.

## Authorship and evaluation

Basic Thoughts LLC and Benjamin Thomas Murphy identify the first-party product and architectural work. Source provenance, historical versions, upstream dependencies, contributor credits and applicable licenses are tracked as separate records. This public selection does not determine ownership or completeness of the full private estate.

For a technical interview or collaboration discussion, select a product and its
linked evidence first; evaluate the actual implementation, delivery scope and method, with access to further materials subject to operator authorization.
