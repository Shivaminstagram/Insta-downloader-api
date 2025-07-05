from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import re

app = Flask(__name__)

def extract_shortcode(insta_url):
    match = re.search(r"instagram\.com/(reel|p|tv)/([A-Za-z0-9_-]+)", insta_url)
    if match:
        return match.group(2)
    return None

@app.route('/')
def home():
    return "Instagram Video Downloader API is running!"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    insta_url = data.get('url')

    if not insta_url:
        return jsonify({"error": "No URL provided"}), 400

    shortcode = extract_shortcode(insta_url)
    if not shortcode:
        return jsonify({"error": "Invalid Instagram URL"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"https://www.instagram.com/reel/{shortcode}", timeout=60000)
            page.wait_for_timeout(3000)

            video_url = page.eval_on_selector("video", "el => el.src")
            browser.close()

        if video_url:
            return jsonify({"video_url": video_url})
        else:
            return jsonify({"error": "Video URL not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Required for Render hosting
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
