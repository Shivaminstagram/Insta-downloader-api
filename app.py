from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import re

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(url, timeout=60000)

            # Wait for video to load
            page.wait_for_selector('video', timeout=10000)
            video_element = page.query_selector("video")
            video_url = video_element.get_attribute("src")

            browser.close()

            if video_url and video_url.startswith("http"):
                return jsonify({"video_url": video_url})
            else:
                return jsonify({"error": "Video not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
