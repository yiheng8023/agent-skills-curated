---
name: obsidian-vault
description: Search, create, and manage notes in an Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

## Vault location

**On first use**: Check if a vault path has been configured. Look for a `.vault-path` file in the repo root or a `VAULT_PATH` environment variable. If neither exists, ask the user once:

> "Where is your Obsidian vault? Please provide the full path (e.g. `C:\Users\you\Documents\MyVault` or `/home/you/Obsidian/MyVault`)."

Remember the answer for the rest of the session. Do not ask again.

## Structure conventions

This skill assumes a **flat vault** — mostly flat at root level, using links and index notes for organization rather than folders. If the user's vault uses a different structure, ask them to describe it before proceeding.

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Skills Index.md`, `RAG Index.md`)
- **Title case** for all note names
- Prefer links and index notes over folders for organization

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are lists of `[[wikilinks]]`

## Workflows

### Search for notes

```bash
# Search by filename
find "<VAULT_PATH>" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "<VAULT_PATH>" --include="*.md"
```

Or use Grep/Glob tools directly on the vault path.

### Create a new note

1. Use **Title Case** for filename
2. Write content as a self-contained unit of learning
3. Add `[[wikilinks]]` to related notes at the bottom
4. If part of a numbered sequence, use the hierarchical numbering scheme already in use in the vault

### Find related notes (backlinks)

```bash
grep -rl "\[\[Note Title\]\]" "<VAULT_PATH>"
```

### Find index notes

```bash
find "<VAULT_PATH>" -name "*Index*"
```
