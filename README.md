# Vyasa Inc. — a Paperclip company

**Vyasa Inc.** is a 29-agent autonomous software & product company. It is the
[Vyasa Agent](https://github.com/darshjme/vyasa-agent) fleet re-expressed as a
[**Paperclip**](https://github.com/paperclipai/paperclip) company that conforms to the
[**Agent Companies** specification](https://agentcompanies.io/specification) (`agentcompanies/v1`).

> If a single agent is an *employee*, this repo is the *company*: an org chart, reporting
> lines, scheduled routines, blocking approval gates, and a hard quality gate — importable
> into any Paperclip deployment with one command.

```
Board (you)
  └─ Vyasa — CEO / Chief Orchestrator
       ├─ Chanakya — CPO ............... Kamadeva, Saraswati
       ├─ Vishwakarma — Chief Architect  Prometheus, Shiva, Hermes, Aryabhata,
       │                                 Sherlock, Garuda, Dharma, Agni
       ├─ Kavach — CISO ⛔ .............. Dr. Reddy
       ├─ Indra — VP SRE ⛔ ............. Vayu, Kubera
       ├─ Varuna — Chief Risk Officer ⛔
       ├─ Mitra — General Counsel ⛔
       ├─ Dr. Kapoor — CMO ............. Dr. Verma
       └─ Dr. Sarabhai — Managing Partner
            └─ Dr. Iyer — Chief Architect (Product)
                 ├─ Dr. Krishnan — HCI Director
                 ├─ Dr. Desai — Mobile Lead
                 └─ Dr. Bose — MCP / Memory
            ├─ Dr. Sharma — QA & Docs Lead
            └─ Dr. Rao — Release Engineer

⛔ = blocking authority (veto power over releases)
```

## Getting started

You need a running [Paperclip](https://github.com/paperclipai/paperclip) deployment
(`npx paperclipai onboard --yes`, dashboard at `http://localhost:3100`) and an Anthropic
API key.

```bash
# clone this package
git clone https://github.com/darshjme/vyasa-paperclip.git
cd vyasa-paperclip

# import the company into Paperclip
paperclipai company import --from .
```

Then open the dashboard, confirm the org chart, and hire **Vyasa** as CEO. Vyasa
decomposes your goals to the directors, who dispatch to specialists.

**Budget:** unlimited by default — no per-agent caps and no company master cap. Cost
tracking stays on for visibility. To add guardrails later, set per-agent budgets in the
Paperclip UI (suggested tiers are in [`PLAN.md`](PLAN.md) §4).

## Workflow

Hub-and-spoke with pipeline stages inside Engineering and Delivery:

1. The **Board** gives **Vyasa** (CEO) a company goal.
2. **Vyasa** decomposes it and routes to the relevant **director**.
3. Directors dispatch to **specialists**; work flows **plan → build → review → secure → ship**.
4. The four **blocking** directors (Kavach, Indra, Varuna, Mitra) must clear before any release.
5. Every output passes the **quality gate** before Vyasa accepts it.

### Quality gate (every output)

- `confidence_score: float` — must be ≥ 0.80 to be accepted
- `verification_step: str` — how the result was verified
- `summary: str` — one paragraph: what changed and why
- `flags: list[str]` — CRITICAL / HIGH / MEDIUM / LOW

Vyasa rejects and re-dispatches any output that fails the gate. A single CRITICAL finding
from a blocking director halts the batch.

## Org chart

| Agent | Title | Reports to | Blocking | Model |
|---|---|---|---|---|
| `vyasa` | Chief Executive Officer / Chief Orchestrator | — | | opus |
| `chanakya` | Chief Product Officer | `vyasa` | | opus |
| `vishwakarma` | Chief Systems Architect | `vyasa` | | opus |
| `kavach` | Chief Information Security Officer | `vyasa` | ⛔ | opus |
| `indra` | VP Site Reliability | `vyasa` | ⛔ | opus |
| `varuna` | Chief Risk Officer | `vyasa` | ⛔ | opus |
| `mitra` | General Counsel | `vyasa` | ⛔ | opus |
| `dr-kapoor` | Chief Marketing Officer | `vyasa` | | sonnet |
| `dr-sarabhai` | Managing Partner (Delivery) | `vyasa` | | opus |
| `prometheus` | Senior Full-Stack Engineer | `vishwakarma` | | opus |
| `shiva` | Refactoring Specialist | `vishwakarma` | | sonnet |
| `hermes` | Integration Specialist | `vishwakarma` | | sonnet |
| `aryabhata` | Data & AI Scientist | `vishwakarma` | | sonnet |
| `sherlock` | Root Cause Analyst | `vishwakarma` | | opus |
| `garuda` | Recon Engineer | `vishwakarma` | | haiku |
| `dharma` | Code Reviewer | `vishwakarma` | | opus |
| `agni` | QA Engineer | `vishwakarma` | | haiku |
| `vayu` | DevOps Engineer | `indra` | | haiku |
| `kubera` | Cloud Cost Optimizer | `indra` | | haiku |
| `kamadeva` | UX & Workflow Designer | `chanakya` | | sonnet |
| `saraswati` | Technical Writer | `chanakya` | | haiku |
| `dr-reddy` | Security Chief (Pen-test) | `kavach` | | sonnet |
| `dr-verma` | Social & Viral Lead | `dr-kapoor` | | sonnet |
| `dr-iyer` | Chief Architect (Product) | `dr-sarabhai` | | opus |
| `dr-sharma` | QA & Docs Lead | `dr-sarabhai` | | sonnet |
| `dr-rao` | GitHub / Release Engineer | `dr-sarabhai` | | haiku |
| `dr-krishnan` | HCI Director | `dr-iyer` | | sonnet |
| `dr-desai` | Mobile Lead | `dr-iyer` | | sonnet |
| `dr-bose` | MCP / Graphify Memory Architect | `dr-iyer` | | haiku |

## Intent routing cheat-sheet

Carried over from the Vyasa fleet — which agent leads, and the typical follow-up chain:

| Incoming intent | Primary | Follow-up |
|---|---|---|
| New greenfield feature | `chanakya` | `vishwakarma` → `kavach` → `prometheus` → `agni` → `dharma` |
| MT5 / bridge integration | `hermes` | `varuna` → `kavach` → `prometheus` → `agni` |
| KYC / AML flow | `kavach` | `mitra` → `varuna` → `prometheus` → `agni` |
| Deploy to prod | `kavach` | `indra` → `vayu` → `kubera` |
| Incident / bug | `sherlock` | `prometheus` → `agni` |
| Codebase recon | `garuda` | hand off to relevant lead |
| Docs / runbook | `saraswati` | `dr-sharma` review |
| UX / admin workflow | `kamadeva` | `dr-krishnan` → `prometheus` |
| Plan / strategy | `chanakya` | `vishwakarma` |
| Cost audit | `kubera` | `vishwakarma` |
| Refactor | `shiva` | `agni` |
| Listing copy | `dr-kapoor` | `dr-verma` |
| Release cut | `dr-rao` | `dr-sharma` → `dr-reddy` |
| Memory / graph query | `dr-bose` | — |

## Scheduled routines

Pre-defined recurring tasks under [`tasks/`](tasks/):

| Routine | Assignee | Cadence |
|---|---|---|
| SLO budget check | `indra` | daily 09:00 |
| Weekly cost audit | `kubera` | Mon 09:00 |
| Weekly recon sweep | `garuda` | Mon 08:00 |
| Weekly security scan | `dr-reddy` → `kavach` | Wed 09:00 |

## Repository layout

```
COMPANY.md              # company root (agentcompanies/v1)
agents/<slug>/AGENTS.md # 29 agent definitions
tasks/<slug>/TASK.md    # scheduled routines
.paperclip.yaml         # Paperclip vendor extension (adapters + env)
source/                 # vendored Vyasa employee YAMLs (single source of truth)
scripts/transpile.py    # regenerates the package from source/
PLAN.md                 # design rationale, mapping, build phases
```

## Regenerating

The package is generated from `source/employees/*.yaml`. Edit the source (or the org
map in the script) and re-run:

```bash
python3 scripts/transpile.py
```

## Citations & references

- Fleet source: [darshjme/vyasa-agent](https://github.com/darshjme/vyasa-agent) (Apache-2.0)
- Platform: [Paperclip](https://github.com/paperclipai/paperclip) (MIT)
- Spec: [Agent Companies specification](https://agentcompanies.io/specification)

## License

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE). Agent roles and tool scopes are
derived from the Apache-2.0 Vyasa Agent project.
