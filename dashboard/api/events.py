from flask import Blueprint, jsonify
from dashboard.services.event_store import EVENTS, SESSIONS
from alerts.incidents import INCIDENTS

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/sessions")
def sessions():
    output = []
    for s in SESSIONS.values():
        output.append({
            "ip": s["ip"],
            "event_count": s["event_count"],
            "max_risk": s["max_risk"],
            "escalation": s["escalation"],
            "verdict": s["verdict"],
            "techniques": list(s["techniques"])
        })
    return jsonify(output)


@api.route("/incidents")
def incidents():
    return jsonify(INCIDENTS)


@api.route("/events")
def events():
    return jsonify(EVENTS)
