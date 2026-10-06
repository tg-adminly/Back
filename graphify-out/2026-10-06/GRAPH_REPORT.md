# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 61 files · ~23,330 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 719 nodes · 1881 edges · 36 communities (22 shown, 14 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 143 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `007c7a0f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- service.py
- api.py
- keyboards.py
- package.json
- build_router
- giveaway/models.py
- Settings
- __main__.py
- giveaway/texts.py
- compilerOptions
- compilerOptions
- _try_join
- main
- server.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- test_panel.py
- participant.py
- TG Agent Q
- check_subscriptions

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 41 edges
2. `build_router()` - 25 edges
3. `Prize` - 25 edges
4. `GiveawayStatus` - 24 edges
5. `Winner` - 24 edges
6. `PrizeType` - 23 edges
7. `owner()` - 23 edges
8. `announce_results()` - 22 edges
9. `main()` - 22 edges
10. `Button()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_live_draw_flow()` --uses--> `Giveaway`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/models.py
- `env()` --uses--> `Deps`  [INFERRED]
  tests/test_panel.py → src/tgagent/panel/api.py
- `env()` --calls--> `init_db()`  [INFERRED]
  tests/test_panel.py → src/tgagent/core/db.py

## Import Cycles
- None detected.

## Communities (36 total, 14 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (94): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+86 more)

### Community 1 - "service.py"
Cohesion: 0.06
Nodes (42): ActionError, add_sponsor(), announce_results(), deliver_prize(), publish_giveaway(), reveal_next(), participants_url(), payout() (+34 more)

### Community 2 - "api.py"
Cohesion: 0.08
Nodes (39): auth_logout(), auth_poll(), auth_start(), bot_chats(), current_staff(), Deps, giveaway_cancel(), giveaway_create() (+31 more)

### Community 3 - "keyboards.py"
Cohesion: 0.17
Nodes (14): claim(), giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+6 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.10
Nodes (5): build_router(), got_prize(), publish(), sponsors_done(), _draft_giveaway()

### Community 6 - "giveaway/models.py"
Cohesion: 0.08
Nodes (22): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), BotChat, build_router() (+14 more)

### Community 7 - "Settings"
Cohesion: 0.12
Nodes (5): build_router(), Settings, build_router(), login_link(), LoginCB

### Community 8 - "__main__.py"
Cohesion: 0.12
Nodes (6): Vault, init_db(), make_engine(), make_sessionmaker(), serve_panel(), sm()

### Community 9 - "giveaway/texts.py"
Cohesion: 0.07
Nodes (31): got_ends_at(), Prize, PrizeType, active_item(), btn_same_for_rest(), giveaway_post(), live_ready(), local_time() (+23 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 15 - "_try_join"
Cohesion: 0.08
Nodes (11): build_router(), join(), start_claim(), _claim_prompt(), JoinCounter, ReplyThrottle, _try_join(), already_joined() (+3 more)

### Community 16 - "main"
Cohesion: 0.38
Nodes (7): bot_is_admin(), chat_link(), ChatRef, _get_member(), is_member(), missing_chats(), main()

### Community 17 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.13
Nodes (14): Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad, Ochiq ishtirokchilar sahifasi (+6 more)

### Community 31 - "test_panel.py"
Cohesion: 0.07
Nodes (14): LoginRequest, LoginRequests, env(), FakeBot, future(), login(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow() (+6 more)

### Community 37 - "participant.py"
Cohesion: 0.15
Nodes (5): CreateGiveaway, Payout, claim_or_default(), notify_users(), mask_card()

### Community 40 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

### Community 41 - "check_subscriptions"
Cohesion: 0.18
Nodes (8): check_subscriptions(), check(), CheckError, CheckProgress, close_participation(), draw_loop(), live_url(), required_chats()

## Knowledge Gaps
- **105 isolated node(s):** `Maqsad`, `Rollar`, `Ikki "qo'l"`, `G'olib tanlash`, `Ochiq ishtirokchilar sahifasi` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 284 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_router()` connect `build_router` to `main`, `giveaway/texts.py`, `participant.py`, `giveaway/models.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 28 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 28 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Maqsad`, `Rollar`, `Ikki "qo'l"` to the rest of the system?**
  _105 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06467181467181467 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `service.py` to `api.py`, `build_router`, `participant.py`, `giveaway/models.py`, `check_subscriptions`, `giveaway/texts.py`, `_try_join`, `test_panel.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Prize` (e.g. with `publish_giveaway()` and `same_prize()`) actually correct?**
  _`Prize` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06306306306306306 - nodes in this community are weakly interconnected._