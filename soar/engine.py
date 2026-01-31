import yaml
import subprocess
from soar.threat_intel import reputation
from soar.severity import score

PLAYBOOKS = yaml.safe_load(open("config/playbooks.yaml"))
INCIDENTS = "logs/incidents.log"

def execute(action, ip=None):
    if action == "block_ip":
        subprocess.call(["bash", "bin/block_ip.sh", ip])

    elif action == "isolate_host":
        subprocess.call(["bash", "bin/isolate_host.sh"])

    elif action == "collect_evidence":
        subprocess.call(["bash", "forensics/collect.sh"])

    elif action == "send_alert":
        print(f"[ALERT] Incident involving {ip}")

for line in open(INCIDENTS):
    parts = line.split()
    incident_type = parts[0]
    ip = parts[1]

    rep_score = reputation(ip)
    severity = score(bruteforce=True, reputation=rep_score)

    actions = PLAYBOOKS[incident_type][severity]["actions"]

    for action in actions:
        execute(action, ip)

