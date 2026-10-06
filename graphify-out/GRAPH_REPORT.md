# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~27,493 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 769 nodes · 2103 edges · 41 communities (23 shown, 18 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 198 edges (avg confidence: 0.95)
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
- auth.py
- __main__.py
- ReplyThrottle
- giveaway/models.py
- compilerOptions
- service.py
- compilerOptions
- env
- keyboards.py
- Vault
- FakeBot
- test_service.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- Winner
- test_panel.py
- actions.py
- jobs.py

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 36 edges
3. `build_router()` - 29 edges
4. `ChatRef` - 28 edges
5. `GiveawayStatus` - 26 edges
6. `Prize` - 25 edges
7. `Winner` - 25 edges
8. `utcnow()` - 25 edges
9. `Button()` - 23 edges
10. `announce_results()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `_giveaway()` --uses--> `PrizeType`  [INFERRED]
  tests/test_service.py → src/tgagent/agents/giveaway/models.py

## Import Cycles
- None detected.

## Communities (41 total, 18 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "announce_results"
Cohesion: 0.33
Nodes (4): announce_results(), claim(), participants_url(), list_picks()

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (46): subscription_misses(), parse_prize(), auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff() (+38 more)

### Community 3 - "Giveaway"
Cohesion: 0.06
Nodes (30): publish_giveaway(), update_giveaway(), join(), JoinCounter, _try_join(), giveaway_post(), Giveaway, Prize (+22 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.06
Nodes (18): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+10 more)

### Community 6 - "auth.py"
Cohesion: 0.11
Nodes (14): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), create_session(), delete_session() (+6 more)

### Community 7 - "__main__.py"
Cohesion: 0.05
Nodes (13): BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat(), build_router(), login_link() (+5 more)

### Community 9 - "giveaway/models.py"
Cohesion: 0.19
Nodes (5): DrawPick, SubscriptionMiss, Base, UTCDateTime, utcnow()

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "service.py"
Cohesion: 0.13
Nodes (20): GiveawayStatus, Participant, SponsorChannel, active_giveaways(), add_participant(), cancel_giveaway(), create_giveaway(), due_giveaway_ids() (+12 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "env"
Cohesion: 0.17
Nodes (6): _add_missing_columns(), init_db(), make_engine(), make_sessionmaker(), test_init_db_adds_new_columns_to_old_tables(), env()

### Community 15 - "keyboards.py"
Cohesion: 0.21
Nodes (12): JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu(), PaidCB, publish_confirm() (+4 more)

### Community 16 - "Vault"
Cohesion: 0.15
Nodes (6): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, Vault

### Community 18 - "test_service.py"
Cohesion: 0.48
Nodes (4): _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 27 - "Winner"
Cohesion: 0.18
Nodes (12): deliver_prize(), start_claim(), _claim_prompt(), payout(), ClaimStep, PrizeType, Winner, WinnerStatus (+4 more)

### Community 31 - "test_panel.py"
Cohesion: 0.19
Nodes (14): future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error(), test_live_draw_flow() (+6 more)

### Community 37 - "actions.py"
Cohesion: 0.14
Nodes (6): CreateGiveaway, Payout, build_router(), claim_or_default(), notify_users(), mask_card()

### Community 41 - "jobs.py"
Cohesion: 0.07
Nodes (28): ActionError, add_sponsor(), cancel_giveaway(), CancelMode, reveal_next(), run_auto_draw(), build_router(), _after_close() (+20 more)

## Knowledge Gaps
- **109 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 306 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `announce_results`, `api.py`, `build_router`, `actions.py`, `giveaway/models.py`, `jobs.py`, `service.py`, `test_panel.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0615702479338843 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `jobs.py` to `announce_results`, `api.py`, `Giveaway`, `build_router`, `actions.py`, `__main__.py`, `auth.py`, `env`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07026307026307026 - nodes in this community are weakly interconnected._