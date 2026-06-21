# Security Review: addyosmani/agent-skills

## Scope

- Repository-wide review of commit `17214a29c429a19f7a9607f2c06f9d650ea87eb0`.
- Reviewed all 24 Skill directories and deeply reviewed instruction, Hook,
  script, command, CI, manifest, persona, setup, and orchestration surfaces.
- Threat model was generated for this scan; it was not an external input.
- Validation used complete-file static tracing. Risky Hooks, network requests,
  plugin installation, and destructive Git examples were not executed.

### Scan Summary

| Field | Value |
|---|---|
| Reportable findings | 5 |
| Severity mix | 3 medium, 2 low |
| Confidence mix | medium to high |
| Runtime set impact | all affected Hook/CI/Git surfaces excluded |
| Upstream structural checks | 24 Skills and 8 commands passed upstream validators |

## Threat Model

Installed Skill text is a behavioral supply-chain surface: it can influence an
Agent that already has filesystem, Shell, Git, browser, MCP, network, account,
or deployment authority. Project files, external URLs, tool output, plans, and
caches are untrusted data. One environment must have one canonical router, and
all install, write, secret, account, commit, push, release, deploy, delete,
migration, and rollback actions retain environment-level authorization.

Primary boundaries are upstream GitHub to curation, curated instructions to
Agent context, instruction to tool execution, project data to Hooks, external
URLs to local network/cache, core to agent adapters, and CI/install sources to
the runtime distribution channel.

## Findings

