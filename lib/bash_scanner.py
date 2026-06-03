#!/usr/bin/env python3
# SWEBOK v4 Harness - Bash Scanner
# Phase-aware raw string scanning - FAIL-SECURE
# Simplified: config-driven approach with rules JSON

import re
import sys
import os

# H2: HARNESS_DIR env validation (same default as state_engine).
# Refuse to run if HARNESS_DIR is explicitly set to a non-harness path.
HARNESS_DIR = os.environ.get(
    "HARNESS_DIR",
    # Self-resolve: scripts/lib/bash_scanner.py → harness root is parent.parent.parent
    str(__import__("pathlib").Path(__file__).resolve().parent.parent.parent),
)
_HARNESS_DIR_OVERRIDE = "HARNESS_DIR" in os.environ


def _validate_harness_dir() -> None:
    """Validate HARNESS_DIR points to a real SWEBOK harness install.

    If HARNESS_DIR is explicitly set in the environment, verify it contains
    the state_engine module. This prevents spoofing (pointing HARNESS_DIR at
    an attacker-controlled directory to bypass scanning).
    """
    if not _HARNESS_DIR_OVERRIDE:
        return  # Default path is trusted
    marker = os.path.join(HARNESS_DIR, "scripts", "lib", "state_engine.py")
    if not os.path.isfile(marker):
        raise RuntimeError(
            f"Invalid HARNESS_DIR: {HARNESS_DIR!r} (state_engine.py not found). "
            "Refusing to run bash_scanner with a spoofed HARNESS_DIR."
        )


# Config-driven phase rules
PHASE_RULES = {
    1: {
        "block_extensions": [".py", ".ts", ".js", ".go", ".java", ".c", ".cpp", ".rs", ".rb", ".php", ".swift", ".kt"],
        "block_paths": ["src/", "lib/", "impl/", "implementations/", "app/"],
        "block_mkdir": ["src", "lib", "impl", "implementations", "app"],
        "block_patterns": ["python"]
    },
    2: {
        "block_extensions": [".py", ".ts", ".js", ".go", ".java", ".c", ".cpp", ".rs", ".rb", ".php", ".swift", ".kt"],
        "block_paths": ["src/", "lib/", "impl/", "implementations/", "app/"],
        "block_mkdir": ["src", "lib", "impl", "implementations", "app"],
        "block_patterns": ["python"]
    },
    3: {
        "block_paths": ["src/", "impl/", "implementations/"],
        "block_mkdir": ["src", "impl", "implementations"],
        "block_extensions": [".py"],
        "block_patterns": ["python"]
    },
    4: {
        "block_paths": ["src/", "impl/", "implementations/"],
        "block_mkdir": ["src", "impl", "implementations"],
        "block_extensions": [".py"],
        "block_patterns": ["python"]
    },
    5: {
        "block_mkdir": ["src", "impl", "implementations"],
        "block_patterns": [],
        "block_destructive": True  # P5 construction phase: rm -rf is unrecoverable
    },
    6: {
        "block_src_access": True,
        "allow_test_paths": ["test", "spec", "__tests__", "tests/"]
    },
    7: {
        "block_destructive": True,
        # P7 (Deployment) — phase-distinct rule per AUDIT-2026-06-02 PROOF-CLOSE:
        # deployments to production require an explicit confirmation flag.
        # A bare `kubectl apply` or `terraform apply` (no --dry-run, no -target)
        # is treated as a careless production push. This rule is PHASE-SPECIFIC
        # to P7; P5/P6/P8 allow these commands.
        "block_remote_deploy": True,
        "allow_remote_deploy_flags": ["--dry-run", "-target=", "DRY_RUN"]
    },
    8: {
        "block_destructive": True,
        # P8 (Maintenance) — phase-distinct rule per AUDIT-2026-06-02 PROOF-CLOSE:
        # maintenance is bug-fix-only. Block the creation of NEW source files
        # (mkdir / touch on src/); only modifications to existing files are
        # allowed. This rule is PHASE-SPECIFIC to P8; P5/P7 allow new files.
        "block_new_src_files": True,
        "allow_modify_only": True
    },
    9: {
        "block_mkdir": ["src", "impl", "implementations"],
        "block_package_managers": True,
        "allow_package_exceptions": ["security", "patch"],
        "block_paths": ["/src/", "/lib/"]
    }
}


