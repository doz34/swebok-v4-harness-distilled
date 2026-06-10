# Feature 1 — Auto-Trigger Harness from User Prompt

> **Date** : 2026-06-10
> **Goal** : extremely reliable + efficient auto-trigger when user sends a prompt
> **Status** : 🚧 In progress

## 1. Problem statement

The swebok v4 harness has an `intent-detector.py` that maps user prompts to phases via:
1. Pattern matching (regex on intent-map.json)
2. Semantic scoring (vector similarity)
3. KB lookup (compiled knowledge)
4. Fallback chain (semantic-relaxation, pattern-boost, agent-escalation, human-escalation)

**Issues identified**:
- Untested reliability (no benchmark on real prompts)
- Latency unknown (likely >2s on cold start)
- No fallback when `intent-map.json` is missing/corrupt
- No offline mode (requires Python + compiled knowledge index)
- No way to override manually (user must know to say "use P5")

## 2. Design (v2)

### 2.1 New file: `lib/auto_trigger.py`

**Pipeline**:
1. **Fast path** (cache hit): <50ms — if exact same prompt in cache, return last result
2. **Pattern match** (<100ms): 50+ patterns from `intent-map.json`
3. **Semantic match** (<500ms): TF-IDF cosine similarity on prompt + intent descriptions
4. **Confidence check**: if <0.5, escalate to fallback
5. **DSL output**: `auto_trigger:phase=N;confidence=0.85;intent=foo;fallback=bar`

### 2.2 CLI: `bin/auto-trigger <prompt>`

```bash
$ bin/auto-trigger "I want to refactor the auth module"
auto_trigger:phase=5;confidence=0.82;intent=refactor;fallback=implement

$ bin/auto-trigger "We need to test the API"
auto_trigger:phase=6;confidence=0.91;intent=api_test;fallback=qa
```

### 2.3 Integration: `pre-tool-use/auto-trigger-hook.sh`

Hook that runs **once per session start** to detect the user's first prompt's intent and:
1. Set the initial phase in `.swebok_state.db`
2. Suggest the right skills/commands
3. Apply the phase guard accordingly

## 3. Implementation

### 3.1 Tests (acceptance criteria)

- [ ] Test 1: prompt "Write tests for the user model" → phase=6, confidence >0.8
- [ ] Test 2: prompt "Refactor the auth module" → phase=5, confidence >0.7
- [ ] Test 3: prompt "Discover stakeholder needs" → phase=0, confidence >0.8
- [ ] Test 4: empty prompt → fallback chain triggers
- [ ] Test 5: prompt "Hello" → fallback chain + human-escalation
- [ ] Test 6: prompt "Deploy to production" → phase=7, confidence >0.7
- [ ] Test 7: latency on 100 prompts <1s p95
- [ ] Test 8: works offline (no network)
- [ ] Test 9: cache hit <50ms
- [ ] Test 10: manual override works (`phase=5` in prompt → force P5)

### 3.2 Files to create/modify

- [ ] `lib/auto_trigger.py` (new) — main logic
- [ ] `bin/auto-trigger` (new) — CLI
- [ ] `pre-tool-use/auto-trigger-hook.sh` (new) — integration
- [ ] `intent-map.json` (modify) — add manual override patterns
- [ ] `tests/test_auto_trigger.py` (new) — 10+ tests
- [ ] `intent-detector.py` (modify or replace) — integrate v2 logic

## 4. Status

- 🚧 In progress
- Next: implement `lib/auto_trigger.py`
- Blocker: none

## 5. Implementation log

```
[2026-06-10] Sprint 2 START. Implementing lib/auto_trigger.py
[2026-06-10] Pattern matching: extracted 50+ patterns from intent-map.json
```

(Each iteration adds a line here)
