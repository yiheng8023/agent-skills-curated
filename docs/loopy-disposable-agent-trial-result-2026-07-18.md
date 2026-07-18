# Loopy Disposable Agent Trial Result (2026-07-18)

## Decision

The exact-pinned Loopy body is retained as **reference-only and is not
admitted**. It behaved correctly and proportionately in the bounded trial, but
did not show a material benefit over both native reasoning and the current
adaptive contract chain. No candidate body was modified, vendored, installed,
or written into a live Agent, configuration, or Hook.

## Bound Trial

- Candidate: `github:Forward-Future/loopy` at
  `75966cbd572a4185064971c9fe5e9c52e8f8456d`.
- Exact Skill blob: `5fe3082a41521c1e5793d1a271990bc841c9a92f`.
- Host/model: Codex CLI 0.144.5 on Windows, `gpt-5.6-sol`, medium reasoning.
- Arms: native, current adaptive chain, and exact Loopy body.
- Scenarios: reversible iterative local repair and a one-shot negative control.
- Repetitions: two per cell, for 12 formal fresh ephemeral Agent tasks.
- Boundary: no network task action, installation, persistence, publication,
  live configuration, Hook mutation, or external action.

The first launch attempt was excluded because the shared child-Agent sandbox
was read-only and blocked the acceptance command. A hard environment preflight
then proved patch writing and local Python execution before the formal matrix
started. This failed attempt is retained only as hashed method evidence and is
not scored.

## Results

All 12 formal runs were correct. All 12 returned complete receipts, honest
terminal states, and preserved the authority boundary. Neither Loopy run on
the one-shot task selected a loop, so the false-positive loop count is zero.
The proportional current-chain arm selected its permitted native/no-Skill path
in all four runs and did not open an installed contract Skill body; this is a
measured routing outcome, not an assumption that the bodies executed.

| Scenario | Arm | Correct | Mean seconds | Mean commands | Mean input tokens | Mean output tokens |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Iterative repair | Native | 2/2 | 56.901 | 4.0 | 189,311.5 | 1,516.0 |
| Iterative repair | Current chain | 2/2 | 64.153 | 4.5 | 195,651.0 | 1,998.5 |
| Iterative repair | Loopy exact body | 2/2 | 59.028 | 3.5 | 201,975.5 | 1,867.5 |
| One-shot control | Native | 2/2 | 23.311 | 1.0 | 60,370.0 | 461.0 |
| One-shot control | Current chain | 2/2 | 24.039 | 1.0 | 60,556.0 | 562.5 |
| One-shot control | Loopy exact body | 2/2 | 22.808 | 1.0 | 68,490.0 | 537.5 |

For iterative repair, Loopy was 3.738% slower than native and 7.989% faster
than the current chain, while using 6.69% and 3.233% more input tokens,
respectively. For the one-shot control it was only 2.158% faster than native
and 5.121% faster than the current chain, while using 13.45% and 13.102% more
input tokens. These trade-offs do not satisfy the predeclared rule requiring a
material benefit over **both** baselines at proportionate cost.

## Evidence And Limits

The checked-in machine result contains only compact metrics, hashes, boundaries,
and the disposition. Raw Agent JSONL, final receipts, and disposable workspaces
remain local and are not checked into the repository. The formal raw result is
62,808 bytes with SHA-256
`5608D775FD26F9CBB50A74FBDAEF80D745C3651A7E237CCCBFF351B0EA492D35`.

This is one Windows host, one model, one reasoning effort, two scenario
families, and two repetitions per cell. The CLI exposed the same ambient Skill
inventory to all arms and had no supported inventory-disable flag. The result
therefore supports only this bounded reference-only disposition; it does not
prove cross-Agent, cross-model, or production superiority.

The next gate is to bind another source-supported demand lane. Loopy should be
rechecked only after a material upstream change or contrary demand evidence.
