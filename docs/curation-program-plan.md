# Curation Program Plan

This is the human-readable projection of the machine program authority in
`registry/curation-program-plan.json`. The objective, acceptance, verification,
and evidence mapping lives in `registry/program-acceptance-map.json`. Bounded
execution rounds live in `registry/curation-expansion-rounds.json` and follow
`registry/round-lifecycle-contract.json`.

## Program Position

`agent-skills-curated` governs the reviewed Skills terminal inside a broader
resource-governance funnel. Skills are the first terminal MVP because they are
portable, comparatively low burden, usable by internal and external consumers,
and able to carry instructions, resources, scripts, and deterministic checks.
They are not the boundary of `YIYUAN-MERIDIAN`, resource discovery, or future
terminal types.

The authority split is:

```text
broader resource discovery and candidate signals
-> reviewed Skill intake, adaptation, release, and lifecycle governance here
-> consumer-owned installation, projection, backup, restore, and live checks
-> bounded research and standard-candidate delivery to YIYUAN-CALIBRATION
-> project-owned admission of any hard standard
```

This repository does not own upstream radar architecture, live Agent state,
consumer configuration, or project hard-standard admission. Consumer
configuration repositories are consumption, validation, and feedback surfaces;
they are not the durable home for cross-project research or standards. After
repeated evidence exists, this repository may produce a traceable standard
candidate package for delivery to `YIYUAN-CALIBRATION`, which provides durable
calibration custody. `YIYUAN-ASSETS` retains the separate decision to admit a
candidate as a project hard standard. Any cross-repository write remains a
separately authorized transaction.

## Strategic Objectives

The program has six stable objectives:

1. Operate Skills as the first terminal MVP without turning the broader funnel
   into a Skills-only system.
2. Govern third-party Skill bodies through provenance, license, security,
   portability, overlap, adaptation, validation, release, and lifecycle gates.
3. Keep releases agent-neutral while requiring evidence-backed consumer
   mappings for each Agent's instruction, Skill, precedence, projection,
   verification, backup, and restore behavior.
4. Improve collaboration reliability through the smallest sufficient layered
   combination of instructions, Skills, deterministic mechanisms, project
   standards, evidence, and accountable human decisions.
5. Extract standard candidates from repeated governance evidence, target their
   durable calibration custody in `YIYUAN-CALIBRATION`, and preserve separate
   `YIYUAN-ASSETS` project-admission authority.
6. Support update, conflict handling, supersession, deprecation, migration,
   rollback, and retirement instead of accumulating Skills indefinitely.

Each objective maps to stable acceptance, verification, and evidence IDs in
`registry/program-acceptance-map.json`. `verified` means the stated criterion
has checked-in evidence; it does not upgrade a partial implementation or dated
runtime observation into current live truth.

## Delivery Lifecycle

The reviewed Skill delivery lifecycle remains:

```text
discovery and coverage
-> source intake and filtering
-> review and adaptation
-> curated admission and release
-> consumer projection readiness
-> local runtime alignment closeout
```

These stages are gates, not a one-way conveyor. Feedback, an upstream update,
a security or license change, a consumer failure, or project-standard conflict
can return released content to an earlier gate.

Discovery and coverage is accepted only when broad domains, read-only discovery,
and non-approval candidate records validate. Source intake is accepted only
when every source is pinned and has license, provenance, detected Skill,
coverage, review-focus, and blocked-action evidence. Review and adaptation is
accepted only when dispositions, safety, portability, overlap, and license
boundaries are explicit. Curated admission and release is accepted only when
approved payload, registries, topology, routing, scenarios, generated
projections, and the release manifest validate together.

Consumer projection readiness and local alignment are consumer-owned actions.
They require a pinned release, read-only inventory, owned-path classification,
backup, rollback, explicit local-write authority, and fresh post-action evidence.
This repository may retain dated evidence without claiming it owns or currently
controls the consumer environment.

## Current Position

Round 02 is not active source-intake execution anymore. The repository contains
evidence for candidate review, admission decisions, approved payload and routing,
and a bounded local runtime sync transaction:

- `registry/round02-release-admission-candidate-review.json`
- `registry/round02-approved-payload-routing-proposal.json`
- `registry/round02-local-runtime-sync-execution.json`

Those records prove that the bounded actions occurred on their recorded dates.
They do not prove current live parity, and they do not include a distinct Round
02 stage-closeout reconciliation. The current state is therefore
`needs-reconciliation`, not `complete`.

The next gate is a requirement-by-requirement stage-closeout reconciliation
that records covered scope, verification evidence, residual risks, deferred
work, current authority boundaries, and the explicit next-round or pause
decision. No new candidate intake should inherit an unclosed Round 02 state.

## Verification And Closeout

The global deterministic set remains:

```text
python -B scripts/verify.py
python -B scripts/build_release_manifest.py --check
python -B scripts/build_topology.py --check
python -B scripts/simulate_routing.py --all
python -B -m unittest discover -s tests -v
```

Passing these commands proves only the contracts they actually cover. Program
closeout additionally requires the mapped acceptance evidence and an honest
closeout outcome. A dated local sync execution record must never be treated as
current live Agent availability or as global completion.
