# GitHub Repository Configuration Evidence

## Remote Result

On 2026-07-18, `yiheng8023/agent-skills-curated` was verified as a public
repository on `main` with Issues, Projects, and Discussions enabled and Wiki
disabled. Its description and seven project-specific topics are configured.
The merge policy matches `home-edge-bootstrap-public`; no merge behavior was
changed in this task.

The following security features were enabled and read back through GitHub's
official API:

- vulnerability alerts;
- Dependabot security updates, not paused;
- secret scanning;
- secret scanning push protection;
- private vulnerability reporting;
- CodeQL default setup.

CodeQL reported `configured` for `actions` and `python` with a weekly schedule.
Its first two analyses completed against remote `main` revision
`d0955bf7f7852b53955f843b20c69709b31459be`: 17 Actions rules and 43 Python
rules produced zero results, and the alert API returned zero alerts. This is
an exact-remote-revision result, not evidence for the unpushed local worktree.

## Community And Sponsorship Boundary

Local PR/Issue templates, support documents, sponsorship documents, and
`.github/FUNDING.yml` are prepared. They are not published because this task
does not commit or push. GitHub's community profile therefore remains at 85%
instead of the reference repository's 100%; this is expected local/remote
separation rather than a template-generation failure.

The sponsorship surface uses the owner's published PayPal link and references
the owner's public WeChat Pay and Alipay assets in the reference repository.
Sponsorship is voluntary and buys no SLA, review or release priority,
governance exception, or technical influence.

## Verification Boundary

This is a dated snapshot. GitHub settings may drift and must be queried again
before a current-state claim. Community health requires a separate authorized
commit and push, then a fresh profile read. CodeQL green status must always be
tied to the exact revision being claimed. The recorded result covers remote
`main` at `d0955bf...`; the local checkout is 12 commits ahead with unpublished
changes and does not inherit that result.

No repository file was published, no branch rule or release was changed, no
extra authentication scope was granted, and no Agent, Hook, consumer, or other
repository was mutated.
