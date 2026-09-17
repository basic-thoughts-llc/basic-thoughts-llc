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

These tests do not validate browser sandboxing, the full authentication boundary, production deployment, load capacity, or every possible credential format. Titles remain plaintext metadata. No independent security certification is claimed.

## OMEGA Recovery Library

Command: `python3 verify_library.py`, run against the local master library.

**Result: 7,119 files matched the SHA-256 manifest; exit status 0.**

The check demonstrates byte agreement with the local manifest. It does not establish scientific validity, authorship, legal ownership, or that every recovered source file executes correctly.

## MAR public edition

The [research brief](research/mar/PUBLIC-BRIEF.md), [presentation](research/mar/PUBLIC-PRESENTATION.md), and [source register](research/mar/evidence-register.json) retain the September 11, 2026 edition and its source qualifications. They are reproduced from the previously prepared public package.

No MAR experiment was rerun for this profile. Software checks elsewhere on this page do not validate the proposed physical substrate or demonstrate a performance advantage.

## Review access

Implementation code and underlying recovery records remain private. These are maintainer-reported checks; public readers cannot reproduce the private-code runs from this profile alone. [Ask about technical review](https://github.com/basic-thoughts-llc/basic-thoughts-llc/issues/new?template=project-inquiry.yml).
