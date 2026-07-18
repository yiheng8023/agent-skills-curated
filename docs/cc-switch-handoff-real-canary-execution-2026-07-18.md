# CC Switch `handoff` Real-Canary Execution — 2026-07-18

## Result

The owner-authorized one-Skill canary converted `local:handoff` into
`mattpocock/skills:skills/productivity/handoff` through CC Switch's own source
download, uninstall backup, install, and projection paths. The Skill count stayed
at 248, the source count moved from five to six, and only Claude and Codex remain
enabled. The target tree contains the exact GitHub archive bytes for `SKILL.md`
and `agents/openai.yaml`.

CC Switch was stopped before mutation. A consistent database backup, independent
Skill copy, and before-state manifest remain under
`C:/tmp/cc-switch-handoff-canary-20260718`. CC Switch also produced the
restorable local backup `20260718_071018_handoff`.

## Fail-closed correction

The first attempt was rejected because the preview hash came from a Windows Git
checkout whose CRLF working-tree bytes differ from the LF bytes in the GitHub
archive that CC Switch installs. The guard rolled back the source registration,
Skill body, and projections. The two versions were then proven equivalent when
end-of-line differences were ignored, the original database metadata was
restored from the before state, and the second attempt used the archive-byte
hash without weakening any semantic or security check.

## Post-state and update verification

All 247 unrelated Skill rows, the five pre-existing source rows, and 14 other
database tables are unchanged. The Claude and Codex paths remain symbolic links
to the CC Switch SSOT. A CC Switch source update check reports no update for
`handoff`, proving that the new source identity and installed hash participate
in the update path.

The same global check reports 20 other update signals, all from `larksuite/cli`.
None was executed. They enter the candidate-review lane and require a source pin
plus security, quality, superiority, overlap, redundancy, name-collision, and
consumer-impact review before any update.

## Follow-up synchronization and remaining boundary

The owner subsequently authorized normal CC Switch WebDAV synchronization. CC
Switch is running and reports a successful local sync at
`2026-07-18T19:17:44+08:00`. A post-sync audit confirms that the source-backed
`handoff` identity, exact body, projections, unrelated Skill rows, and source
rows remain intact. The observed runtime delta removed the `fetch`,
`sequential-thinking`, and `time` MCP rows, appended proxy request logs, and
advanced session-log synchronization; the owner accepted normal sync behavior.

Fresh-session Skill invocation and cross-device content equality remain open. A
secret-bearing settings file was read during preflight; no secret was copied
into repository evidence, and out-of-band credential rotation remains
recommended.

No other Skill, Hook, MCP, Plugin, App, instruction carrier, consumer repository,
commit, or remote Git state was changed.

Machine evidence:
`registry/cc-switch-handoff-real-canary-execution-2026-07-18.json`.
