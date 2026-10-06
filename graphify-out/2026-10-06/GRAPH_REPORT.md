# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 61 files · ~21,860 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 681 nodes · 1829 edges · 37 communities (19 shown, 18 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 161 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4e58d41e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- service.py
- api.py
- build_router
- package.json
- build_router
- giveaway/models.py
- Settings
- admin.py
- giveaway/texts.py
- compilerOptions
- draw.py
- compilerOptions
- __main__.py
- ReplyThrottle
- participant.py
- server.py
- auth.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- test_panel.py

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 40 edges
2. `Settings` - 29 edges
3. `build_router()` - 26 edges
4. `Prize` - 25 edges
5. `Winner` - 25 edges
6. `PrizeType` - 23 edges
7. `main()` - 22 edges
8. `announce_results()` - 22 edges
9. `GiveawayStatus` - 22 edges
10. `owner()` - 22 edges

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

## Communities (37 total, 18 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.07
Nodes (91): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+83 more)

### Community 1 - "service.py"
Cohesion: 0.07
Nodes (33): ActionError, add_sponsor(), announce_results(), deliver_prize(), publish_giveaway(), join(), _try_join(), participants_url() (+25 more)

### Community 2 - "api.py"
Cohesion: 0.08
Nodes (45): Winner, WinnerStatus, list_winners(), open_payouts(), pending_claim(), auth_logout(), auth_poll(), auth_start() (+37 more)

### Community 3 - "build_router"
Cohesion: 0.13
Nodes (10): build_router(), claim_or_default(), start_claim(), _claim_prompt(), JoinCounter, ClaimStep, normalize_card(), normalize_phone() (+2 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (16): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), _draft_giveaway(), _digits(), parse_amount() (+8 more)

### Community 6 - "giveaway/models.py"
Cohesion: 0.12
Nodes (10): DrawPick, BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat(), Base (+2 more)

### Community 7 - "Settings"
Cohesion: 0.14
Nodes (8): build_router(), close_participation(), draw_loop(), live_url(), live_ready(), Settings, main(), build_router()

### Community 9 - "giveaway/texts.py"
Cohesion: 0.08
Nodes (30): claim(), giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+22 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "draw.py"
Cohesion: 0.23
Nodes (6): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash()

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 16 - "participant.py"
Cohesion: 0.19
Nodes (8): reveal_next(), required_chats(), bot_is_admin(), chat_link(), ChatRef, _get_member(), is_member(), missing_chats()

### Community 17 - "server.py"
Cohesion: 0.17
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 18 - "auth.py"
Cohesion: 0.20
Nodes (7): create_session(), delete_session(), _hash(), LoginRequest, LoginRequests, session_staff(), staff_role()

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
Cohesion: 0.06
Nodes (26): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, Vault, init_db(), make_engine() (+18 more)

## Knowledge Gaps
- **105 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 261 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `service.py`, `api.py`, `build_router`, `build_router`, `admin.py`, `__main__.py`, `participant.py`, `auth.py`, `config.py`, `test_panel.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 27 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _105 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.07035796155880797 - nodes in this community are weakly interconnected._
- **Why does `build_router()` connect `build_router` to `admin.py`, `service.py`, `test_panel.py`, `Settings`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Should `service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06980433632998413 - nodes in this community are weakly interconnected._