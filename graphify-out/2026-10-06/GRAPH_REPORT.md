# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~28,392 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 791 nodes · 2099 edges · 39 communities (24 shown, 15 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 147 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d06c98a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- _after_close
- api.py
- giveaway/texts.py
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
- TG Agent Q
- validators.py
- db.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- check_subscriptions
- Vault
- test_panel.py
- build_router
- test_init_db_adds_new_columns_to_old_tables

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 37 edges
2. `build_router()` - 29 edges
3. `Settings` - 27 edges
4. `utcnow()` - 27 edges
5. `Prize` - 23 edges
6. `Button()` - 23 edges
7. `announce_results()` - 23 edges
8. `PrizeType` - 22 edges
9. `main()` - 22 edges
10. `ChatRef` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `env()` --uses--> `Deps`  [INFERRED]
  tests/test_panel.py → src/tgagent/panel/api.py
- `env()` --calls--> `Vault`  [INFERRED]
  tests/test_panel.py → src/tgagent/core/crypto.py
- `env()` --calls--> `init_db()`  [INFERRED]
  tests/test_panel.py → src/tgagent/core/db.py

## Import Cycles
- None detected.

## Communities (39 total, 15 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "_after_close"
Cohesion: 0.17
Nodes (10): _after_close(), close_now(), close_participation(), draw_loop(), freeze(), live_url(), remind(), staff_ids() (+2 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (46): list_winners(), participant_counts(), subscription_misses(), auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn (+38 more)

### Community 3 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (32): JoinCounter, _try_join(), run(), Prize, PrizeType, active_item(), already_joined(), auto_draw_failed() (+24 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.10
Nodes (6): build_router(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway()

### Community 6 - "service.py"
Cohesion: 0.10
Nodes (28): ClaimStep, DrawPick, Giveaway, GiveawayStatus, Participant, SubscriptionMiss, WinnerStatus, active_giveaways() (+20 more)

### Community 7 - "server.py"
Cohesion: 0.17
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 9 - "auth.py"
Cohesion: 0.08
Nodes (18): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), create_session(), delete_session() (+10 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "actions.py"
Cohesion: 0.11
Nodes (17): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next() (+9 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "jobs.py"
Cohesion: 0.09
Nodes (8): CreateGiveaway, Payout, build_router(), bot_is_admin(), chat_link(), notify_users(), Settings, main()

### Community 15 - "keyboards.py"
Cohesion: 0.18
Nodes (15): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+7 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

### Community 17 - "validators.py"
Cohesion: 0.21
Nodes (8): got_ends_at(), _digits(), normalize_card(), parse_amount(), parse_local_datetime(), test_amount(), test_card(), test_datetime_is_local()

### Community 18 - "db.py"
Cohesion: 0.10
Nodes (11): BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat(), _add_missing_columns(), init_db() (+3 more)

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 27 - "check_subscriptions"
Cohesion: 0.24
Nodes (7): check_subscriptions(), check(), CheckError, CheckProgress, _get_member(), is_member(), missing_chats()

### Community 30 - "Vault"
Cohesion: 0.25
Nodes (3): mask_card(), Vault, test_vault_roundtrip()

### Community 31 - "test_panel.py"
Cohesion: 0.08
Nodes (17): env(), FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts() (+9 more)

### Community 36 - "build_router"
Cohesion: 0.20
Nodes (7): build_router(), claim_or_default(), join(), start_claim(), _claim_prompt(), normalize_phone(), test_phone()

## Knowledge Gaps
- **109 isolated node(s):** `Role`, `PrizeType`, `CANCEL_MODES`, `Stage`, `Start` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 317 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_router()` connect `build_router` to `giveaway/texts.py`, `service.py`, `actions.py`, `jobs.py`, `validators.py`, `Vault`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 23 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 23 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Role`, `PrizeType`, `CANCEL_MODES` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06170798898071626 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `service.py` to `_after_close`, `api.py`, `giveaway/texts.py`, `build_router`, `actions.py`, `jobs.py`, `db.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `build_router()` (e.g. with `Giveaway` and `ChatRef`) actually correct?**
  _`build_router()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05877742946708464 - nodes in this community are weakly interconnected._