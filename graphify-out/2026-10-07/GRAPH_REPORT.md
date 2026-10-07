# Graph Report - tg-agent-q  (2026-10-07)

## Corpus Check
- 71 files · ~35,532 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 938 nodes · 2576 edges · 57 communities (28 shown, 29 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 239 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6d51b69e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- api.py
- Giveaway
- package.json
- build_router
- giveaway/texts.py
- server.py
- ReplyThrottle
- content_api.py
- compilerOptions
- Settings
- compilerOptions
- actions.py
- keyboards.py
- Vault
- llm.py
- FakeBot
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- check_subscriptions
- env
- test_panel.py
- build_router
- announce_results
- _try_join
- db.py
- Prize
- test_content.py
- test_init_db_adds_new_columns_to_old_tables
- auth.py
- LoginRequests

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 41 edges
3. `Button()` - 32 edges
4. `utcnow()` - 31 edges
5. `ChatRef` - 30 edges
6. `cx()` - 30 edges
7. `build_router()` - 29 edges
8. `ErrorBox()` - 28 edges
9. `GiveawayStatus` - 26 edges
10. `Winner` - 25 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `env()` --calls--> `ChatRef`  [INFERRED]
  tests/test_content.py → src/tgagent/channels/telegram_bot/chats.py
- `env()` --calls--> `Settings`  [INFERRED]
  tests/test_content.py → src/tgagent/config.py
- `env()` --calls--> `Vault`  [INFERRED]
  tests/test_content.py → src/tgagent/core/crypto.py

## Import Cycles
- None detected.

## Communities (57 total, 29 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.05
Nodes (125): AiUsage, api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, GuideVersion (+117 more)

### Community 2 - "api.py"
Cohesion: 0.06
Nodes (49): SponsorChannel, list_sponsors(), list_winners(), participant_counts(), subscription_misses(), auth_logout(), auth_poll(), auth_start() (+41 more)

### Community 3 - "Giveaway"
Cohesion: 0.10
Nodes (30): reveal_next(), ClaimStep, DrawPick, Giveaway, GiveawayStatus, Participant, SubscriptionMiss, Winner (+22 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (18): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+10 more)

### Community 6 - "giveaway/texts.py"
Cohesion: 0.13
Nodes (17): PrizeType, active_item(), btn_same_for_rest(), draw_mode(), giveaway_post(), join_button(), live_ready(), local_time() (+9 more)

### Community 7 - "server.py"
Cohesion: 0.19
Nodes (3): make_server(), serve_panel(), _Server

### Community 9 - "content_api.py"
Cohesion: 0.06
Nodes (38): BadImage, delete_image(), image_path(), read_image(), save_image(), ProposalStatus, Sample, SampleSource (+30 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "Settings"
Cohesion: 0.08
Nodes (18): build_router(), _after_close(), close_now(), close_participation(), draw_loop(), freeze(), live_url(), remind() (+10 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "actions.py"
Cohesion: 0.14
Nodes (9): add_sponsor(), CreateGiveaway, Payout, required_chats(), bot_is_admin(), chat_link(), _get_member(), is_member() (+1 more)

### Community 15 - "keyboards.py"
Cohesion: 0.18
Nodes (15): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+7 more)

### Community 16 - "Vault"
Cohesion: 0.18
Nodes (6): Buyruqlar, graphify, Qat'iy qoidalar, TG Agent Q, Tuzilma, Vault

### Community 17 - "llm.py"
Cohesion: 0.11
Nodes (9): Completion, LLM, LlmError, LlmUsage, month_start(), Msg, _openai_provider(), call() (+1 more)

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
Cohesion: 0.25
Nodes (5): check_subscriptions(), check(), CheckError, CheckProgress, run()

### Community 30 - "env"
Cohesion: 0.18
Nodes (4): create_app(), env(), FakeAI, env()

### Community 31 - "test_panel.py"
Cohesion: 0.19
Nodes (15): future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error(), test_live_draw_flow() (+7 more)

### Community 33 - "build_router"
Cohesion: 0.14
Nodes (8): build_router(), claim_or_default(), start_claim(), _claim_prompt(), JoinCounter, normalize_phone(), notify_users(), mask_card()

### Community 36 - "announce_results"
Cohesion: 0.13
Nodes (10): ActionError, announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), run_auto_draw(), update_giveaway() (+2 more)

### Community 37 - "_try_join"
Cohesion: 0.19
Nodes (6): join(), _try_join(), already_joined(), joined(), joined_but_missing(), not_subscribed()

### Community 40 - "Prize"
Cohesion: 0.23
Nodes (5): Prize, _giveaway(), sm(), test_due_giveaways(), test_participant_numbers_are_sequential_and_unique()

### Community 41 - "test_content.py"
Cohesion: 0.16
Nodes (4): jpeg(), test_monthly_limit_stops_ai(), test_new_proposal_supersedes_old(), test_training_chat_flow()

### Community 46 - "auth.py"
Cohesion: 0.08
Nodes (19): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), BotChat, build_router() (+11 more)

### Community 49 - "LoginRequests"
Cohesion: 0.17
Nodes (5): LoginRequest, LoginRequests, build_router(), login_link(), LoginCB

## Knowledge Gaps
- **118 isolated node(s):** `Maqsad`, `Rollar`, `Ikki "qo'l"`, `Bekor qilish`, `G'olib tanlash` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 367 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Settings` to `build_router`, `api.py`, `announce_results`, `build_router`, `actions.py`, `auth.py`, `llm.py`, `LoginRequests`, `env`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Maqsad`, `Rollar`, `Ikki "qo'l"` to the rest of the system?**
  _118 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.053544061302681994 - nodes in this community are weakly interconnected._
- **Why does `Giveaway` connect `Giveaway` to `build_router`, `api.py`, `announce_results`, `build_router`, `_try_join`, `giveaway/texts.py`, `Prize`, `Settings`, `actions.py`, `auth.py`, `check_subscriptions`, `test_panel.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 24 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0642570281124498 - nodes in this community are weakly interconnected._