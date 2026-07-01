# Curation Program Plan

This is the overall execution plan for expanding `agent-skills-curated` and
then closing the stage by aligning local Codex, agents, and cc Switch Skill
directories.

The machine-readable plan lives in
`registry/curation-program-plan.json`. The round lifecycle contract lives in
`registry/round-lifecycle-contract.json`.

## Control Principle

The work is not complete when sources are discovered, and it is not complete
when one repository batch validates. The intended path is:

```text
discovery and coverage
-> source intake and filtering
-> review and adaptation
-> curated admission and release
-> consumer projection readiness
-> local runtime alignment closeout
```

Each step has its own acceptance criteria and verification surface. Discovery,
source intake, and adaptation drafts are not approval. Local runtime alignment
is the stage closeout, not the starting point.

## Current Position

The current active step is `program-02-source-intake-and-filtering`.

The current evidence is the pinned round-02 source batch. It is review evidence,
not approved payload and not runtime inventory. The next gate is candidate
review and adaptation:

- license and attribution review;
- provenance and source stability review;
- security review for commands, network calls, credentials, and file access;
- portability review across agents and runtimes;
- overlap and conflict review against curated, official, runtime, and local
  capabilities;
- disposition as adopt, merge, recipe-only, adapter-only, reference-only, or
  reject.

## Acceptance And Verification Mapping

Discovery and coverage is accepted only when broad domain coverage, read-only
discovery, and non-approval candidate records validate.

Source intake and filtering is accepted only when each source is pinned to a
full revision, has license posture, detected Skill evidence, coverage hints,
review focus, and explicit blocked actions for release and runtime sync.

Review and adaptation is accepted only when every candidate has a reviewed
disposition, unsafe behavior is removed or rejected, agent-specific assumptions
are neutralized or bounded, and duplicate Skills are merged or rejected.

Curated admission and release is accepted only when approved payload,
registries, topology, routing scenarios, generated projections, and the release
manifest all validate together.

Consumer projection readiness is accepted only when the exact release SHA,
consumer sync plan, read-only local inventory, backup plan, rollback plan, and
directory-specific parity rules are recorded.

Local runtime alignment closeout is accepted only when local write authorization
is explicit, approved portable Skills are synced to the intended directories,
Codex-specific system or runtime surfaces are preserved, source-intake-only
candidates are not installed, backups and parity checks exist, and residual
exceptions are documented.

## Final Local Alignment Shape

The final closeout target is:

- `.agents/skills` and `.cc-switch/skills` align to the same approved portable
  curated Skill set, except for documented, intentionally local exceptions.
- `.codex/skills` receives the appropriate shared curated Skill set while
  preserving Codex-specific system, plugin, or runtime-owned surfaces.
- No source-intake-only candidate, adaptation draft, or official/runtime-owned
  body is installed as curated payload.

That final sync is a later authorized local-write stage. Until then, this
repository work remains discovery, review, adaptation, release, and readiness
work.
