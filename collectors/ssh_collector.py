import time, json, re

LOG="/var/log/auth.log"
OUT="logs/events.json"
regex=re.compile(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)")

with open(LOG) as f:
    f.seek(0,2)
    while True:
        line=f.readline()
        if not line:
            time.sleep(0.5); continue
        m=regex.search(line)
        if m:
            event={
              "type":"failed_login",
              "ip":m.group(1),
              "time":time.time()
            }
            open(OUT,"a").write(json.dumps(event)+"\n")
