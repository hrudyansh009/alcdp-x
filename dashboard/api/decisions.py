from flask import Blueprint, jsonify
from dashboard.services.decision_store import get_decisions

api = Blueprint("decisions_api", __name__)

@api.route("/api/decisions", methods=["GET"])
def decisions():
    return jsonify(get_decisions())
