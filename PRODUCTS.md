# Product catalog · purpose, evidence, and maturity

[Overview](README.md) · [Results](RESULTS.md) · [For employers](FOR-EMPLOYERS.md) · [Architecture](ARCHITECTURE.md)

Basic Thoughts LLC · Benjamin Thomas Murphy

OMEGA is the umbrella architecture. The products and research lines below retain
their own responsibilities. This is a product map, not a claim that every listed
system is deployed. A recorded local test is not a production certification.

## Products with implementation or bounded execution evidence

| Product or component | What it does | Engineering work it makes inspectable | Evidence and boundary |
| :--- | :--- | :--- | :--- |
| **Monument Notes** | Notes, ingestion, search and archive workflows with consumer and operator surfaces. | Python/FastAPI, SQLite full-text search, encrypted private-note bodies when configured. | [Implementation and seven-test record](PROJECTS.md#monument-notes); not a current hosted-service claim. |
| **Factory / LISA** | Coordinates the operating environment and presents system state to an operator. | Service orchestration, isolated runtime preparation, API identity checks and supervised shutdown. | [Local core integration receipt](data/factory-core-verification.json) records offline preparation, LISA/Sentinel/portal startup and shutdown. Simulation surfaces are not native compute. |
| **Sentinel NEO** | Proxy-side observation, detectors and audit telemetry. | Observable service behavior and ledger verification. | [Local integration receipt](data/factory-core-verification.json); distinct from a comprehensive independent host observer. |
| **Saturn address resolver** | Provides receive-only addressing and analysis functions for the Saturn line. | Packaged Python resolver and testable addressing logic. | Resolver implementation is staged in the Factory collection. Resolving an address does not execute Saturn compute. |
| **Distributed-agent fleet tooling** | Prepares authenticated package transfer and bounded remote jobs across configured nodes. | SSH boundaries, package hashes, dry-run planning and explicit job profiles. | Local implementation and tests exist; live multi-node acceptance requires enrollment and actual agent engines. |
| **Recovery and evidence library** | Preserves distributed source artifacts with searchable provenance and file-level integrity records. | Artifact recovery, indexing, repeatable integrity checking. | [Historical 7,119-file manifest check](VERIFICATION.md); an artifact count is not a product or performance count. |

## Distinct architecture and research lines

| Line | Intended role | Available work and open boundary |
| :--- | :--- | :--- |
| **MAR** | Twin-core programmable-substrate architecture with ordered transitions before compute. | Architecture papers, adapters and [reported classical-control comparison](RESULTS.md#mar-sequence). Native substrate execution and physical validation are separate, unresolved requirements. |
| **OmegaCQ / Saturn compute** | Compute architecture and its context-bound handshake. | Recovered addressing, authentication, routing and bridge candidates. No claim of verified native compute execution; handshake acknowledgement is not execution. |
| **PAION / RIMAC** | Agent routing, transport and compute integration. | Recovered source and architecture; authoritative runtime interfaces and end-to-end integration still need acceptance. |
| **Omega X** | Acquisition, intake and retrieval-augmented knowledge workflows. | [Source and architecture records](PROJECTS.md#paion--rimac-omega-x-and-factory-orchestration); current deployment unverified. |
| **BTOL** | Governed state transitions, identity, policy and execution continuity. | [Governance specification and source lineage](ARCHITECTURE.md#btol-and-lisa); specification is distinct from enforcement coverage. |
| **OMEA / OAIE / BORG** | Operating and application-layer architecture. | Recovered architecture/source lineage; integrated runtime entry points unresolved. |
| **Lilly / Zero Touch** | Node provisioning and environment setup. | Historical provisioning sources; disk selection and operator enrollment remain explicit deployment decisions. |
| **WRA / HUD telemetry** | Device-facing state and telemetry interfaces. | Dashboard sources; actual device-feed integration requires verification. |
| **Finance and parts tooling** | Finance-department and parts-acquisition workflows. | Source bundles retained; no live trading, financial returns or production execution claimed. |
| **Factory departments** | Specialized departmental services across the architecture. | 37 lane definitions: 16 core and 21 departmental. Definitions are not 37 completed services. |

## Audit platforms stay distinct

| Name | Role in this portfolio | Boundary |
| :--- | :--- | :--- |
| **Veritas Aquanias** | Operator-defined audit platform, separate from OMEGA and MAR. | Named architecture line; this edition does not establish its full implementation or deployment. |
| **BTO Provider Accountability** | Scope, claims and execution-receipt review workflow. | A loaded reporting skill is not continuous host monitoring. |
| **AVL Watchtower** | Intended independent host process/network observer. | Full observer package and runtime are not verified by this portfolio. It is not relabeled Sentinel. |

## How to read the evidence

**Recorded execution:** a bounded workload or local integration run has a receipt.
**Source available:** code exists but the corresponding deployment is not established.
**Architecture/research:** design or model evidence exists; runtime and physical
claims require their own tests. **Integration pending:** a necessary interface,
backend, hardware configuration or end-to-end test remains open.

The catalog combines the existing [architecture record](ARCHITECTURE.md),
[source provenance](data/provenance.json) and a September 16 Factory staging
component inventory. That inventory describes a recovery/staging release, not
an operational fleet. Public benchmark files retain their original provenance.
