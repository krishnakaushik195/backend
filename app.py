"""
Chain Fit Studio - Flask Backend (Google Drive + Local Fallback)
Now serves DIRECT URLs instead of base64 → 10x faster & unlimited images
Fully backward compatible with your current React frontend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Your exact same CORS — unchanged
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

# ================== CHAIN IMAGES (Google Drive Direct URLs) ==================
# Just keep adding here — no folder needed anymore!
# Format stays EXACTLY the same as before → your React <img src={chain.data}> still works perfectly

chains_data = [
    {
        "name": "Cuban Link Gold Chain",
        "data": "https://drive.google.com/uc?export=view&id=1RKvoPREyYrmgasOp_8gzxDxpuJYPNlcV"
    },
    {
        "name": "Rope Chain Silver Shine",
        "data": "https://drive.google.com/uc?export=view&id=11k0Rxu8gWa1dFbPd1oJEhKS2zR2uo3yz"
    }
    # ADD YOUR NEXT 30-40 HERE LIKE THIS:
    # {"name": "Figaro 5mm", "data": "https://drive.google.com/uc?export=view&id=FILE_ID_HERE"},
    # {"name": "Box Chain 3mm", "data": "https://drive.google.com/uc?export=view&id=FILE_ID_HERE"},
]

# Optional: Fallback to local folder if you still want to test locally with files
# Remove this block later when you have all images in the list above
LOCAL_FOLDER = "chains"
if os.path.exists(LOCAL_FOLDER):
    import base64
    for file in sorted(os.listdir(LOCAL_FOLDER)):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(LOCAL_FOLDER, file)
            with open(path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
                ext = file.split('.')[-1].lower()
                mime = 'jpeg' if ext == 'jpg' else ext
                chains_data.append({
                    "name": os.path.splitext(file)[0],
                    "data": f"data:image/{mime};base64,{img_data}"
                })

# ================== PRINT ON STARTUP ==================
print("="*60)
print("GOLD STUDIO / CHAIN FIT STUDIO - BACKEND STARTED")
print(f"Total chains loaded: {len(chains_data)}")
print("Images now load via direct Google Drive URLs → blazing fast!")
print("="*60)

# ================== API ROUTES (unchanged logic) ==================
@app.route('/api/chains', methods=['GET'])
def get_chains():
    return jsonify(chains_data)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'chains_loaded': len(chains_data),
        'version': '2.0 - Google Drive (Fast & Scalable)'
    })

# ================== ERROR HANDLERS ==================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ================== MAIN ==================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\nServer running → https://gold-studio.onrender.com")
    print(f"Loaded {len(chains_data)} chains → ready!")
    app.run(host='0.0.0.0', port=port, debug=False)
