import json
from datetime import datetime

def emit_event(ip, score, verdict, techniques):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "risk_score": score,
        "verdict": verdict,
        "mitre_techniques": techniques
    }

    with open("logs/events.json", "a") as f:
        f.write(json.dumps(event) + "\n")

    return event
