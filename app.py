from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Instagram Video Downloader API is running!'

@app.route('/api/download', methods=['POST'])
def download_instagram_video():
    data = request.json
    url = data.get("url")

    if not url or "instagram.com" not in url:
        return jsonify({"success": False, "message": "Invalid Instagram URL"}), 400

    try:
        # Generate a random filename
        filename = f"{uuid.uuid4().hex}.mp4"
        output_path = f"downloads/{filename}"

        # Create downloads folder if not exist
        os.makedirs("downloads", exist_ok=True)

        # Use yt-dlp to download Instagram video
        command = [
            "yt-dlp",
            "-f", "mp4",
            "-o", output_path,
            url
        ]
        subprocess.run(command, check=True)

        # Return download URL
        download_url = request.host_url + "downloads/" + filename
        return jsonify({"success": True, "download_url": download_url})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Serve downloaded files
from flask import send_from_directory

@app.route('/downloads/<filename>')
def serve_video(filename):
    return send_from_directory("downloads", filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
