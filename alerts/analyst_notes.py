ANALYST_DECISIONS = {}

def add_decision(ip, decision, note):
    ANALYST_DECISIONS[ip] = {
        "decision": decision,  # TRUE_POSITIVE / FALSE_POSITIVE / MONITOR
        "note": note
    }

def get_decisions():
    return ANALYST_DECISIONS
