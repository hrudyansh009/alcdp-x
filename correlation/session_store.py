# correlation/session_store.py
from datetime import datetime, timedelta

SESSIONS = {}
WINDOW = timedelta(minutes=5)

def _parse_ts(ts: str) -> datetime:
    # accept "2026-02-02T11:27:12.499263" or with "Z" or with offset
    if ts.endswith("Z"):
        ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)

def add_event_to_session(event: dict):
    ip = event.get("ip")
    if not ip:
        return None

    now = _parse_ts(event["timestamp"])

    session = SESSIONS.get(ip)
    if not session:
        SESSIONS[ip] = {
            "ip": ip,
            "first_seen": now,
            "last_seen": now,
            "event_count": 1,
            "max_risk": event.get("risk_score", 0),
            "techniques": set(event.get("mitre_techniques", [])),
            "escalation": "LOW",
            "verdict": "MONITOR"
        }
        return SESSIONS[ip]

    # if the last event is outside the window, reset session
    if now - session["last_seen"] > WINDOW:
        SESSIONS[ip] = {
            "ip": ip,
            "first_seen": now,
            "last_seen": now,
            "event_count": 1,
            "max_risk": event.get("risk_score", 0),
            "techniques": set(event.get("mitre_techniques", [])),
            "escalation": "LOW",
            "verdict": "MONITOR"
        }
        return SESSIONS[ip]

    # update existing session
    session["last_seen"] = now
    session["event_count"] += 1
    session["max_risk"] = max(session["max_risk"], event.get("risk_score", 0))
    session["techniques"].update(event.get("mitre_techniques", []))
    return session

def get_sessions():
    # return sessions as list with techniques as list and iso timestamps
    out = []
    for s in SESSIONS.values():
        out.append({
            "ip": s["ip"],
            "first_seen": s["first_seen"].isoformat(),
            "last_seen": s["last_seen"].isoformat(),
            "event_count": s["event_count"],
            "max_risk": s["max_risk"],
            "techniques": list(s["techniques"]),
            "escalation": s["escalation"],
            "verdict": s["verdict"]
        })
    return out
