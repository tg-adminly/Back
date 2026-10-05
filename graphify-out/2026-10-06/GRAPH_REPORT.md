# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 59 files · ~17,962 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 635 nodes · 1664 edges · 31 communities (19 shown, 12 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 144 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f2445e77`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- service.py
- api.py
- _try_join
- package.json
- build_router
- giveaway/models.py
- keyboards.py
- giveaway/texts.py
- compilerOptions
- compilerOptions
- participant.py
- server.py
- LoginRequests
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- test_panel.py
- TG Agent Q

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 34 edges
2. `Settings` - 27 edges
3. `build_router()` - 26 edges
4. `Winner` - 26 edges
5. `Prize` - 25 edges
6. `PrizeType` - 23 edges
7. `main()` - 22 edges
8. `finalize()` - 20 edges
9. `ChatRef` - 20 edges
10. `utcnow()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_payout_deliver()` --uses--> `WinnerStatus`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/models.py
- `test_payout_deliver()` --uses--> `Winner`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/models.py
- `test_vault_roundtrip()` --uses--> `Vault`  [INFERRED]
  tests/test_validators.py → src/tgagent/core/crypto.py

## Import Cycles
- None detected.

## Communities (31 total, 12 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.09
Nodes (72): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, Me, Participant (+64 more)

### Community 1 - "service.py"
Cohesion: 0.08
Nodes (33): ActionError, add_sponsor(), deliver_prize(), publish_giveaway(), start_claim(), _claim_prompt(), payout(), ClaimStep (+25 more)

### Community 2 - "api.py"
Cohesion: 0.08
Nodes (34): auth_logout(), auth_start(), bot_chats(), current_staff(), Deps, giveaway_cancel(), giveaway_create(), giveaway_detail() (+26 more)

### Community 3 - "_try_join"
Cohesion: 0.19
Nodes (6): join(), JoinCounter, _try_join(), already_joined(), joined(), not_subscribed()

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.10
Nodes (5): build_router(), got_prize(), publish(), sponsors_done(), _draft_giveaway()

### Community 6 - "giveaway/models.py"
Cohesion: 0.08
Nodes (21): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), BotChat, on_my_status() (+13 more)

### Community 7 - "keyboards.py"
Cohesion: 0.18
Nodes (14): claim(), giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+6 more)

### Community 9 - "giveaway/texts.py"
Cohesion: 0.07
Nodes (32): got_ends_at(), Prize, PrizeType, active_item(), btn_same_for_rest(), draw_summary(), giveaway_post(), local_time() (+24 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "participant.py"
Cohesion: 0.05
Nodes (28): CreateGiveaway, Payout, build_router(), build_router(), claim_or_default(), ReplyThrottle, _announce(), draw_loop() (+20 more)

### Community 15 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

### Community 16 - "LoginRequests"
Cohesion: 0.17
Nodes (5): LoginRequest, LoginRequests, build_router(), login_link(), LoginCB

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.14
Nodes (13): Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash (tekshirsa bo'ladigan random), Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad, Oqim 1 — Rozigrish (+5 more)

### Community 31 - "test_panel.py"
Cohesion: 0.14
Nodes (10): FakeBot, future(), login(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error(), test_past_end_time_rejected() (+2 more)

### Community 32 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

## Knowledge Gaps
- **99 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+94 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 244 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `participant.py` to `service.py`, `api.py`, `build_router`, `giveaway/models.py`, `LoginRequests`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Giveaway` (e.g. with `publish_giveaway()` and `JoinCounter`) actually correct?**
  _`Giveaway` has 21 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _99 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.09243697478991597 - nodes in this community are weakly interconnected._
- **Why does `build_router()` connect `build_router` to `giveaway/texts.py`, `participant.py`, `giveaway/models.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 12 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `publish_giveaway()`) actually correct?**
  _`Settings` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Should `service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07878787878787878 - nodes in this community are weakly interconnected._