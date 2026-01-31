from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

COWRIE_LOG = "/home/kali/cowrie/var/log/cowrie/cowrie.json"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/attacks")
def api_attacks():
    events = []
    try:
        with open(COWRIE_LOG, "r") as f:
            for line in f.readlines()[-50:]:  # last 50 events
                events.append(json.loads(line))
    except Exception as e:
        return jsonify({"error": str(e)})

    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
