# Graph Report - tg-agent-q  (2026-10-07)

## Corpus Check
- 71 files · ~35,532 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 919 nodes · 2582 edges · 52 communities (33 shown, 19 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 242 edges (avg confidence: 0.94)
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
- Giveaway
- validators.py
- ReplyThrottle
- trainer.py
- compilerOptions
- Settings
- compilerOptions
- jobs.py
- keyboards.py
- TG Agent Q
- llm.py
- UTCDateTime
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- check_subscriptions
- db.py
- test_panel.py
- build_router
- StyleGuide
- actions.py
- _try_join
- chat_sample
- giveaway/models.py
- Prize
- parse_local_datetime
- JoinCounter
- utcnow
- _openai_provider
- build_router

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 41 edges
3. `Button()` - 32 edges
4. `utcnow()` - 31 edges
5. `cx()` - 30 edges
6. `ChatRef` - 30 edges
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

## Communities (52 total, 19 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.05
Nodes (125): AiUsage, api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, GuideVersion (+117 more)

### Community 1 - "content_api.py"
Cohesion: 0.21
Nodes (11): Sample, pending_samples(), chat(), chat_message(), ChatIn, guide(), media_file(), message_out() (+3 more)

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (45): subscription_misses(), auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff(), Deps (+37 more)

### Community 3 - "service.py"
Cohesion: 0.11
Nodes (21): Participant, SponsorChannel, SubscriptionMiss, active_giveaways(), add_participant(), create_giveaway(), due_giveaway_ids(), due_reminder_ids() (+13 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.10
Nodes (5): build_router(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway()

### Community 6 - "Giveaway"
Cohesion: 0.13
Nodes (18): Giveaway, active_item(), auto_draw_failed(), btn_same_for_rest(), draw_mode(), draw_summary(), giveaway_post(), join_button() (+10 more)

### Community 7 - "validators.py"
Cohesion: 0.23
Nodes (9): got_prize(), _digits(), normalize_card(), parse_amount(), parse_prize(), test_amount(), test_card(), test_datetime_is_local() (+1 more)

### Community 9 - "trainer.py"
Cohesion: 0.16
Nodes (10): ProposalStatus, SampleSource, TrainMessage, guide_block(), sample_block(), add_sample(), current_guide(), history() (+2 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "Settings"
Cohesion: 0.16
Nodes (11): _after_close(), close_now(), close_participation(), draw_loop(), freeze(), live_url(), remind(), staff_ids() (+3 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "jobs.py"
Cohesion: 0.11
Nodes (3): CreateGiveaway, Payout, notify_users()

### Community 15 - "keyboards.py"
Cohesion: 0.18
Nodes (15): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+7 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.33
Nodes (5): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma

### Community 17 - "llm.py"
Cohesion: 0.16
Nodes (6): Image, LLM, LlmError, LlmUsage, month_start(), Msg

### Community 18 - "UTCDateTime"
Cohesion: 0.15
Nodes (7): BotChat, build_router(), on_my_status(), forget_chat(), list_chats(), remember_chat(), UTCDateTime

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.09
Nodes (21): Agent bilimi, Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Jadval (+13 more)

### Community 27 - "check_subscriptions"
Cohesion: 0.24
Nodes (7): check_subscriptions(), check(), CheckError, CheckProgress, _get_member(), is_member(), missing_chats()

### Community 30 - "db.py"
Cohesion: 0.08
Nodes (12): build_router(), chat_link(), Vault, _add_missing_columns(), init_db(), make_engine(), make_sessionmaker(), main() (+4 more)

### Community 31 - "test_panel.py"
Cohesion: 0.07
Nodes (23): make_server(), serve_panel(), _Server, jpeg(), test_monthly_limit_stops_ai(), test_new_proposal_supersedes_old(), test_training_chat_flow(), FakeBot (+15 more)

### Community 33 - "build_router"
Cohesion: 0.24
Nodes (7): build_router(), claim_or_default(), start_claim(), normalize_phone(), mask_card(), test_phone(), test_vault_roundtrip()

### Community 34 - "StyleGuide"
Cohesion: 0.22
Nodes (9): StyleGuide, decide(), save_guide(), chat_decide(), DecisionIn, guide_out(), guide_restore(), guide_save() (+1 more)

### Community 36 - "actions.py"
Cohesion: 0.13
Nodes (13): ActionError, add_sponsor(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next(), run_auto_draw() (+5 more)

### Community 37 - "_try_join"
Cohesion: 0.22
Nodes (6): join(), _try_join(), already_joined(), joined(), joined_but_missing(), not_subscribed()

### Community 38 - "chat_sample"
Cohesion: 0.13
Nodes (7): BadImage, delete_image(), image_path(), read_image(), save_image(), chat_sample(), sample_delete()

### Community 39 - "giveaway/models.py"
Cohesion: 0.15
Nodes (13): announce_results(), _claim_prompt(), ClaimStep, DrawPick, GiveawayStatus, Winner, WinnerStatus, cancel_giveaway() (+5 more)

### Community 40 - "Prize"
Cohesion: 0.36
Nodes (3): Prize, PrizeType, test_prizes_block_groups_equal_places()

### Community 46 - "utcnow"
Cohesion: 0.09
Nodes (19): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), utcnow(), create_session() (+11 more)

### Community 47 - "_openai_provider"
Cohesion: 0.24
Nodes (5): Completion, _openai_provider(), call(), part(), FakeAI

### Community 49 - "build_router"
Cohesion: 0.33
Nodes (3): build_router(), login_link(), LoginCB

## Knowledge Gaps
- **118 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 350 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `build_router`, `api.py`, `actions.py`, `build_router`, `giveaway/models.py`, `jobs.py`, `utcnow`, `_openai_provider`, `llm.py`, `build_router`, `db.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.053544061302681994 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `Giveaway` to `api.py`, `service.py`, `actions.py`, `build_router`, `_try_join`, `giveaway/models.py`, `Prize`, `Settings`, `JoinCounter`, `jobs.py`, `UTCDateTime`, `check_subscriptions`, `test_panel.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0688088283024992 - nodes in this community are weakly interconnected._