# Selected systems · public product and architecture map

[Overview](README.md) · [Results](RESULTS.md) · [For employers](FOR-EMPLOYERS.md) · [Architecture](ARCHITECTURE.md)

Basic Thoughts LLC · Benjamin Thomas Murphy

OMEGA is the umbrella architecture. The systems and research lines below retain their own responsibilities. This is a **selected public map**, not the complete Basic Thoughts product/tool/skill/connector catalog. Source links describe the named component or workload; they do not set a ceiling on the wider OMEGA estate.

## Products with implementation or bounded execution evidence

| Product or component | What it does | Engineering work it makes inspectable | Evidence and boundary |
| :--- | :--- | :--- | :--- |
| **Monument Notes** | Notes, ingestion, search and archive workflows with consumer and operator surfaces. | Python/FastAPI, SQLite full-text search, encrypted private-note bodies when configured. | [Implementation and seven-test record](PROJECTS.md#monument-notes); the linked record covers that application version and test context. |
| **Factory / LISA** | Coordinates the operating environment and presents system state to an operator. | Service orchestration, isolated runtime preparation, API identity checks and supervised shutdown. | [Local core integration receipt](data/factory-core-verification.json) documents the named preparation, LISA/Sentinel/portal startup, and lifecycle checks in that local run. |
| **Sentinel NEO** | Proxy-side observation, detectors and audit telemetry. | Observable service behavior and ledger verification. | [Local integration receipt](data/factory-core-verification.json) for the named detector/ledger workflow; additional observability components have their own source lineage. |
| **Saturn address resolver** | Provides receive-only addressing and analysis functions for the Saturn line. | Packaged Python resolver and testable addressing logic. | Resolver implementation and integration artifacts are maintained in the Factory collection; Saturn compute is a distinct architectural component. |
| **Distributed-agent fleet tooling** | Prepares authenticated package transfer and bounded remote jobs across configured nodes. | SSH boundaries, package hashes, dry-run planning and explicit job profiles. | Implementation and tests are documented; deployment and multi-node acceptance are evaluated by their corresponding node receipts. |
| **Recovery and evidence library** | Preserves distributed source artifacts with searchable provenance and file-level integrity records. | Artifact recovery, indexing, repeatable integrity checking. | [Historical 7,119-file integrity check](VERIFICATION.md), which covers the documented recovery-library workload. |

## Distinct architecture and research lines

| Line | Intended role | Available work and open boundary |
| :--- | :--- | :--- |
| **MAR** | Twin-core programmable-substrate architecture with ordered transitions before compute. | Architecture and implementation records, adapters and a [staged-control comparison](RESULTS.md#mar-sequence); each source describes its respective execution context. |
| **OmegaCQ / Saturn compute** | Compute architecture and its context-bound handshake. | Addressing, bilateral authentication, routing and bridge implementation lineages; the named handshake experiment and native compute workloads are separate evidence categories. |
| **PAION / RIMAC** | Agent routing, transport and compute integration. | Recovered source and architecture; authoritative runtime interfaces and end-to-end integration still need acceptance. |
| **BTOL** | Governed state transitions, identity, policy and execution continuity. | [Governance specification and source lineage](ARCHITECTURE.md#btol-and-lisa) covering identity, access tiers, policy evaluation and execution continuity. |
| **OMEA / OAIE / BORG** | Operating and application-layer architecture. | Architecture and implementation source lineage; service-specific integration details reside in their respective runtime records. |
| **Lilly / Zero Touch** | Node provisioning and environment setup. | Provisioning sources, node initialization logic and operator-directed enrollment design. |
| **WRA / HUD telemetry** | Device-facing state and telemetry interfaces. | HUD and dashboard sources, telemetry identity and device-facing interfaces. |
| **Finance and parts tooling** | Finance-department and parts-acquisition workflows. | Finance-department and parts-workflow source bundles; each workflow has a distinct deployment and evidence record. |
| **Factory departments** | Specialized departmental services across the architecture. | Historical source documents describe 16 core and 21 departmental lane definitions. The full current department/service total is subject to the whole-estate inventory. |

## Audit platforms stay distinct

| Name | Role in this portfolio | Boundary |
| :--- | :--- | :--- |
| **Liberty Maps / BTO VERITAS AEQUITAS lineage** | Operator-defined audit platform and source-preserving audit workflow, distinct from MAR and other OMEGA engines. | Audit architecture, full-chain evidence mapping, source lineage, and operator verification records. |
| **BTO Provider Accountability** | Scope, claims and execution-receipt review workflow. | Reporting and accountability workflows, including scope, claims and execution receipts. |
| **AVL Watchtower** | Intended independent host process/network observer. | Separate host process/network observation lineage with its own identity and evidence records, distinct from Sentinel. |

## How to read the evidence

**Evidence context:** each linked item documents a specific source, workload, model or execution receipt. **Portfolio scope:** this public selection is not a comprehensive audit of all S26, Factory, cloud, device, or commercial implementations. **Verification attribution:** keep operator-verified and independently reproduced results distinct; absent public evidence does not establish absent system functionality.

The catalog combines the existing [architecture record](ARCHITECTURE.md),
[source provenance](data/provenance.json) and a September 16 Factory staging
component inventory. This page preserves the historical inventory's provenance and directs evaluation to the actual implementation and execution records. Public benchmark files retain their original provenance.
