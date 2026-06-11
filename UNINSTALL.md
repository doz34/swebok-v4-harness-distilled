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
# Use jq to strip the harness hooks (keeps your other hooks intact).
# The harness wires:
#   - PreToolUse / PostToolUse / UserPromptSubmit:  `bash ${HARNESS_DIR}/<hook>` paths
#   - permissions.allow:                              `bash scripts/<tool>` and `python3 scripts/<tool>` paths
#   - env.HARNESS_DIR:                                the harness root
#
# Pipe the filter through `jq` (or save to a file and use `jq -f`).
cat > /tmp/swebok-uninstall.jq <<'EOF'
.hooks.PreToolUse        |= map(select((.hooks // []) | map(test("\\$\\{HARNESS_DIR\\}")) | any | not))
| .hooks.PostToolUse     |= map(select((.hooks // []) | map(test("\\$\\{HARNESS_DIR\\}")) | any | not))
| .hooks.UserPromptSubmit |= map(select((.hooks // []) | map(test("\\$\\{HARNESS_DIR\\}")) | any | not))
| .permissions.allow     |= map(select(test("scripts/(swebok-|adversarial-gate|multiagent-launcher|validate-gates|validate-qa-gates|act-observe-verify|self-heal|browser-use-orchestrator|skill-invoker|generate-kg|generate-ka-index|generate-keyword-index|search-knowledge-base|intent-detector)") | not))
| del(.env.HARNESS_DIR)
EOF
jq -f /tmp/swebok-uninstall.jq ~/.claude/settings.json > /tmp/settings.json.new
mv /tmp/settings.json.new ~/.claude/settings.json
rm -f /tmp/swebok-uninstall.jq
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
# Should NOT contain any ${HARNESS_DIR}/... hook paths
grep -F '${HARNESS_DIR}/' ~/.claude/settings.json && echo "FAIL: harness hooks still wired" || echo "OK: no HARNESS_DIR hooks"

# Should NOT contain any harness permission entries (bash/python3 scripts/...)
grep -E '(bash|python3) scripts/(swebok-|adversarial-gate|multiagent-launcher|generate-kg|generate-ka|generate-keyword|search-knowledge-base|intent-detector)' ~/.claude/settings.json && echo "FAIL: harness permissions still present" || echo "OK: no harness permissions"

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
