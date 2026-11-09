# Systems and engineering artifacts

[Overview](README.md) · [Architecture](ARCHITECTURE.md) · [Results and datasets](RESULTS.md)

## MAR and compute engineering

The deliverables contain a twin-core architecture paper and evidence deck, an expert-routing dataset, NUMA placement scenarios, historical device execution records, and a staged-control comparison. The HP15 branch adds CPU/OpenCL benchmark code, raw timing samples, charts, a notebook, and reports.

Start with the [results register](RESULTS.md): it brings the quantitative work together and keeps each workload attached to its own baseline and method.

## PAION / RIMAC, acquisition and Factory orchestration

Recovered architecture records describe agent routing, acquisition, RAG intake, and their interfaces with the operating environment. The collection includes PAION server and router material, BORG architecture records, and acquisition and department-fleet deliverables. Their role is system coordination and knowledge flow.

**Evidence available:** architecture documents, implementation source and operational records. Host-specific runtime verification is documented by its corresponding Factory execution receipts.

## BTOL, LISA, and observability

BTOL defines governed execution and state continuity. LISA supplies the operator view. The source collection contains React/TypeScript dashboards, heartbeat and handshake services, state and topology engines, and access-governance specifications.

**Evidence available:** source code and specifications. These identify concrete components and the intended architecture; the current deployment state is tracked separately from source availability.

## Monument Notes

Monument's version 0.1.0 implementation serves separate consumer and operator FastAPI applications over SQLite storage. It supports note creation, notebook suggestions, full-text search, text ingestion, and encrypted private-note bodies when a vault key is configured.

**Verification:** seven existing automated tests passed in the September 14 local run. [Read their scope](VERIFICATION.md). The source archive includes deployment templates and execution records.

## Recovery and evidence infrastructure

OMEGA's recovery workflow collects distributed project artifacts into a searchable local library and records file-level hashes and source dispositions. The September 14 local verification confirmed **7,119 files** against its manifest.

This supports continuity and inspection across the ecosystem. Recovery counts measure preserved artifacts, while benchmark results measure their named workloads.

## Technical access

The public profile includes selected datasets, calculation checks, benchmark source, and research summaries. The main implementation archive remains private. [Open a technical or commercial inquiry](https://github.com/basic-thoughts-llc/basic-thoughts-llc/issues/new?template=project-inquiry.yml) to discuss the relevant system and evaluation scope.
