# Round 02 Local Runtime Sync Approval Request

Machine-readable request:
[`registry/round02-local-runtime-sync-approval-request.json`](../registry/round02-local-runtime-sync-approval-request.json).

Source execution record:
[`registry/round02-approved-payload-routing-proposal.json`](../registry/round02-approved-payload-routing-proposal.json).

This is an approval request, not approval.

## Current State

```text
status: awaiting_owner_approval
approval recorded: false
local runtime sync allowed: false
write cc-switch skills allowed: false
write agents skills allowed: false
write codex skills allowed: false
create symlink allowed: false
backup or rollback snapshot allowed: false
delete or cleanup allowed: false
publish or release allowed: false
dependency install allowed: false
credential use allowed: false
network access required: false
```

Round-02 approved payload/routing is already validated and pushed. The release
manifest now contains 20 Skills, 42 files, and 105 passing routing scenarios.
The local runtime directories have not been synchronized.

## Read-Only Preflight

Observed local directory model:

- `C:\Users\15521\.cc-switch\skills` is the canonical physical Skill directory
  for portable Skills.
- `C:\Users\15521\.agents\skills` entries are symbolic links to cc-switch
  Skill directories.
- `C:\Users\15521\.codex\skills` portable entries are symbolic links to
  cc-switch Skill directories; `.system` and `codex-primary-runtime` are
  Codex-owned and must be preserved.

Manifest hash preflight against `C:\Users\15521\.cc-switch\skills`:

```text
match: 34
drift: 7
missing: 1
```

Drifted files:

- `skills/grill-with-docs/SKILL.md`
- `skills/prototype/SKILL.md`
- `skills/review/SKILL.md`
- `skills/shipping-and-launch/SKILL.md`
- `skills/to-issues/SKILL.md`
- `skills/to-prd/SKILL.md`
- `skills/triage/SKILL.md`

Missing file:

- `skills/obsidian-open-format-knowledge-files/SKILL.md`

Missing release root in all three local Skill directories:

- `obsidian-open-format-knowledge-files`

## Requested Approval

The smallest useful approval phrase is:

```text
批准执行 Round-02 local runtime sync
```

or:

```text
Approve Round-02 local runtime sync only
```

If approved, the next work may synchronize only the release-manifest payload
from source commit `e9832c89c21593d4671db5a731deb49a300cd730` into the local
portable Skill layout:

1. update the 7 drifted files in `C:\Users\15521\.cc-switch\skills`;
2. add `obsidian-open-format-knowledge-files` to
   `C:\Users\15521\.cc-switch\skills`;
3. create or repair only the missing `obsidian-open-format-knowledge-files`
   symbolic links in `C:\Users\15521\.agents\skills` and
   `C:\Users\15521\.codex\skills`;
4. preserve `.system`, `codex-primary-runtime`, plugin/cache-owned Skills, and
   all non-release local Skills;
5. create a temporary rollback snapshot for changed local files and remove it
   after successful verification unless verification fails;
6. verify cc-switch hashes against `release-manifest.json` and verify the
   agents/codex symbolic-link targets.

## Explicitly Not Requested

This request does not ask permission to:

- modify official, runtime-owned, plugin-cache, `.system`, or
  `codex-primary-runtime` Skill directories;
- delete non-release local Skills;
- change Codex, agents, cc-switch, plugin, MCP, account, credential, or memory
  configuration;
- install dependencies;
- use credentials;
- fetch external sources;
- publish a GitHub release;
- redistribute upstream source text or assets beyond the already approved
  repository payload;
- sync adapter-only, reference-only, or rejected Round-02 candidates;
- change `C:\Users\15521\.agents\skills` or
  `C:\Users\15521\.codex\skills` entries other than the missing
  `obsidian-open-format-knowledge-files` symbolic links.

## Evidence That Must Exist After Approval

If the owner approves this request, the next record must include:

1. owner approval event record;
2. before/after local directory and hash diff summary;
3. temporary rollback snapshot path and cleanup result;
4. cc-switch manifest hash verification;
5. agents and codex symbolic-link target verification;
6. explicit record that official/runtime/plugin/cache directories and
   non-release local Skills were preserved;
7. repository verification result after recording the sync execution.

Until the approval event exists, local runtime sync remains blocked: no write
to `C:\Users\15521\.cc-switch\skills`,
`C:\Users\15521\.agents\skills`, or `C:\Users\15521\.codex\skills` may occur.
