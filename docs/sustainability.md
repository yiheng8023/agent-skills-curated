# Sustainability

`agent-skills-curated` should remain a lightweight governance repository, not a high-cost platform. The goal is to make reviewed Skills portable, auditable, and safe enough for downstream consumers without turning every candidate into a heavy process.

## Cost posture

Current expected costs are intentionally small:

- GitHub Free is sufficient for the current private/public-readiness path.
- Public validation workloads should stay compatible with standard GitHub Actions.
- GitHub Team or Pro is not required now; consider it only when private Actions minutes, organization governance, or multi-maintainer review requirements exceed the free tier.
- Hosted services, paid scanning, or paid LLM review are optional future additions, not prerequisites for governance.

## Funding model

Acceptable future funding paths:

- individual sponsorship for maintenance and review time;
- transparent donations to cover AI collaboration and validation costs;
- paid private review or adaptation work;
- supporter reports on reviewed Skill ecosystem coverage.

Funding must not buy approval. A paid request may fund review effort, but it cannot bypass source pinning, license, provenance, security, portability, overlap, neutralization, validation, or release gates.

## Free-first discipline

The repository should prefer:

- deterministic manifests over live install automation;
- small review batches over bulk imports;
- links and evidence over copied third-party content when redistribution is unclear;
- reference or adapter-only outcomes over unnecessary vendoring;
- explicit human approval before runtime release.

## Public readiness note

This repository may be opened later, but public release requires a separate owner decision on visibility, license, private-overlay removal, third-party redistribution boundaries, and funding links.
