# Security Policy

`agent-skills-curated` handles third-party Skill content and release metadata. Treat every unapproved Skill candidate as untrusted review material, not executable runtime content.

## Supported versions

The default branch and explicitly pinned release manifests are supported. A
Skill is not supported merely because it appears in source, intake, draft,
audit, or candidate-review material.

## Reporting security issues

If you find a malicious Skill, unsafe instruction, license/provenance issue, leaked material, unsafe executable surface, prompt-injection risk, or supply-chain concern:

1. Prefer a private GitHub Security Advisory when available.
2. If private advisories are unavailable, open a minimal issue without exploit payloads, secrets, or copied restricted material.
3. Do not paste tokens, private memory, proprietary Skill bodies, leaked prompts, or private account data into public issues.

Please include:

- affected source, Skill, registry entry, manifest path, or generated projection;
- whether the issue is security, license, provenance, privacy, portability, overlap, or runtime-boundary related;
- safe reproduction steps or evidence references;
- whether downstream consumers may already have installed the affected release.

## Runtime safety boundary

This repository does not install Skills or write to live Agent environments. Downstream consumers must verify pinned releases before installation and must not execute candidate Skills that have not been approved and released.

## Non-goals

This repository does not certify that any third-party Skill is universally safe, legally sufficient for every jurisdiction, or suitable for every Agent. It provides governed review evidence, deterministic manifests, and portable release artifacts under explicit boundaries.
