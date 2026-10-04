# Graph Report - tg-agent-q  (2026-10-04)

## Corpus Check
- 57 files · ~16,997 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 623 nodes · 1557 edges · 36 communities (20 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 104 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5bbef301`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- service.py
- api.py
- draw.py
- package.json
- build_router
- giveaway/models.py
- Settings
- publish_giveaway
- keyboards.py
- compilerOptions
- compilerOptions
- participant.py
- admin.py
- __main__.py
- LoginRequests
- build_router
- ReplyThrottle
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- test_panel.py
- TG Agent Q

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 29 edges
2. `build_router()` - 26 edges
3. `Winner` - 22 edges
4. `Prize` - 22 edges
5. `PrizeType` - 21 edges
6. `Settings` - 20 edges
7. `finalize()` - 20 edges
8. `Button()` - 19 edges
9. `ChatRef` - 19 edges
10. `main()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `env()` --uses--> `Deps`  [INFERRED]
  tests/test_panel.py → src/tgagent/panel/api.py
- `env()` --uses--> `LoginRequests`  [INFERRED]
  tests/test_panel.py → src/tgagent/panel/auth.py
- `env()` --calls--> `ChatRef`  [INFERRED]
  tests/test_panel.py → src/tgagent/channels/telegram_bot/chats.py
- `env()` --calls--> `Vault`  [INFERRED]
  tests/test_panel.py → src/tgagent/core/crypto.py

## Import Cycles
- None detected.

## Communities (36 total, 16 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.10
Nodes (69): api, ApiError, Giveaway, GiveawayDetail, GiveawayStatus, Me, Participant, PayoutDetails (+61 more)

### Community 1 - "service.py"
Cohesion: 0.05
Nodes (50): join(), start_claim(), _claim_prompt(), JoinCounter, _try_join(), _announce(), finalize(), ClaimStep (+42 more)

### Community 2 - "api.py"
Cohesion: 0.09
Nodes (34): auth_logout(), auth_poll(), auth_start(), current_staff(), Deps, giveaway_cancel(), giveaway_create(), giveaway_detail() (+26 more)

### Community 3 - "draw.py"
Cohesion: 0.18
Nodes (6): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash()

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.06
Nodes (17): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), _draft_giveaway(), _digits(), normalize_card() (+9 more)

### Community 6 - "giveaway/models.py"
Cohesion: 0.11
Nodes (14): SponsorChannel, Base, UTCDateTime, utcnow(), create_session(), delete_session(), _hash(), session_staff() (+6 more)

### Community 8 - "publish_giveaway"
Cohesion: 0.20
Nodes (4): ActionError, add_sponsor(), deliver_prize(), publish_giveaway()

### Community 9 - "keyboards.py"
Cohesion: 0.19
Nodes (14): claim(), giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+6 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "participant.py"
Cohesion: 0.21
Nodes (7): required_chats(), bot_is_admin(), chat_link(), ChatRef, _get_member(), is_member(), missing_chats()

### Community 15 - "__main__.py"
Cohesion: 0.12
Nodes (10): draw_loop(), init_db(), make_engine(), make_sessionmaker(), main(), create_app(), make_server(), serve_panel() (+2 more)

### Community 16 - "LoginRequests"
Cohesion: 0.16
Nodes (5): LoginRequest, LoginRequests, build_router(), login_link(), LoginCB

### Community 17 - "build_router"
Cohesion: 0.17
Nodes (6): build_router(), claim_or_default(), notify_users(), mask_card(), Vault, test_vault_roundtrip()

### Community 19 - "permissions"
Cohesion: 0.33
Nodes (5): permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.14
Nodes (13): Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash (tekshirsa bo'ladigan random), Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad, Oqim 1 — Rozigrish (+5 more)

### Community 31 - "test_panel.py"
Cohesion: 0.11
Nodes (9): FakeBot, future(), login(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_past_end_time_rejected(), test_payout_deliver(), test_requires_login_and_csrf_header() (+1 more)

### Community 32 - "TG Agent Q"
Cohesion: 0.40
Nodes (4): Buyruqlar, Qat'iy qoidalar, TG Agent Q, Tuzilma

## Knowledge Gaps
- **96 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `name` (+91 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 248 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `build_router()` connect `build_router` to `giveaway/models.py`, `Settings`, `admin.py`, `__main__.py`, `build_router`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Vault` connect `build_router` to `TG Agent Q`, `service.py`, `api.py`, `build_router`, `participant.py`, `admin.py`, `__main__.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `Settings` connect `Settings` to `service.py`, `api.py`, `build_router`, `giveaway/models.py`, `participant.py`, `admin.py`, `__main__.py`, `build_router`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Giveaway` (e.g. with `JoinCounter` and `_try_join()`) actually correct?**
  _`Giveaway` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `build_router()` (e.g. with `Settings` and `Vault`) actually correct?**
  _`build_router()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Winner` (e.g. with `build_router()` and `_claim_prompt()`) actually correct?**
  _`Winner` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Prize` (e.g. with `same_prize()` and `create_giveaway()`) actually correct?**
  _`Prize` has 9 INFERRED edges - model-reasoned connections that need verification._