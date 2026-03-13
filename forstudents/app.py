from flask import Flask, request, jsonify

app = Flask(__name__)



@app.route("/api/data", methods=["GET", "POST"])
def data():
    #put headers in a list here
    headers = {
 
    }

    return jsonify({"status":"success"}), 200, headers


app.run(host='0.0.0.0', port='5001')
