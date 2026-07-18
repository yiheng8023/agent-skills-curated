# CC Switch Disposable Source Update And Recovery Review — 2026-07-18

## Result

A loopback HTTP server supplied GitHub-compatible v1 and v2 repository archives
to a temporary CC Switch 3.17.0 source copy. The fixture verified source-backed
installation, hash-based update detection, pre-update backup, v2 replacement,
and manual restoration of v1. The targeted Rust test passed once the disposable
configuration directory was made authoritative.

The failure injection found a real transaction gap. `update_skill` ignores an
error from backup creation, removes the old SSOT directory before copying the
new source, and has no automatic rollback. A failure after removal can therefore
leave the SSOT absent while the old database row remains. Manual recovery was
verified by removing the stale record through the existing uninstall path and
restoring the readable pre-update backup.

## Isolation incident

Diagnostic tests run before the isolation correction temporarily created two
test-only Skill rows, one test-only repository row, one `demo` SSOT directory,
and three fixture backup directories in the real CC Switch home. The cause was
another Windows isolation defect: when the
disposable database did not yet exist, `get_app_config_dir` preferred the
legacy `HOME` database fallback over the explicit `CC_SWITCH_TEST_HOME`.

Cleanup was fail-closed. The first transaction matched the fixture identity,
repository metadata, description, content hash, exact directory tree, and
backup metadata before removing anything. A later full-row audit found two
older database-only test records; a second transaction required their exact row
values and aborted if any matching payload directory existed. Consistent
pre-cleanup database copies remain under `C:/tmp` with SHA-256 values
`F0A041FFB6AF2103D5874AFC899CC8808FA863876704A520AE7108232B203C6D` and
`EF2EE5728842E3BFF594EE328C91AB511C0187F4CDC51475A0286D61C758F209`.

Final post-cleanup checks found zero test Skill rows, zero test repository rows,
zero fixture backups, no `demo` or `duplicate-skill` SSOT, and no Agent
projection. The live database returned to 248 Skill rows and five repository
rows, with 514 files in the CC Switch Skill store. The corrected second run
created no new live fixture residue.

## Revised canary gate

CC Switch remains the selected operational manager, but its updater is not an
atomic transaction. The first real canary must use one reviewed Skill, a
consistent database backup, exact before-state hashes, a separately readable
Skill backup, a previewed ownership transition, and an explicit failure
recovery rehearsal. Automatic update is not allowed for the first canary, and
the existing `update_skill` path must not be treated as rollback evidence.

No real user Skill, Hook, MCP, Plugin, App, instruction carrier, consumer
configuration, upstream repository, commit, or remote was changed.

Machine evidence:
`registry/cc-switch-disposable-source-update-and-recovery-review-2026-07-18.json`.
