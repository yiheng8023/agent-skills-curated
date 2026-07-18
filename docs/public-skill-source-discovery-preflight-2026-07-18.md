# Public Skill Source Discovery And Balanced Preflight

Date: 2026-07-18
State: verified public-metadata discovery; no candidate approved
Machine evidence:
`registry/public-skill-source-discovery-preflight-2026-07-18.json`

## Outcome

Ten explicit `is:public` GitHub queries produced 188 unique source records. A
balanced strategy selected at least two results per query before filling by
global rank. All 20 selected sources received an immutable revision and a
successful recursive-tree preflight: 14 multi-Skill suites, one single-Skill
source, five sources with no detected `SKILL.md`, and six sources with a
separate Agent Hook surface.

This fixes two weaknesses in the earlier generic discovery path: authenticated
search can no longer mix private metadata because every query must declare
`is:public`, and low-star shortfall-focused sources are no longer displaced by
globally popular but unrelated repositories.

The raw 234,083-byte capture was not added to the repository. Its SHA-256 is
`AA7945430DF45A4111C71F88F43D2DC47C1CCADF401ED3D9426E86C12E105E13`.
The durable machine projection preserves all 188 source IDs, all query counts,
and the 20 source-pinned preflight records.

## Preflight Result

The preflight rejects whole-source reasoning. Large collections such as ECC,
Ruflo, and agentic-awesome-skills require component-level provenance,
atomicity, overlap, redundancy, security, and update review. Skill presence
does not approve bundled Hooks. CC Switch is retained as an operational manager
baseline rather than misclassified as a Skill source, while ordinary query
noise with no `SKILL.md` is excluded from the current Skill lane.

Five sources advance only to non-executing static review:

- `Forward-Future/loopy`: small adaptive-loop suite;
- `cbcraftlab/governed-skill-tree`: shortfall-aligned governance suite;
- `sanjay3290/ai-skills`: cross-Agent suite;
- `diet103/claude-code-infrastructure-showcase`: host-specific auto-activation
  and Hook suite;
- `mksglu/context-mode`: context, memory, routing, MCP, and Hook system with an
  unresolved license classification and a large executable surface.

Advancement means only that metadata and structure justify reading pinned
public source text next. It is not a quality, superiority, coverage, adoption,
download, execution, installation, or Hook decision.

## Shortfall And Standardization Boundary

Candidate links to STM/P coordinates are hypotheses derived from descriptions
and structure. They do not prove that a source fixes a shortfall, outperforms a
native path, or provides positive net value. Static review must compare each
candidate with native, official, runtime, installed, composed, no-Skill, and
no-Hook alternatives.

The current query fields, selection rules, Harness modes, and preflight checks
remain correctable working hypotheses and observation protocols. Hard
standardization is deferred; they are not hard standards. Eligibility starts
only after stable value repeats across independent
sources, Agents or hosts, task classes, and real feedback cycles, with benefit
greater than context, control, and maintenance cost and with separate adoption
authority.

## Authority Boundary

No source body was vendored, no candidate was executed or installed, no Hook or
consumer configuration was changed, no source was approved, no residual gap was
proven, and no repository-authored Skill, Hook, or hard standard became
eligible. The next gate is source-pinned static license, provenance, security,
portability, atomicity, overlap, redundancy, and Hook-separation review for the
five-source batch.
