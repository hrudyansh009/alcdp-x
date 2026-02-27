# collectors/cowrie_collector.py

import json
import time
from correlation.correlator import generate_event

COWRIE_LOG = "/home/kali/cowrie/var/log/cowrie/cowrie.json"

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line

def main():
    print("[+] Cowrie collector started")
    with open(COWRIE_LOG, "r") as f:
        for line in follow(f):
            try:
                entry = json.loads(line)
                ip = entry.get("src_ip")

                if not ip or ip.startswith("127."):
                    continue

                if entry.get("eventid") in [
                    "cowrie.login.failed",
                    "cowrie.login.success",
                    "cowrie.command.input",
                    "cowrie.session.file_download"
                ]:
                    generate_event(ip)

            except Exception:
                pass

if __name__ == "__main__":
    main()
