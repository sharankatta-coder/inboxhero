import os
import json

def record_trace(event_type, cap, data):
    with open("trace.jsonl", "a") as f:
        log_entry = {"event": event_type, "cap": cap, "data": data}
        f.write(json.dumps(log_entry) + "\n")

def gate_action(action_type, details, dry_run=False, cap="R3"):
    """
    Gates irreversible actions (send, delete).
    """
    if action_type in ["send", "delete"]:
        if dry_run:
            print(f"[DRY-RUN GATED] Would perform {action_type}: {details}")
            record_trace("gate", cap, {"proposed": action_type, "details": details, "status": "dry_run"})
            return False
        else:
            print(f"\n⚠️ APPROVAL REQUIRED for irreversible action [{action_type.upper()}]:")
            print(f"Details: {details}")
            ans = input("Approve action? (y/N): ").strip().lower()
            if ans == "y":
                record_trace("gate", cap, {"proposed": action_type, "details": details, "status": "approved"})
                return True
            else:
                record_trace("gate", cap, {"proposed": action_type, "details": details, "status": "rejected"})
                return False
    return True
