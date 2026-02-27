# dashboard/services/event_store.py
from __future__ import annotations

from datetime import datetime
from typing import Dict, Any, List

EVENTS: List[Dict[str, Any]] = []
SESSIONS: Dict[str, Dict[str, Any]] = {}
INCIDENTS: List[Dict[str, Any]] = []


def add_event(event: Dict[str, Any]) -> None:
    """Store event + update session + raise incident if threshold hit."""
    EVENTS.append(event)
    _update_session(event)
    print("[EVENT_STORE] Event saved")


def get_events(limit: int = 200) -> List[Dict[str, Any]]:
    return EVENTS[-limit:]


def get_sessions() -> Dict[str, Dict[str, Any]]:
    return SESSIONS


def get_incidents() -> List[Dict[str, Any]]:
    return INCIDENTS


def _update_session(event: Dict[str, Any]) -> None:
    ip = event.get("ip")
    if not ip:
        return

    now = datetime.fromisoformat(event["timestamp"])
    risk = int(event.get("risk_score", 0))
    verdict = event.get("verdict", "MONITOR")
    techniques = set(event.get("mitre_techniques", []))

    if ip not in SESSIONS:
        SESSIONS[ip] = {
            "ip": ip,
            "first_seen": now.isoformat(),
            "last_seen": now.isoformat(),
            "event_count": 1,
            "max_risk": risk,
            "techniques": sorted(list(techniques)),
            "escalation": "LOW",
            "verdict": verdict,
        }
        return

    s = SESSIONS[ip]
    s["last_seen"] = now.isoformat()
    s["event_count"] += 1
    s["max_risk"] = max(int(s.get("max_risk", 0)), risk)

    old = set(s.get("techniques", []))
    s["techniques"] = sorted(list(old.union(techniques)))

    # Escalation rules (simple, but real enough)
    if s["event_count"] >= 5 and s["max_risk"] >= 60:
        s["escalation"] = "HIGH"
        s["verdict"] = "BLOCKED"
        _create_incident(s)
    elif s["event_count"] >= 3:
        s["escalation"] = "ESCALATING"
        s["verdict"] = verdict
    else:
        s["escalation"] = "LOW"
        s["verdict"] = verdict


def _create_incident(session: Dict[str, Any]) -> Dict[str, Any]:
    """No circular imports. Incident lives here."""
    # prevent duplicates
    for inc in INCIDENTS:
        if inc["ip"] == session["ip"] and inc["status"] == "OPEN":
            return inc

    incident = {
        "id": f"INC-{len(INCIDENTS)+1:05d}",
        "ip": session["ip"],
        "severity": session["escalation"],
        "campaign": "AUTO",
        "techniques": session.get("techniques", []),
        "events": session["event_count"],
        "risk": session["max_risk"],
        "status": "OPEN",
        "first_seen": session["first_seen"],
        "last_seen": session["last_seen"],
    }
    INCIDENTS.append(incident)
    print(f"[INCIDENT] {incident['id']} | {incident['ip']}")
    return incident
