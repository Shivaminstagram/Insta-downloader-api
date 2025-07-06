from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Instagram Downloader API is Live!"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing Instagram URL"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            page.wait_for_timeout(3000)

            video = page.query_selector("video")
            if not video:
                return jsonify({"error": "No video found"}), 404

            video_url = video.get_attribute("src")
            browser.close()

            return jsonify({"video_url": video_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
