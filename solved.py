from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route("/api/data", methods=["GET", "POST", "OPTIONS"])
def data():
    #put headers in a list here
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Student-ID",
    }

    return jsonify({"status":"success"}), 200, headers


app.run(host='0.0.0.0', port='5001')
