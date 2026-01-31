#!/usr/bin/env python3

from soar.threat_intel import score_ip
from correlation.output import emit_event

# Example activity weights (can later move to YAML)
WEIGHTS = {
    "RECON": 5,
    "ENUMERATION": 5,
    "BRUTE_FORCE": 15,
    "PERSISTENCE": 20,
    "MALWARE_DOWNLOAD": 25,
    "LATERAL_MOVEMENT": 30,
    "UNKNOWN": 10,
}


def calculate_risk(activity: dict) -> int:
    score = 0
    for tactic, count in activity.items():
        score += WEIGHTS.get(tactic, 5) * count
    return min(score, 100)


def correlate(ip: str, activity: dict):
    """
    Correlate attacker behavior and generate a security event
    """
    risk_score = calculate_risk(activity)

    reputation = score_ip(ip)
    risk_score = min(risk_score + reputation, 100)

    verdict = "BLOCKED" if risk_score >= 70 else "MONITOR"

    mitre_techniques = []
    if "BRUTE_FORCE" in activity:
        mitre_techniques.append("T1110")
    if "MALWARE_DOWNLOAD" in activity:
        mitre_techniques.append("T1105")
    if "LATERAL_MOVEMENT" in activity:
        mitre_techniques.append("T1021")

    event = emit_event(
        ip=ip,
        score=risk_score,
        verdict=verdict,
        techniques=mitre_techniques
    )

    print(f"[+] Event Generated → {event}")
    return event


if __name__ == "__main__":
    # 🔥 test run (safe to delete later)
    sample_activity = {
        "RECON": 4,
        "ENUMERATION": 3,
        "BRUTE_FORCE": 5,
        "PERSISTENCE": 2,
        "UNKNOWN": 1
    }

    correlate("10.0.2.15", sample_activity)
