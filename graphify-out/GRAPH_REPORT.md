# Graph Report - tg-agent-q  (2026-10-07)

## Corpus Check
- 71 files · ~35,165 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 918 nodes · 2578 edges · 53 communities (31 shown, 22 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 242 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `261146c3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- content_api.py
- api.py
- Prize
- package.json
- build_router
- service.py
- __main__.py
- ReplyThrottle
- LoginRequests
- compilerOptions
- Settings
- compilerOptions
- actions.py
- keyboards.py
- TG Agent Q
- utcnow
- giveaway/models.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- ChatRef
- main
- test_panel.py
- test_service.py
- BotChat
- update_giveaway
- test_init_db_adds_new_columns_to_old_tables
- Giveaway
- _try_join
- draw.py
- _openai_provider
- auth.py
- build_router
- _add_missing_columns
- build_router
- CheckError

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 41 edges
3. `Button()` - 32 edges
4. `utcnow()` - 31 edges
5. `ChatRef` - 30 edges
6. `cx()` - 29 edges
7. `build_router()` - 29 edges
8. `ErrorBox()` - 28 edges
9. `GiveawayStatus` - 26 edges
10. `Staff` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_new_second_sponsor_marks_old_participants()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py

## Import Cycles
- None detected.

## Communities (53 total, 22 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.05
Nodes (124): AiUsage, api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, GuideVersion (+116 more)

### Community 1 - "content_api.py"
Cohesion: 0.06
Nodes (39): BadImage, delete_image(), image_path(), read_image(), save_image(), ProposalStatus, Sample, SampleSource (+31 more)

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (47): deliver_prize(), Winner, WinnerStatus, list_winners(), mark_done(), open_payouts(), auth_logout(), auth_poll() (+39 more)

### Community 3 - "Prize"
Cohesion: 0.13
Nodes (16): announce_results(), start_claim(), _claim_prompt(), ClaimStep, Prize, PrizeType, first_claim_step(), btn_same_for_rest() (+8 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.06
Nodes (19): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), claim_or_default() (+11 more)

### Community 6 - "service.py"
Cohesion: 0.10
Nodes (24): GiveawayStatus, Participant, SponsorChannel, SubscriptionMiss, active_giveaways(), add_participant(), cancel_giveaway(), create_giveaway() (+16 more)

### Community 7 - "__main__.py"
Cohesion: 0.16
Nodes (3): make_server(), serve_panel(), _Server

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "Settings"
Cohesion: 0.16
Nodes (9): _after_close(), close_now(), close_participation(), draw_loop(), freeze(), live_url(), remind(), staff_ids() (+1 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "actions.py"
Cohesion: 0.13
Nodes (3): CreateGiveaway, Payout, notify_users()

### Community 15 - "keyboards.py"
Cohesion: 0.17
Nodes (16): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+8 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.40
Nodes (4): Buyruqlar, graphify, TG Agent Q, Tuzilma

### Community 17 - "utcnow"
Cohesion: 0.16
Nodes (6): utcnow(), LLM, LlmError, LlmUsage, month_start(), Msg

### Community 18 - "giveaway/models.py"
Cohesion: 0.21
Nodes (3): DrawPick, Base, UTCDateTime

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.09
Nodes (21): Agent bilimi, Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Jadval (+13 more)

### Community 27 - "ChatRef"
Cohesion: 0.16
Nodes (14): reveal_next(), run_auto_draw(), check_subscriptions(), check(), CheckProgress, required_chats(), start_check(), run() (+6 more)

### Community 30 - "main"
Cohesion: 0.11
Nodes (14): Qat'iy qoidalar, build_router(), build_router(), mask_card(), Vault, init_db(), make_engine(), make_sessionmaker() (+6 more)

### Community 31 - "test_panel.py"
Cohesion: 0.09
Nodes (20): jpeg(), test_monthly_limit_stops_ai(), test_new_proposal_supersedes_old(), test_training_chat_flow(), FakeBot, future(), login(), test_auto_draw_and_editor_runs_live() (+12 more)

### Community 33 - "test_service.py"
Cohesion: 0.48
Nodes (4): _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 34 - "BotChat"
Cohesion: 0.43
Nodes (5): BotChat, on_my_status(), forget_chat(), list_chats(), remember_chat()

### Community 36 - "update_giveaway"
Cohesion: 0.15
Nodes (7): ActionError, add_sponsor(), cancel_giveaway(), CancelMode, publish_giveaway(), update_giveaway(), participants_url()

### Community 40 - "Giveaway"
Cohesion: 0.19
Nodes (10): Giveaway, active_item(), auto_draw_failed(), draw_mode(), draw_summary(), giveaway_post(), live_ready(), live_reminder() (+2 more)

### Community 45 - "_try_join"
Cohesion: 0.16
Nodes (7): join(), JoinCounter, _try_join(), already_joined(), joined(), joined_but_missing(), not_subscribed()

### Community 46 - "draw.py"
Cohesion: 0.26
Nodes (6): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash()

### Community 47 - "_openai_provider"
Cohesion: 0.24
Nodes (5): Completion, _openai_provider(), call(), part(), FakeAI

### Community 48 - "auth.py"
Cohesion: 0.40
Nodes (6): create_session(), delete_session(), _hash(), session_staff(), staff_role(), PanelSession

### Community 49 - "build_router"
Cohesion: 0.33
Nodes (3): build_router(), login_link(), LoginCB

## Knowledge Gaps
- **118 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 350 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `api.py`, `Prize`, `update_giveaway`, `build_router`, `__main__.py`, `actions.py`, `_openai_provider`, `auth.py`, `utcnow`, `build_router`, `build_router`, `ChatRef`, `main`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.054001554001554 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `Giveaway` to `api.py`, `Prize`, `update_giveaway`, `build_router`, `service.py`, `Settings`, `actions.py`, `_try_join`, `giveaway/models.py`, `ChatRef`, `test_panel.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Should `content_api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05980861244019139 - nodes in this community are weakly interconnected._