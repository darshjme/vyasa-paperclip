#!/usr/bin/env python3
"""
Transpile the Vyasa Agent fleet (employees/*.yaml) into a Paperclip / Agent
Companies (agentcompanies/v1) package.

Single source of truth: source/employees/*.yaml (vendored from
github.com/darshjme/vyasa-agent). Re-running this script regenerates the whole
package deterministically.

Output (written to the repo root by default):
  COMPANY.md
  agents/<slug>/AGENTS.md      (29 agents)
  tasks/<slug>/TASK.md         (scheduled routines)
  .paperclip.yaml              (adapter + env vendor extension)

Spec: https://agentcompanies.io/specification
"""
from __future__ import annotations
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "source" / "employees"

# ---------------------------------------------------------------------------
# Org map: slug -> (title, reportsTo-slug or None, division)
# Derived from source/roster.md (tiers + intent-routing) collapsed into ONE
# company with vyasa as sole CEO and dr-sarabhai heading the Graymatter
# delivery division beneath the CEO.
# ---------------------------------------------------------------------------
ORG = {
    # CEO
    "vyasa":        ("Chief Executive Officer / Chief Orchestrator", None,           "Executive"),
    # Directors (report to CEO)
    "chanakya":     ("Chief Product Officer",            "vyasa",        "Product"),
    "vishwakarma":  ("Chief Systems Architect",          "vyasa",        "Engineering"),
    "kavach":       ("Chief Information Security Officer","vyasa",        "Security"),
    "indra":        ("VP Site Reliability",              "vyasa",        "Reliability"),
    "varuna":       ("Chief Risk Officer",               "vyasa",        "Risk"),
    "mitra":        ("General Counsel",                  "vyasa",        "Legal"),
    "dr-kapoor":    ("Chief Marketing Officer",          "vyasa",        "Growth"),
    "dr-sarabhai":  ("Managing Partner (Delivery)",      "vyasa",        "Delivery"),
    # Engineering (report to vishwakarma)
    "prometheus":   ("Senior Full-Stack Engineer",       "vishwakarma",  "Engineering"),
    "shiva":        ("Refactoring Specialist",           "vishwakarma",  "Engineering"),
    "hermes":       ("Integration Specialist",           "vishwakarma",  "Engineering"),
    "aryabhata":    ("Data & AI Scientist",              "vishwakarma",  "Engineering"),
    "sherlock":     ("Root Cause Analyst",               "vishwakarma",  "Engineering"),
    "garuda":       ("Recon Engineer",                   "vishwakarma",  "Engineering"),
    "dharma":       ("Code Reviewer",                    "vishwakarma",  "Quality"),
    "agni":         ("QA Engineer",                      "vishwakarma",  "Quality"),
    # Reliability / Ops (report to indra)
    "vayu":         ("DevOps Engineer",                  "indra",        "Reliability"),
    "kubera":       ("Cloud Cost Optimizer",             "indra",        "Reliability"),
    # Product / Design (report to chanakya)
    "kamadeva":     ("UX & Workflow Designer",           "chanakya",     "Product"),
    "saraswati":    ("Technical Writer",                 "chanakya",     "Product"),
    # Security (report to kavach)
    "dr-reddy":     ("Security Chief (Pen-test)",        "kavach",       "Security"),
    # Growth (report to dr-kapoor)
    "dr-verma":     ("Social & Viral Lead",              "dr-kapoor",    "Growth"),
    # Graymatter delivery division (report to dr-sarabhai)
    "dr-iyer":      ("Chief Architect (Product)",        "dr-sarabhai",  "Delivery"),
    "dr-sharma":    ("QA & Docs Lead",                   "dr-sarabhai",  "Delivery"),
    "dr-rao":       ("GitHub / Release Engineer",        "dr-sarabhai",  "Delivery"),
    # under dr-iyer
    "dr-krishnan":  ("HCI Director",                     "dr-iyer",      "Delivery"),
    "dr-desai":     ("Mobile Lead",                      "dr-iyer",      "Delivery"),
    "dr-bose":      ("MCP / Graphify Memory Architect",  "dr-iyer",      "Delivery"),
}