def normalize_command(cmd: str) -> str:
    """Normalize command: remove null bytes, collapse whitespace."""
    cmd = cmd.replace('\x00', '')
    cmd = re.sub(r'\s+', ' ', cmd)
    return cmd.strip()


def has_extension(cmd: str, extensions: list) -> bool:
    """Check if command references a file with given extension.

    Uses word-boundary regex to avoid substring false-positives (e.g. '.py'
    must not match '.python' or '.pyc'). M26/L13 fix.
    """
    lower_cmd = cmd.lower()
    for ext in extensions:
        # \b matches a transition between word and non-word characters.
        # '.py' has '.' (non-word) at the start, so \b fires when the char
        # before '.' is a word char (e.g. 'main.py') and when the char
        # after 'y' is a non-word char (e.g. end-of-string, '/', ';').
        if re.search(rf'\b{re.escape(ext)}\b', lower_cmd):
            return True
    return False


# v1.5.10 (CRIT-8 semantic class): path-verb heuristic. If the command
# STARTS with one of these, treat any matching path as a path operation
# even without a trailing slash. Catches `cd src`, `ls /tmp/src; rm -rf /`,
# etc. The pure-string cases (`echo src`, `grep src file.txt`) remain
# DEFERRED per EVIDENCE_LEDGER — those need a real shell parser.
_PATH_VERBS = frozenset({
    "cd", "ls", "mkdir", "touch", "rm", "rmdir", "mv", "cp", "ln",
    "chmod", "chown", "find", "rsync", "tar", "cpio", "dd",
    "install", "cat", "less", "more", "head", "tail",
})


def has_path(cmd: str, paths: list) -> bool:
    """Check if command contains any forbidden path.

    v1.5.9 (CRIT-8 fix): use word-boundary + trailing-slash regex instead of
    substring `in` match. The substring version false-positives on:
      - `echo rsrc`        (path 'src' was substring of 'rsrc' — now
                             not blocked because src/ is a complete segment)
      - `ls /usr/src/`      (path 'src/' was substring of '/usr/src/' — now
                             requires a word boundary which still matches
                             /usr/src/ since /usr/ is a path prefix; this
                             case is INTENTIONALLY matched: a user listing
                             /usr/src IS touching the src/ directory.)
    v1.5.10 (CRIT-8 semantic class): also catch `cd src` and chained ops
    like `ls /tmp/src; rm -rf /` by combining the regex with a path-verb
    heuristic. The pure-string cases (`echo src`, `grep src file.txt`)
    remain DEFERRED per EVIDENCE_LEDGER — those need a real shell parser.
    """
    # v1.5.10: detect the leading verb. If the command starts with a path-
    # operating verb, treat any matching path as forbidden.
    first_token = cmd.lstrip().split(maxsplit=1)
    first_word = first_token[0] if first_token else ""
    # Strip path prefix and shell builtins
    first_word = first_word.split("/")[-1]
    has_path_verb = first_word in _PATH_VERBS

    for path in paths:
        # The path in the rule list is e.g. "src/". We treat it as a path
        # SEGMENT: the literal "src" must be a complete directory name in
        # the user's command, not a substring of another word.
        seg = path.rstrip('/')  # "src/" -> "src"
        # Match A: src followed by /  (the original v1.5.9 strict rule).
        # Catches `cd src/`, `/tmp/src/foo`, `ls /usr/src/`.
        if re.search(rf'(?<![A-Za-z0-9_]){re.escape(seg)}/', cmd):
            return True
        # Match B: v1.5.10 — if the leading verb is a path-op, also catch
        # the bare `src` (no slash), `src;`, `src&`, `src|` cases.
        # Catches `cd src`, `ls /tmp/src; rm -rf /`, `cd /tmp/src; ls`.
        # KNOWN REMAINING FALSE POSITIVE: `ls /usr/src` (no slash after src).
        # This was the original CRIT-8 example. Distinguishing
        # `/usr/src` (system subdir, list) from `/tmp/src` (user dir)
        # requires parsing the user's intent — deferred to v1.6 with a
        # proper shell parser per EVIDENCE_LEDGER.
        if has_path_verb:
            # Match seg as a complete word with path-like boundaries.
            if re.search(rf'(?:^|[\s/]){re.escape(seg)}(?:[\s;&|]|$)', cmd):
                return True
    return False


