# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~25,088 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 748 nodes · 1983 edges · 43 communities (23 shown, 20 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 158 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ec58880a`
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
- Settings
- build_router
- Giveaway
- compilerOptions
- validators.py
- compilerOptions
- PrizeType
- Prize
- __main__.py
- server.py
- admin.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- JoinCounter
- test_panel.py
- ReplyThrottle
- parse_local_datetime
- participant.py
- check_subscriptions

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 46 edges
2. `build_router()` - 27 edges
3. `GiveawayStatus` - 25 edges
4. `Prize` - 25 edges
5. `Winner` - 25 edges
6. `announce_results()` - 23 edges
7. `PrizeType` - 23 edges
8. `Button()` - 22 edges
9. `main()` - 22 edges
10. `utcnow()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `test_participant_numbers_are_sequential_and_unique()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py
- `test_prize()` --uses--> `PrizeType`  [INFERRED]
  tests/test_validators.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (43 total, 20 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (100): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+92 more)

### Community 1 - "service.py"
Cohesion: 0.07
Nodes (34): ActionError, add_sponsor(), announce_results(), deliver_prize(), publish_giveaway(), reveal_next(), run_auto_draw(), update_giveaway() (+26 more)

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (47): Winner, WinnerStatus, list_winners(), open_payouts(), pending_claim(), auth_logout(), auth_poll(), auth_start() (+39 more)

### Community 3 - "keyboards.py"
Cohesion: 0.17
Nodes (15): claim(), giveaway_post(), JoinCB, manage(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+7 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.09
Nodes (6): build_router(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway()

### Community 6 - "giveaway/models.py"
Cohesion: 0.07
Nodes (23): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), BotChat, on_my_status() (+15 more)

### Community 7 - "Settings"
Cohesion: 0.11
Nodes (5): build_router(), Settings, build_router(), login_link(), LoginCB

### Community 8 - "build_router"
Cohesion: 0.19
Nodes (6): build_router(), claim_or_default(), join(), mask_card(), Vault, test_vault_roundtrip()

### Community 9 - "Giveaway"
Cohesion: 0.16
Nodes (12): _try_join(), Giveaway, active_item(), already_joined(), auto_draw_failed(), draw_mode(), draw_summary(), giveaway_post() (+4 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "validators.py"
Cohesion: 0.25
Nodes (9): _digits(), normalize_card(), normalize_phone(), parse_amount(), parse_prize(), test_amount(), test_card(), test_phone() (+1 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "PrizeType"
Cohesion: 0.21
Nodes (10): start_claim(), _claim_prompt(), PrizeType, btn_same_for_rest(), money(), payout_card(), prize_text(), results_post() (+2 more)

### Community 15 - "Prize"
Cohesion: 0.28
Nodes (3): Prize, prizes_block(), test_prizes_block_groups_equal_places()

### Community 16 - "__main__.py"
Cohesion: 0.17
Nodes (9): bot_is_admin(), chat_link(), ChatRef, _get_member(), is_member(), missing_chats(), build_router(), main() (+1 more)

### Community 17 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

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
Cohesion: 0.05
Nodes (28): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, _add_missing_columns(), init_db(), make_engine() (+20 more)

### Community 33 - "parse_local_datetime"
Cohesion: 0.33
Nodes (3): got_ends_at(), parse_local_datetime(), test_datetime_is_local()

### Community 41 - "check_subscriptions"
Cohesion: 0.16
Nodes (9): check_subscriptions(), check(), CheckError, CheckProgress, close_participation(), draw_loop(), live_url(), required_chats() (+1 more)

## Knowledge Gaps
- **107 isolated node(s):** `Buyruqlar`, `Tuzilma`, `graphify`, `Maqsad`, `Rollar` (+102 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 296 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `service.py`, `api.py`, `build_router`, `participant.py`, `giveaway/models.py`, `check_subscriptions`, `PrizeType`, `Prize`, `admin.py`, `JoinCounter`, `test_panel.py`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 33 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Buyruqlar`, `Tuzilma`, `graphify` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06200202810372302 - nodes in this community are weakly interconnected._
- **Why does `build_router()` connect `build_router` to `parse_local_datetime`, `giveaway/models.py`, `Giveaway`, `validators.py`, `__main__.py`, `admin.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `GiveawayStatus` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`GiveawayStatus` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Should `service.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06875 - nodes in this community are weakly interconnected._