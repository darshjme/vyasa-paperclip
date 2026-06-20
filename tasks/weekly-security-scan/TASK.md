---
name: Weekly Security Scan
assignee: dr-reddy
schedule:
  timezone: America/Chicago
  startsAt: '2026-06-24T09:00:00-05:00'
  recurrence:
    frequency: weekly
    interval: 1
    weekdays:
    - wednesday
    time:
      hour: 9
      minute: 0
---

Run a full pen-test and dependency/secret scan. Escalate any CRITICAL finding to the CISO (kavach) as a blocking gate.