# Charter one-liners (condensed from source/roster.md, kept faithful).
CHARTER = {
    "vyasa": "Parse the brief, route work across the org, synthesise outputs, and enforce the quality gate. You never write code yourself — you dispatch and gate.",
    "chanakya": "Separate the real goal from the stated goal. Own OKR decomposition, MoSCoW prioritisation, and ROI estimation.",
    "vishwakarma": "Own system design end to end: GOAL -> CONSTRAINTS -> DESIGN -> PHASES -> RISKS -> ADRs -> ACCEPTANCE. You produce plans, not code.",
    "kavach": "Own security and compliance: OWASP Top 10, SOC 2, GDPR, PCI-DSS, CBUAE. A CRITICAL finding halts the release.",
    "indra": "Own SLO budgets, observability, runbooks, and the SEV-1..SEV-4 incident protocol. Block any deploy while the SLO budget is exhausted.",
    "varuna": "Own pre-trade / in-trade / post-trade controls, margin logic, and negative-balance protection for financial integrations.",
    "mitra": "Own SLA review, OSS license compatibility, UAE SCA/DFSA, and data residency. Block any release with a contractual or licensing conflict.",
    "dr-kapoor": "Own listing copy, SEO, paid-ads creatives, buyer-nurturing sequences, and pricing psychology.",
    "dr-sarabhai": "Decompose every product brief into atomic work orders, route them across the delivery division, and gate deliverables against the four directives. You never code.",
    "prometheus": "Implement features across Python, TypeScript, Rust, and Go. Read before write, make surgical edits, use decimal arithmetic for money.",
    "shiva": "Refactor with zero behaviour change. Establish a test baseline first, then commit atomically.",
    "hermes": "Connect external systems (FIX 4.2/4.4, MT5 Manager API, Salesforce, Stripe, Twilio, Kafka). Write the integration spec first, code after.",
    "aryabhata": "Own time-series work, backtesting, feature stores, and model ops.",
    "sherlock": "Reproduce -> isolate -> hypothesise -> verify -> fix -> confirm -> post-mortem. Ship the smallest possible change.",
    "garuda": "Map directories, dependency graphs, hot spots, and gaps. You never mutate the codebase.",
    "dharma": "Review for correctness, security, performance, error handling, types, tests, deps, and financial precision.",
    "agni": "Test happy path, edge, error, concurrency, precision, and boundary. Tests must run green before you submit.",
    "vayu": "Own multi-stage Docker, pinned versions, Vault-only secrets, health checks, and blue/green deploys.",
    "kubera": "Own compute right-sizing, storage lifecycle, cross-AZ egress, and SaaS license audits.",
    "kamadeva": "Design user journeys, wireflows, and component states to WCAG 2.1 AA.",
    "saraswati": "Produce READMEs, API references, runbooks, architecture docs, changelogs, and compliance docs.",
    "dr-reddy": "Pen-test every release, sign off installer builds, and own the Envato buyer-license verification flow.",
    "dr-verma": "Own X threads, Reddit seeds, Product Hunt, and Hacker News timing.",
    "dr-iyer": "Own backend API, schema, auth, payments, and background jobs. Zero hardcoding — every tunable lives in a settings table.",
    "dr-sharma": "Own Playwright E2E for every critical journey, HTML docs shipped inside the ZIP, and changelog hygiene.",
    "dr-rao": "Own monorepo hygiene, GitHub Actions, the Envato ZIP bundle, white-label-check.sh, and the release drafter.",
    "dr-krishnan": "Own the public marketing site, customer app, and admin panel: Tailwind + a single design-token file, EN-IN + HI i18n, WCAG 2.1 AA.",
    "dr-desai": "Own Flutter for Android + iOS: Riverpod, go_router, offline-first, FCM push, and Play/App Store delivery.",
    "dr-bose": "Own the context graph and the deployed graph.sqlite. Compress every file read into a graph node.",
}

# Blocking agents (veto power per roster quality gate).
BLOCKING = {"kavach", "varuna", "mitra", "indra"}

# OpenRouter model id (from YAML) -> Claude Code model id for the adapter.
MODEL_MAP = {
    "openrouter/anthropic/opus-4-7": "claude-opus-4-8",
    "openrouter/anthropic/sonnet-4-6": "claude-sonnet-4-6",
    "openrouter/anthropic/haiku-4-5": "claude-haiku-4-5",
}

# Agents that touch GitHub and need a GH_TOKEN env input.
NEEDS_GH = {"dr-rao", "vayu", "prometheus", "shiva", "dr-iyer"}


def slug_of(emp_id: str) -> str:
    return emp_id.replace(".", "-")


def load_employees() -> dict:
    out = {}
    for p in sorted(SRC.glob("*.yaml")):
        data = yaml.safe_load(p.read_text())
        out[slug_of(data["id"])] = data
    return out


