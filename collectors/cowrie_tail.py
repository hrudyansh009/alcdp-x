import json
import time
from datetime import datetime, timezone

from dashboard.services.event_store import add_event
from correlation.correlator import score_from_command, technique_from_command
from geoip.lookup import lookup_ip

COWRIE_JSON = "/home/kali/cowrie/var/log/cowrie/cowrie.json"  # CHANGE THIS


def follow(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line


def to_event(obj):
    """
    Convert Cowrie log line -> our event schema
    We care mostly about: src_ip + input (command) + timestamp
    """
    src_ip = obj.get("src_ip") or obj.get("src_ip", None)
    cmd = obj.get("input") or obj.get("message") or ""

    if not src_ip:
        return None

    tech = technique_from_command(cmd)
    risk = score_from_command(cmd)

    verdict = "BLOCKED" if risk >= 60 else "MONITOR"

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip": src_ip,
        "risk_score": risk,
        "verdict": verdict,
        "mitre_techniques": [tech] if tech else [],
        "geo": lookup_ip(src_ip),
        "raw": {"cowrie_eventid": obj.get("eventid"), "cmd": cmd},
    }


def main():
    print("[*] Cowrie tail collector running...")
    print(f"[*] Watching: {COWRIE_JSON}")

    for line in follow(COWRIE_JSON):
        try:
            obj = json.loads(line.strip())
        except Exception:
            continue

        # We only want command input events
        if obj.get("eventid") not in ("cowrie.command.input", "cowrie.login.success", "cowrie.login.failed"):
            continue

        event = to_event(obj)
        if not event:
            continue

        add_event(event)
        print(f"[COWRIE] {event['ip']} | {event['risk_score']} | {event['raw'].get('cmd','')}")


if __name__ == "__main__":
    main()
