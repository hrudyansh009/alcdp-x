BLOCKLIST = set()

def take_action(session):
    actions = []

    if session["escalation"] == "HIGH":
        ip = session["ip"]
        if ip not in BLOCKLIST:
            BLOCKLIST.add(ip)
            actions.append(f"BLOCK_IP → {ip}")

    return actions
