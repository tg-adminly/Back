# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 61 files · ~23,330 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 703 nodes · 1901 edges · 42 communities (24 shown, 18 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 170 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4e58d41e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- service.py
- D
- build_router
- package.json
- build_router
- giveaway/models.py
- Settings
- admin.py
- giveaway/texts.py
- compilerOptions
- api.py
- compilerOptions
- ReplyThrottle
- actions.py
- server.py
- LoginRequests
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- publish_giveaway
- test_panel.py
- participant.py
- Winner
- auth_logout
- TG Agent Q
- CheckError

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 42 edges
2. `Settings` - 29 edges
3. `build_router()` - 26 edges
4. `Prize` - 25 edges
5. `Winner` - 25 edges
6. `GiveawayStatus` - 24 edges
7. `PrizeType` - 23 edges
8. `owner()` - 23 edges
9. `main()` - 22 edges
10. `announce_results()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `test_participant_numbers_are_sequential_and_unique()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `test_prize()` --uses--> `PrizeType`  [INFERRED]
  tests/test_validators.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (42 total, 18 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.07
Nodes (94): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+86 more)

### Community 1 - "service.py"
Cohesion: 0.13
Nodes (25): announce_results(), ClaimStep, Giveaway, GiveawayStatus, Participant, active_giveaways(), add_participant(), cancel_giveaway() (+17 more)

### Community 2 - "D"
Cohesion: 0.14
Nodes (14): auth_start(), bot_chats(), giveaway_cancel(), giveaway_detail(), giveaway_finish(), giveaway_participants(), live_announce(), live_check() (+6 more)

### Community 3 - "build_router"
Cohesion: 0.23
Nodes (6): build_router(), claim_or_default(), normalize_card(), normalize_phone(), notify_users(), mask_card()

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (16): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), _draft_giveaway(), _digits(), parse_amount() (+8 more)

### Community 6 - "giveaway/models.py"
Cohesion: 0.08
Nodes (23): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), DrawPick, SubscriptionMiss (+15 more)

### Community 7 - "Settings"
Cohesion: 0.20
Nodes (5): build_router(), close_participation(), draw_loop(), live_url(), Settings

### Community 8 - "admin.py"
Cohesion: 0.15
Nodes (3): CreateGiveaway, Payout, Vault

### Community 9 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (38): join(), start_claim(), _claim_prompt(), JoinCounter, _try_join(), claim(), giveaway_post(), JoinCB (+30 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "api.py"
Cohesion: 0.18
Nodes (16): list_winners(), Deps, giveaway_create(), giveaway_out(), giveaway_preview(), GiveawayIn, parse_giveaway(), ParsedGiveaway (+8 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 16 - "actions.py"
Cohesion: 0.23
Nodes (11): reveal_next(), check_subscriptions(), check(), required_chats(), bot_is_admin(), chat_link(), ChatRef, _get_member() (+3 more)

### Community 17 - "server.py"
Cohesion: 0.17
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 18 - "LoginRequests"
Cohesion: 0.17
Nodes (5): LoginRequest, LoginRequests, build_router(), login_link(), LoginCB

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.13
Nodes (14): Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad, Ochiq ishtirokchilar sahifasi (+6 more)

### Community 27 - "publish_giveaway"
Cohesion: 0.13
Nodes (8): ActionError, add_sponsor(), deliver_prize(), publish_giveaway(), participants_url(), SponsorChannel, list_sponsors(), upsert_sponsor()

### Community 31 - "test_panel.py"
Cohesion: 0.09
Nodes (20): init_db(), make_engine(), make_sessionmaker(), env(), FakeBot, future(), login(), test_bot_chats_lists_admin_channels_not_yet_sponsors() (+12 more)

### Community 38 - "Winner"
Cohesion: 0.27
Nodes (9): Winner, WinnerStatus, mark_done(), open_payouts(), pending_claim(), payout_details(), payout_list(), stats() (+1 more)

### Community 39 - "auth_logout"
Cohesion: 0.39
Nodes (5): auth_logout(), auth_poll(), current_staff(), me(), Staff

### Community 40 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

## Knowledge Gaps
- **105 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 272 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `service.py`, `build_router`, `build_router`, `participant.py`, `giveaway/models.py`, `admin.py`, `api.py`, `__main__.py`, `actions.py`, `LoginRequests`, `publish_giveaway`, `test_panel.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 29 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _105 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06547619047619048 - nodes in this community are weakly interconnected._
- **Why does `build_router()` connect `build_router` to `admin.py`, `actions.py`, `giveaway/models.py`, `Settings`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Should `service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12802275960170698 - nodes in this community are weakly interconnected._