# Program Control Plan Completeness Audit

Date: 2026-07-15

Status: evidence audit for program-plan correction; not program authority,
release approval, candidate admission, runtime state, or permission to start a
new discovery round.

## Question

Does the current master control plan cover the agreed long-term purpose and
decision chain well enough that execution ordering can be trusted?

## Evidence Boundary

Current repository truth was taken from:

- `registry/curation-program-plan.json`;
- `registry/program-acceptance-map.json`;
- `registry/curation-expansion-rounds.json`;
- `registry/round-lifecycle-contract.json`;
- `registry/collaboration-domain-coverage.json`;
- `registry/github-skill-discovery-profile.json`;
- `docs/curation-program-plan.md`;
- `docs/curation-harness-model.md`;
- `docs/coverage-and-curation-expansion.md`;
- `policies/intake.md` and `policies/overlap-resolution.md`.

The bound handoff at
`C:\tmp\agent-skills-curated-capability-survey-handoff-20260714.md` was used as
historical mission and requirement evidence. Its old repository snapshot and
its direction to return research to user-configuration mainlines are not
current authority. The current agreed custody direction is
`YIYUAN-CALIBRATION`, with `YIYUAN-ASSETS` retaining project-admission
authority.

No live Agent state, user configuration repository, upstream radar repository,
CALIBRATION repository, or ASSETS repository was inspected for this audit.

## Classification

- `covered`: a current authority surface and acceptance path represent the
  requirement at the right abstraction level.
- `partial`: some governed structure exists, but material inputs, outputs,
  acceptance, or evidence are missing.
- `missing`: no current program or acceptance representation exists.
- `misplaced`: content exists, but at a historical, consumer, or lower-level
  surface that cannot serve as stable program architecture.
- `conflicting`: current surfaces point in materially incompatible directions.

## Requirement Ledger

| ID | Requirement | Assessment | Current evidence | Finding |
| --- | --- | --- | --- | --- |
| PCR-01 | Skills terminal and repository-matrix role | covered | `strategicPositioning.systemRole`, upstream boundary, harness model | Skills are correctly framed as the first terminal MVP rather than the whole MERIDIAN funnel. |
| PCR-02 | Broad multi-domain coverage | partial | `registry/collaboration-domain-coverage.json`, program step 01 | Ten domains and general/specialist types exist, but multi-domain scope has no strategic objective or acceptance criterion and can silently regress after step 01. |
| PCR-03 | Evidence-backed demand and shortfall coordinates | missing | capability-survey handoff only | STM/P/SG inputs, evidence states, held claims, promotion firewall, and refresh rules are absent from the machine program and acceptance map. |
| PCR-04 | Native, official, runtime, and installed baseline comparison | partial | intake policy, official-baseline boundary, runtime-resolved capability records | The repository knows these are comparison baselines, but no dated host/model/loader/permission baseline contract or survey deliverable exists. |
| PCR-05 | Broad discovery, clustering, deduplication, and stopping rule | partial | GitHub discovery profile, starred-source registry, overlap policy | Read-only discovery and overlap policy exist. Capability clustering, representative sampling, marginal-yield stopping, and remaining-uncertainty evidence are not program acceptance. |
| PCR-06 | Native / single-Skill / composition / non-Skill comparison | missing | handoff requirement; individual routing and Recipe structures only | The program does not require ordered alternatives, composition failure analysis, or total context/permission/maintenance-cost comparison before choosing a solution. |
| PCR-07 | Residual-gap proof before repository-authored implementation | missing | no program objective, acceptance criterion, or source-origin gate | Nothing machine-checkable prevents a newly authored Skill from being proposed merely because a shortfall or similar draft exists. |
| PCR-08 | Third-party and repository-authored candidate governance | conflicting | third-party intake is strong; official/runtime/vendor first-party is baseline-only | Third-party candidates are governed, but there is no distinct repository-authored gap-fill class. The term `first-party` may be misread as forbidding the user-requested self-built path unless vendor/platform first-party and repository-authored work are separated. |
| PCR-09 | Admission, release, rollback, and consumer projection boundary | partial | admissions, manifest, release evidence, consumer boundary | Admission and release are strong. Consumer projection is correctly external in prose, but the stable `steps` sequence ends in local runtime alignment, making one dated consumer transaction look like the universal program terminal. |
| PCR-10 | Multi-Agent evidence and claim limits | partial | strategic objective and partial acceptance | Instruction roots, ownership, precedence, projection, backup, restore, explicit/implicit loading, host/model distinctions, and cross-Agent behavioral evidence remain incomplete as correctly assessed. |
| PCR-11 | Feedback, refresh, deprecation, replacement, and retirement | partial | lifecycle objective, harness loop, lifecycle policy | The intent is present, but no implemented refresh/diff decision records, usage telemetry contract, recheck triggers, or retirement fixtures prove the full metabolism loop. |
| PCR-12 | Standard extraction and YIYUAN-CALIBRATION delivery | partial | custody boundary verified; candidate contract planned | Destination and authority are now correct. Candidate package schema, repeated-evidence threshold, delivery manifest, calibration receipt, and ASSETS admission separation remain unimplemented. |
| PCR-13 | Decision-ready external-brain projection and cognitive-load reduction | missing | abstract topology and routing exist, but no outcome objective | The plan does not state that consumers should receive a small decision-ready set instead of enumerating unknown Skills, nor does it measure routing/context/maintenance burden or decision quality. |
| PCR-14 | Sequence, reroute, acceptance, and closeout integrity | partial | lifecycle contract and prose gates | Round lifecycle is explicit, but prerequisite ordering across demand evidence, baseline comparison, clustering, gap proof, self-build, release, standards extraction, and CALIBRATION handoff is not governed data. |
| PCR-15 | Bounded initiative and result-package management | missing | historical Round 02 records and a handoff | Stable program architecture, current initiatives, historical rounds, and consumer transactions are not distinct. The ten-part capability-survey result package is absent from program acceptance. |

