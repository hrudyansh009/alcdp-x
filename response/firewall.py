# response/firewall.py

import json
import subprocess
from datetime import datetime, timezone

STATE_FILE = "state/blocked_ips.json"

def load_blocked_ips():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_blocked_ips(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def block_ip(ip: str):
    blocked = load_blocked_ips()

    if ip in blocked:
        return  # already blocked

    # nftables rule
    cmd = [
        "sudo", "nft", "add", "rule",
        "inet", "filter", "input",
        "ip", "saddr", ip, "drop"
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    blocked[ip] = {
        "blocked_at": datetime.now(timezone.utc).isoformat()
    }

    save_blocked_ips(blocked)

    print(f"🔥 IP BLOCKED: {ip}")
