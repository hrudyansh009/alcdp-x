from datetime import datetime, timezone

INCIDENTS = []

def map_severity(max_risk: int) -> str:
    if max_risk >= 80:
        return "CRITICAL"
    if max_risk >= 60:
        return "HIGH"
    if max_risk >= 40:
        return "MEDIUM"
    return "LOW"

def create_incident(session: dict) -> dict:
    # avoid duplicates for same IP while OPEN
    for inc in INCIDENTS:
        if inc["ip"] == session["ip"] and inc["status"] == "OPEN":
            return inc

    incident = {
        "id": f"INC-{len(INCIDENTS)+1:05d}",
        "ip": session["ip"],
        "severity": map_severity(session["max_risk"]),
        "event_count": session["event_count"],
        "max_risk": session["max_risk"],
        "techniques": sorted(list(session["techniques"])),
        "status": "OPEN",
        "first_seen": session["first_seen"].isoformat(),
        "last_seen": session["last_seen"].isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    INCIDENTS.append(incident)
    print(f"[INCIDENT] {incident['id']} | {incident['ip']} | {incident['severity']}")
    return incident
