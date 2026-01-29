
import subprocess
import json
import os
from datetime import datetime, timedelta

STATE_FILE = os.path.expanduser("../state/blocked_ips.json")
BLOCK_TTL = 3600  # 1 hour

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def block_ip(ip):
    state = load_state()
    now = datetime.utcnow().isoformat()
    if ip.startswith("127.") or ip in state:
        return False
    try:
        subprocess.run(
            ["sudo", "nft", "add", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"],
            check=True
        )
        state[ip] = now
        save_state(state)
        print(f"[BLOCKED] {ip}")
        return True
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to block IP: {ip}")
        return False

def expire_ips():   # <-- this must exist
    state = load_state()
    changed = False
    now = datetime.utcnow()
    to_delete = []
    for ip, ts in state.items():
        ts_dt = datetime.fromisoformat(ts)
        if (now - datetime.fromisoformat(ts)).total_seconds() > BLOCK_TTL:
            try:
                subprocess.run(
                    ["sudo", "nft", "delete", "rule", "inet", "filter", "input", "ip", "saddr", ip, "drop"],
                    check=True
                )
                to_delete.append(ip)
                changed = True
                print(f"[EXPIRED] {ip}")
            except subprocess.CalledProcessError:
                print(f"[ERROR] Failed to remove IP: {ip}")
    for ip in to_delete:
        del state[ip]
    if changed:
        save_state(state)
