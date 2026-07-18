# Legacy Curated Skill Source Migration Review — 2026-07-18

This is a read-only migration review for the 19 legacy adapted Skills currently
projected through CC Switch local rows. It does not authorize source
registration, replacement, relinking, retirement, installation, or execution.

## Result

None of the 19 live trees is a whole-tree exact match to the current upstream
source. Sixteen have an active current upstream path and are provisional
candidates for reviewed, source-backed, upstream-exact replacement. Three are
provisional retirement or supersession candidates:

- `git-guardrails` duplicates the separately present upstream-named
  `git-guardrails-claude-code` capability;
- `setup-project-skills` duplicates the separately present upstream-named
  `setup-matt-pocock-skills` capability;
- `ubiquitous-language` remains under the upstream `deprecated` namespace.

No adapted derivative is currently justified for retention. That does not
prove that no residual gap exists; it means a rewritten fork must not survive
by inertia. A derivative requires separate, reproducible shortfall evidence.

## Current source drift

The Addy Osmani source advanced 91 commits from the prior reviewed revision to
`06300e258ef62cdbfbc9b1615ac5b4f58bee05ac`. Two mapped Skill bodies are
unchanged and three changed. The Matt Pocock source advanced 176 commits to
`9603c1cc8118d08bc1b3bf34cf714f62178dea3b`; several Skills changed, graduated,
or were renamed, and current trees add OpenAI metadata. The only mapped shell
surfaces are the non-executed diagnosis template and the executable Git
guardrail script. Both require static review before any adoption decision.

The exact-revision bodies were then read without execution. No embedded
credential was observed, but several bodies cross real authority boundaries:
Git push or throwaway-branch capture, issue publication or triage, repository
instruction writes, temporary artifact writes and GUI opening, and
Claude-specific Hook installation. Some also assume named sub-agent features.
These are routing and authorization requirements, not reasons to rewrite the
source body. OpenAI display metadata does not prove cross-Agent portability or
safe implicit activation.

## Gate

The next step is current-revision license, provenance, security, quality,
overlap, redundancy, and shortfall review. Only after that may a disposable CC
Switch preview test exact source registration, collisions, backup, restore,
activation, and foreign-state preservation. Live change still requires a
separate user authorization.
