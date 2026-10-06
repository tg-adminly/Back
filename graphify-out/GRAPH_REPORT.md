# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~25,088 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 735 nodes · 1995 edges · 43 communities (24 shown, 19 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 181 edges (avg confidence: 0.95)
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
- __main__.py
- admin.py
- giveaway/texts.py
- compilerOptions
- announce_results
- compilerOptions
- Winner
- _try_join
- ChatRef
- server.py
- draw.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- JoinCounter
- test_panel.py
- ReplyThrottle
- CheckError
- participant.py
- TG Agent Q
- Settings

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 46 edges
2. `Settings` - 32 edges
3. `build_router()` - 28 edges
4. `GiveawayStatus` - 25 edges
5. `Prize` - 25 edges
6. `Winner` - 25 edges
7. `ChatRef` - 24 edges
8. `announce_results()` - 23 edges
9. `PrizeType` - 23 edges
10. `Button()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `test_participant_numbers_are_sequential_and_unique()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (43 total, 19 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (100): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+92 more)

### Community 1 - "service.py"
Cohesion: 0.15
Nodes (20): Giveaway, GiveawayStatus, Participant, active_giveaways(), add_participant(), cancel_giveaway(), create_giveaway(), due_giveaway_ids() (+12 more)

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (45): SponsorChannel, parse_prize(), auth_logout(), auth_poll(), auth_start(), bot_chats(), current_staff(), Deps (+37 more)

### Community 3 - "keyboards.py"
Cohesion: 0.22
Nodes (12): claim(), giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+4 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.06
Nodes (18): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+10 more)

### Community 6 - "giveaway/models.py"
Cohesion: 0.06
Nodes (28): DrawPick, SubscriptionMiss, BotChat, on_my_status(), forget_chat(), list_chats(), remember_chat(), _add_missing_columns() (+20 more)

### Community 7 - "__main__.py"
Cohesion: 0.11
Nodes (4): build_router(), login_link(), LoginCB, serve_panel()

### Community 8 - "admin.py"
Cohesion: 0.14
Nodes (6): CreateGiveaway, Payout, build_router(), claim_or_default(), mask_card(), Vault

### Community 9 - "giveaway/texts.py"
Cohesion: 0.11
Nodes (17): same_prize(), Prize, active_item(), auto_draw_failed(), btn_same_for_rest(), draw_mode(), giveaway_post(), join_button() (+9 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "announce_results"
Cohesion: 0.14
Nodes (11): ActionError, announce_results(), deliver_prize(), publish_giveaway(), reveal_next(), run_auto_draw(), update_giveaway(), participants_url() (+3 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "Winner"
Cohesion: 0.20
Nodes (11): start_claim(), _claim_prompt(), payout(), ClaimStep, PrizeType, Winner, WinnerStatus, first_claim_step() (+3 more)

### Community 15 - "_try_join"
Cohesion: 0.29
Nodes (5): join(), _try_join(), already_joined(), joined(), not_subscribed()

### Community 16 - "ChatRef"
Cohesion: 0.20
Nodes (12): add_sponsor(), check_subscriptions(), check(), CheckProgress, bot_is_admin(), chat_link(), ChatRef, _get_member() (+4 more)

### Community 17 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

### Community 18 - "draw.py"
Cohesion: 0.23
Nodes (6): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash()

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
Cohesion: 0.11
Nodes (13): FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error() (+5 more)

### Community 40 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

### Community 41 - "Settings"
Cohesion: 0.15
Nodes (6): build_router(), close_participation(), draw_loop(), live_url(), staff_ids(), Settings

## Knowledge Gaps
- **107 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+102 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 287 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `service.py` to `api.py`, `build_router`, `participant.py`, `giveaway/models.py`, `admin.py`, `Settings`, `giveaway/texts.py`, `announce_results`, `_try_join`, `ChatRef`, `JoinCounter`, `test_panel.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0628712154135883 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `api.py`, `build_router`, `participant.py`, `__main__.py`, `admin.py`, `giveaway/models.py`, `announce_results`, `ChatRef`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Should `service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14623655913978495 - nodes in this community are weakly interconnected._