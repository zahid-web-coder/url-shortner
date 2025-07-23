import string
import random
import time
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

url_db = {}  

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "URL Shortener API is running"}), 200

@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url or not original_url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    while short_code in url_db:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    url_db[short_code] = {
        "original_url": original_url,
        "clicks": 0,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    }

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    data = url_db.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404
    data["clicks"] += 1
    return redirect(data["original_url"])

@app.route("/api/stats/<short_code>", methods=["GET"])
def get_stats(short_code):
    data = url_db.get(short_code)
    if not data:
        return jsonify({"error": "Short code not found"}), 404
    return jsonify({
        "url": data["original_url"],
        "clicks": data["clicks"],
        "created_at": data["created_at"]
    }), 200
