# CC Switch Live Source And Ownership Reconciliation — 2026-07-18

The accepted strategy remains sound: reuse CC Switch for operational Skill
management and do not rebuild a custom Manager. The current live projection,
however, has not yet reached the source-preserving target state.

## Read-only findings

The shared Agent Skill root contains 73 directories. Forty-three resolve into
the CC Switch Skill store: 42 symbolic links and one junction. The remaining
30 are materialized directories: 27 are declared by the Lark schema-3 lock,
and `capability-router`, `closure-contract`, and `intent-contract` exactly match
the pinned `codex-user-config` HEAD.

The live CC Switch database contains 248 Skill rows and five repository rows.
Its `enabled_codex` flags are not proof of the shared-root projection: all 248
rows are flagged, while only 43 CC Switch targets are present there. Of those
43 active targets, 42 have `local:*` database rows, zero have source-backed
rows, and `obsidian-open-format-knowledge-files` has no database row.

All 19 Skills claimed by the old curated transaction are symbolic links into
CC Switch. Their trees exactly match this repository's current release, and
all 19 CC Switch rows are local records without Git source metadata. They are
reviewed adapted derivatives from the two pinned upstream families, not
byte-for-byte upstream payloads. All 19 differ from the older transaction
manifest because the current curated release moved after that transaction.

## Authority result

CC Switch operational distribution is observed. Live source preservation is
not: zero of the 43 active projections has a source-backed database row. The
current curated repository therefore remains body authority for the 19 legacy
derivatives until each is reviewed for replacement with an exact upstream
Skill, explicit derivative retention, or retirement. CC Switch owns their
current operational storage and links, not their missing upstream provenance.

The old curated transaction is historical install, backup, and routing
evidence. It is not current body authority and does not authorize rollback over
the CC Switch links. Unknown, foreign, or ecosystem-managed content remains
frozen by default.

`acceptance.cc-switch-source-preserving-skill-pool` is downgraded from
`verified` to `partial`. The strategy and operational reuse are verified; the
live source-backed migration is not. Consumer mapping and foreign coexistence
also remain partial.

The subsequent read-only per-Skill migration review produced bounded
dispositions for the 19 legacy derivatives. A separate disposable CC Switch
preview then verified source-repository state, collision rejection, selective
projection, backup, restore, and migration-snapshot contracts. It also exposed
a stock Windows test-isolation defect: five Skill-service path groups bypassed
`CC_SWITCH_TEST_HOME`. A temporary extracted-source diagnostic correction made
all seven upstream `skill_sync` tests pass. This is not evidence of a real
source-backed network update or live migration.

The next safe gate is either a network-controlled disposable update fixture or
an explicitly authorized single canary migration with backup and rollback.
No real CC Switch, Skill, Agent Home, Hook, transaction, backup, repository,
commit, or remote was changed by this reconciliation or preview.
