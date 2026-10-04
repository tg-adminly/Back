# Graph Report - tg-agent-q  (2026-10-04)

## Corpus Check
- 57 files · ~16,851 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: (none) 4, .example 1, .css 1)

## Summary
- 608 nodes · 1587 edges · 33 communities (19 shown, 14 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- ui.tsx
- service.py
- api.py
- build_router
- package.json
- giveaway/texts.py
- giveaway/models.py
- bot_login.py
- actions.py
- keyboards.py
- compilerOptions
- __main__.py
- compilerOptions
- participant.py
- admin.py
- server.py
- LoginRequests
- build_router
- ReplyThrottle
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- JoinCounter
- FakeBot
- TG Agent Q

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 34 edges
2. `Settings` - 27 edges
3. `build_router()` - 26 edges
4. `Winner` - 26 edges
5. `Prize` - 25 edges
6. `PrizeType` - 23 edges
7. `finalize()` - 20 edges
8. `ChatRef` - 20 edges
9. `Button()` - 19 edges
10. `main()` - 19 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `test_participant_numbers_are_sequential_and_unique()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `_giveaway()` --uses--> `Prize`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (33 total, 14 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.10
Nodes (69): api, ApiError, Giveaway, GiveawayDetail, GiveawayStatus, Me, Participant, PayoutDetails (+61 more)

### Community 1 - "service.py"
Cohesion: 0.06
Nodes (41): ActionError, add_sponsor(), deliver_prize(), commit_of(), new_seed(), participants_file(), participants_hash(), rank() (+33 more)

### Community 2 - "api.py"
Cohesion: 0.09
Nodes (34): auth_logout(), auth_poll(), auth_start(), current_staff(), Deps, giveaway_cancel(), giveaway_create(), giveaway_detail() (+26 more)

### Community 3 - "build_router"
Cohesion: 0.10
Nodes (5): build_router(), got_prize(), publish(), sponsors_done(), _draft_giveaway()

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (33): got_ends_at(), _try_join(), same_prize(), Prize, PrizeType, active_item(), already_joined(), btn_same_for_rest() (+25 more)

### Community 6 - "giveaway/models.py"
Cohesion: 0.09
Nodes (21): Base, UTCDateTime, utcnow(), create_session(), delete_session(), _hash(), session_staff(), staff_role() (+13 more)

### Community 7 - "bot_login.py"
Cohesion: 0.12
Nodes (4): build_router(), build_router(), login_link(), LoginCB

### Community 9 - "keyboards.py"
Cohesion: 0.23
Nodes (11): giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB, publish_confirm() (+3 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "__main__.py"
Cohesion: 0.21
Nodes (9): draw_loop(), bot_is_admin(), chat_link(), ChatRef, init_db(), make_engine(), make_sessionmaker(), main() (+1 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "participant.py"
Cohesion: 0.27
Nodes (4): required_chats(), _get_member(), is_member(), missing_chats()

### Community 15 - "server.py"
Cohesion: 0.16
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 17 - "build_router"
Cohesion: 0.16
Nodes (6): build_router(), claim_or_default(), join(), notify_users(), mask_card(), Vault

### Community 19 - "permissions"
Cohesion: 0.33
Nodes (5): permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.14
Nodes (13): Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash (tekshirsa bo'ladigan random), Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad, Oqim 1 — Rozigrish (+5 more)

### Community 32 - "TG Agent Q"
Cohesion: 0.40
Nodes (4): Buyruqlar, Qat'iy qoidalar, TG Agent Q, Tuzilma

## Knowledge Gaps
- **96 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `$schema` (+91 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 235 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `actions.py` to `service.py`, `api.py`, `build_router`, `giveaway/models.py`, `bot_login.py`, `__main__.py`, `participant.py`, `admin.py`, `build_router`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `build_router()` connect `build_router` to `giveaway/texts.py`, `giveaway/models.py`, `actions.py`, `__main__.py`, `admin.py`, `build_router`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `Vault` connect `build_router` to `TG Agent Q`, `api.py`, `build_router`, `giveaway/texts.py`, `__main__.py`, `participant.py`, `admin.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Giveaway` (e.g. with `publish_giveaway()` and `JoinCounter`) actually correct?**
  _`Giveaway` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `publish_giveaway()`) actually correct?**
  _`Settings` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `build_router()` (e.g. with `Settings` and `Vault`) actually correct?**
  _`build_router()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Winner` (e.g. with `deliver_prize()` and `build_router()`) actually correct?**
  _`Winner` has 15 INFERRED edges - model-reasoned connections that need verification._