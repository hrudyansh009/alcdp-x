from datetime import datetime, timezone
from alerts.incidents import create_incident, INCIDENTS

EVENTS: list[dict] = []
SESSIONS: dict[str, dict] = {}

def add_event(event: dict) -> None:
    EVENTS.append(event)
    _update_session(event)

def get_events() -> list[dict]:
    return EVENTS[-200:]  # keep API light

def get_sessions() -> dict:
    # JSON safe copy (convert set + datetime)
    out = {}
    for ip, s in SESSIONS.items():
        out[ip] = {
            **s,
            "first_seen": s["first_seen"].isoformat(),
            "last_seen": s["last_seen"].isoformat(),
            "techniques": sorted(list(s["techniques"])),
        }
    return out

def get_incidents() -> list[dict]:
    return INCIDENTS

def _update_session(event: dict) -> None:
    ip = event["ip"]
    now = datetime.now(timezone.utc)
    risk = int(event["risk_score"])
    techniques = set(event.get("mitre_techniques", []))

    if ip not in SESSIONS:
        SESSIONS[ip] = {
            "ip": ip,
            "first_seen": now,
            "last_seen": now,
            "event_count": 0,
            "max_risk": 0,
            "techniques": set(),
            "escalation": "LOW",
            "verdict": "MONITOR",
        }

    s = SESSIONS[ip]
    s["last_seen"] = now
    s["event_count"] += 1
    s["max_risk"] = max(s["max_risk"], risk)
    s["techniques"].update(techniques)
    s["verdict"] = event["verdict"]

    # escalation logic
    if s["event_count"] >= 5 or s["max_risk"] >= 60:
        s["escalation"] = "HIGH"
        s["verdict"] = "BLOCKED"
        create_incident(s)
    elif s["event_count"] >= 3:
        s["escalation"] = "ESCALATING"
