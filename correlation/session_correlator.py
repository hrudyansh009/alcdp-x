# correlation/session_correlator.py
from correlation.session_store import add_event_to_session

def evaluate_session(session: dict):
    # escalation rules (simple, transparent)
    # default escalation stays LOW; rules can upgrade it
    if session is None:
        return None

    # rule: 3+ events -> ESCALATING
    if session["event_count"] >= 3:
        session["escalation"] = "ESCALATING"

    # rule: max_risk >= 70 -> HIGH
    if session["max_risk"] >= 70:
        session["escalation"] = "HIGH"

    # rule: multiple techniques -> ADVERSARY
    if len(session["techniques"]) >= 2:
        session["escalation"] = "ADVERSARY"

    # decision: if HIGH + ADVERSARY -> BLOCK
    if session["escalation"] == "HIGH" and len(session["techniques"]) >= 2:
        session["verdict"] = "BLOCK"

    # you can add more rules here later
    return session

def correlate_event(event: dict):
    session = add_event_to_session(event)
    session = evaluate_session(session)
    return session
