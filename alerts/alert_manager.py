# alerts/alert_manager.py

import json
from datetime import datetime

ALERT_LOG = "reports/alerts.log"

def send_alert(event: dict):
    """
    Print alert to terminal and save to alerts.log
    """
    print("\n🚨 ALERT GENERATED 🚨")
    print(f"""
Time     : {event['timestamp']}
SourceIP : {event['src_ip']}
Session  : {event['session']}
Command  : {event['command']}
Type     : {event['attack_type']}
Severity : {event['severity']}
MITRE    : {event['mitre']}
""")

    # Save to alerts log
    with open(ALERT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")
