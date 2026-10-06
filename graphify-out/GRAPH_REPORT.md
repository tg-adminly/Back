# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~27,045 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 762 nodes · 2092 edges · 37 communities (20 shown, 17 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec58880a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- Giveaway
- api.py
- giveaway/texts.py
- package.json
- build_router
- giveaway/models.py
- Settings
- participant.py
- _try_join
- compilerOptions
- LoginRequests
- compilerOptions
- missing_chats
- CheckError
- __main__.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- test_panel.py
- actions.py
- ChatRef

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 50 edges
2. `Settings` - 36 edges
3. `build_router()` - 29 edges
4. `ChatRef` - 28 edges
5. `GiveawayStatus` - 26 edges
6. `Prize` - 25 edges
7. `Winner` - 25 edges
8. `utcnow()` - 25 edges
9. `Button()` - 23 edges
10. `announce_results()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (37 total, 17 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "Giveaway"
Cohesion: 0.07
Nodes (35): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, publish_giveaway(), reveal_next(), run_auto_draw() (+27 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (46): DrawPick, list_picks(), auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff() (+38 more)

### Community 3 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (39): deliver_prize(), claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB (+31 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (17): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+9 more)

### Community 6 - "giveaway/models.py"
Cohesion: 0.05
Nodes (35): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, commit_of(), new_seed(), participants_file() (+27 more)

### Community 7 - "Settings"
Cohesion: 0.11
Nodes (5): build_router(), Settings, build_router(), login_link(), LoginCB

### Community 8 - "participant.py"
Cohesion: 0.13
Nodes (9): build_router(), claim_or_default(), start_claim(), _claim_prompt(), ReplyThrottle, ClaimStep, notify_users(), mask_card() (+1 more)

### Community 9 - "_try_join"
Cohesion: 0.19
Nodes (6): join(), JoinCounter, _try_join(), already_joined(), joined(), not_subscribed()

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "missing_chats"
Cohesion: 0.60
Nodes (4): check(), _get_member(), is_member(), missing_chats()

### Community 16 - "__main__.py"
Cohesion: 0.19
Nodes (4): chat_link(), build_router(), main(), serve_panel()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 31 - "test_panel.py"
Cohesion: 0.07
Nodes (18): create_app(), make_server(), _Server, env(), FakeBot, future(), login(), test_auto_draw_and_editor_runs_live() (+10 more)

### Community 37 - "actions.py"
Cohesion: 0.21
Nodes (3): CreateGiveaway, Payout, bot_is_admin()

### Community 41 - "ChatRef"
Cohesion: 0.15
Nodes (14): _after_close(), check_subscriptions(), CheckProgress, close_now(), close_participation(), draw_loop(), freeze(), live_url() (+6 more)

## Knowledge Gaps
- **109 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 302 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `api.py`, `giveaway/texts.py`, `build_router`, `actions.py`, `giveaway/models.py`, `participant.py`, `_try_join`, `ChatRef`, `test_panel.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 37 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 37 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0615702479338843 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `Giveaway`, `api.py`, `build_router`, `actions.py`, `giveaway/models.py`, `participant.py`, `ChatRef`, `__main__.py`, `test_panel.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Should `Giveaway` be split into smaller, more focused modules?**
  _Cohesion score 0.06923076923076923 - nodes in this community are weakly interconnected._