| Severity | Finding |
|---|---|
| medium | [Project cache can control simplify-ignore restore destinations](#1-project-cache-can-control-simplify-ignore-restore-destinations) |
| medium | [CI executes an unversioned npm package after checkout](#2-ci-executes-an-unversioned-npm-package-after-checkout) |
| medium | [CI Actions use mutable major-version tags](#3-ci-actions-use-mutable-major-version-tags) |
| low | [Post-fetch cache Hook performs an unrestricted redirecting request](#4-post-fetch-cache-hook-performs-an-unrestricted-redirecting-request) |
| low | [Project cache content can impersonate revalidated documentation](#5-project-cache-content-can-impersonate-revalidated-documentation) |

### Confidence Scale

| Label | Meaning |
|---|---|
| high | Direct source and control evidence; no material code-path gap. |
| medium | Direct source evidence with deployment or runtime assumptions. |
| low | Weak or incomplete evidence retained only for follow-up. |

### [1] Project cache can control simplify-ignore restore destinations

| Field | Value |
|---|---|
| Severity | medium |
| Confidence | medium-high |
| Confidence rationale | Project-controlled path and backup bytes directly reach file writes; a trusted global/plugin deployment of the Hook is the remaining deployment precondition. |
| Category | Arbitrary file write |
| CWE | CWE-22, CWE-73 |
| Affected lines | `hooks/simplify-ignore.sh:145-161`, `hooks/simplify-ignore.sh:287-297` |

#### Summary

The Stop and post-tool paths trust `.path`, `.bak`, and related files under a
project-controlled cache. They do not canonicalize the target, enforce project
containment, reject links, or authenticate cache state before overwriting or
creating a current-user-writable path.

#### Validation

Complete-file code tracing confirmed attacker-controlled path and content reach
the write sinks. The Hook is optional; severity assumes a trusted installed
Hook processes an untrusted project cache.

#### Dataflow

Project cache `.path/.bak` → cache iteration → target path read → `cat > target`
or recovered-file move.

#### Reachability

An untrusted project can prepopulate cache data. A configured Stop Hook runs as
the developer and can write anywhere that identity can write.

#### Severity

Medium: impact can be high, but reachability depends on optional Hook enablement
and a trusted-script deployment mode. Proof that the only supported mode runs a
project-owned script would lower reportability because the project already has
equivalent code execution.

#### Remediation

Do not import the Hook. A redesign must operate on temporary copies, enforce
realpath containment, reject symlinks/reparse points, authenticate cache state,
use transactional recovery, and test crash behavior.

### [2] CI executes an unversioned npm package after checkout

| Field | Value |
|---|---|
| Severity | medium |
| Confidence | medium-high |
| Confidence rationale | The workflow installs and executes a registry-selected latest package; token permissions determine maximum impact. |
| Category | CI supply-chain integrity |
| CWE | CWE-829, CWE-1104 |
| Affected lines | `.github/workflows/test-plugin-install.yml:42-45`, `.github/workflows/test-plugin-install.yml:55-58` |

#### Summary

Two jobs install the latest `@anthropic-ai/claude-code` globally after checkout,
without a version, lock, integrity value, minimal workflow permission, or
disabled checkout credential persistence.

#### Validation

Static workflow tracing confirms registry content executes in the checked-out
runner. Repository token authority is external to the file and remains the main
impact-calibration gap.

#### Dataflow

npm latest resolution → package install/lifecycle → installed CLI execution →
CI validation and plugin installation.

#### Reachability

A compromised package publisher or malicious latest release reaches every
matching workflow run.

#### Severity

Medium: CI result integrity is directly exposed; repository mutation is
conditional on effective token policy. Read-only token proof would narrow, but
not remove, the validation-integrity risk.

#### Remediation

Pin an exact reviewed version and integrity, set `permissions: contents: read`,
disable persisted checkout credentials, and separate untrusted package
execution from write-capable release jobs.

### [3] CI Actions use mutable major-version tags

| Field | Value |
|---|---|
| Severity | medium |
| Confidence | medium |
| Confidence rationale | Mutable tags execute in the runner; compromise of GitHub-owned first-party Actions is a high-friction prerequisite. |
| Category | CI supply-chain integrity |
| CWE | CWE-829, CWE-1104 |
| Affected lines | `.github/workflows/test-plugin-install.yml:13`, `.github/workflows/test-plugin-install.yml:16`, `.github/workflows/test-plugin-install.yml:27`, `.github/workflows/test-plugin-install.yml:30`, `.github/workflows/test-plugin-install.yml:42`, `.github/workflows/test-plugin-install.yml:55` |

#### Summary

Checkout and Node setup Actions are referenced by movable major tags rather
than full immutable commit SHAs.

#### Validation

The executable dependency boundary is direct. GitHub ownership reduces
likelihood but does not make the source immutable or reproducible.

#### Dataflow

Mutable Action tag → resolved Action code → checked-out CI runner → validation
and credential context.

#### Reachability

Requires upstream official Action distribution compromise followed by a push,
pull request, or manual workflow run.

#### Severity

Medium under a curated supply-chain standard. Exact repository token policy and
resolved SHAs would refine likelihood and write impact.

#### Remediation

Pin full Action SHAs, declare minimal permissions, disable credential
persistence where unnecessary, and update pins through controlled automation.

### [4] Post-fetch cache Hook performs an unrestricted redirecting request

| Field | Value |
|---|---|
| Severity | low |
| Confidence | high |
| Confidence rationale | Tool URL reaches an independent `curl -L`; concrete internal-service impact and Hook network policy are not known. |
| Category | Server-side request forgery primitive |
| CWE | CWE-918 |
| Affected lines | `hooks/sdd-cache-post.sh:79-82` |

#### Summary

The optional post-fetch Hook repeats a WebFetch URL through unrestricted local
`curl -L`, without scheme, host, IP, port, private-network, metadata, or
per-redirect checks.

#### Validation

Static source-to-sink tracing is complete. HEAD and a five-second timeout limit
data extraction but do not constrain destinations.

#### Dataflow

WebFetch tool URL → post Hook JSON extraction → `curl -sI -L` → local/LAN
network destination.

#### Reachability

Requires explicit Hook enablement and a WebFetch result with extractable body.
The request uses the developer workstation's network position.

#### Severity

Low because there is no demonstrated sensitive internal target, response-body
read, or public service entry point. A proven metadata or privileged internal
endpoint would raise severity.

#### Remediation

Do not import the Hook. If redesigned, use the platform-controlled fetch path,
allowlisted HTTPS destinations, IP-range rejection, and per-hop redirect
validation.

### [5] Project cache content can impersonate revalidated documentation

| Field | Value |
|---|---|
| Severity | low |
| Confidence | medium-high |
| Confidence rationale | Cache content is not bound to the URL or validator; downstream Agent trust and tool action remain host-dependent. |
| Category | Content integrity / prompt-cache poisoning |
| CWE | CWE-345, CWE-353 |
| Affected lines | `hooks/sdd-cache-pre.sh:50-83`, `hooks/sdd-cache-pre.sh:91-105` |

#### Summary

An HTTP 304 validates server state, not the integrity of project-local cached
content. A project can replace `.content` while retaining a validator and have
that content returned as revalidated documentation.

#### Validation

Code tracing confirms no content hash, signature, MAC, or cache provenance
binding. Result delimiters reduce instruction ambiguity but do not prove source
identity.

#### Dataflow

Project cache JSON → URL hash lookup → HTTP 304 → local `.content` → Agent tool
result channel.

#### Reachability

Requires the optional pre Hook, a cache entry, and a URL that returns 304. An
attacker-controlled source can satisfy the validator precondition reliably.

#### Severity

Low: the project can already influence Agent context, while this defect adds a
false external-source identity. Demonstrated higher prompt priority or approval
bypass would raise severity.

#### Remediation

Do not import prompt-shaped URL-only caching. Bind canonical URL, prompt,
source revision, validators, and content hash; mark cached content as untrusted.

## Reviewed Surfaces

| Surface | Risk Area | Outcome | Notes |
|---|---|---|---|
| 24 Skills | prompt supply chain, overlap | Reviewed | only five non-overlapping Skills adopted after adaptation |
| SessionStart Hook | project fallback, competing router | Needs follow-up | excluded; abnormal-install reachability not proven |
| SDD cache Hooks | SSRF, integrity, sensitive cache | Reported | excluded from curated runtime |
| simplify-ignore Hook | arbitrary write, crash recovery | Reported | excluded from curated runtime |
| Git workflow Skill | destructive reset, secret output | Rejected | unsafe but developer-only under final security policy; excluded |
| build/ship commands | broad authorization, persona provenance, cost | Rejected | governance defects; not adopted |
| validators | false-positive acceptance | Rejected | upstream validators retained only as evidence, not reused |
| CI and manifests | mutable dependencies and sources | Reported | upstream files are not copied into curated CI |
| personas and adapters | trust and semantic drift | Reviewed | not installed in initial release |

## Open Questions And Follow Up

- Verify Claude plugin behavior when the packaged SessionStart script is
  missing but Hook configuration remains loadable.
- Verify same-name project persona resolution and tool inheritance in a
  disposable Claude environment before considering any persona adapter.
- Re-evaluate only if future intake proposes importing an executable or Hook;
  the approved initial runtime contains no upstream executable.