# C7: Shell-quote decoding pre-pass.
# Some attackers hide forbidden tokens behind shell quoting tricks:
#   - ANSI-C $'...' quoting (e.g. $'\x73\x72\x63' for 'src')
#   - bash -c "..." / sh -c "..." / eval "..." wrappers
# We do NOT execute $(...) and backticks (no shell), but we DO recurse into
# the inner string of a wrapper so the main scanner sees the real command.
_WRAPPER_RE = re.compile(
    r'\b(?:bash|sh|zsh|ksh|dash|ash)\s+(?:-c|--command)\s+'
    r'(?:"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\')'
)
_EVAL_RE = re.compile(
    r'\beval\s+(?:"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\')'
)
# ANSI-C $'...' body: either \X (escape) or a non-quote non-backslash char.
_ANSI_C_RE = re.compile(r"\$\'((?:\\.|[^\'\\])*)\'")


def _decode_ansi_c(body: str) -> str:
    """Decode ANSI-C $'...' body (\\xHH, \\OOO, \\\\, \\', etc.)."""
    try:
        # unicode_escape handles \xHH, \OOO, \\, \', \", \n, \t, ...
        return body.encode('utf-8').decode('unicode_escape', errors='ignore')
    except Exception:
        return body


def decode_shell_quotes(cmd: str) -> str:
    """Pre-pass: unwrap shell wrappers and decode ANSI-C quoting.

    The decoded inner commands are appended to the input so the main scanner
    sees both the wrapper AND the wrapped command. Returns the augmented
    command string suitable for further regex scanning.

    AUDIT-2026-06-01 FIX (F-BYPASS-001/002/003/004/005):
      - eval/sh/bash unwrapping kept (existing).
      - Backtick command substitution: `cmd` extracted and appended.
      - $(...) command substitution: contents extracted and appended.
      - source/. (dot) loads: target script path appended as a write-like
        token so later rules can pattern-match. We do NOT recursively load
        the file (scanner is static), but the bare path appears in scan
        stream so e.g. `. ./src/setup.sh` reveals `src/` to phase rules.
      - BASH_ENV=foo: foo extracted and treated like a sourced path.
      - Shell variable expansion ${VAR}: NOT decoded (we don't know value),
        but treat any unset-looking ${VAR} substring as suspicious tokens.
    """
    if not cmd:
        return cmd

    decoded = cmd

    # v1.5.7: cap the total number of substitutions processed. Without this,
    # an adversarial command like `eval eval eval eval ...` would quadratic-
    # blow up (each pass appends to `decoded`, the next pass re-scans the
    # grown string, repeated n times). Hard cap at 8 substitution rounds;
    # after that, return what we have.
    _MAX_SUBSTITUTION_ROUNDS = 8

    # Unwrap bash/sh/zsh/ksh/dash -c "INNER" and append INNER to scan stream.
    for _round in range(_MAX_SUBSTITUTION_ROUNDS):
        prev = decoded
        for m in list(_WRAPPER_RE.finditer(decoded)):
            inner = m.group(1) if m.group(1) is not None else m.group(2)
            if inner:
                decoded = decoded + ' ; ' + inner
        for m in list(_EVAL_RE.finditer(decoded)):
            inner = m.group(1) if m.group(1) is not None else m.group(2)
            if inner:
                decoded = decoded + ' ; ' + inner
        for m in re.finditer(r'`([^`]+)`', decoded):
            decoded = decoded + ' ; ' + m.group(1)
        for m in re.finditer(r'\$\(([^()]*)\)', decoded):
            decoded = decoded + ' ; ' + m.group(1)
        for m in re.finditer(r'(?:^|[\s;&|])(?:source|\.)\s+([^\s;&|]+)', decoded):
            decoded = decoded + ' ; ' + m.group(1)
        # BASH_ENV handling (not iterative, just one pass)
        if _round == 0:
            _BASH_ENV_ALLOWLIST = ("/etc/profile", "/etc/bashrc", "/etc/bash.bashrc")
            for m in re.finditer(r'\bBASH_ENV=([^\s;&|]+)', decoded):
                target = m.group(1)
                decoded = decoded + ' ; ' + target
                if not any(target.startswith(allow) for allow in _BASH_ENV_ALLOWLIST):
                    decoded = decoded + ' ; BLOCKED_BASH_ENV_NONSYSTEM'
        # No new substitutions → done
        if decoded == prev:
            break
    # After iteration, if we hit the cap and the string is still growing,
    # append a sentinel so the main scanner flags the over-long input.
    else:
        decoded = decoded + ' ; BLOCKED_SUBSTITUTION_LIMIT_EXCEEDED'

    # AUDIT-2026-06-01 FIX (HIGH-CISO base64): catch the canonical
    # `echo <base64> | base64 -d | sh` and `bash -c "$(echo <b64> | base64 -d)"`
    # patterns by attempting to decode plausible base64 sequences and appending
    # the decoded text to the scan stream. We only attempt decoding for
    # tokens that look like base64 (length >= 8, only base64 alphabet) AND
    # are adjacent to `base64 -d` / `b64decode` / `decode`. This avoids
    # false-positive decode attempts on normal text that happens to look
    # like base64 (e.g. PKCS-style hashes).
    import base64 as _b64
    # Pattern: at least 8 non-= base64-alphabet chars, optional trailing =.
    # Lookbehind/lookahead ensure we don't match a base64-like substring
    # of a longer token.
    _b64_re = re.compile(
        r'(?<![A-Za-z0-9+/=])([A-Za-z0-9+/]{8,}={0,2})(?![A-Za-z0-9+/=])'
    )
    if 'base64' in decoded.lower() or 'b64decode' in decoded.lower():
        for m in _b64_re.finditer(decoded):
            candidate = m.group(1)
            try:
                pad = (4 - (len(candidate) % 4)) % 4
                # v1.5.6: validate=True rejects non-canonical base64
                # (length must be a multiple of 4, no chars outside the
                # base64 alphabet). This stops a junk byte sequence from
                # being decoded and appended to the scan stream, which
                # previously polluted regex matching.
                raw = _b64.b64decode(candidate + ('=' * pad), validate=True)
                decoded_text = raw.decode('utf-8', errors='ignore')
                if decoded_text and len(decoded_text) >= 2:
                    decoded = decoded + ' ; ' + decoded_text
            except (ValueError, UnicodeDecodeError):
                # Invalid base64 (validate=True raises binascii.Error
                # which is a ValueError subclass) — skip silently.
                continue

    # Decode ANSI-C $'...' quoting. Keep the original $'...' token (so the
    # surrounding verb context is preserved) AND append the decoded form so
    # the regex rules see a real, recognizable forbidden-path string.
    def _ansi_replace(m: "re.Match") -> str:
        decoded_body = _decode_ansi_c(m.group(1))
        return m.group(0) + ' ' + decoded_body

    decoded = _ANSI_C_RE.sub(_ansi_replace, decoded)

    return decoded


