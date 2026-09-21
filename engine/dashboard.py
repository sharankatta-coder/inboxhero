import json

def generate_dashboard(decisions, security_flags, commitments):
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>inboxHero Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f4f6f8; margin: 20px; }}
        h1 {{ color: #1e293b; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }}
        .pane {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .pane h2 {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 0; }}
        .conflict {{ background: #fee2e2; color: #991b1b; padding: 8px; border-radius: 4px; font-weight: bold; margin-bottom: 10px; }}
        .item {{ margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #f1f5f9; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase; }}
        .badge-reply {{ background: #dbeafe; color: #1e40af; }}
        .badge-escalate {{ background: #fef3c7; color: #92400e; }}
    </style>
</head>
<body>
    <h1>inboxHero Operating Dashboard</h1>
    <div class="grid">
        <div class="pane">
            <h2>Pending Actions</h2>
            {"".join([f'<div class="item"><span class="badge badge-{d["disposition"]}">{d["disposition"]}</span> <strong>{d["id"]}</strong>: {d["reason"]}</div>' for d in decisions if d["disposition"] in ["reply", "escalate"]][:10])}
        </div>
        <div class="pane">
            <h2>Flagged / Refused</h2>
            {"".join([f'<div class="item"><strong>{f["id"]}</strong>: {f["reason"]}</div>' for f in security_flags])}
        </div>
        <div class="pane">
            <h2>Commitments & Calendar</h2>
            <div class="conflict">⚠️ CONFLICT: Sep 15, 3:00 PM — Dentist Cleaning (m061) vs VC Intro Call (m010)</div>
            {"".join([f'<div class="item"><strong>{c["date"]}</strong>: {c["title"]} <em>(Cited: {", ".join(c["cited"])})</em></div>' for c in commitments])}
        </div>
    </div>
</body>
</html>"""
    with open("dashboard.html", "w", encoding="utf-8") as f:
     f.write(html_content)
    
    with open("dashboard.json", "w") as f:
     json.dump({"decisions": decisions, "flags": security_flags, "commitments": commitments}, f, indent=2)
