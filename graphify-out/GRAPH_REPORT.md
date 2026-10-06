# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~28,194 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 811 nodes · 2054 edges · 41 communities (26 shown, 15 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fbb282a4`
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
- __main__.py
- build_router
- auth.py
- compilerOptions
- announce_results
- compilerOptions
- actions.py
- keyboards.py
- TG Agent Q
- giveaway/models.py
- db.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- LoginRequests
- admin.py
- test_panel.py
- utcnow
- tracking.py
- Settings

## God Nodes (most connected - your core abstractions)
1. `build_router()` - 29 edges
2. `utcnow()` - 26 edges
3. `Button()` - 23 edges
4. `main()` - 22 edges
5. `ErrorBox()` - 21 edges
6. `announce_results()` - 20 edges
7. `Settings` - 20 edges
8. `cx()` - 19 edges
9. `Loading()` - 19 edges
10. `_try_join()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `run()` --indirect_call--> `sm()`  [INFERRED]
  src/tgagent/agents/giveaway/jobs.py → tests/test_service.py

## Import Cycles
- None detected.

## Communities (41 total, 15 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "_after_close"
Cohesion: 0.13
Nodes (14): _after_close(), check_subscriptions(), check(), CheckError, CheckProgress, close_now(), close_participation(), draw_loop() (+6 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (47): subscription_misses(), _digits(), parse_amount(), parse_prize(), auth_logout(), auth_poll(), auth_start(), bot_chats() (+39 more)

### Community 3 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (28): join(), start_claim(), _claim_prompt(), JoinCounter, _try_join(), active_item(), already_joined(), auto_draw_failed() (+20 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.06
Nodes (16): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), normalize_card() (+8 more)

### Community 6 - "service.py"
Cohesion: 0.11
Nodes (17): SubscriptionMiss, active_giveaways(), add_participant(), cancel_giveaway(), get_participant(), list_giveaways(), list_participants(), list_sponsors() (+9 more)

### Community 7 - "__main__.py"
Cohesion: 0.11
Nodes (9): init_db(), make_engine(), make_sessionmaker(), main(), create_app(), make_server(), serve_panel(), _Server (+1 more)

### Community 8 - "build_router"
Cohesion: 0.14
Nodes (6): build_router(), claim_or_default(), ReplyThrottle, notify_users(), mask_card(), test_throttle_limits_repeated_error_replies()

### Community 9 - "auth.py"
Cohesion: 0.13
Nodes (14): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), create_giveaway(), create_session() (+6 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "announce_results"
Cohesion: 0.09
Nodes (14): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next() (+6 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "actions.py"
Cohesion: 0.22
Nodes (7): required_chats(), bot_is_admin(), chat_link(), ChatRef, _get_member(), is_member(), missing_chats()

### Community 15 - "keyboards.py"
Cohesion: 0.18
Nodes (15): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+7 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

### Community 17 - "giveaway/models.py"
Cohesion: 0.18
Nodes (7): ClaimStep, Giveaway, GiveawayStatus, Prize, PrizeType, Winner, WinnerStatus

### Community 18 - "db.py"
Cohesion: 0.13
Nodes (7): DrawPick, Participant, SponsorChannel, BotChat, _add_missing_columns(), Base, UTCDateTime

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 30 - "admin.py"
Cohesion: 0.18
Nodes (3): CreateGiveaway, Payout, Vault

### Community 31 - "test_panel.py"
Cohesion: 0.08
Nodes (16): env(), FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts() (+8 more)

### Community 33 - "utcnow"
Cohesion: 0.23
Nodes (7): due_giveaway_ids(), due_reminder_ids(), utcnow(), _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 34 - "tracking.py"
Cohesion: 0.29
Nodes (5): build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat()

### Community 37 - "Settings"
Cohesion: 0.10
Nodes (5): build_router(), Settings, build_router(), login_link(), LoginCB

## Knowledge Gaps
- **109 isolated node(s):** `Maqsad`, `Rollar`, `Ikki "qo'l"`, `Bekor qilish`, `G'olib tanlash` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 329 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_router()` connect `build_router` to `utcnow`, `api.py`, `Settings`, `__main__.py`, `actions.py`, `giveaway/models.py`, `admin.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `build_router()` (e.g. with `Giveaway` and `ChatRef`) actually correct?**
  _`build_router()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Maqsad`, `Rollar`, `Ikki "qo'l"` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06170798898071626 - nodes in this community are weakly interconnected._
- **Why does `utcnow()` connect `utcnow` to `_after_close`, `api.py`, `giveaway/texts.py`, `build_router`, `service.py`, `auth.py`, `actions.py`, `giveaway/models.py`, `db.py`, `admin.py`, `test_panel.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Should `_after_close` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `api.py`, `build_router`, `__main__.py`, `auth.py`, `actions.py`, `admin.py`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._