# CAPABILITIES.md — inboxHero

**Student:** Ada Example, 2026XXXXXX
**Repository:** https://github.com/ada-example/inboxhero

Run everything through one entry point:

```bash
python demo.py --cap R1        # one capability
python demo.py --all           # all of them, in the order below
```

---

## The system, in one paragraph

A clean Python pipeline with deterministic rule filtering and architectural safety gates. Messages are loaded from `inbox.json`. Receipts, newsletters, and automated system alerts are dispatched via rules before hitting any model calls. High-risk messages (prompt injections, phishing wire requests) are detected, flagged, and prevented from executing outbox actions. Reversible operations run directly, while irreversible actions (`send`, `delete`) are routed through approval/dry-run gates.

## Design choices

- **Framework: none.** Built with raw Python for low latency, transparent auditability, and precise control over execution gates.
- **Retrieval: thread-walk.** Uses `thread_id` walking to retrieve context chronologically across email threads.
- **Reversible vs Irreversible.** `send` and `delete` are irreversible and gated via `gate.py`. `draft`, `label`, `archive`, and `defer` are reversible.
- **Escalation line.** Automatic approval for standard internal archives and defers. Escalation required for external sends, legal signatures, and monetary transfers.

## Capabilities

| id | name | tier | one-line claim |
|----|------|------|----------------|
| R1 | Zero the inbox | B | every message gets one disposition + reason, none left |
| R2 | Grounded reply | B | drafts cite the earlier message they used |
| R3 | Gate the irreversible | C | no send/delete without approval or --dry-run |
| R4 | Persistent preference | C | a stated preference survives a restart |
| R5 | Refuse embedded instructions | C | detects, refuses, flags, reports injections |
| R6 | Dashboard | C | three panes, commitments cited, conflicts surfaced |
| X1 | Follow-up tracking | B | unanswered sent mail, with a drafted chase |
| X2 | Morning digest | B | what needs me / what can wait / what was archived |
