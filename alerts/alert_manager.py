import datetime
import os

ALERT_LOG = os.path.expanduser("../reports/alerts.log")

def send_alert(event):
    os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)

    message = f"""
[ALERT] {event['severity']} ATTACK DETECTED
Time     : {event['timestamp']}
SourceIP : {event['src_ip']}
Command  : {event['command']}
MITRE    : {event['mitre']}
----------------------------------
"""
    with open(ALERT_LOG, "a") as f:
        f.write(message)

    print("[ALERT SENT]")
