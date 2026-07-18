# CC Switch Disposable Source-Management Preview — 2026-07-18

## Result

CC Switch 3.17.0 is sufficient to remain the operational Skill manager candidate. In a disposable source copy, its source registration, source enablement, cross-source directory collision, selective projection, backup, restore, and migration-snapshot contracts passed. This does not authorize or prove a real migration.

The stock Windows test boundary has a defect: `CC_SWITCH_TEST_HOME` is honored by the central configuration path, but five Skill-service paths still called `dirs::home_dir()` directly. The unmodified suite therefore produced one real failure and four poisoned-lock follow-on failures. A diagnostic-only patch in `C:/tmp` routed those lookups through the central home resolver; the seven official `skill_sync` tests then passed. A repository-owned disposable test also passed source registration, disabled/enabled persistence, and `SKILL_DIRECTORY_CONFLICT` before network download.

## Evidence boundary

- Official baseline: `farion1231/cc-switch` tag `v3.17.0`, commit `3d176b98cc0bfd151a42882e88ab59b62083b92f`.
- The downloaded source archive SHA-256 was `82273F854AB6C969BEC61AA9FB2BFFAB870B2988513071BCA18B3CDEEDFED947`.
- The temporary isolation patch and contract test were not applied to the installed product or any upstream repository.
- Real shared Skill tree hashes were identical before and after the tests.
- The running desktop process locked the live database, so no whole-database digest claim is made.

## Remaining gate

Acceptance remains partial because no active projection is source-backed and no source-backed network update was exercised. A real canary requires separate authority plus exact source pinning, backup, collision, rollback, and post-state verification. The stock Windows isolation defect should be handled as an upstream issue or patch only under separate external-write authority.

A later loopback source-update fixture closed the disposable success-path gap
but confirmed that `update_skill` is not atomic and also exposed a second
Windows test-home precedence defect. See
`registry/cc-switch-disposable-source-update-and-recovery-review-2026-07-18.json`.

Machine evidence: `registry/cc-switch-disposable-source-management-preview-2026-07-18.json`.
