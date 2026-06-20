# Vyasa Inc. — A Paperclip Company Built on the 29-Partner Fleet

**Status:** Plan (not yet built)
**Author:** Vyasa orchestrator (Claude Code)
**Date:** 2026-06-21
**Sources:** Paperclip — `github.com/paperclipai/paperclip` (MIT) · Fleet — `github.com/darshjme/vyasa-agent` (Apache-2.0)

---

## 0. One-line goal

Stand up a single **Paperclip** deployment that runs **"Vyasa Inc."** — a zero-human company whose org chart, reporting lines, budgets, heartbeats, routines, and governance gates are the 29 Vyasa partners, with the four blocking authorities (Kavach, Indra, Mitra, Varuna) wired as hard approval gates.

---

## 1. How the two systems map

| Concept | Paperclip | Vyasa Agent | Decision |
|---|---|---|---|
| Owner | Board member (human) | Operator | **Darsh = Board** |
| Top agent | CEO agent | `vyasa` Chief Orchestrator | **`vyasa` = CEO** |
| Managers | Directors (CMO/CTO/COO) | C-suite specialists | mapped in §3 |
| Workers | Specialist agents | Vyasa 19 + Graymatter 10 | mapped in §3 |
| Identity/voice/tools | `AGENTS.md` per agent | `employees/*.yaml` (voice/model/tool scope) | **transpile YAML → AGENTS.md** (§5) |
| Permissions | scoped per position | capability matrix (least-privilege) | **carry matrix into AGENTS.md tool scope** |
| Wake mechanism | heartbeat | lazy-load on `/ask <partner>` | **warm 3, heartbeat the rest** (§6) |
| Spend control | per-agent monthly budget, hard stop | (none today) | **add budgets** (§4) |
| Recurring work | routines (cron/webhook/API) → tracked issue | (none today) | **define routines** (§7) |
| Hard stops | governance approval workflows | blocking authority (4 partners) | **map to approval gates** (§8) |
| Distribution | portable skill pack (zip, auto-discovered) | repo + installer | **ship "Vyasa Inc." as a skill pack** (§9) |

**Key insight:** Paperclip is the *org/governance/billing* layer; the Vyasa partners are the *labor*. We do not throw away the Vyasa daemon — we either (A) wrap each partner as a heartbeat-able agent, or (B) re-express each partner as a Claude Code adapter with the partner's prompt + tool scope. Recommended: **B** for engineering partners (they need Claude Code's tools), **A** (HTTP adapter to the running Vyasa daemon) for partners that already have bespoke logic. See §5.

---

## 2. Topology

```
Darsh (Board)
   │  approves: hires, budget changes, strategy, blocking-gate overrides
   ▼
Paperclip server (localhost:3100, embedded Postgres)
   │  org chart · heartbeats · budgets · routines · audit log · approvals
   ▼
Company "Vyasa Inc."
   ├─ CEO: vyasa
   ├─ Directors (7)
   └─ Specialists (21)  ── each = Claude Code adapter OR HTTP adapter → Vyasa daemon
```

---

## 3. Org chart (all 29 partners placed)

### Board
- **Darsh** — human board member. Sole authority to approve hires, raise budgets, override blocking gates, change strategy.

### CEO (reports to Board)
- **`vyasa`** — Chief Orchestrator. Decomposes board goals → department objectives, routes briefs, gates final outputs.

### Directors (report to CEO)
| Partner | Title | Department |
|---|---|---|
| `iyer` | CTO / Chief Architect | Engineering |
| `chanakya` | Chief Product Officer | Product & Design |
| `sarabhai` | Managing Partner (Delivery) | Delivery/PMO |
| `kavach` | CISO **(blocking)** | Security |
| `varuna` | Chief Risk Officer **(blocking)** | Risk |
| `mitra` | General Counsel **(blocking)** | Legal |
| `kapoor` | CMO | Growth |

### Engineering (reports to `iyer`)
- `vishwakarma` — Systems Architect (GOAL→DESIGN→PHASES→ADR)
- `prometheus` — Senior Full-Stack Engineer (Py/TS/Rust/Go)
- `shiva` — Refactoring Specialist (zero behavioral change)
- `hermes` — Integration Specialist (FIX, MT5, Stripe, Kafka)
- `aryabhata` — Data & AI Scientist (time-series, backtests, model ops)
- `bose` — MCP / Graphify Memory architect
- `desai` — Mobile Lead (Flutter, Android, iOS)

### Reliability & Quality (reports to `indra`, who reports to `iyer`)
- `indra` — SRE **(blocking on SLO breach)** — sub-director under Engineering
- `dharma` — Code Reviewer (correctness, security, coverage)
- `agni` — QA Engineer (happy/edge/error/concurrency)
- `sherlock` — Root Cause Analyst (reproduce→isolate→fix)
- `sharma` — QA & Docs Lead (Playwright, HTML docs)