def quality_gate_block() -> str:
    return (
        "## Quality gate (every output)\n\n"
        "Every deliverable you produce must include:\n\n"
        "- `confidence_score: float` (>= 0.80 to be accepted)\n"
        "- `verification_step: str` (how you verified the result)\n"
        "- `summary: str` (one paragraph: what changed and why)\n"
        "- `flags: list[str]` (CRITICAL / HIGH / MEDIUM / LOW)\n\n"
        "The CEO rejects and re-dispatches any output that fails the gate.\n"
    )


def execution_contract() -> str:
    return (
        "## Execution contract\n\n"
        "- Start actionable work in the same heartbeat; do not stop at a plan unless planning was requested.\n"
        "- Leave durable progress in comments, documents, or work products, always with the next action.\n"
        "- Use child issues for long or parallel delegated work instead of polling agents or processes.\n"
        "- Mark blocked work with the unblock owner and the action needed.\n"
        "- Respect budget, pause/cancel, approval gates, and company boundaries.\n"
    )


def agent_md(slug: str, emp: dict) -> str:
    title, boss, division = ORG[slug]
    name = emp["display_name"].strip('"')
    tools = emp.get("allowed_tools", []) or []
    model_default = (emp.get("model_preference") or {}).get("default", "")
    fm = [
        "---",
        f"name: {name}",
        f"title: {title}",
        f"reportsTo: {boss if boss else 'null'}",
        "skills:",
        "  - paperclip",
        "---",
        "",
    ]
    body = [f"You are **{name}**, {title} in the {division} division of Vyasa Inc.", ""]
    body.append(CHARTER.get(slug, ""))
    body.append("")
    # Workflow context
    body.append("## How you fit the workflow\n")
    if boss is None:
        body.append("- **Work comes from:** the Board (the human operator) as company goals.")
        body.append("- **You produce:** decomposed objectives routed to directors, plus gated, synthesised final outputs.")
        body.append("- **You hand off to:** your directors (Product, Engineering, Security, Reliability, Risk, Legal, Growth, Delivery).")
        body.append("- **You are triggered by:** a new company goal, or any output returned for the quality gate.")
    else:
        body.append(f"- **Work comes from:** `{boss}`, as assigned issues/tasks.")
        body.append("- **You produce:** the work product for your role, satisfying the quality gate below.")
        body.append(f"- **You hand off to:** `{boss}` (report back) and downstream roles per the routing cheat-sheet in the README.")
        body.append("- **You are triggered by:** an issue assigned to you, a heartbeat, or a routine.")
    body.append("")
    # Tool scope
    body.append("## Tool scope (least privilege)\n")
    if tools:
        body.append("Stay within this scope (from the Vyasa capability matrix):\n")
        body.append("\n".join(f"- `{t}`" for t in tools))
    else:
        body.append("No direct tools — you dispatch and gate only.")
    body.append("")
    # Blocking authority
    if slug in BLOCKING:
        body.append("## Blocking authority\n")
        body.append(
            "You hold **veto power**. A single CRITICAL finding from you halts the batch and "
            "blocks the release until resolved or until the Board explicitly overrides the gate.\n"
        )
    body.append(quality_gate_block())
    body.append(execution_contract())
    return "\n".join(fm) + "\n".join(body) + "\n"


def company_md(emps: dict) -> str:
    fm = [
        "---",
        "name: Vyasa Inc.",
        "description: A 29-agent autonomous software & product company — the Vyasa Agent fleet expressed as a Paperclip company.",
        "slug: vyasa-inc",
        "schema: agentcompanies/v1",
        "version: 0.1.0",
        "license: Apache-2.0",
        "authors:",
        "  - name: darshjme",
        "goals:",
        "  - Turn product briefs into shipped, reviewed, secured software end to end.",
        "  - Enforce a hard quality gate (confidence_score >= 0.80) on every output.",
        "  - Honour four blocking authorities: Security, Risk, Legal, Reliability.",
        "tags:",
        "  - engineering",
        "  - product",
        "  - autonomous-company",
        "---",
        "",
        "**Vyasa Inc.** is the [Vyasa Agent](https://github.com/darshjme/vyasa-agent) "
        "29-partner fleet re-expressed as a [Paperclip](https://github.com/paperclipai/paperclip) "
        "company conforming to the [Agent Companies spec](https://agentcompanies.io/specification).",
        "",
        "**Vyasa** is the CEO. Eight directors run Product, Engineering, Security, Reliability, "
        "Risk, Legal, Growth, and Delivery. Specialists execute beneath them. Four directors "
        "(Security/`kavach`, Risk/`varuna`, Legal/`mitra`, Reliability/`indra`) hold blocking veto power.",
        "",
        "**Workflow** is hub-and-spoke with pipeline stages inside Engineering and Delivery: the "
        "CEO decomposes a goal to directors; directors dispatch to specialists; work flows "
        "plan -> build -> review -> secure -> ship; blocking gates clear before any release.",
        "",
        "**Budget:** unlimited for now (no caps); cost tracking stays on for visibility.",
        "",
        "Generated from [vyasa-agent](https://github.com/darshjme/vyasa-agent) with the "
        "company-creator conventions from [Paperclip](https://github.com/paperclipai/paperclip).",
    ]
    return "\n".join(fm) + "\n"