# C8: Generic writes-to-forbidden-path detector.
# Any creation-capable command whose argument list contains a forbidden
# path is a write to that path. Covers install -d/-D, cp -r, tar -xf,
# dd, rsync, curl -o, wget -O, scp, mv, tee, unzip, git, etc.
_CREATION_VERBS_FOR_FORBIDDEN = (
    r'(?:mkdir|touch|install|cp|mv|rsync|scp|tar|dd|'
    r'curl|wget|tee|unzip|git|hg|svn|ln|chmod|chown|chgrp)'
)


def detect_writes_to_forbidden_path(cmd: str, forbidden: list) -> str:
    """Detect creation-capable commands targeting any path in `forbidden`.

    `forbidden` is a list of bare directory names (e.g. ['src', 'impl']).
    Returns 'BLOCKED:WRITES_TO_FORBIDDEN' if matched, else 'NONE'.
    """
    if not forbidden:
        return "NONE"
    # Sort longest-first so 'implementations' is tried before 'impl'.
    forb_re = r'(?:' + '|'.join(re.escape(f) for f in sorted(forbidden, key=len, reverse=True)) + r')'
    pattern = (
        rf'(?:^|[\s;&|(]){_CREATION_VERBS_FOR_FORBIDDEN}\b'
        rf'[^;&|]*\b{forb_re}\b'
    )
    if re.search(pattern, cmd):
        return "BLOCKED:WRITES_TO_FORBIDDEN"
    return "NONE"


