from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ API is Live"

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://ssstik.io/en")
            page.fill('input[name="id"]', url)
            page.click('button[type="submit"]')
            page.wait_for_selector("a.download_link", timeout=15000)
            link = page.query_selector("a.download_link")
            download_url = link.get_attribute("href") if link else None
            browser.close()

            if not download_url:
                return jsonify({"error": "No video found."}), 404

            return jsonify({"video_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ This is the only addition required for Render to bind the port:
if __name__ == "__main__":
    from waitress import serve
    import os
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