### Infrastructure & Ops (reports to `iyer`)
- `vayu` — DevOps (Docker, secrets, health checks)
- `kubera` — Cloud Cost Optimizer
- `garuda` — Recon Agent (read-only dependency/hotspot mapping)
- `rao` — Release Engineer (GH Actions, bundles, semver)

### Product & Design (reports to `chanakya`)
- `kamadeva` — UX Designer (wireflows, WCAG 2.1 AA)
- `krishnan` — HCI Director (Web UI, i18n, accessibility)
- `saraswati` — Technical Writer (READMEs, runbooks, API refs)

### Growth (reports to `kapoor`)
- `verma` — Social & Viral Lead

### Security (reports to `kavach`)
- `reddy` — Security Chief (pentest, installer approval)

> Note: `aryabhata` appears in both the Vyasa-19 and Graymatter-10 rosters; deduped to a single Engineering seat. Total distinct seats = **28 agents + 1 board human**.

---

## 4. Budget policy — UNLIMITED (current decision)

**Board decision (2026-06-21): no budget caps for now.** Every agent runs uncapped; no per-agent monthly limit, no company master cap. The goal right now is full capability, not cost control.

In Paperclip terms this means: leave per-agent budget **unset/null** (or set to a very high sentinel if the schema requires a number, e.g. `999999`), and do not configure a company master cap. Keep **cost tracking ON** (Paperclip tracks tokens/cost by company/agent/project/goal regardless) so we still have full visibility — we just don't enforce a stop.

- **Hard stops:** none.
- **Visibility:** dashboard cost tracking stays on for observability only.
- **Re-tightening later:** when we want guardrails, drop in the tiered caps below as a starting point — no structural change required, just fill in budget fields.

<details><summary>Reference tiers for when we re-enable caps (not active now)</summary>

| Tier | Agents | Suggested cap |
|---|---|---|
| CEO | vyasa | $50 |
| Directors | iyer, chanakya, sarabhai, kavach, varuna, mitra, kapoor | $30 |
| Eng sub-director | indra | $25 |
| Specialists (heavy) | prometheus, vishwakarma, aryabhata, hermes, dharma, agni | $20 |
| Specialists (standard) | shiva, bose, desai, sherlock, sharma, vayu, kubera, garuda, rao, kamadeva, krishnan, saraswati, verma, reddy | $15 |

</details>

---

## 5. Agent definition: YAML → AGENTS.md transpile

Each `employees/<partner>.yaml` (voice, model, tool scope, capability matrix) is transpiled to a Paperclip `AGENTS.md`. Template per agent:

```markdown
# <Title> — <partner>
**Reports to:** <boss>
**Adapter:** claude-code | http
**Model:** <from YAML, default claude-opus-4-8>
**Budget:** unlimited (no cap; cost tracking on for visibility)

## Charter
<one-paragraph role from roster.md, verbatim voice>

## Tool scope (from capability matrix)
- read: <paths/globs>           # default: read-only
- write: <paths/globs>          # only if granted
- shell: <allowed cmds>         # only if granted
- network: <allowed hosts>      # only if granted

## Blocking authority
<yes/no — if yes, which actions require this agent's sign-off>

## Heartbeat
<warm | cron expr | webhook>
```

**Adapter choice per agent:**
- **claude-code adapter** — all Engineering, Reliability, Infra, Design, Docs partners (need real tools/file edits). Each runs as a tracked Claude Code instance with the partner's AGENTS.md as system context.
- **http adapter → Vyasa daemon** — partners whose bespoke logic already lives in the Vyasa Python package (router/gateway). Paperclip heartbeats hit a thin HTTP endpoint that maps to `/ask <partner> <request>` and returns the result as the issue resolution.

A tiny build script (`scripts/transpile.py`) reads `employees/*.yaml` + `docs/roster.md` and emits one `AGENTS.md` per agent into the skill-pack layout (§9). This keeps Vyasa's YAML as the single source of truth.

---

## 6. Heartbeats (wake schedule)

Mirror Vyasa's lazy-load doctrine:
- **Warm always:** `vyasa` (CEO), `sarabhai` (delivery), `prometheus` (lead eng) — boot warm, frequent heartbeat.
- **On-demand / webhook:** all other engineering & quality partners wake on issue assignment or VCS webhook.
- **Scheduled (cron):** ops/growth partners — see routines §7.

This preserves the "only 3 warm by default" cost profile while letting Paperclip's heartbeat scheduler replace the manual `/ask` trigger.

---

## 7. Routines (recurring, tracked work)

Each routine creates a tracked Paperclip issue and wakes the assignee.