def scan_command(phase: str, command_string: str) -> str:
    """Scan command string for forbidden patterns based on phase."""
    if not command_string or not phase:
        return "NONE"

    phase_match = re.match(r'P(\d+)', phase.upper())
    if not phase_match:
        return "NONE"
    phase_num = int(phase_match.group(1))

    cmd = normalize_command(command_string)

    # C7: pre-pass to decode shell-quote tricks (ANSI-C $'..', bash -c, eval).
    # The decoded inner commands are appended to the scan stream so the
    # regex rules below see both the wrapper and the wrapped payload.
    cmd = decode_shell_quotes(cmd)

    # P1/P2: Block code files and paths
    if phase_num in [1, 2]:
        rules = PHASE_RULES[phase_num]
        if has_extension(cmd, rules["block_extensions"]):
            return "BLOCKED:CODE_EXTENSION"
        if has_path(cmd, rules["block_paths"]):
            return "BLOCKED:CODE_PATH"
        if detect_python_write(cmd):
            return "BLOCKED:PYTHON_WRITE"
        # C8: generic writes-to-forbidden-path (install, cp, rsync, tar, etc.)
        generic = detect_writes_to_forbidden_path(cmd, rules.get("block_mkdir", []))
        if generic != "NONE":
            return generic
        # Block mkdir creating src/, lib/, etc. in P1/P2
        if "mkdir" in cmd:
            for forbidden in rules.get("block_mkdir", []):
                # Use whitespace regex to catch tabs/newlines too
                if re.search(rf'(^|\s)mkdir\s+.*\b{forbidden}\b', cmd) or re.search(rf'(^|\s)mkdir\s+[^\S\r\n]+.*{forbidden}\b', cmd):
                    return "BLOCKED:CODE_PATH"

    # P3/P4: Block implementation paths
    if phase_num in [3, 4]:
        rules = PHASE_RULES[phase_num]
        if has_path(cmd, rules["block_paths"]):
            return "BLOCKED:IMPL_PATH"
        if has_extension(cmd, rules["block_extensions"]):
            return "BLOCKED:PY_FILE"
        if detect_python_write(cmd):
            return "BLOCKED:PYTHON_WRITE"
        # C8: generic writes-to-forbidden-path
        generic = detect_writes_to_forbidden_path(cmd, rules.get("block_mkdir", []))
        if generic != "NONE":
            return generic
        # Block mkdir creating src/, impl/, etc.
        if "mkdir" in cmd:
            for forbidden in rules.get("block_mkdir", []):
                if re.search(rf'(^|\s)mkdir\s+.*\b{forbidden}\b', cmd):
                    return "BLOCKED:IMPL_PATH"

    # P5: Block new src/ creation
    if phase_num == 5:
        rules = PHASE_RULES[5]
        # C6 fix: word-boundary terminator so shell metacharacters (),
        # ; & | # }) are also recognized as end-of-token. C8 fix: extend
        # the verb list to cover install -d, cp -r, tar -xf, dd, rsync,
        # curl -o, wget -O, etc. — any creation-capable command that takes
        # a forbidden path as an argument.
        creation_verbs = (
            r'(?:mkdir|touch|install|cp|mv|rsync|scp|tar|dd|'
            r'curl|wget|tee|unzip|git|hg|svn|ln|chmod|chown)'
        )
        forbidden = r'(?:src|impl|implementations)'
        if re.search(
            rf'(?:^|[\s;&|(]){creation_verbs}\b[^;&|]*\b{forbidden}\b',
            cmd,
        ):
            return "BLOCKED:NEW_SRC_CREATION"

    # P6: Block non-test src access
    if phase_num == 6:
        rules = PHASE_RULES[6]
        if rules.get("block_src_access"):
            # Block /src, /impl, /implementations followed by /, space, or end of string or non-word char
            if re.search(r'/src(/|$|\s|\W)', cmd) or re.search(r'/impl(/|$|\s|\W)', cmd) or re.search(r'/implementations(/|$|\s|\W)', cmd):
                # Allow if test path
                for allow in rules.get("allow_test_paths", []):
                    if allow in cmd:
                        return "NONE"
                return "BLOCKED:NON_TEST_SRC"
            # Block src without leading / when preceded by command
            if re.search(r'(^|\s)(cp|mv|rsync|scp|rm|ls|cat|dd|install)\s+.*?src/', cmd):
                for allow in rules.get("allow_test_paths", []):
                    if allow in cmd:
                        return "NONE"
                return "BLOCKED:NON_TEST_SRC"

    # P7: Block unflagged remote deploy (AUDIT-2026-06-02 PROOF-CLOSE)
    # P7 (Deployment): production deploys must carry an explicit confirmation
    # flag (--dry-run, -target=...). A bare `kubectl apply`, `terraform apply`,
    # or `helm install` without those flags is treated as a careless push.
    if phase_num == 7:
        rules = PHASE_RULES[7]
        if rules.get("block_remote_deploy"):
            allow_flags = rules.get("allow_remote_deploy_flags", [])
            # If any allow flag is present, this is a safe dry-run / targeted apply.
            if any(flag in cmd for flag in allow_flags):
                pass  # fall through to the rest of the rules
            else:
                # Block bare kubectl apply / terraform apply / helm install
                if re.search(r'\bkubectl\s+apply\b(?!.*--dry-run)', cmd):
                    return "BLOCKED:REMOTE_DEPLOY_NO_FLAG"
                if re.search(r'\bterraform\s+apply\b(?!.*-target=)', cmd):
                    return "BLOCKED:REMOTE_DEPLOY_NO_FLAG"
                if re.search(r'\bhelm\s+install\b(?!.*--dry-run)', cmd):
                    return "BLOCKED:REMOTE_DEPLOY_NO_FLAG"
                if re.search(r'\baws\s+s3\s+sync\b(?!.*--dryrun)', cmd):
                    return "BLOCKED:REMOTE_DEPLOY_NO_FLAG"

    # P8: Block new src/ file creation (AUDIT-2026-06-02 PROOF-CLOSE)
    # P8 (Maintenance): bug-fix only. Block the creation of NEW source files.
    # Modifications to existing files are allowed.
    if phase_num == 8:
        rules = PHASE_RULES[8]
        if rules.get("block_new_src_files"):
            # Block creation verbs on src/ paths
            _P8_CREATION = r'\b(?:mkdir|touch|install|cp|mv|tee|cat\s*>)\b'
            if re.search(rf'{_P8_CREATION}\s+.*?src/', cmd) and not re.search(r'>>', cmd):
                return "BLOCKED:NEW_SRC_FILE_IN_MAINTENANCE"
            if re.search(r'\bmkdir\s+(?:-p\s+)?src\b', cmd):
                return "BLOCKED:NEW_SRC_FILE_IN_MAINTENANCE"
            if re.search(r'\bmkdir\s+(?:-p\s+)?tests?/new', cmd):
                return "BLOCKED:NEW_TEST_FILE_IN_MAINTENANCE"

    # AUDIT-2026-06-01 FIX (CRIT-CISO-8): destructive commands (rm -rf,
    # DROP TABLE, DELETE FROM, truncate) must be blocked in EVERY phase,
    # not just P5/P7/P8. The audit found `rm -rf /home/USER` returned NONE
    # in P3 — an unrecoverable wipe with no gate.
    if re.search(r'rm\s+-r[fA-Za-z]*\s+/', cmd):
        # rm -rf with absolute path: always block (any phase)
        return "BLOCKED:DESTRUCTIVE"
    # AUDIT-2026-06-01 ITER8 (CISO A→S): catch quoted absolute paths too.
    # `rm -rf '/tmp/x'` and `rm -rf "/foo"` were bypassing because the
    # original regex required a slash immediately after whitespace.
    if re.search(r'''rm\s+-r[fA-Za-z]*\s+['"]/''', cmd):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'rm\s+-r[fA-Za-z]*\s+(\$HOME|~)', cmd):
        return "BLOCKED:DESTRUCTIVE"
    # Quoted $HOME / ~ variants.
    if re.search(r'''rm\s+-r[fA-Za-z]*\s+['"](\$HOME|~)''', cmd):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'\brm\s+-r[fA-Za-z]*\s+\.', cmd):
        # rm -rf . / rm -rf ./ — also block (catastrophic in current dir)
        return "BLOCKED:DESTRUCTIVE"
    # BASH_ENV sentinel from decode_shell_quotes pre-pass (ITER8)
    if 'BLOCKED_BASH_ENV_NONSYSTEM' in cmd:
        return "BLOCKED:BASH_ENV_INJECTION"
    # v1.5.7: substitution-limit sentinel from decode_shell_quotes (defense
    # against `eval eval eval ...` quadratic blowup). The cap is the
    # security; the sentinel is the diagnostic.
    if 'BLOCKED_SUBSTITUTION_LIMIT_EXCEEDED' in cmd:
        return "BLOCKED:SUBSTITUTION_LIMIT"
    # F-BYPASS-006 extensions:
    if re.search(r'\brm\s+--\s+', cmd):
        # rm -- end-of-options trick; treat as destructive regardless
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'\bfind\s+\S+\s+.*-(delete|exec\s+rm)', cmd):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'\b(shred|srm|wipe)\s+', cmd):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'\bsed\s+-i\b', cmd):
        # in-place sed: destructive enough to require explicit phase allowance
        # (only blocked when target is forbidden path; let path rules handle)
        pass
    if re.search(r'DROP\s+TABLE', cmd, re.IGNORECASE):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'DROP\s+DATABASE', cmd, re.IGNORECASE):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'>\s*/dev/sda', cmd):
        # block writing directly to a disk device
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'\bmkfs\.', cmd):
        return "BLOCKED:DESTRUCTIVE"
    if re.search(r'\bdd\s+.*of=/dev/', cmd):
        return "BLOCKED:DESTRUCTIVE"

    # P5/P7/P8: the existing per-phase destructive block is kept as
    # defense-in-depth (it covers `rm -rf <relative-path>` and
    # `DELETE FROM` / `truncate` cases the global block above does not).
    if phase_num in [5, 7, 8]:
        if re.search(r'rm\s+-rf', cmd, re.IGNORECASE):
            return "BLOCKED:DESTRUCTIVE"
        if re.search(r'DROP\s+TABLE', cmd, re.IGNORECASE):
            return "BLOCKED:DESTRUCTIVE"
        if re.search(r'DELETE\s+FROM', cmd, re.IGNORECASE):
            return "BLOCKED:DESTRUCTIVE"
        if re.search(r'truncate', cmd, re.IGNORECASE):
            return "BLOCKED:DESTRUCTIVE"

    # P9: Block package managers UNLESS security/patch exception
    if phase_num == 9:
        rules = PHASE_RULES[9]
        if rules.get("block_package_managers"):
            # Check for package manager commands
            pkg_patterns = [
                r'\bnpm\s+install\b',
                r'\bpip\s+install\b',
                r'\bapt-get\s+install\b',
                # F-BYPASS-008: apt (no -get) is also a package manager.
                r'\bapt\s+install\b',
                r'\byum\s+install\b',
                r'\bdnf\s+install\b',
                r'\bpacman\s+-S\b',
                r'\bbrew\s+install\b',
                r'\bcomposer\s+require\b',
                r'\bgo\s+get\b'
            ]
            for pattern in pkg_patterns:
                if re.search(pattern, cmd, re.IGNORECASE):
                    # Check if exception applies
                    if rules.get("allow_package_exceptions"):
                        for exc in rules["allow_package_exceptions"]:
                            if exc.lower() in cmd.lower():
                                return "NONE"
                    return "BLOCKED:PACKAGE_MANAGER"
        # Block mkdir in src/
        if "mkdir" in cmd:
            for forbidden in rules.get("block_mkdir", []):
                if re.search(rf'(^|\s)mkdir\s+.*\b{forbidden}\b', cmd):
                    return "BLOCKED:IMPL_PATH"
        # Block /src/ and /lib/ paths except /archived/ and /docs/
        if rules.get("block_paths"):
            for blocked_path in rules["block_paths"]:
                if blocked_path in cmd and "/archived/" not in cmd and "/docs/" not in cmd:
                    return "BLOCKED:P9_RESTRICTED_PATH"

    # Check redirections to forbidden paths
    if detect_redirection_to_forbidden(cmd):
        return "BLOCKED:REDIRECT_TO_FORBIDDEN"

    # Check interpreter writes
    if detect_interpreter_write(cmd):
        return "BLOCKED:INTERPRETER_WRITE"

    # Check heredocs
    if re.search(r'<<\s*[\'"]?\w+[\'"]?\s*.*?(src|impl|implementations)', cmd):
        return "BLOCKED:HEREDOC_FORBIDDEN"

    return "NONE"


