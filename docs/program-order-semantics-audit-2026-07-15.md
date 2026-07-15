# Program Order Semantics Audit

Date: 2026-07-15

Status: evidence audit for order-semantics correction; not owner acceptance,
Git closeout, Round 02 execution authority, external discovery authority,
runtime state, or cross-repository delivery authority.

## Question

After correcting the master plan's completeness, does its process model express
the right prerequisites, safe parallel work, optional branches, feedback loops,
and current control initiative without implying a false linear conveyor?

## Evidence Boundary

The audit used current repository truth from:

- `registry/curation-program-plan.json`;
- `registry/program-acceptance-map.json`;
- `registry/round-lifecycle-contract.json`;
- `registry/curation-expansion-rounds.json`;
- `docs/curation-program-plan.md`;
- `docs/curation-harness-model.md`;
- `docs/coverage-and-curation-expansion.md`;
- `policies/intake.md` and `policies/overlap-resolution.md`.

The completeness audit remains evidence for why the eleven operating lanes
exist. This audit asks a narrower question: how those lanes may actually be
entered, joined, skipped, revisited, or closed. No live Agent, upstream radar,
consumer configuration, CALIBRATION, or ASSETS repository was inspected.

## Classification

- `correct`: prerequisites and branch meaning are explicit and enforceable.
- `ambiguous`: prose suggests the intended behavior, but governed data permits
  a materially different reading.
- `misordered`: a required input or list placement creates a false dependency.
- `missing`: the process cannot represent the needed control relationship.

## Finding Ledger

| ID | Ordering concern | Assessment | Evidence | Finding and required correction |
| --- | --- | --- | --- | --- |
| POS-01 | Core reuse-before-build prerequisites | correct | First eight `operatingLanes` and demand/baseline/alternative/gap gates | Demand evidence, current baseline, bounded discovery, representative review, alternative comparison, residual-gap decision, candidate governance, and admission/release form a defensible core path. Preserve this order. |
| POS-02 | Array order versus executable semantics | ambiguous | `operatingLanes` is one eleven-item array | The array has no machine distinction between mandatory core work, optional branches, and cross-cutting loops. Add a dependency-graph model, lane modes, dependencies, and branch declarations; keep display order only as a projection. |
| POS-03 | Consumer projection | ambiguous | Consumer prose says optional, but the lane sits between release and lifecycle | A reader or scheduler can infer that every release must be installed before lifecycle work. Declare consumer projection as an optional branch from approved release with separate consumer authority. |
| POS-04 | Lifecycle metabolism | misordered | `requiredInputs` says `release and consumer evidence` | Update, security, license, conflict, deprecation, rollback, and retirement signals can arise from candidates, releases, upstream changes, or consumers. Model lifecycle as cross-cutting with any-of trigger inputs; never require consumer evidence. |
| POS-05 | Standard extraction and CALIBRATION handoff | ambiguous | The lane appears after lifecycle as the last array element | Repeated standard evidence can arise from demand research, reviews, failures, consumer evidence, or lifecycle evidence and may never require a released Skill. Model extraction as a conditional evidence branch gated by repetition and separate cross-repository authority, not as a universal terminal. |
| POS-06 | Source trust before representative deep review | ambiguous | Deep review accepts `pinned source or dated metadata` | Metadata is enough for shortlist triage, not for inspecting third-party instructions or executable surfaces. Require an exact source pin and license/provenance boundary before third-party deep review; inspection remains non-execution. |
| POS-07 | Current initiative versus historical step | missing | `currentStep` points to historical `program-06`; docs say completeness reconciliation is current, but no matching initiative exists | Add `currentInitiativeId` and a completeness-reconciliation initiative with technical evidence, pending owner review, and explicit blocked actions. Preserve the historical step as dated execution posture. |
| POS-08 | Parallelism, upstream radar, and closeout join | missing | Prose mentions a broader funnel and reroute triggers, but no execution semantics describe them | Record that upstream radar discovery is independently owned; within this repository, baseline probes may parallelize by host and representative reviews by cluster, then join before comparison. Require initiative closeout before activating the next intake round. |

## Resulting Process Shape

```text
core path
  demand evidence
  -> native / official / runtime baseline
  -> bounded candidate intake, clustering, and exact source trust
  -> representative deep review
  -> alternative comparison
  -> residual-gap or covered decision
  -> candidate governance
  -> admission, verification, and release

optional branch
  approved release + separate consumer authority
  -> consumer projection and feedback

cross-cutting loop
  candidate | release | upstream | consumer signal
  -> lifecycle metabolism
  -> reroute to the affected core lane

conditional branch
  repeated evidence from demand | review | feedback | lifecycle
  -> standard candidate
  -> separately authorized CALIBRATION handoff
  -> separately decided ASSETS admission
```

Broad resource discovery may continue in an upstream radar without waiting for
this repository. A radar signal is not a curated decision. This repository may
use the signal only inside a bounded initiative after demand, baseline,
source-trust, authority, review, and acceptance gates are bound.

## Conclusion

The corrected lane inventory contains the right core stages, but its order is
not yet safe as governed execution semantics. The remaining defect is not the
core sequence; it is the absence of explicit dependency, optional-branch,
cross-cutting, conditional-branch, and current-initiative structure.

This audit authorizes only in-repository plan correction and verification. It
does not authorize commit, merge, push, Round 02 closeout, external discovery,
candidate execution, Skill authoring, runtime mutation, standard promotion, or
cross-repository delivery.
