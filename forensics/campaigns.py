from collections import defaultdict

CAMPAIGNS = defaultdict(list)

def assign_campaign(session):
    signature = tuple(sorted(session["techniques"]))

    CAMPAIGNS[signature].append({
        "ip": session["ip"],
        "events": session["event_count"],
        "max_risk": session["max_risk"],
        "severity": session["escalation"]
    })

def get_campaigns():
    return [
        {
            "techniques": list(sig),
            "members": members
        }
        for sig, members in CAMPAIGNS.items()
        if len(members) > 1  # real campaign, not noise
    ]
