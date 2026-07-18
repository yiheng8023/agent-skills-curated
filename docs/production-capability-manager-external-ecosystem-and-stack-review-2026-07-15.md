# Production Capability Manager External Ecosystem And Stack Review

## Status And Method

- Date: 2026-07-15
- State: decision support recorded
- Mode: read-only official documentation and source-pinned public repository metadata
- Side effects: no candidate installed, executed, vendored, forked, or enabled

This review tests whether the accepted independent Manager node still has a
real residual job after mature external work is reused. Stars and recency are
discovery signals only; they are not quality, safety, license, or admission
proof.

## External Baseline

The open Agent Skills format standardizes a portable `SKILL.md` folder and
progressive discovery, activation, and execution. It does not define curated
admission, local ownership arbitration, transaction rollback, or a broad
capability control plane.

The official MCP Registry is a metadata and namespace layer. Its own contract
delegates code security to package registries and downstream curators and says
host applications should normally consume downstream aggregators. Therefore
registry visibility is candidate metadata, never execution approval.

## Mature Work To Reuse

| Source | Pinned revision | Best reusable value | Current disposition |
| --- | --- | --- | --- |
| `vercel-labs/skills` | `5527c09...` | multi-Agent source parsing, path mapping, add/list/find/update/remove/use | adapter or upstream-library candidate; license must be resolved before code reuse |
| `farion1231/cc-switch` | `f6e37ed...` | mature Tauri/Rust multi-Agent, provider, MCP, and Skill manager evidence | adjacent-manager reference and observed integration; foreign owner |
| `yibie/skills-manager` | `69e81e0...` | native macOS UX | UX reference only |
| `cchao123/skills-manager` | `f5ab5fb...` | cross-platform Tauri Skill manager | reference pending deeper telemetry review |
| `beautyfree/skiller` | `43a3683...` | file watch, SQLite, Git, multi-Agent desktop UX | Electron reference only |
| `mcp360/mTarsier` | `8f14301...` | combined MCP and Skill management | broad-ecosystem reference only |
| `stakpak/paks` | `117ae77...` | Agent Skills package-management patterns | adapter candidate |
| `rohitg00/skillkit` | `d2e5c34...` | portability and conversion across Agents | adapter candidate |

The default integration boundary is a pinned adapter or subprocess contract.
Vendoring or forking is a later governed decision after license, security,
maintenance, and overlap review. Native host installers remain preferable when
they are available, healthy, and sufficient.

## Residual Core That Still Justifies The Manager

External tools materially reduce the amount of code we should write, but they
do not remove the following combined responsibility:

- consume an exact curated release and manifest digest;
- represent native capabilities, Rules, Skills, Hooks, MCP, Plugins, Apps,
  tools, services, project mechanisms, and accountable human authority in one
  ownership-aware graph;
- coexist with user-installed and Agent-installed foreign state;
- evaluate local policy and profiles without a product account;
- preview, lock, back up, apply, verify, roll back, and journal mutations;
- observe runtime drift and emit bounded evidence and retirement decisions.

This is why the independent node remains justified after reuse. The Manager is
an orchestrator over mature package operations and native installers, not a new
generic Skill package manager.

## Stack Recommendation

The recommended core is Rust: a library plus `clap` CLI, SQLite through
`rusqlite`, explicit file-system and host-adapter traits, followed by a
Ratatui TUI. A later Tauri v2 GUI stays a replaceable client over the same
headless transaction core. Tauri's system-webview approach, Rust foundation,
explicit permission/capability model, signing, updater, packaging, and test
surfaces fit the local control-plane boundary, and the strongest adjacent
manager reviewed here already uses this family.

The bounded fallback is Go with Cobra, Bubble Tea, SQLite, and Wails. It may win
if a prototype proves materially faster delivery while preserving equivalent
transaction, migration, permission, and rollback guarantees.

TypeScript/Electron is not the default. It offers fast UI iteration but adds a
larger runtime and dependency surface and is a weaker foundation for the
transaction authority. Telemetry remains absent and off by default in every
option.

## Decision Boundary

The topology placement is accepted. This review recommends, but does not
finally select, the Rust/Ratatui/Tauri route. It does not authorize a new
repository, product implementation, candidate installation or execution,
Hook mutation, cross-repository writes, commit, push, publication, or deploy.

Remaining owner decisions are the final repository slug and branding, and
whether to accept the Rust route directly or first authorize a bounded
Rust-versus-Go transaction-core prototype.
