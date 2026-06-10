#!/bin/bash
#==========================================
# SWEBOK v4 Harness - Installation Script
# AUDIT-2026-06-01 rewrite: MERGE not OVERWRITE.
#
# Previous installer destructively wrote ~/.claude/settings.json,
# wiping ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN, hook wiring, and
# every other user setting. This rewrite uses jq to merge.
#==========================================

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

# Colors (with TTY check so the output is clean when piped)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' NC=''
fi

echo "🔧 SWEBOK v4 Harness Installer"
echo "=============================="
echo

# Validate harness root
for required in CLAUDE.md lib/state_engine.py pre-tool-use/phase-guard.sh; do
    if [[ ! -e "$HARNESS_DIR/$required" ]]; then
        echo -e "${RED}Error: harness directory missing $required${NC}"
        echo "Run this script from inside a valid swebok-v4-harness checkout."
        exit 1
    fi
done
echo -e "${GREEN}✓${NC} Validated harness at $HARNESS_DIR"

# Require jq for safe merge
if ! command -v jq >/dev/null 2>&1; then
    echo -e "${RED}Error: jq is required for safe settings merge.${NC}"
    echo "Install it (apt-get install jq / brew install jq) and re-run."
    exit 1
fi

mkdir -p "$CLAUDE_DIR"

# Confirmation: warn the user before touching settings.json
if [[ -f "$SETTINGS_FILE" ]]; then
    echo -e "${YELLOW}⚠${NC}  Existing settings.json found at $SETTINGS_FILE"
    echo "    This installer will MERGE the harness hook wiring into your"
    echo "    existing config. Your ANTHROPIC_*, env, permissions, mounts,"
    echo "    and existing hook entries are preserved."
    echo
    if [[ -z "${HARNESS_INSTALL_YES:-}" ]]; then
        read -p "    Continue? [y/N] " -n 1 -r reply
        echo
        if [[ ! "$reply" =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
    backup_path="$SETTINGS_FILE.bak.$(date +%s)"
    cp "$SETTINGS_FILE" "$backup_path"
    echo -e "${GREEN}✓${NC} Backed up existing settings to $backup_path"
else
    echo '{}' > "$SETTINGS_FILE"
fi

# The harness's own hook entries — these are what we merge into the user file.
read -r -d '' HARNESS_HOOKS_FRAGMENT <<JSON || true
{
  "permissions": {
    "allow": [
      "bash $HARNESS_DIR/scripts/swebok-bootstrap.sh",
      "bash $HARNESS_DIR/scripts/adversarial-gate.sh",
      "bash $HARNESS_DIR/scripts/validate-gates.sh",
      "bash $HARNESS_DIR/scripts/validate-qa-gates.sh",
      "bash $HARNESS_DIR/scripts/act-observe-verify.sh",
      "bash $HARNESS_DIR/scripts/self-heal.sh",
      "bash $HARNESS_DIR/scripts/browser-use-orchestrator.sh",
      "bash $HARNESS_DIR/scripts/multiagent-launcher.sh",
      "bash $HARNESS_DIR/scripts/skill-invoker.sh",
      "python3 $HARNESS_DIR/scripts/compiled_knowledge.py",
      "python3 $HARNESS_DIR/generate-kg.py",
      "python3 $HARNESS_DIR/intent-detector.py",
      "python3 $HARNESS_DIR/generate-ka-index.py",
      "python3 $HARNESS_DIR/generate-keyword-index.py",
      "python3 $HARNESS_DIR/search-knowledge-base.py"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|NotebookEdit",
        "hooks": ["bash $HARNESS_DIR/pre-tool-use/phase-guard.sh"]
      },
      {
        "matcher": "Bash",
        "hooks": ["bash $HARNESS_DIR/pre-tool-use/bash-guard.sh"]
      },
      {
        "matcher": "Skill|Task|Agent|WebFetch|WebSearch",
        "hooks": ["bash $HARNESS_DIR/pre-tool-use/phase-guard.sh"]
      },
      {
        "matcher": "mcp__.*|Glob|Grep|LS|TodoWrite|NotebookRead|ExitPlanMode",
        "hooks": ["bash $HARNESS_DIR/pre-tool-use/phase-guard.sh"]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|NotebookEdit",
        "hooks": ["bash $HARNESS_DIR/hooks/post-tool-use/auto-verify.sh"]
      },
      {
        "matcher": "Skill|Task|Agent|WebFetch|WebSearch",
        "hooks": ["bash $HARNESS_DIR/hooks/post-tool-use/auto-verify.sh"]
      },
      {
        "matcher": "Read",
        "hooks": ["bash $HARNESS_DIR/hooks/post-tool-use/auto-verify.sh"]
      }
    ]
  },
  "env": {
    "HARNESS_DIR": "$HARNESS_DIR",
    "MULTIAGENT_BRIDGE_ENABLED": "0"
  }
}
JSON

# Validate that the fragment parses
echo "$HARNESS_HOOKS_FRAGMENT" | jq empty 2>/dev/null || {
    echo -e "${RED}Internal error: harness hooks fragment did not parse as JSON.${NC}"
    exit 1
}

# Merge: existing settings on the LEFT, harness fragment on the RIGHT,
# but DON'T overwrite top-level "env", "permissions.allow", existing hooks
# — instead, union/concat them so the user keeps their config.
#
# jq strategy:
#   .permissions.allow = (existing union harness, dedup by string)
#   .env merged shallowly (existing keys win unless absent)
#   .hooks.PreToolUse = existing ++ harness (concat; dups removed by matcher+hook)
merged=$(jq -n \
    --argjson existing "$(cat "$SETTINGS_FILE")" \
    --argjson harness "$HARNESS_HOOKS_FRAGMENT" '
def uniq_strings: . // [] | unique;
def merge_hook_array(a; b):
    ((a // []) + (b // []))
    | unique_by(.matcher);
$existing
| .permissions.allow = (((.permissions.allow // []) + ($harness.permissions.allow // [])) | unique)
| .permissions.deny = (.permissions.deny // [])
| .env = ((($harness.env // {}) ) + (.env // {}))   # existing env wins
| .hooks.PreToolUse  = merge_hook_array(.hooks.PreToolUse;  $harness.hooks.PreToolUse)
| .hooks.PostToolUse = merge_hook_array(.hooks.PostToolUse; $harness.hooks.PostToolUse)
')

echo "$merged" | jq . > "$SETTINGS_FILE"
echo -e "${GREEN}✓${NC} Merged harness hooks into $SETTINGS_FILE"
echo

echo "✅ Installation complete."
echo
echo "Next steps:"
echo "  1. Restart Claude Code so the merged settings.json is loaded."
echo "  2. Verify with: jq '.hooks.PreToolUse | length' ~/.claude/settings.json"
echo "  3. To undo: cp $backup_path $SETTINGS_FILE (if applicable)"
echo "  4. Opt-in council bridge: export MULTIAGENT_BRIDGE_ENABLED=1 then run"
echo "       bash \$HARNESS_DIR/scripts/adversarial-gate.sh --council P5 P6"
echo "     See OPERATIONS.md §12 and ADR-003-multiagent-bridge.md."
echo
echo "To uninstall, see UNINSTALL.md (planned)."