def detect_python_write(cmd: str) -> bool:
    """Detect Python one-liner that writes files."""
    # Check for python -c with code
    match = re.search(r'(python|python2|python3)\s+-c\s+"', cmd, re.IGNORECASE)
    if match:
        start = match.end()
        code = _extract_python_code(cmd[start:], '"')
        if code and _contains_dangerous(code):
            return True

    match = re.search(r"(python|python2|python3)\s+-c\s+'", cmd, re.IGNORECASE)
    if match:
        start = match.end()
        code = _extract_python_code(cmd[start:], "'")
        if code and _contains_dangerous(code):
            return True

    return False


def _extract_python_code(cmd: str, quote_char: str) -> str:
    """Extract Python code handling escaped quotes."""
    if not cmd:
        return ""
    i = 0
    while i < len(cmd):
        if cmd[i] == '\\' and i + 1 < len(cmd) and cmd[i+1] == quote_char:
            i += 2
            continue
        if cmd[i] == quote_char:
            return cmd[:i]
        i += 1
    return cmd


def _contains_dangerous(code: str) -> bool:
    """Check if code contains dangerous operations."""
    # Full pattern: open(filename, 'w') or open(filename, "w")
    if re.search(r'open\s*\([^)]*,\s*["\']?[wwaamm]["\']?\s*\)', code, re.IGNORECASE):
        return True
    # Simple open( without mode check (handles truncated extractions)
    if re.search(r'open\s*\(', code, re.IGNORECASE):
        return True
    if re.search(r'(exec|system|eval|subprocess|os\.system)\s*\(', code, re.IGNORECASE):
        return True
    if re.search(r'\s>\s', code):
        return True
    # PHP
    if re.search(r'file_put_contents\s*\(', code, re.IGNORECASE):
        return True
    # Ruby File.write
    if re.search(r'File\.write\s*\(', code, re.IGNORECASE):
        return True
    # Perl open for writing
    if re.search(r'open\s*\([^,]*,\s*["\']?>[^"\']*["\']?\s*\)', code, re.IGNORECASE):
        return True
    return False


def detect_redirection_to_forbidden(cmd: str) -> bool:
    """Detect redirections to forbidden paths."""
    cleaned = re.sub(r'["\'][^"\']*["\']', '', cmd)
    if re.search(r'>>?\s*/?(src|impl|implementations)/', cleaned):
        return True
    return False


def detect_interpreter_write(cmd: str) -> bool:
    """Detect interpreter -e/-c writes."""
    if re.search(r'(perl|ruby|php|node)\s+-[er]\s+["\'].*?["\']', cmd, re.IGNORECASE):
        match = re.search(r'(perl|ruby|php|node)\s+-[er]\s+["\'](.+?)["\']', cmd, re.IGNORECASE)
        if match and _contains_dangerous(match.group(2)):
            return True
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: bash_scanner.py <phase> <command_string>")
        sys.exit(1)

    # H2: validate HARNESS_DIR before any work, fail-secure on mismatch.
    try:
        _validate_harness_dir()
    except RuntimeError as e:
        print(f"BASH_SCANNER_HARNESS_DIR_INVALID: {e}")
        sys.exit(2)

    phase = sys.argv[1]
    command = sys.argv[2]

    result = scan_command(phase, command)
    print(result)


if __name__ == "__main__":
    main()
