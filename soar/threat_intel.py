# soar/threat_intel.py

import random

# Simulated threat feeds (Phase 2 = offline intelligence)
KNOWN_MALICIOUS_IPS = {
    "185.220.101.1": "TOR Exit Node",
    "91.121.222.45": "Known Brute Force Host",
}

SUSPICIOUS_ASNS = {
    "103.21.244.0": "Bulletproof Hosting"
}

def score_ip(ip: str) -> int:
    """
    Returns base threat score (0–5)
    """

    if ip in KNOWN_MALICIOUS_IPS:
        return 5

    for prefix in SUSPICIOUS_ASNS:
        if ip.startswith(prefix.split(".")[0]):
            return 3

    # Random low noise to simulate unknown activity
    return random.randint(0, 2)


def explain_ip(ip: str) -> dict:
    """
    Explain WHY an IP is risky
    """
    if ip in KNOWN_MALICIOUS_IPS:
        return {
            "confidence": "HIGH",
            "reason": KNOWN_MALICIOUS_IPS[ip]
        }

    for prefix, reason in SUSPICIOUS_ASNS.items():
        if ip.startswith(prefix.split(".")[0]):
            return {
                "confidence": "MEDIUM",
                "reason": reason
            }

    return {
        "confidence": "LOW",
        "reason": "Unknown / Opportunistic Activity"
    }
