# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~27,493 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 793 nodes · 2047 edges · 36 communities (22 shown, 14 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 108 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b0602b9d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- Settings
- api.py
- giveaway/texts.py
- package.json
- build_router
- build_router
- server.py
- Vault
- giveaway/models.py
- compilerOptions
- service.py
- compilerOptions
- __main__.py
- keyboards.py
- TG Agent Q
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- test_panel.py
- actions.py
- jobs.py

## God Nodes (most connected - your core abstractions)
1. `build_router()` - 29 edges
2. `Giveaway` - 27 edges
3. `Settings` - 27 edges
4. `utcnow()` - 25 edges
5. `Button()` - 23 edges
6. `main()` - 22 edges
7. `ChatRef` - 21 edges
8. `announce_results()` - 20 edges
9. `ErrorBox()` - 20 edges
10. `Prize` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_prizes_block_groups_equal_places()` --calls--> `prizes_block()`  [INFERRED]
  tests/test_validators.py → src/tgagent/agents/giveaway/texts.py

## Import Cycles
- None detected.

## Communities (36 total, 14 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "Settings"
Cohesion: 0.16
Nodes (9): _after_close(), close_now(), close_participation(), draw_loop(), freeze(), live_url(), remind(), staff_ids() (+1 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (44): subscription_misses(), auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff(), Deps (+36 more)

### Community 3 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (27): join(), start_claim(), _claim_prompt(), JoinCounter, _try_join(), active_item(), already_joined(), auto_draw_failed() (+19 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.06
Nodes (24): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), ClaimStep (+16 more)

### Community 6 - "build_router"
Cohesion: 0.33
Nodes (3): build_router(), login_link(), LoginCB

### Community 7 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

### Community 8 - "Vault"
Cohesion: 0.11
Nodes (6): build_router(), claim_or_default(), ReplyThrottle, mask_card(), Vault, test_throttle_limits_repeated_error_replies()

### Community 9 - "giveaway/models.py"
Cohesion: 0.07
Nodes (24): DrawPick, SubscriptionMiss, BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat() (+16 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "service.py"
Cohesion: 0.08
Nodes (31): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), payout(), Giveaway (+23 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "__main__.py"
Cohesion: 0.16
Nodes (6): build_router(), init_db(), make_engine(), make_sessionmaker(), main(), serve_panel()

### Community 15 - "keyboards.py"
Cohesion: 0.07
Nodes (27): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next() (+19 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

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
Cohesion: 0.06
Nodes (18): LoginRequest, LoginRequests, env(), FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors() (+10 more)

### Community 37 - "actions.py"
Cohesion: 0.14
Nodes (3): CreateGiveaway, Payout, notify_users()

### Community 41 - "jobs.py"
Cohesion: 0.17
Nodes (11): check_subscriptions(), check(), CheckError, CheckProgress, required_chats(), bot_is_admin(), chat_link(), ChatRef (+3 more)

## Knowledge Gaps
- **109 isolated node(s):** `Maqsad`, `Rollar`, `Ikki "qo'l"`, `Bekor qilish`, `G'olib tanlash` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 323 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_router()` connect `build_router` to `Settings`, `actions.py`, `Vault`, `jobs.py`, `giveaway/models.py`, `service.py`, `__main__.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `build_router()` (e.g. with `Giveaway` and `ChatRef`) actually correct?**
  _`build_router()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Maqsad`, `Rollar`, `Ikki "qo'l"` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0615702479338843 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `api.py`, `build_router`, `actions.py`, `build_router`, `jobs.py`, `giveaway/models.py`, `__main__.py`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `Giveaway` (e.g. with `build_router()` and `_after_close()`) actually correct?**
  _`Giveaway` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.059917920656634746 - nodes in this community are weakly interconnected._