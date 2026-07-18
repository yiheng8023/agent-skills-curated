# Consumer-Mapping Evidence Gap Reconciliation — 2026-07-18

This record prevents conceptual or historical consumer examples from being
presented as current supported mappings.

## Current evidence

Codex now has four dated evidence slices. In addition to historical consumer
feedback, a historical local sync transaction, and a static local metadata
baseline, this review read the current consumer repository at exact HEAD
`0c93458d48cb1ebaa6d0d289e3a21f46d2f61f65`. Dirty consumer files were
excluded. The pinned HEAD defines AGENTS installation, managed and foreign
Skill locations, ownership classes, a digest-bound routing projection,
backup-first transactions, rollback, and restore behavior. Five disposable
install, verify, retirement, and rollback tests passed without writing the
consumer repository.

The review then read the shared `C:/Users/15521/.agents` metadata without
changing it. The root contains 73 Skill directories. Forty-three resolve into
CC Switch, 27 are declared by the Lark schema-3 lock, and three collaboration
chain Skills exactly match the pinned consumer repository. Of the 43 CC Switch
targets, 42 have local database rows, zero have source-backed rows, and one has
no database row. The old curated transaction claims 19 of those targets; all
19 exactly match this repository's current release but differ from the older
transaction manifest. Its routing index still matches the old transaction and
its backup still exists. This is live ownership and drift evidence, not
permission to overwrite, relink, or roll back any Skill.

This advances Codex beyond historical-only evidence, but not to a current
supported live mapping. Live loader precedence and implicit activation remain
unproven. More importantly, none of the 43 CC Switch targets currently has a
source-backed database row. The 19 transaction-claimed bodies are legacy
curated derivatives rather than upstream-exact payloads, so live restore is
intentionally unexercised even though the old backup exists.

Claude Code is only a conceptual chain example in this repository. There is no
dated consumer-owned inventory, ownership or precedence map, minimal behavior
probe, or backup and restore evidence here.

Public templates illustrate a portable configuration pattern. They are not
current consumer evidence. Private configuration repositories are not assumed
to be current downstreams merely because they exist or existed historically.

## Acceptance result

`acceptance.consumer-mapping-evidence` remains partial. This is not made
vacuously true by declaring that there are zero supported consumers: at least
one explicitly supported current consumer must satisfy instruction discovery,
Skill locations, ownership, precedence, projection, verification, backup, and
restore.

The next gate is a read-only per-Skill source migration review for the 19
legacy curated derivatives and the other 24 CC Switch targets, followed by
separately authorized migration and live consumer-evidence tasks for source
registration, loader precedence, activation, release pin, and safe restore.
This review read the external consumer repository, CC Switch database, and
Agent Home metadata but wrote none and did not read or modify a Hook.
