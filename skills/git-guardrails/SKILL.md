---
name: git-guardrails
description: Set up hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Works in any agent environment or manual terminal workflow. Use when the user wants to prevent destructive git operations or add git safety guardrails.
---

# Setup Git Guardrails

Sets up hooks that intercept and block dangerous git commands before they execute — whether triggered by an agent, a human, or any other tool.

Two complementary layers are available. Use one or both:

| Layer | Mechanism | Who it stops |
|---|---|---|
| **Git native hooks** (primary, universal) | Scripts in `.git/hooks/` or global git hooks path | Any caller — agent, human, CI, any tool |
| **Agent PreToolUse hooks** (optional, agent-specific) | Agent's own pre-execution interception config | Only commands the agent issues via its Bash/shell tool |

The git native hook layer is recommended as the foundation because it is unconditionally universal.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd`
- `git branch -D`
- `git checkout .` / `git restore .`

When blocked, the caller sees a BLOCKED message and the command exits with a non-zero code.

## Steps

### 1. Ask scope

Ask the user: protect **this project only** or **all git repos globally**?

- **Project**: hooks go in `.git/hooks/` of the current repo
- **Global**: hooks go in `~/.config/git/hooks/` (requires one-time git config)

### 2. Write the blocker script

Create `block-dangerous-git.sh` at the chosen location:

**Project**: `.git/hooks/block-dangerous-git.sh`
**Global**: `~/.config/git/hooks/block-dangerous-git.sh`

```bash
#!/bin/sh
# block-dangerous-git.sh — blocks destructive git commands
# Works as a git hook, an agent PreToolUse hook, or a shell wrapper.
CMD="$*"
case "$CMD" in
  *"reset --hard"*|*"clean -f"*|*"branch -D"*|*"checkout ."*|*"restore ."*)
    echo "BLOCKED: '$CMD' is not permitted. Run manually if you are sure." >&2
    exit 2
    ;;
  *"push"*)
    echo "BLOCKED: 'git push' is not permitted. Push manually after review." >&2
    exit 2
    ;;
esac
exit 0
```

Make it executable:

```bash
chmod +x <path>/block-dangerous-git.sh
```

### 3. Install as a git native hook

**Project scope** — create `.git/hooks/pre-push`:

```bash
#!/bin/sh
exec "$(git rev-parse --show-toplevel)/.git/hooks/block-dangerous-git.sh" "push $*"
```

Also create `.git/hooks/pre-auto-gc` or use a `command.alias` approach for `reset`/`clean`/`branch` if full coverage is needed. At minimum, `pre-push` covers the most destructive common case.

Make hooks executable with `chmod +x`.

**Global scope** — point git at the hooks directory:

```bash
mkdir -p ~/.config/git/hooks
git config --global core.hooksPath ~/.config/git/hooks
# Then copy block-dangerous-git.sh there and create pre-push as above
```

### 4. (Optional) Add agent-specific PreToolUse hook

If your agent supports pre-execution interception, add a second layer for defence in depth:

**Claude Code** — add to `.claude/settings.json` (project) or `~/.claude/settings.json` (global):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "<absolute-path-to>/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Other agents**: consult your agent's documentation for an equivalent pre-execution or tool-interception hook mechanism and configure accordingly.

### 5. Ask about customisation

Ask if the user wants to add or remove patterns from the blocked list. Edit the script accordingly.

### 6. Verify

Test the script directly:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
# Should exit 2 with a BLOCKED message
```

Test the git native hook with a dry-run:

```bash
git push --dry-run 2>&1 | head -5
# Should be intercepted before reaching the remote
```
