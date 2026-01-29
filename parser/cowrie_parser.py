import json
from datetime import datetime, timezone
from collections import defaultdict

from detections.rules import classify_command

COWRIE_LOG = "logs/cowrie.json"
ALERT_LOG = "reports/alerts.log"

# Track session activity
session_activity = defaultdict(list)

# Attack chain definition
ATTACK_CHAIN = [
    "RECON",
    "MALWARE_DOWNLOAD"
]


def send_alert(alert):
    with open(ALERT_LOG, "a") as f:
        f.write(json.dumps(alert) + "\n")
    print("[SESSION ALERT SENT]")


def check_attack_chain(session_id):
    activities = session_activity[session_id]

    for step in ATTACK_CHAIN:
        if step not in activities:
            return False
    return True


def parse_cowrie():
    with open(COWRIE_LOG, "r") as f:
        for line in f:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("eventid") != "cowrie.command.input":
                continue

            session = event.get("session")
            src_ip = event.get("src_ip")
            command = event.get("input", "").strip()

            attack_type, severity, mitre = classify_command(command)

            session_activity[session].append(attack_type)

            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "src_ip": src_ip,
                "session": session,
                "command": command,
                "attack_type": attack_type,
                "severity": severity,
                "mitre": mitre
            }

            print(log_entry)

            # SESSION-LEVEL ESCALATION
            if check_attack_chain(session):
                alert = {
                    "alert_time": datetime.now(timezone.utc).isoformat(),
                    "src_ip": src_ip,
                    "session": session,
                    "alert_type": "ATTACK_CHAIN_DETECTED",
                    "severity": "CRITICAL",
                    "mitre_chain": ["T1082", "T1105"],
                    "description": "Recon followed by malware download"
                }
                send_alert(alert)
                session_activity[session].clear()  # prevent alert spam


if __name__ == "__main__":
    parse_cowrie()
