import threading
import time
import requests
from flask import Flask, jsonify, request, render_template, send_from_directory

app = Flask(__name__)

teams = {}
lock = threading.Lock()
MAX_TEAMS = 30


def empty_status():
    return {
        "reachable": False,
        "cors_origin": False,
        "options_supported": False,
        "methods_allowed": False,
        "headers_allowed": False,
        "post_success": False,
    }


def check_team(url):
    status = empty_status()
    try:
        r = requests.get(url, timeout=3)
        status["reachable"] = True
        if r.headers.get("Access-Control-Allow-Origin"):
            status["cors_origin"] = True
    except Exception:
        return status

    try:
        r = requests.options(
            url,
            headers={
                "Origin": "http://localhost",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, X-Student-ID",
            },
            timeout=3,
        )
        if r.status_code in (200, 204) and r.headers.get("Access-Control-Allow-Methods"):
            status["options_supported"] = True
        methods = r.headers.get("Access-Control-Allow-Methods", "")
        if "POST" in methods:
            status["methods_allowed"] = True
        headers = r.headers.get("Access-Control-Allow-Headers", "")
        if "Content-Type" in headers and "X-Student-ID" in headers:
            status["headers_allowed"] = True
    except Exception:
        pass

    try:
        r = requests.post(
            url,
            json={"message": "hello"},
            headers={"Content-Type": "application/json", "X-Student-ID": "123"},
            timeout=3,
        )
        if r.status_code == 200:
            r.json()
            status["post_success"] = True
    except Exception:
        pass

    return status


def polling_loop():
    while True:
        with lock:
            snapshot = list(teams.items())
        for name, data in snapshot:
            status = check_team(data["url"])
            with lock:
                if name in teams:
                    teams[name]["status"] = status
        time.sleep(5)


thread = threading.Thread(target=polling_loop, daemon=True)
thread.start()

@app.route("/downloadindex")
def download_index():
    return send_from_directory(
        directory="forstudents",
        path="index.html",
        as_attachment=True
    )
@app.route("/downloadapp")
def download_app():
    return send_from_directory(
        directory="forstudents",
        path="app.py",
        as_attachment=True
    )

@app.route("/downloadreadme")
def download_readme():
    return send_from_directory(
        directory="forstudents",
        path="readme.txt",
        as_attachment=True
    )

@app.route("/")
def index():
    return render_template("leaderboard.html")


@app.route("/register.html")
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    url = str(data.get("url", "")).strip()

    if not name:
        return jsonify({"error": "Team name is required"}), 400
    if not url.startswith("http"):
        return jsonify({"error": "URL must start with http"}), 400
    if "/api/data" not in url:
        return jsonify({"error": "URL must contain /api/data"}), 400

    with lock:
        if name in teams:
            return jsonify({"error": "Team name already registered"}), 409
        if len(teams) >= MAX_TEAMS:
            return jsonify({"error": "Maximum team limit reached"}), 403
        teams[name] = {
            "url": url,
            "registered_at": time.time(),
            "status": empty_status(),
        }

    return jsonify({"message": f"Team '{name}' registered successfully"}), 201


@app.route("/teams")
def get_teams():
    with lock:
        result = []
        for name, data in teams.items():
            status = data["status"]
            score = sum(1 for v in status.values() if v)
            result.append({"name": name, "url": data["url"], "status": status, "score": score})
    result.sort(key=lambda t: t["score"], reverse=True)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
