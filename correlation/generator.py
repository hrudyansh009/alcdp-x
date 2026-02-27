import time
import random
from datetime import datetime, timezone
from dashboard.services.store import add_event

def score_ip(ip: str) -> int:
    # placeholder (1..5)
    return random.randint(1, 5)

def generate_event(ip: str, technique: list[str]) -> dict:
    score = score_ip(ip)
    risk = score * 20
    verdict = "BLOCKED" if risk >= 60 else "MONITOR"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip": ip,
        "risk_score": risk,
        "verdict": verdict,
        "mitre_techniques": technique,
        "geo": {"country": "Unknown", "city": None, "lat": None, "lon": None},
    }

def run_forever(interval_sec: int = 3) -> None:
    print("[*] Generator running…")
    ips = ["8.8.8.8", "1.1.1.1", "185.220.101.1", "103.21.244.7"]
    techs = [["T1046"], ["T1110"], ["T1059"], ["T1078"]]

    while True:
        for i, ip in enumerate(ips):
            ev = generate_event(ip, techs[i])
            add_event(ev)
            print(f"[EVENT] {ev['timestamp']} | {ev['ip']} | {ev['verdict']} | {ev['risk_score']}")
        time.sleep(interval_sec)
