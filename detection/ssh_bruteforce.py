import json, time
from collections import defaultdict

events="logs/events.json"
attempts=defaultdict(list)

MAX=5; WINDOW=60

for line in open(events):
    e=json.loads(line)
    ip=e["ip"]; now=e["time"]
    attempts[ip].append(now)
    attempts[ip]=[t for t in attempts[ip] if now-t<WINDOW]
    if len(attempts[ip])>=MAX:
        open("logs/detections.log","a").write(f"SSH_BRUTE_FORCE {ip}\n")
        attempts[ip]=[]
