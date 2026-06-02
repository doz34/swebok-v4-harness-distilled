# Uninstall the SWEBOK v4 Harness

This document describes how to safely remove the harness from a Claude Code installation.

## Step 1 — Restore your original Claude Code settings

The installer always writes a timestamped backup at `~/.claude/settings.json.bak.<ts>` before merging the harness hooks. To restore:

```bash
# List backups (newest first)
ls -lt ~/.claude/settings.json.bak.* | head -5

# Restore the most recent pre-install backup
cp ~/.claude/settings.json.bak.<ts> ~/.claude/settings.json
```

If you have no backup (rare, or the installer was interrupted), you can manually remove the harness entries from `~/.claude/settings.json`:

```bash
# Use jq to strip the harness hooks (keeps your other hooks intact)
jq '
.hooks.PreToolUse = ((.hooks.PreToolUse // []) | map(select(.hooks[0]? | test("swebok-v4-harness") | not)))
| .hooks.PostToolUse = ((.hooks.PostToolUse // []) | map(select(.hooks[0]? | test("swebok-v4-harness") | not)))
| .permissions.allow = ((.permissions.allow // []) | map(select(test("swebok-v4-harness") | not)))
| del(.env.HARNESS_DIR)
' ~/.claude/settings.json > /tmp/settings.json.new
mv /tmp/settings.json.new ~/.claude/settings.json
```

## Step 2 — Remove the state DB (optional)

The harness's runtime state lives in `<HARNESS_DIR>/.swebok_state.db` plus its WAL/SHM sidecars and `.bak.*`/`.corrupt.*` archive copies. To remove them:

```bash
cd /path/to/swebok-v4-harness
rm -f .swebok_state.db .swebok_state.db-wal .swebok_state.db-shm
rm -f .swebok_state.db.bak.* .swebok_state.db.corrupt.* .swebok_state.db.pre-rebuild.*
```

If you want to keep an audit forensic trail, **archive** these files first (`tar czf swebok-audit-$(date +%s).tar.gz .swebok_state.db*`) before removing.

## Step 3 — Remove the harness source

```bash
# OPTIONAL — delete the harness clone if you no longer want the source
rm -rf /path/to/swebok-v4-harness
```

## Step 4 — Restart Claude Code

Reload Claude Code (kill the current process and restart) so it re-reads `~/.claude/settings.json` with the harness entries removed.

## Verification

```bash
# Should NOT contain swebok-v4-harness
grep -i swebok ~/.claude/settings.json || echo "OK: harness fully unwired"

# Should NOT have HARNESS_DIR env var
jq '.env.HARNESS_DIR // "absent"' ~/.claude/settings.json
```

## Recovery (in case uninstall went wrong)

If Claude Code becomes unresponsive after editing `settings.json`, the file may be malformed JSON. Restore the most recent valid backup:

```bash
ls -lt ~/.claude/settings.json.bak.* | head -1
cp ~/.claude/settings.json.bak.<latest> ~/.claude/settings.json
```

If no backup exists, you can reset to a minimal config:

```bash
cat > ~/.claude/settings.json <<'EOF'
{
  "permissions": { "allow": [], "deny": [] },
  "hooks": { "PreToolUse": [], "PostToolUse": [] },
  "env": {}
}
EOF
```

## Reporting issues

If the uninstall procedure fails or leaves residual state, file an issue with the output of:
- `cat ~/.claude/settings.json | jq .`
- `ls -la <HARNESS_DIR>/.swebok_state.db*`
- `find ~/.claude -name 'swebok*' 2>/dev/null`
