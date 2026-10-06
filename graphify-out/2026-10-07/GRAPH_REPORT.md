# Graph Report - tg-agent-q  (2026-10-07)

## Corpus Check
- 71 files · ~35,165 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 930 nodes · 2547 edges · 54 communities (30 shown, 24 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 210 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dc3b0d78`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- content_api.py
- api.py
- service.py
- package.json
- build_router
- AsyncSession
- __main__.py
- ReplyThrottle
- trainer.py
- compilerOptions
- jobs.py
- compilerOptions
- actions.py
- giveaway/texts.py
- TG Agent Q
- llm.py
- giveaway/models.py
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- main
- env
- test_panel.py
- build_router
- tracking.py
- Giveaway
- _try_join
- chat_sample
- GiveawayStatus
- SubscriptionMiss
- JoinCounter
- auth.py
- _openai_provider
- build_router
- _add_missing_columns

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 44 edges
2. `Settings` - 41 edges
3. `Button()` - 32 edges
4. `utcnow()` - 31 edges
5. `ChatRef` - 29 edges
6. `cx()` - 29 edges
7. `build_router()` - 29 edges
8. `ErrorBox()` - 28 edges
9. `main()` - 24 edges
10. `Loading()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `env()` --uses--> `Settings`  [INFERRED]
  tests/test_content.py → src/tgagent/config.py
- `env()` --uses--> `Settings`  [INFERRED]
  tests/test_panel.py → src/tgagent/config.py
- `env()` --uses--> `LLM`  [INFERRED]
  tests/test_content.py → src/tgagent/core/llm.py

## Import Cycles
- None detected.

## Communities (54 total, 24 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.05
Nodes (124): AiUsage, api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, GuideVersion (+116 more)

### Community 1 - "content_api.py"
Cohesion: 0.16
Nodes (18): Sample, StyleGuide, chat(), chat_decide(), chat_message(), ChatIn, DecisionIn, guide() (+10 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (39): parse_prize(), auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff(), Deps (+31 more)

### Community 3 - "service.py"
Cohesion: 0.18
Nodes (9): add_sponsor(), ClaimStep, SponsorChannel, create_giveaway(), due_giveaway_ids(), due_reminder_ids(), first_claim_step(), list_sponsors() (+1 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (15): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+7 more)

### Community 6 - "AsyncSession"
Cohesion: 0.14
Nodes (16): active_giveaways(), list_giveaways(), list_participants(), list_picks(), list_winners(), open_payouts(), participant_counts(), participants_count() (+8 more)

### Community 7 - "__main__.py"
Cohesion: 0.13
Nodes (4): create_app(), make_server(), serve_panel(), _Server

### Community 9 - "trainer.py"
Cohesion: 0.15
Nodes (14): ProposalStatus, SampleSource, TrainMessage, guide_block(), sample_block(), add_sample(), current_guide(), decide() (+6 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "jobs.py"
Cohesion: 0.12
Nodes (18): _after_close(), check_subscriptions(), check(), CheckError, CheckProgress, close_now(), close_participation(), draw_loop() (+10 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 15 - "giveaway/texts.py"
Cohesion: 0.06
Nodes (42): deliver_prize(), start_claim(), _claim_prompt(), claim(), giveaway_post(), JoinCB, manage(), manage_cancel() (+34 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.40
Nodes (4): Buyruqlar, graphify, TG Agent Q, Tuzilma

### Community 17 - "llm.py"
Cohesion: 0.17
Nodes (5): LLM, LlmError, LlmUsage, month_start(), Msg

### Community 18 - "giveaway/models.py"
Cohesion: 0.22
Nodes (4): DrawPick, Base, UTCDateTime, utcnow()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.09
Nodes (21): Agent bilimi, Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Jadval (+13 more)

### Community 27 - "main"
Cohesion: 0.24
Nodes (6): build_router(), bot_is_admin(), chat_link(), _get_member(), is_member(), main()

### Community 30 - "env"
Cohesion: 0.18
Nodes (7): Qat'iy qoidalar, init_db(), make_engine(), make_sessionmaker(), env(), test_init_db_adds_new_columns_to_old_tables(), env()

### Community 31 - "test_panel.py"
Cohesion: 0.06
Nodes (29): BadImage, delete_image(), image_path(), read_image(), save_image(), run(), jpeg(), test_monthly_limit_stops_ai() (+21 more)

### Community 33 - "build_router"
Cohesion: 0.15
Nodes (7): build_router(), claim_or_default(), normalize_phone(), notify_users(), mask_card(), Vault, test_vault_roundtrip()

### Community 34 - "tracking.py"
Cohesion: 0.31
Nodes (6): BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat()

### Community 36 - "Giveaway"
Cohesion: 0.12
Nodes (14): ActionError, announce_results(), cancel_giveaway(), CancelMode, publish_giveaway(), reveal_next(), run_auto_draw(), update_giveaway() (+6 more)

### Community 37 - "_try_join"
Cohesion: 0.27
Nodes (6): join(), _try_join(), Participant, add_participant(), get_participant(), set_miss()

### Community 39 - "GiveawayStatus"
Cohesion: 0.40
Nodes (3): freeze(), GiveawayStatus, cancel_giveaway()

### Community 46 - "auth.py"
Cohesion: 0.10
Nodes (15): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), create_session(), delete_session() (+7 more)

### Community 47 - "_openai_provider"
Cohesion: 0.24
Nodes (5): Completion, _openai_provider(), call(), part(), FakeAI

### Community 49 - "build_router"
Cohesion: 0.33
Nodes (3): build_router(), login_link(), LoginCB

## Knowledge Gaps
- **118 isolated node(s):** `Buyruqlar`, `Tuzilma`, `graphify`, `Maqsad`, `Rollar` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 359 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `jobs.py` to `build_router`, `api.py`, `service.py`, `Giveaway`, `build_router`, `__main__.py`, `actions.py`, `auth.py`, `_openai_provider`, `llm.py`, `build_router`, `main`, `env`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Buyruqlar`, `Tuzilma`, `graphify` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.05312742812742813 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `Giveaway` to `api.py`, `service.py`, `_try_join`, `build_router`, `GiveawayStatus`, `AsyncSession`, `jobs.py`, `JoinCounter`, `actions.py`, `giveaway/texts.py`, `giveaway/models.py`, `test_panel.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.062342342342342344 - nodes in this community are weakly interconnected._