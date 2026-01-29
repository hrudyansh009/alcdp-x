# parser/cowrie_parser.py

import json
from datetime import datetime, timezone

from detections.rules import classify_command
from alerts.alert_manager import send_alert
from response.firewall import block_ip

COWRIE_LOG = "logs/cowrie.json"

def parse_cowrie_logs():
    try:
        with open(COWRIE_LOG, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Cowrie command field
                command = data.get("input") or data.get("command")
                if not command:
                    continue

                classification = classify_command(command)

                # Defensive defaults (important)
                attack_type = classification.get("attack_type", "UNKNOWN")
                severity = classification.get("severity", "INFO")
                mitre = classification.get("mitre", "N/A")

                event = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "src_ip": data.get("src_ip", "N/A"),
                    "session": data.get("session", "N/A"),
                    "command": command,
                    "attack_type": attack_type,
                    "severity": severity,
                    "mitre": mitre
                }

                # Always print parsed event
                print(event)

                # Alert only on meaningful threats
                if severity in ["HIGH", "CRITICAL"]:
                    send_alert(event)
                    block_ip(event["src_ip"])

    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {COWRIE_LOG}")

if __name__ == "__main__":
    parse_cowrie_logs()

