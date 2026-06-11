#!/usr/bin/env bash
# SWEBOK v4 Harness - MCP availability precheck (shared)
# Sourced by act-observe-verify.sh, self-heal.sh, browser-use-orchestrator.sh
# Behavior:
#   - Returns 0 (ok) if MCP bridge is available or explicitly enabled
#   - Returns 1 (unavailable) if MCP is required but not available
#   - Emits DSL: AOV/HEAL/ORCH prefix used by caller
# Environment overrides:
#   MCP_BRIDGE_ENABLED=1   - force enable (caller already verified dispatcher)
#   MCP_KNOWN_TOOLS=...    - tool names that confirm availability
#
# Usage: source "$HARNESS_DIR/scripts/lib/mcp_precheck.sh" && mcp_precheck "AOV"

mcp_precheck() {
    local prefix="${1:-MCP}"
    if [[ -n "${MCP_BRIDGE_ENABLED:-}" ]]; then
        return 0
    fi
    if [[ -n "${MCP_KNOWN_TOOLS:-}" ]]; then
        return 0
    fi
    echo "[$prefix] MCP_UNAVAILABLE: cannot emit <MCP_CALL>; set MCP_BRIDGE_ENABLED=1 or MCP_KNOWN_TOOLS=mcp__zai-mcp-server__diagnose_error_screenshot to override" >&2
    return 1
}
