# response/auto_block.py

import datetime

BLOCK_LOG = "logs/blocked_ips.log"

def block_ip(ip, score):
    timestamp = datetime.datetime.utcnow().isoformat()

    entry = f"[{timestamp}] BLOCKED {ip} | Risk={score}\n"

    with open(BLOCK_LOG, "a") as f:
        f.write(entry)

    return entry
