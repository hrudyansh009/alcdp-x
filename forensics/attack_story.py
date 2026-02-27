def generate_attack_story(session):
    ip = session["ip"]
    severity = session["escalation"]
    techniques = session["techniques"]
    events = session["event_count"]
    risk = session["max_risk"]

    technique_list = ", ".join(techniques)

    if severity == "HIGH":
        assessment = "High-confidence malicious activity detected. Immediate containment recommended."
    elif severity == "ESCALATING":
        assessment = "Suspicious behavior increasing. Monitor closely."
    else:
        assessment = "Low-risk activity observed."

    story = {
        "ip": ip,
        "severity": severity,
        "events": events,
        "max_risk": risk,
        "techniques": list(techniques),
        "analysis": f"IP {ip} executed techniques: {technique_list}. "
                    f"Observed across {events} events with max risk score {risk}.",
        "assessment": assessment
    }

    return story