def paperclip_yaml(emps: dict) -> str:
    lines = ["schema: paperclip/v1", "agents:"]
    for slug in ORG:
        emp = emps[slug]
        model_default = (emp.get("model_preference") or {}).get("default", "")
        cc_model = MODEL_MAP.get(model_default, "claude-opus-4-8")
        lines.append(f"  {slug}:")
        lines.append("    adapter:")
        lines.append("      type: claude_local")
        lines.append("      config:")
        lines.append(f"        model: {cc_model}")
        if slug in NEEDS_GH:
            lines.append("    inputs:")
            lines.append("      env:")
            lines.append("        GH_TOKEN:")
            lines.append("          kind: secret")
            lines.append("          requirement: optional")
    return "\n".join(lines) + "\n"


# Scheduled routines (PROJECT-less starter tasks under tasks/).
TASKS = [
    ("slo-budget-check", "indra", "Check SLO budgets and error rates across all services. "
     "Block deploys if any budget is exhausted; open a child issue per breach.",
     {"timezone": "America/Chicago", "startsAt": "2026-06-23T09:00:00-05:00",
      "recurrence": {"frequency": "daily", "interval": 1, "time": {"hour": 9, "minute": 0}}}),
    ("weekly-cost-audit", "kubera", "Right-size compute, review storage lifecycle and cross-AZ "
     "egress, and audit SaaS licenses. Produce a cost-savings report with recommendations.",
     {"timezone": "America/Chicago", "startsAt": "2026-06-22T09:00:00-05:00",
      "recurrence": {"frequency": "weekly", "interval": 1, "weekdays": ["monday"],
                     "time": {"hour": 9, "minute": 0}}}),
    ("weekly-security-scan", "dr-reddy", "Run a full pen-test and dependency/secret scan. "
     "Escalate any CRITICAL finding to the CISO (kavach) as a blocking gate.",
     {"timezone": "America/Chicago", "startsAt": "2026-06-24T09:00:00-05:00",
      "recurrence": {"frequency": "weekly", "interval": 1, "weekdays": ["wednesday"],
                     "time": {"hour": 9, "minute": 0}}}),
    ("weekly-recon-sweep", "garuda", "Map directories, dependency graphs, and hot spots. "
     "Produce a read-only recon report and hand off gaps to the relevant lead.",
     {"timezone": "America/Chicago", "startsAt": "2026-06-22T08:00:00-05:00",
      "recurrence": {"frequency": "weekly", "interval": 1, "weekdays": ["monday"],
                     "time": {"hour": 8, "minute": 0}}}),
]


def task_md(slug: str, assignee: str, body: str, schedule: dict) -> str:
    fm = {"name": slug.replace("-", " ").title(), "assignee": assignee, "schedule": schedule}
    return "---\n" + yaml.safe_dump(fm, sort_keys=False).strip() + "\n---\n\n" + body + "\n"


def main() -> None:
    emps = load_employees()
    missing = set(ORG) - set(emps)
    extra = set(emps) - set(ORG)
    assert not missing, f"org map references unknown agents: {missing}"
    assert not extra, f"employees not placed in org map: {extra}"

    (ROOT / "COMPANY.md").write_text(company_md(emps))

    for slug, emp in emps.items():
        d = ROOT / "agents" / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "AGENTS.md").write_text(agent_md(slug, emp))

    for slug, assignee, body, schedule in TASKS:
        d = ROOT / "tasks" / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "TASK.md").write_text(task_md(slug, assignee, body, schedule))

    (ROOT / ".paperclip.yaml").write_text(paperclip_yaml(emps))

    print(f"Generated {len(emps)} agents, {len(TASKS)} tasks.")
    print("Wrote: COMPANY.md, agents/<slug>/AGENTS.md, tasks/<slug>/TASK.md, .paperclip.yaml")


if __name__ == "__main__":
    main()
