🛡 ALCDP-X

Autonomous Linux Cyber Defense Platform – Experimental SOC Engine

🚀 Current Phase: 7

Live SOC dashboard with session correlation, incident generation, and simulated campaign engine.

🔥 Overview

ALCDP-X is a modular cybersecurity platform designed to simulate and analyze attacker behavior in a Linux environment.

It includes:

Real-time event ingestion

Session-based correlation

Automated incident generation

SOAR-style response simulation

Live SOC dashboard (Chart.js + Flask)

This is not a static dashboard.
It models attacker behavior progression over time.

🧠 Architecture
Correlation Engine
        ↓
Event Store (In-Memory)
        ↓
Session Correlation Logic
        ↓
Incident Generation
        ↓
Flask API
        ↓
Live Dashboard (Auto-refresh)

Single-process architecture ensures shared memory between engine and dashboard.

📂 Project Structure
ALCDP_X/
│
├── dashboard/
│   ├── app.py
│   ├── services/event_store.py
│   ├── static/
│   └── templates/
│
├── correlation/
│   └── correlator.py
│
├── collectors/
│   └── cowrie_tail.py (planned ingestion)
│
├── geoip/
│
└── detection/
⚙️ Features Implemented (Phase 7)
1️⃣ Event Generation

Simulated attacker campaigns

Command-based scoring logic

MITRE technique tagging

2️⃣ Session Correlation

Tracks per-IP:

First seen

Last seen

Event count

Max risk

Technique set

Escalation states:

LOW

ESCALATING

HIGH

3️⃣ Incident Engine

Automatic incident creation when:

Event count ≥ threshold

Risk ≥ threshold

Unique incident IDs (INC-00001)

Prevents duplicate OPEN incidents

4️⃣ Live Dashboard

Top Attackers Chart

Risk Timeline Chart

Sessions Table

Incidents Table

Auto-refresh every 2 seconds

🖥 How To Run
1. Activate Environment
cd ALCDP_X
source venv/bin/activate
2. Start Dashboard (includes background engine)
python -m dashboard.app

Open browser:

http://127.0.0.1:5000
🛠 Tech Stack

Python 3.11+

Flask

Chart.js

GeoIP (optional)

Modular correlation engine

🧩 MITRE ATT&CK Techniques Modeled
Technique	Description
T1082	System Information Discovery
T1083	File Discovery
T1003	Credential Access
T1105	Ingress Tool Transfer
T1053	Scheduled Task
T1021	Remote Services
🎯 Next Roadmap (Phase 8)

SQLite persistence layer

Real Cowrie log ingestion

Campaign classification engine

MITRE heatmap visualization

SOAR real system response hooks

⚠ Disclaimer

This project is for educational and defensive research purposes only.

👤 Author

Hrudyansh
Cybersecurity & AI Systems Research
