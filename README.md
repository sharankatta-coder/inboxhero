# inboxHero — Autonomous Inbox Hero

## Overview
inboxHero is an agentic email management system designed to process messy inboxes down to zero while enforcing strict safety gates and contextual awareness.

## Setup & Running
1. Extract project files.
2. Ensure Python 3.9+ is installed.
3. Run capabilities via CLI:

```bash
python demo.py --cap R1
python demo.py --cap R2 --msg m008
python demo.py --cap R3 --dry-run
python demo.py --cap R4
python demo.py --cap R5
python demo.py --cap R6
python demo.py --cap X1
python demo.py --cap X2
python demo.py --all
```

## Architectural Highlights
- **Deterministic Pre-filtering:** Standard newsletters, transactional receipts, and alerts bypass expensive LLM calls.
- **Safety Gate:** Irreversible actions (`send`, `delete`) require explicit human confirmation or dry-run execution.
- **Security Isolation:** Hostile prompt injections are flagged in a pre-execution pass and prevented from triggering outbox writes.
