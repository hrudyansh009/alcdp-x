from flask import Flask, jsonify, render_template
from threading import Thread
import time

from dashboard.services.event_store import (
    get_events,
    get_sessions,
    get_incidents,
    add_event,
)

from correlation.correlator import generate_event, ATTACK_PROFILES


def background_engine():
    ips = list(ATTACK_PROFILES.keys())
    while True:
        for ip in ips:
            event = generate_event(ip)
            add_event(event)
        time.sleep(3)


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/events")
    def api_events():
        return jsonify(get_events())

    @app.route("/api/sessions")
    def api_sessions():
        return jsonify(list(get_sessions().values()))

    @app.route("/api/incidents")
    def api_incidents():
        return jsonify(get_incidents())

    return app


app = create_app()

# Start correlator inside Flask process
engine_thread = Thread(target=background_engine, daemon=True)
engine_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
