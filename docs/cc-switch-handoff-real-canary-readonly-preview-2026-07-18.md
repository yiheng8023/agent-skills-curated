# CC Switch `handoff` Real-Canary Read-Only Preview — 2026-07-18

## Decision package

`handoff` is the lowest-risk first real-canary candidate among the 16 active
exact-source replacement candidates reviewed in this slice. It has no executable
surface. Relative to the current local body, the pinned upstream revision adds
`disable-model-invocation: true`, replaces `PRDs` with the more general `specs`,
and adds OpenAI display metadata with implicit invocation disabled. It removes no
current safety or capability boundary.

The reviewed source is `mattpocock/skills` at
`9603c1cc8118d08bc1b3bf34cf714f62178dea3b`, MIT licensed. Remote `main` still
resolved to that exact revision when observed on 2026-07-18. The reviewed target
contains only `SKILL.md` and `agents/openai.yaml`, with no script or binary.

The target hashes in this preview were corrected after the first authorized
attempt failed closed: a Windows checkout uses CRLF working-tree bytes, whereas
CC Switch installs LF bytes from the GitHub archive. The files are equivalent
when end-of-line differences are ignored. Archive-byte hashes are canonical for
this CC Switch transaction; no semantic or security gate was weakened.

## Before state and operational limits

The live item is `local:handoff`, enabled only for Claude and Codex. Both
consumer paths are symbolic links to the CC Switch SSOT and resolve to the same
`SKILL.md` hash. The live database contains 248 Skill rows and five source rows;
`mattpocock/skills` is not registered.

The stored local database content hash is stale relative to the current SSOT.
This does not trigger source update checks because the row is local, but it is a
real before-state mismatch and must not be silently normalized. The existing
directory also makes a source install fail closed, so this is an uninstall-install
ownership transition, not an `update_skill` operation.

CC Switch records `main` rather than the reviewed commit and downloads a moving
`refs/heads/main` archive. It therefore cannot preserve the commit pin by itself.
Immediately before any mutation, remote `main` must still equal the reviewed
revision or the canary aborts. Automatic update remains prohibited.

## Transaction and rollback

Before mutation, quiesce CC Switch writes, create independently readable and
hashed database and Skill backups, recalculate the live row/tree/projection
state, and re-check the remote revision. The bounded mutation would register one
source, uninstall only `local:handoff` through the backup-producing path, install
only the exact source-backed `handoff`, and restore only the prior Claude and
Codex enablement flags.

Acceptance requires the exact reviewed tree hash, the expected source-backed
row, unchanged unrelated rows, intact symbolic-link projections, and readable
pre-change backups. Rollback removes only the exact source-backed row, restores
the verified local backup and prior projections, and removes the new source only
when no other Skill references it. The database copy is a last-resort recovery
surface while writes remain quiesced, not a routine overwrite.

This artifact was the decision-ready read-only preview. The subsequently
authorized local canary is recorded separately; automatic update, external sync,
commit, and push remain outside this preview.

Machine evidence:
`registry/cc-switch-handoff-real-canary-readonly-preview-2026-07-18.json`.
