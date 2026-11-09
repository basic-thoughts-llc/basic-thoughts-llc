# Verification record

**Compute evidence:** [Results and datasets](RESULTS.md) · [Reproduction instructions](reproduce/README.md). The revision-2 checker verifies six published source/data hashes, 360 HP15 timing samples, and all four routing-scenario ratios. The exact baseline benchmark source matches its recorded SHA-256.

**Checked September 14, 2026.** This page reports bounded checks of the private working materials behind the public project descriptions.

## Monument Notes

Command: `python -m pytest -q`, run from the application directory using its existing test environment.

**Result: 7 tests passed; exit status 0.** The test run emitted two dependency deprecation warnings.

| Test area | Behavior checked |
| :--- | :--- |
| Create and search | A created note is searchable and is associated with an internal department. Selected internal keys are absent from the tested consumer responses. |
| Ingestion | A sample credential pattern is redacted. |
| Live Mode | The API accepts example markup as note data and returns the Live Mode flag. |
| Vault configuration | Creating a private note without a vault key returns HTTP 503. |
| Vault storage | A private-note body is encrypted in SQLite, omitted from the full-text index, and not returned by the tested search. |
| Classification | Title weighting and the default notebook pass their two examples. |

**Test coverage:** the seven September 14 checks cover the operations listed above. Security, deployment, capacity and broader application behavior are evaluated in their own source and execution records; no system-wide conclusion follows from this subset.

## OMEGA Recovery Library

Command: `python3 verify_library.py`, run against the local master library.

**Result: 7,119 files matched the SHA-256 manifest; exit status 0.**

This check establishes byte agreement with the specified local manifest. Source provenance, implementation behavior, authorship and intellectual-property records are maintained as distinct evidence categories.

## MAR public edition

The [research brief](research/mar/PUBLIC-BRIEF.md), [presentation](research/mar/PUBLIC-PRESENTATION.md), and [source register](research/mar/evidence-register.json) retain the September 11, 2026 edition and its source qualifications. They are reproduced from the previously prepared public package.

The September 11 research-publication checks concern those public artifacts. Other MAR results and host/device validations must be assessed from their own source records; this selected public review does not assess all OMEGA or MAR capabilities.

## Review access

Selected implementation materials and recovery records are private. This page reports the identified checks and their source context; [request an authorized technical review](https://github.com/basic-thoughts-llc/basic-thoughts-llc/issues/new?template=project-inquiry.yml). [Ask about technical review](https://github.com/basic-thoughts-llc/basic-thoughts-llc/issues/new?template=project-inquiry.yml).
