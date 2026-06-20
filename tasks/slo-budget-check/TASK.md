---
name: Slo Budget Check
assignee: indra
schedule:
  timezone: America/Chicago
  startsAt: '2026-06-23T09:00:00-05:00'
  recurrence:
    frequency: daily
    interval: 1
    time:
      hour: 9
      minute: 0
---

Check SLO budgets and error rates across all services. Block deploys if any budget is exhausted; open a child issue per breach.
