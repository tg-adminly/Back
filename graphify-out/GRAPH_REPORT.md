# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~28,599 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 778 nodes · 2141 edges · 45 communities (25 shown, 20 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 203 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `03f16ea4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- api.py
- auth.py
- giveaway/texts.py
- package.json
- build_router
- Giveaway
- server.py
- ReplyThrottle
- bot_login.py
- compilerOptions
- Settings
- compilerOptions
- jobs.py
- keyboards.py
- TG Agent Q
- FakeBot
- giveaway/models.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- actions.py
- main
- test_panel.py
- test_service.py
- BotChat
- build_router
- init_db
- env

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 36 edges
3. `build_router()` - 29 edges
4. `ChatRef` - 29 edges
5. `utcnow()` - 27 edges
6. `GiveawayStatus` - 26 edges
7. `Button()` - 25 edges
8. `Prize` - 25 edges
9. `Winner` - 25 edges
10. `announce_results()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `run()` --indirect_call--> `sm()`  [INFERRED]
  src/tgagent/agents/giveaway/jobs.py → tests/test_service.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (45 total, 20 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (104): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+96 more)

### Community 1 - "api.py"
Cohesion: 0.15
Nodes (18): Winner, WinnerStatus, list_winners(), mark_done(), open_payouts(), pending_claim(), giveaway_detail(), giveaway_list() (+10 more)

### Community 2 - "auth.py"
Cohesion: 0.06
Nodes (35): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), auth_logout(), auth_poll() (+27 more)

### Community 3 - "giveaway/texts.py"
Cohesion: 0.08
Nodes (27): Prize, PrizeType, active_item(), btn_same_for_rest(), draw_mode(), giveaway_post(), local_time(), money() (+19 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.08
Nodes (9): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), parse_local_datetime() (+1 more)

### Community 6 - "Giveaway"
Cohesion: 0.11
Nodes (25): DrawPick, Giveaway, GiveawayStatus, Participant, SponsorChannel, active_giveaways(), add_participant(), cancel_giveaway() (+17 more)

### Community 7 - "server.py"
Cohesion: 0.21
Nodes (3): make_server(), serve_panel(), _Server

### Community 9 - "bot_login.py"
Cohesion: 0.12
Nodes (5): LoginRequest, LoginRequests, build_router(), login_link(), LoginCB

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "Settings"
Cohesion: 0.06
Nodes (28): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), run_auto_draw() (+20 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 15 - "keyboards.py"
Cohesion: 0.18
Nodes (16): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+8 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

### Community 18 - "giveaway/models.py"
Cohesion: 0.22
Nodes (4): SubscriptionMiss, Base, UTCDateTime, utcnow()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 27 - "actions.py"
Cohesion: 0.14
Nodes (12): reveal_next(), check_subscriptions(), check(), CheckError, CheckProgress, required_chats(), bot_is_admin(), chat_link() (+4 more)

### Community 30 - "main"
Cohesion: 0.25
Nodes (4): build_router(), build_router(), make_sessionmaker(), main()

### Community 31 - "test_panel.py"
Cohesion: 0.08
Nodes (23): join(), JoinCounter, _try_join(), already_joined(), joined(), joined_but_missing(), not_subscribed(), sponsor_ref() (+15 more)

### Community 33 - "test_service.py"
Cohesion: 0.48
Nodes (4): _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 34 - "BotChat"
Cohesion: 0.43
Nodes (5): BotChat, on_my_status(), forget_chat(), list_chats(), remember_chat()

### Community 36 - "build_router"
Cohesion: 0.15
Nodes (11): build_router(), claim_or_default(), start_claim(), _claim_prompt(), ClaimStep, _digits(), normalize_card(), normalize_phone() (+3 more)

### Community 38 - "init_db"
Cohesion: 0.24
Nodes (4): _add_missing_columns(), init_db(), make_engine(), test_init_db_adds_new_columns_to_old_tables()

## Knowledge Gaps
- **109 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 309 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `api.py`, `auth.py`, `giveaway/texts.py`, `build_router`, `Settings`, `jobs.py`, `giveaway/models.py`, `actions.py`, `test_panel.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06090896974543516 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `api.py`, `auth.py`, `build_router`, `build_router`, `env`, `bot_login.py`, `jobs.py`, `actions.py`, `main`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14814814814814814 - nodes in this community are weakly interconnected._