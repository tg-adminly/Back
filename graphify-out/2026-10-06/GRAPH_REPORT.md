# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~27,045 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 777 nodes · 2076 edges · 42 communities (27 shown, 15 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 165 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a1ea94b9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- announce_results
- api.py
- Giveaway
- package.json
- build_router
- giveaway/models.py
- Settings
- ReplyThrottle
- _try_join
- compilerOptions
- service.py
- compilerOptions
- check_subscriptions
- keyboards.py
- __main__.py
- server.py
- validators.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- GiveawayStatus
- test_panel.py
- test_validators.py
- build_router
- TG Agent Q
- parse_local_datetime
- actions.py
- jobs.py

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 49 edges
2. `build_router()` - 27 edges
3. `GiveawayStatus` - 26 edges
4. `Prize` - 25 edges
5. `utcnow()` - 25 edges
6. `Winner` - 24 edges
7. `Button()` - 23 edges
8. `announce_results()` - 23 edges
9. `PrizeType` - 23 edges
10. `main()` - 22 edges

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

## Communities (42 total, 15 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "announce_results"
Cohesion: 0.11
Nodes (15): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next() (+7 more)

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (42): auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff(), Deps, giveaway_cancel() (+34 more)

### Community 3 - "Giveaway"
Cohesion: 0.11
Nodes (20): Giveaway, Prize, PrizeType, active_item(), auto_draw_failed(), btn_same_for_rest(), draw_mode(), draw_summary() (+12 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.10
Nodes (5): build_router(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway()

### Community 6 - "giveaway/models.py"
Cohesion: 0.06
Nodes (27): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), BotChat, on_my_status() (+19 more)

### Community 7 - "Settings"
Cohesion: 0.11
Nodes (5): build_router(), Settings, build_router(), login_link(), LoginCB

### Community 9 - "_try_join"
Cohesion: 0.19
Nodes (5): JoinCounter, _try_join(), already_joined(), joined(), not_subscribed()

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "service.py"
Cohesion: 0.12
Nodes (22): Participant, SponsorChannel, SubscriptionMiss, Winner, WinnerStatus, active_giveaways(), add_participant(), create_giveaway() (+14 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "check_subscriptions"
Cohesion: 0.23
Nodes (8): check_subscriptions(), check(), CheckError, CheckProgress, bot_is_admin(), _get_member(), is_member(), missing_chats()

### Community 15 - "keyboards.py"
Cohesion: 0.16
Nodes (16): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+8 more)

### Community 16 - "__main__.py"
Cohesion: 0.11
Nodes (11): Qat'iy qoidalar, claim_or_default(), chat_link(), build_router(), mask_card(), Vault, init_db(), make_engine() (+3 more)

### Community 17 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

### Community 18 - "validators.py"
Cohesion: 0.36
Nodes (6): got_prize(), _digits(), normalize_card(), parse_amount(), parse_prize(), test_prize()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 27 - "GiveawayStatus"
Cohesion: 0.22
Nodes (5): ClaimStep, GiveawayStatus, cancel_giveaway(), due_giveaway_ids(), due_reminder_ids()

### Community 31 - "test_panel.py"
Cohesion: 0.07
Nodes (17): LoginRequest, LoginRequests, env(), FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors() (+9 more)

### Community 32 - "test_validators.py"
Cohesion: 0.25
Nodes (6): normalize_phone(), test_amount(), test_card(), test_datetime_is_local(), test_phone(), test_vault_roundtrip()

### Community 33 - "build_router"
Cohesion: 0.29
Nodes (4): build_router(), join(), start_claim(), _claim_prompt()

### Community 34 - "TG Agent Q"
Cohesion: 0.40
Nodes (4): Buyruqlar, graphify, TG Agent Q, Tuzilma

### Community 37 - "actions.py"
Cohesion: 0.17
Nodes (4): CreateGiveaway, Payout, required_chats(), ChatRef

### Community 41 - "jobs.py"
Cohesion: 0.19
Nodes (9): _after_close(), close_now(), close_participation(), draw_loop(), freeze(), live_url(), remind(), staff_ids() (+1 more)

## Knowledge Gaps
- **109 isolated node(s):** `Maqsad`, `Rollar`, `Ikki "qo'l"`, `Bekor qilish`, `G'olib tanlash` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 311 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `announce_results`, `api.py`, `build_router`, `actions.py`, `giveaway/models.py`, `_try_join`, `jobs.py`, `service.py`, `check_subscriptions`, `GiveawayStatus`, `test_panel.py`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 36 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 36 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Maqsad`, `Rollar`, `Ikki "qo'l"` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0615702479338843 - nodes in this community are weakly interconnected._
- **Why does `build_router()` connect `build_router` to `Giveaway`, `parse_local_datetime`, `actions.py`, `giveaway/models.py`, `__main__.py`, `validators.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `GiveawayStatus` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`GiveawayStatus` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Should `announce_results` be split into smaller, more focused modules?**
  _Cohesion score 0.10695187165775401 - nodes in this community are weakly interconnected._