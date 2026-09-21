import re

NOISE_PATTERNS = [
    r"no-reply@", r"notifications@", r"ship-confirm@", r"info@members\.",
    r"calendar-notification@", r"noreply@", r"receipts@", r"billing@",
    r"alerts@", r"support@namecheap", r"digest@", r"updates@", r"orders@"
]

def classify_rule_based(msg):
    sender = msg.get("from", "").lower()
    subject = msg.get("subject", "").lower()
    
    # Check for obvious noise/receipts/newsletters
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, sender):
            return "archive", "Automated notification/receipt matched noise rule."
            
    if "receipt" in subject or "statement" in subject or "weekly activity" in subject:
        return "archive", "Transaction/activity statement matched noise rule."
        
    return None, None
