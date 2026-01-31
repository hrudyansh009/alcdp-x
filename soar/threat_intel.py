# soar/threat_intel.py

import requests

ABUSEIPDB_API_KEY = None  # keep None for now (offline mode)

def score_ip(ip: str) -> int:
    """
    Returns a threat score for an IP.
    Offline-safe (no API required).
    """

    # Basic heuristic scoring (extend later)
    score = 0

    if ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("127."):
        return 0  # internal / localhost

    # Placeholder threat logic
    score += 5

    return score
