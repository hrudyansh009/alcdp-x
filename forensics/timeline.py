from datetime import datetime

TIMELINES = {}

def add_to_timeline(event):
    ip = event["ip"]

    entry = {
        "time": event["timestamp"],
        "techniques": event["mitre_techniques"],
        "risk": event["risk_score"],
        "verdict": event["verdict"]
    }

    if ip not in TIMELINES:
        TIMELINES[ip] = []

    TIMELINES[ip].append(entry)

def get_timeline(ip):
    return TIMELINES.get(ip, [])
