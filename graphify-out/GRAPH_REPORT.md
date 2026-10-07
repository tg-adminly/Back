# Graph Report - tg-agent-q  (2026-10-07)

## Corpus Check
- 71 files · ~36,244 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 937 nodes · 2617 edges · 51 communities (29 shown, 22 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 246 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6d51b69e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Content.tsx
- _openai_provider
- api.py
- service.py
- package.json
- build_router
- Giveaway
- server.py
- ReplyThrottle
- content_api.py
- compilerOptions
- Settings
- compilerOptions
- admin.py
- keyboards.py
- init_db
- LLM
- env
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- jobs.py
- FakeAI
- test_panel.py
- participant.py
- StyleGuide
- actions.py
- media.py
- env
- test_content.py
- chat_message
- trainer.py
- utcnow

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 41 edges
3. `utcnow()` - 31 edges
4. `Button()` - 30 edges
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

## Communities (51 total, 22 thin omitted)

### Community 0 - "Content.tsx"
Cohesion: 0.05
Nodes (128): AiUsage, api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, GuideVersion (+120 more)

### Community 1 - "_openai_provider"
Cohesion: 0.47
Nodes (3): _openai_provider(), call(), part()

### Community 2 - "api.py"
Cohesion: 0.08
Nodes (42): auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff(), Deps, giveaway_cancel() (+34 more)

### Community 3 - "service.py"
Cohesion: 0.05
Nodes (51): announce_results(), deliver_prize(), _claim_prompt(), payout(), ClaimStep, DrawPick, GiveawayStatus, Participant (+43 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (18): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+10 more)

### Community 6 - "Giveaway"
Cohesion: 0.09
Nodes (17): JoinCounter, _try_join(), Giveaway, active_item(), already_joined(), auto_draw_failed(), draw_mode(), draw_summary() (+9 more)

### Community 7 - "server.py"
Cohesion: 0.18
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 9 - "content_api.py"
Cohesion: 0.20
Nodes (11): Sample, Staff, chat(), chat_retry(), guide(), media_file(), message_out(), sample_delete() (+3 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "Settings"
Cohesion: 0.09
Nodes (5): build_router(), Settings, build_router(), login_link(), LoginCB

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 15 - "keyboards.py"
Cohesion: 0.18
Nodes (13): claim(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu(), PaidCB (+5 more)

### Community 16 - "init_db"
Cohesion: 0.15
Nodes (8): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, _add_missing_columns(), init_db(), test_init_db_adds_new_columns_to_old_tables()

### Community 17 - "LLM"
Cohesion: 0.23
Nodes (4): LLM, LlmError, month_start(), Msg

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.09
Nodes (21): Agent bilimi, Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Jadval (+13 more)

### Community 27 - "jobs.py"
Cohesion: 0.14
Nodes (14): _after_close(), check_subscriptions(), check(), CheckError, CheckProgress, close_now(), close_participation(), draw_loop() (+6 more)

### Community 31 - "test_panel.py"
Cohesion: 0.19
Nodes (15): future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error(), test_live_draw_flow() (+7 more)

### Community 33 - "participant.py"
Cohesion: 0.11
Nodes (9): build_router(), claim_or_default(), join(), start_claim(), chat_link(), notify_users(), mask_card(), Vault (+1 more)

### Community 34 - "StyleGuide"
Cohesion: 0.22
Nodes (9): StyleGuide, decide(), save_guide(), chat_decide(), DecisionIn, guide_out(), guide_restore(), guide_save() (+1 more)

### Community 36 - "actions.py"
Cohesion: 0.12
Nodes (16): ActionError, add_sponsor(), cancel_giveaway(), CancelMode, publish_giveaway(), reveal_next(), run_auto_draw(), update_giveaway() (+8 more)

### Community 38 - "media.py"
Cohesion: 0.22
Nodes (5): BadImage, delete_image(), image_path(), read_image(), save_image()

### Community 40 - "env"
Cohesion: 0.21
Nodes (7): make_engine(), make_sessionmaker(), env(), _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 41 - "test_content.py"
Cohesion: 0.22
Nodes (7): answered(), jpeg(), send(), test_messages_while_thinking_get_one_reply(), test_monthly_limit_stops_ai(), test_new_proposal_supersedes_old(), test_training_chat_flow()

### Community 44 - "chat_message"
Cohesion: 0.18
Nodes (4): ProposalStatus, SampleSource, add_sample(), chat_message()

### Community 45 - "trainer.py"
Cohesion: 0.15
Nodes (15): TrainMessage, guide_block(), sample_block(), add_message(), current_guide(), history(), _history_text(), kick() (+7 more)

### Community 46 - "utcnow"
Cohesion: 0.08
Nodes (21): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), BotChat, build_router() (+13 more)

## Knowledge Gaps
- **120 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+115 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 358 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `participant.py`, `_openai_provider`, `service.py`, `actions.py`, `build_router`, `api.py`, `env`, `admin.py`, `utcnow`, `LLM`, `env`, `jobs.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _120 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Content.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.05148005148005148 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `Giveaway` to `participant.py`, `api.py`, `service.py`, `actions.py`, `build_router`, `admin.py`, `jobs.py`, `test_panel.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0761904761904762 - nodes in this community are weakly interconnected._