| Routine | Trigger | Assignee | Output |
|---|---|---|---|
| Code review | PR opened (webhook) | `dharma` | review verdict, blocks merge on fail |
| QA pass | PR ready / nightly cron | `agni` | test report |
| E2E + docs HTML | merge to main (webhook) | `sharma` | Playwright run + HTML docs |
| Release cut | tag push (webhook) | `rao` | bundle + semver + changelog |
| SLO check | cron `*/15 * * * *` | `indra` | SLO budget status (blocks deploy on breach) |
| Cloud cost report | cron weekly Mon 09:00 | `kubera` | right-sizing recommendations |
| Recon sweep | cron weekly | `garuda` | dependency/hotspot map (read-only) |
| Security scan | cron weekly + pre-release | `reddy` → `kavach` | OWASP/pentest report (blocking gate) |
| Marketing batch | cron weekly | `kapoor` → `verma` | listing copy, SEO, social |
| Risk review | pre-release | `varuna` | pre/in/post-trade controls sign-off (blocking) |
| License/compliance | pre-release | `mitra` | OSS license + data-residency clearance (blocking) |

---

## 8. Governance & approval gates

Map Vyasa's **four blocking authorities** onto Paperclip approval workflows. A blocked action cannot proceed until the named agent (and, for high-impact actions, the Board) signs off.

| Gate | Owner | Blocks |
|---|---|---|
| Security gate | `kavach` (+ `reddy`) | any release with unresolved OWASP/SOC2/PCI finding |
| Reliability gate | `indra` | any deploy while SLO budget is exhausted |
| Legal gate | `mitra` | any release with license conflict or data-residency violation |
| Risk gate | `varuna` | any trading-path change failing pre/in/post-trade controls |

**Board-only approvals (Paperclip governance):**
- Hiring a new agent / changing the org chart.
- Raising any budget cap or the company master cap.
- Overriding any of the four blocking gates.
- Strategic-direction changes to the company mission.

---

## 9. "Vyasa Inc." as a portable skill pack

Package the whole company as a Paperclip skill pack (zip, auto-discovered, no restart) so it's reproducible and shareable:

```
vyasa-inc-pack/
├── company.json            # name, mission template, master budget, gates
├── org-chart.json          # 28 agents, titles, reporting lines
├── budgets.json            # per-agent caps + thresholds (§4)
├── routines.json           # cron/webhook routines (§7)
├── governance.json         # 4 blocking gates + board approvals (§8)
└── agents/
    ├── vyasa/AGENTS.md
    ├── iyer/AGENTS.md
    ├── ... (one dir per partner)
    └── reddy/AGENTS.md
```

Generated by `scripts/transpile.py` from the Vyasa repo so the YAML stays SSOT.

---

## 10. Build phases

1. **Provision Paperclip** — `npx paperclipai onboard --yes`; verify dashboard at `:3100`; set Anthropic API key.
2. **Transpile** — write `scripts/transpile.py`; generate the `vyasa-inc-pack/` from `employees/*.yaml` + `roster.md`.
3. **Create company** — import the pack; create "Vyasa Inc." with mission template; hire `vyasa` as CEO.
4. **Org build** — approve director hires, then specialist hires; verify reporting lines match §3.
5. **Adapters** — wire claude-code adapters for the build partners; stand up the HTTP shim to the Vyasa daemon for bespoke partners (§5).
6. **Gates** — apply `governance.json` (budgets left unlimited per §4); test a blocking gate with a deliberate failing case.
7. **Routines** — register `routines.json`; dry-run the PR-review and SLO-check routines.
8. **E2E** — run one real goal end-to-end (e.g. "ship a small feature"): brief → vyasa decomposes → eng builds → dharma/agni gate → kavach/indra/mitra/varuna clear → rao releases. Audit the trail.
9. **Harden** — confirm PII scrubber + white-label CI check still run inside agent prompts; confirm no vendor-name leakage; confirm budget caps held.

---

## 11. Acceptance criteria

- [ ] All 28 agents present with correct titles and reporting lines (§3).
- [ ] Budgets unlimited (no caps); cost tracking visible per agent on the dashboard.
- [ ] Each of the 4 blocking gates demonstrably blocks a release on a seeded failure.
- [ ] Board approval required for hires, budget raises, gate overrides, strategy changes.
- [ ] At least the PR-review, SLO-check, and release routines fire and create tracked issues.
- [ ] One full goal runs E2E through the org with a clean audit trail.
- [ ] Vyasa YAML remains SSOT; re-running the transpiler reproduces the pack.

---

## 12. Open questions for the Board

1. **Adapter strategy** — go all-Claude-Code (re-express every partner), or keep the Vyasa daemon alive behind HTTP for the bespoke partners? (Plan recommends hybrid, §5.)
2. **Hosting** — local Mac (per Vyasa's design) or the .161/.172 server (per the no-local-runtime standing rule)? The latter fits "test+push, no local runtime" but Paperclip's onboarding assumes localhost.
3. ~~**Budget ceiling**~~ — RESOLVED: unlimited for now (§4), re-tighten later.
4. **First mission** — what real goal should Vyasa Inc. run first as the E2E proof?
