# Graph Report - tg-agent-q  (2026-10-06)

## Corpus Check
- 62 files · ~28,194 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .graphify-bak 1, .example 1)

## Summary
- 774 nodes · 2124 edges · 41 communities (23 shown, 18 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 202 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b0602b9d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ui.tsx
- Settings
- api.py
- giveaway/texts.py
- package.json
- build_router
- build_router
- server.py
- participant.py
- giveaway/models.py
- compilerOptions
- Giveaway
- compilerOptions
- __main__.py
- keyboards.py
- TG Agent Q
- Prize
- _try_join
- permissions
- .oxlintrc.json
- TG Agent Q — 1-agent: Rozigrish kanali agenti
- tsconfig.json
- tgagent
- LoginRequests
- test_panel.py
- admin.py
- actions.py

## God Nodes (most connected - your core abstractions)
1. `Giveaway` - 51 edges
2. `Settings` - 36 edges
3. `build_router()` - 29 edges
4. `ChatRef` - 29 edges
5. `GiveawayStatus` - 26 edges
6. `utcnow()` - 26 edges
7. `Prize` - 25 edges
8. `Winner` - 25 edges
9. `Button()` - 23 edges
10. `announce_results()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Qat'iy qoidalar` --references--> `Vault`  [INFERRED]
  CLAUDE.md → src/tgagent/core/crypto.py
- `Qat'iy qoidalar` --references--> `init_db()`  [INFERRED]
  CLAUDE.md → src/tgagent/core/db.py
- `test_live_mode_time_is_only_reminder()` --calls--> `_try_join()`  [INFERRED]
  tests/test_panel.py → src/tgagent/agents/giveaway/handlers/participant.py
- `test_throttle_limits_repeated_error_replies()` --uses--> `ReplyThrottle`  [INFERRED]
  tests/test_throttle.py → src/tgagent/agents/giveaway/handlers/participant.py
- `run()` --indirect_call--> `sm()`  [INFERRED]
  src/tgagent/agents/giveaway/jobs.py → tests/test_service.py

## Import Cycles
- None detected.

## Communities (41 total, 18 thin omitted)

### Community 0 - "ui.tsx"
Cohesion: 0.06
Nodes (102): api, ApiError, BotChat, Giveaway, GiveawayDetail, GiveawayStatus, LivePick, LiveState (+94 more)

### Community 1 - "Settings"
Cohesion: 0.20
Nodes (8): _after_close(), close_now(), close_participation(), draw_loop(), live_url(), remind(), staff_ids(), Settings

### Community 2 - "api.py"
Cohesion: 0.07
Nodes (38): SponsorChannel, auth_logout(), auth_poll(), auth_start(), bot_chats(), CancelIn, current_staff(), Deps (+30 more)

### Community 3 - "giveaway/texts.py"
Cohesion: 0.17
Nodes (9): active_item(), auto_draw_failed(), draw_mode(), live_ready(), live_reminder(), local_time(), payout_card(), results_post() (+1 more)

### Community 4 - "package.json"
Cohesion: 0.06
Nodes (34): dependencies, react, react-dom, react-router-dom, @tanstack/react-query, devDependencies, oxlint, tailwindcss (+26 more)

### Community 5 - "build_router"
Cohesion: 0.07
Nodes (17): build_router(), got_ends_at(), got_prize(), publish(), sponsors_done(), toggle_auto(), _draft_giveaway(), _digits() (+9 more)

### Community 6 - "build_router"
Cohesion: 0.33
Nodes (3): build_router(), login_link(), LoginCB

### Community 7 - "server.py"
Cohesion: 0.19
Nodes (3): create_app(), make_server(), _Server

### Community 8 - "participant.py"
Cohesion: 0.11
Nodes (9): build_router(), claim_or_default(), ReplyThrottle, normalize_phone(), notify_users(), mask_card(), Vault, test_throttle_limits_repeated_error_replies() (+1 more)

### Community 9 - "giveaway/models.py"
Cohesion: 0.06
Nodes (27): commit_of(), new_seed(), participants_file(), participants_hash(), rank(), ticket_hash(), DrawPick, BotChat (+19 more)

### Community 10 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 11 - "Giveaway"
Cohesion: 0.05
Nodes (52): ActionError, add_sponsor(), announce_results(), cancel_giveaway(), CancelMode, deliver_prize(), publish_giveaway(), reveal_next() (+44 more)

### Community 12 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 13 - "__main__.py"
Cohesion: 0.12
Nodes (13): Qat'iy qoidalar, build_router(), bot_is_admin(), chat_link(), _get_member(), is_member(), build_router(), init_db() (+5 more)

### Community 15 - "keyboards.py"
Cohesion: 0.17
Nodes (16): claim(), giveaway_post(), JoinCB, manage(), manage_cancel(), manage_confirm(), ManageCB, owner_menu() (+8 more)

### Community 16 - "TG Agent Q"
Cohesion: 0.40
Nodes (4): Buyruqlar, graphify, TG Agent Q, Tuzilma

### Community 17 - "Prize"
Cohesion: 0.18
Nodes (10): start_claim(), _claim_prompt(), Prize, PrizeType, btn_same_for_rest(), money(), prize_text(), prizes_block() (+2 more)

### Community 18 - "_try_join"
Cohesion: 0.16
Nodes (7): join(), JoinCounter, _try_join(), already_joined(), joined(), joined_but_missing(), not_subscribed()

### Community 19 - "permissions"
Cohesion: 0.25
Nodes (7): hooks, PreToolUse, permissions, allow, defaultMode, deny, $schema

### Community 20 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 21 - "TG Agent Q — 1-agent: Rozigrish kanali agenti"
Cohesion: 0.12
Nodes (15): Bekor qilish, Boshqaruv paneli (CRM sayt, keyin Mini App), Bosqichlar, G'olib tanlash, Ikki "qo'l", Ishga tushirish uchun kerak bo'ladi, Kanal yoki guruh, Maqsad (+7 more)

### Community 31 - "test_panel.py"
Cohesion: 0.10
Nodes (15): FakeBot, future(), login(), test_auto_draw_and_editor_runs_live(), test_bot_chats_lists_admin_channels_not_yet_sponsors(), test_create_giveaway_flow(), test_editor_cannot_see_payouts(), test_invite_link_in_ref_gives_clear_error() (+7 more)

### Community 41 - "actions.py"
Cohesion: 0.18
Nodes (9): check_subscriptions(), check(), CheckError, CheckProgress, required_chats(), start_check(), run(), ChatRef (+1 more)

## Knowledge Gaps
- **109 isolated node(s):** `$schema`, `defaultMode`, `allow`, `deny`, `PreToolUse` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 308 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Giveaway` connect `Giveaway` to `Settings`, `api.py`, `giveaway/texts.py`, `build_router`, `admin.py`, `participant.py`, `actions.py`, `giveaway/models.py`, `Prize`, `_try_join`, `test_panel.py`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `Giveaway` (e.g. with `announce_results()` and `publish_giveaway()`) actually correct?**
  _`Giveaway` has 38 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `defaultMode`, `allow` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ui.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.06170798898071626 - nodes in this community are weakly interconnected._
- **Why does `Settings` connect `Settings` to `api.py`, `build_router`, `admin.py`, `build_router`, `participant.py`, `actions.py`, `giveaway/models.py`, `Giveaway`, `__main__.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `Settings` (e.g. with `add_sponsor()` and `announce_results()`) actually correct?**
  _`Settings` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06956521739130435 - nodes in this community are weakly interconnected._