## Structural Findings

### P0-1: The stable program is conflated with one historical execution path

`registry/curation-program-plan.json#steps` moves from Round 01 and Round 02
through consumer projection readiness to local runtime alignment closeout. This
is useful historical execution truth, but it is not the complete recurring
program. A consumer-owned, separately authorized sync transaction cannot be the
mandatory terminal for every curation round.

Impact: sequencing from `currentStep` can be locally valid while the long-lived
program remains incomplete.

Required correction: retain the historical steps and Round 02 closeout state,
but add stable operating lanes plus a bounded initiative portfolio. Make
consumer projection an optional downstream evidence branch.

### P0-2: The reuse-before-build decision chain is absent

The stable harness starts with `discover -> filter -> review -> adapt`. It does
not start from evidenced demand, measure native/official/runtime coverage,
compare single and composed solutions, or prove the residual gap.

Impact: the program can govern a candidate safely after discovery while still
selecting the wrong candidate or manufacturing unnecessary Skill inventory.

Required correction: govern the full chain from demand evidence through
alternative comparison and residual-gap disposition before adoption,
adaptation, composition, or repository-authored design.

### P0-3: Repository-authored gap-fill Skills have no governed origin class

Current policy distinguishes external platform/runtime/vendor baselines,
third-party candidates, and curated approved payload. The agreed path also
requires repository-authored Skills when a material residual gap is proven.

Impact: self-built work is either impossible under the written model or can
enter through an implicit exception with weaker provenance and review.

Required correction: define `repository-authored-gap-fill-candidate` as a
non-executable candidate class requiring gap evidence, alternative comparison,
design provenance, license ownership, security, portability, overlap,
validation, and owner approval before admission.

### P0-4: The capability survey is not represented in program acceptance

The handoff requires native baselines, clustered candidate inventory,
STM/P/SG coverage, single/composed alternatives, dispositions, residual gaps,
evidence limitations, recommendations for the experimental three-Skill chain
and Hooks, discovery stopping evidence, and a non-authorization statement.
None is a current program initiative or acceptance package.

Impact: starting discovery now would create artifacts without an agreed
machine-verifiable result contract.

Required correction: add a bounded planned initiative with all ten result
deliverables and explicit prerequisites. Planning may proceed, but external
discovery execution remains blocked until program reconciliation and the
applicable Round 02 closeout gate are satisfied.

### P1-1: Six objectives are treated as a closed universe

`scripts/verify.py` requires exactly six strategic objectives. The six capture
important positioning and governance, but omit demand evidence, multi-domain
coverage, reuse-before-build gap proof, full-chain solution comparison, and the
decision-ready external-brain outcome.

Impact: the verifier turns an incomplete snapshot into a structural ceiling.

Required correction: validate a required core objective subset, unique IDs,
and reference closure while allowing reviewed additions.

### P1-2: Discovery infrastructure lacks governed saturation evidence

The weekly discovery profile and starred-source registry are useful inputs.
They do not prove clustering completeness, representative shortlist quality,
or why discovery can stop.

Impact: the project can either browse indefinitely or stop arbitrarily.

Required correction: require marginal-yield stopping evidence, remaining
uncertainty, and recheck triggers for every bounded survey round.

### P1-3: Consumer value is implicit rather than accepted

The repository has abstract topology and deterministic routing, but its program
does not accept against the intended user outcome: reduce unknown-Skill
enumeration and let consumers focus on creation and accountable decisions.

Impact: registry richness can grow without demonstrating that it reduces
routing burden, context burden, collision, or maintenance rent.

Required correction: add a decision-ready projection objective with honest
planned/partial metrics. Do not claim model-ceiling improvement or universal
Agent equality.

### P1-4: Standard custody is correct but delivery is not yet a process

The plan now correctly directs durable research and standard candidates to
`YIYUAN-CALIBRATION`, not user configuration repositories. The actual package,
receipt, revision, supersession, and admission interfaces are still planned.

Impact: research can still accumulate in temporary consumer surfaces because
the destination exists only as a boundary statement.

Required correction: keep the boundary verified but the delivery capability
planned until a separately authorized cross-repository contract is designed and
tested.

## What Is Not A Defect

- Skills remaining the first terminal MVP is consistent with the broader
  MERIDIAN funnel.
- Official/runtime/built-in/platform first-party bodies remaining external
  baselines is consistent with repository authority.
- Third-party pinning, license, provenance, security, portability, overlap,
  adaptation, validation, and approval gates are strong and should be retained.
- Partial multi-Agent evidence and planned standard-candidate extraction are
  honest statuses, not failures to be relabeled as verified.
- The dated Round 02 local sync record remains valid evidence for that bounded
  authorized transaction; it is only insufficient as current live-state or
  universal-program evidence.

## Audit Conclusion

The current master control plan is directionally correct but not complete
enough to trust its execution ordering as the whole program. It strongly
governs intake and release after a candidate exists, but it does not yet govern
why a capability is needed, whether native or composed alternatives already
cover it, when a residual gap is real, when repository-authored work is allowed,
or what the capability-survey result must contain.

Therefore Round 02 stage closeout must remain pending while the program-control
completeness correction is reviewed and verified. No new external discovery,
candidate execution, self-built Skill implementation, runtime sync, standards
promotion, or cross-repository delivery is authorized by this audit.
