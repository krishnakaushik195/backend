"""
Chain Fit Studio - Flask Backend
Loads chain images from Google Drive links → Base64 → Sends to React frontend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)

# CORS for frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8080",
            "https://*.lovable.app",
            "https://chain-fit-studio-23234.onrender.com",
            "https://gold-studio.onrender.com",
            "https://*.onrender.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ================== GOOGLE DRIVE LINKS ==================
GOOGLE_DRIVE_LINKS = [
    "https://drive.google.com/uc?export=view&id=1RKvoPREyYrmgasOp_8gzxDxpuJYPNlcV",
    "https://drive.google.com/uc?export=view&id=11k0Rxu8gWa1dFbPd1oJEhKS2zR2uo3yz",
    # Add remaining 38 links here...
]

# ================== LOAD IMAGES FROM GOOGLE DRIVE ==================
chains_data = []

print("=" * 50)
print("CHAIN FIT STUDIO - Loading Google Drive Images...")
print("=" * 50)

for index, url in enumerate(GOOGLE_DRIVE_LINKS, start=1):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            img_bytes = response.content
            img_base64 = base64.b64encode(img_bytes).decode()

            # assume PNG (Drive auto-detects), can change if needed
            mime_type = "image/png"

            chains_data.append({
                "name": f"chain_{index}",
                "data": f"data:{mime_type};base64,{img_base64}"
            })

            print(f" ✓ Loaded chain {index}")

        else:
            print(f" ✗ Failed to load chain {index}: HTTP {response.status_code}")

    except Exception as e:
        print(f" ✗ Error loading chain {index}: {e}")

print(f"\n✓ Total chains loaded: {len(chains_data)}")
print("=" * 50)

# ================== API ROUTES ==================
@app.route('/api/chains', methods=['GET'])
def get_chains():
    """Return all base64-encoded chain images"""
    return jsonify(chains_data)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'chains_loaded': len(chains_data),
        'version': '1.1.0'
    })

# ================== ERROR HANDLERS ==================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ================== START SERVER ==================
if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("CHAIN FIT STUDIO - SERVER STARTING")
    print("=" * 50)
    print(f"Loaded {len(chains_data)} chains from Google Drive\n")

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
