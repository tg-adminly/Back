# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~28,392 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 776 nodes · 2132 edges · 47 communities (28 shown, 19 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 203 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cec41c4b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- Settings
- api.py
- Giveaway
- package.json
- build_router
- service.py
- server.py
- ReplyThrottle
- auth.py
- compilerOptions
- actions.py
- compilerOptions
- jobs.py
- keyboards.py
- Vault
- validators.py
- giveaway/models.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- missing_chats
- parse_local_datetime
- test_panel.py
- test_service.py
- tracking.py
- test_validators.py
- build_router
- main
- test_init_db_adds_new_columns_to_old_tables
- env

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 36 edges
3. `build_router()` - 29 edges
4. `ChatRef` - 29 edges
5. `utcnow()` - 27 edges
6. `GiveawayStatus` - 26 edges
7. `Prize` - 25 edges
8. `Winner` - 25 edges
9. `Button()` - 23 edges
10. `announce_results()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_new_second_sponsor_marks_old_participants()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py

## Import Cycles
- None detected.

## Communities (47 total, 19 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "Settings"
Cohesion: 0.11
Nodes (14): _after_close(), check_subscriptions(), CheckError, CheckProgress, close_now(), close_participation(), draw_loop(), freeze() (+6 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (49): SponsorChannel, list_sponsors(), list_winners(), participant_counts(), subscription_misses(), auth_logout(), auth_poll(), auth_start() (+41 more)

### Community 3 - "Giveaway"
Cohesion: 0.07
Nodes (28): JoinCounter, _try_join(), Giveaway, Prize, PrizeType, active_item(), already_joined(), auto_draw_failed() (+20 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.10
Nodes (5): build_router(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway()

### Community 6 - "service.py"
Cohesion: 0.11
Nodes (22): ClaimStep, GiveawayStatus, Participant, SubscriptionMiss, WinnerStatus, active_giveaways(), add_participant(), cancel_giveaway() (+14 more)

### Community 7 - "server.py"
Cohesion: 0.17
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 9 - "auth.py"
Cohesion: 0.11
Nodes (15): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), create_giveaway(), create_session() (+7 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "actions.py"
Cohesion: 0.12
Nodes (16): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next() (+8 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "jobs.py"
Cohesion: 0.13
Nodes (3): CreateGiveaway, Payout, notify_users()

### Community 15 - "keyboards.py"
Cohesion: 0.17
Nodes (16): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+8 more)

### Community 16 - "Vault"
Cohesion: 0.18
Nodes (6): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, Vault

### Community 17 - "validators.py"
Cohesion: 0.42
Nodes (5): got_prize(), _digits(), normalize_card(), parse_amount(), parse_prize()

### Community 18 - "giveaway/models.py"
Cohesion: 0.22
Nodes (4): Winner, Base, UTCDateTime, utcnow()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 27 - "missing_chats"
Cohesion: 0.38
Nodes (5): check(), chat_link(), _get_member(), is_member(), missing_chats()

### Community 31 - "test_panel.py"
Cohesion: 0.10
Nodes (16): FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error() (+8 more)

### Community 33 - "test_service.py"
Cohesion: 0.48
Nodes (4): _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 34 - "tracking.py"
Cohesion: 0.31
Nodes (6): BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat()

### Community 35 - "test_validators.py"
Cohesion: 0.40
Nodes (3): test_amount(), test_card(), test_datetime_is_local()

### Community 36 - "build_router"
Cohesion: 0.18
Nodes (9): build_router(), claim_or_default(), join(), start_claim(), _claim_prompt(), normalize_phone(), mask_card(), test_phone() (+1 more)

### Community 37 - "main"
Cohesion: 0.20
Nodes (5): build_router(), main(), build_router(), login_link(), LoginCB

### Community 40 - "env"
Cohesion: 0.22
Nodes (5): _add_missing_columns(), init_db(), make_engine(), make_sessionmaker(), env()

## Knowledge Gaps
- **109 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 309 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `Settings`, `api.py`, `build_router`, `service.py`, `auth.py`, `actions.py`, `jobs.py`, `giveaway/models.py`, `test_panel.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06170798898071626 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `api.py`, `build_router`, `main`, `build_router`, `env`, `auth.py`, `actions.py`, `jobs.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Should `Settings` be split into smaller, more focused modules?**
  _Cohesion score 0.10887096774193548 - nodes in this community are weakly interconnected._