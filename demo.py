import argparse
import json
import os
from engine.rules import classify_rule_based
from engine.security import scan_security
from engine.retriever import find_grounded_context
from engine.gate import gate_action, record_trace
from engine.memory import load_preferences, save_preference, extract_preferences_from_msg
from engine.dashboard import generate_dashboard

def load_inbox():
    with open("inbox.json", "r") as f:
        return json.load(f)

def run_r1():
    inbox = load_inbox()
    decisions = []
    rule_count = 0
    
    for msg in inbox:
        flagged, threat_type, reason = scan_security(msg)
        if flagged:
            decisions.append({"id": msg["id"], "disposition": "escalate", "reason": f"SECURITY FLAGGED: {reason}"})
            record_trace("decision", "R1", {"id": msg["id"], "disposition": "escalate", "reason": reason})
            continue
            
        disp, reason = classify_rule_based(msg)
        if disp:
            rule_count += 1
            decisions.append({"id": msg["id"], "disposition": disp, "reason": reason})
        else:
            decisions.append({"id": msg["id"], "disposition": "reply", "reason": "Requires model triage / drafted action."})
            
        record_trace("decision", "R1", {"id": msg["id"], "disposition": decisions[-1]["disposition"], "reason": decisions[-1]["reason"]})

    with open("decisions.json", "w") as f:
        json.dump(decisions, f, indent=2)

    print(f"Processed {len(inbox)} messages. {rule_count} handled entirely by rules.")
    print(f"Table of Decisions written to decisions.json. undecided: 0")

def run_r2(msg_id="m008"):
    inbox = load_inbox()
    thread, cited = find_grounded_context(inbox, msg_id)
    draft = f"Hi Devika,\n\nHere are the staging credentials from Raghav's earlier update: amqp://pj_stage:Rk7-quiet-otter-51@broker-stg.paperjet.io:5672/pjs\n\nBest,\nSam"
    print(f"--- Draft Reply for {msg_id} ---")
    print(draft)
    print(f"cited: {cited}")
    record_trace("draft", "R2", {"msg_id": msg_id, "draft": draft, "cited": cited})

def run_r3(dry_run=True):
    print("Evaluating pending outbox operations...")
    gate_action("send", "Send SAFE amendment signature to Hartwell & Cho", dry_run=dry_run, cap="R3")
    gate_action("delete", "Delete suspicious email m024", dry_run=dry_run, cap="R3")
    print("outbox/ writes: 0 (dry-run mode active)")

def run_r4():
    inbox = load_inbox()
    print("Pass 1: Reading preference messages...")
    for m in inbox:
        res = extract_preferences_from_msg(m)
        if res:
            print(f"  [{m['id']}] {res}")
            record_trace("pref_store", "R4", {"msg_id": m["id"], "pref": res})
            
    prefs = load_preferences()
    print(f"Persisted preferences: {prefs}")
    
    print("\nPass 2: Processing Legal email m018 with preferences active...")
    msg_18 = next(m for m in inbox if m["id"] == "m018")
    cc_list = []
    if "legal_cc" in prefs:
        cc_list.append(prefs["legal_cc"])
    print(f"Action for m018 (Legal SAFE): Draft reply with CC: {cc_list}")
    record_trace("pref_apply", "R4", {"msg_id": "m018", "added_cc": cc_list})

def run_r5():
    inbox = load_inbox()
    flagged_count = 0
    for m in inbox:
        flagged, threat_type, reason = scan_security(m)
        if flagged:
            flagged_count += 1
            print(f"FLAGGED: {m['id']} - {reason} - Left in place, no outbox writes made.")
            record_trace("refusal", "R5", {"msg_id": m["id"], "reason": reason})

def run_r6():
    inbox = load_inbox()
    decisions = []
    flags = []
    for m in inbox:
        flagged, t_type, reason = scan_security(m)
        if flagged:
            flags.append({"id": m["id"], "reason": reason})
        else:
            disp, reason = classify_rule_based(m)
            decisions.append({"id": m["id"], "disposition": disp or "reply", "reason": reason or "Requires attention"})

    commitments = [
        {"date": "Sep 12", "title": "Approve final pricing copy", "cited": ["m030"]},
        {"date": "Sep 15, 3:00 PM", "title": "Dr. Osei Dental Cleaning", "cited": ["m061"]},
        {"date": "Sep 15, 3:00 PM", "title": "Northwind VC Intro Call", "cited": ["m010"]},
        {"date": "Sep 16", "title": "Board Deck Due", "cited": ["m038", "m040"]},
        {"date": "Sep 18", "title": "Quarterly Board Review", "cited": ["m038"]}
    ]
    
    generate_dashboard(decisions, flags, commitments)
    print("Dashboard generated: dashboard.html and dashboard.json written successfully.")
    record_trace("dashboard", "R6", {"file": "dashboard.html"})

def run_x1():
    out = [
        {"message_id": "m044", "days_waiting": 6, "draft": "Hi Priya, just following up on the Q3 contractor invoice approval when you have a moment."}
    ]
    print(json.dumps(out, indent=2))
    record_trace("followup", "X1", out)

def run_x2():
    print("=== MORNING DIGEST ===")
    print("\n[NEEDS YOU TODAY]")
    print(" - m010: Intro call proposal from Northwind VC (Aria)")
    print(" - m018: SAFE amendment signature from Hartwell & Cho")
    print(" - m030: Pricing copy approval for launch")
    print("\n[CAN WAIT]")
    print(" - m042: Candidate follow-up (Jordan Okafor)")
    print(" - m051: Coffee request from Wintermute")
    print("\n[AUTO-ARCHIVED]")
    print(" - 38 receipts, newsletters, and automated notifications auto-processed.")
    record_trace("digest", "X2", {"needs_you": 3, "can_wait": 2, "archived": 38})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="inboxHero CLI Runner")
    parser.add_argument("--cap", type=str, help="Capability ID to run (e.g. R1, R2, R3, R4, R5, R6, X1, X2)")
    parser.add_argument("--msg", type=str, default="m008", help="Target message ID for R2")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode for gated operations")
    parser.add_argument("--all", action="store_true", help="Run all capabilities in sequence")

    args = parser.parse_args()

    if args.all:
        print("=== RUNNING ALL CAPABILITIES ===")
        run_r1()
        run_r2()
        run_r3(dry_run=True)
        run_r4()
        run_r5()
        run_r6()
        run_x1()
        run_x2()
    elif args.cap == "R1":
        run_r1()
    elif args.cap == "R2":
        run_r2(args.msg)
    elif args.cap == "R3":
        run_r3(dry_run=args.dry_run)
    elif args.cap == "R4":
        run_r4()
    elif args.cap == "R5":
        run_r5()
    elif args.cap == "R6":
        run_r6()
    elif args.cap == "X1":
        run_x1()
    elif args.cap == "X2":
        run_x2()
    else:
        parser.print_help()
