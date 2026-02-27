from flask import Blueprint, jsonify
from dashboard.services.store import get_events, get_sessions, get_incidents

api = Blueprint("api", __name__, url_prefix="/api")

@api.get("/events")
def events():
    return jsonify(get_events())

@api.get("/sessions")
def sessions():
    return jsonify(get_sessions())

@api.get("/incidents")
def incidents():
    return jsonify(get_incidents())
