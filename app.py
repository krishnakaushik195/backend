"""
Chain Fit Studio - Flask Backend
Serves chain images as base64 data to React frontend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import base64

app = Flask(__name__)

# Configure CORS for React frontend - UPDATED
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8080",
            "https://*.lovable.app",
            "https://chain-fit-studio-23234.onrender.com",
            "https://*.onrender.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ================== CONFIG ==================
CHAIN_FOLDER = "chains"
os.makedirs(CHAIN_FOLDER, exist_ok=True)

# Load chains and convert to base64
chains_data = []

print("="*50)
print("CHAIN FIT STUDIO - Loading chains...")
print("="*50)

for file in sorted(os.listdir(CHAIN_FOLDER)):
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(CHAIN_FOLDER, file)
        try:
            with open(path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
                ext = file.lower().split('.')[-1]
                mime_type = f"image/{'jpeg' if ext == 'jpg' else ext}"
                
                chains_data.append({
                    'name': os.path.splitext(file)[0],
                    'data': f"data:{mime_type};base64,{img_data}"
                })
                print(f"   ✓ Loaded: {file}")
        except Exception as e:
            print(f"   ✗ Error loading {file}: {e}")

if not chains_data:
    print("\n⚠️  WARNING: No chain images found in 'chains/' folder!")
else:
    print(f"\n✓ Total chains loaded: {len(chains_data)}\n")

print("="*50)

# ================== API ROUTES ==================

@app.route('/api/chains', methods=['GET'])
def get_chains():
    """Get all chain images as base64"""
    return jsonify(chains_data)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'chains_loaded': len(chains_data),
        'version': '1.0.0'
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
    print("\n" + "="*50)
    print("CHAIN FIT STUDIO - SERVER STARTING")
    print("="*50)
    print(f"\n🔗 API Endpoints:")
    print(f"   GET  /api/chains  - Get all chains")
    print(f"   GET  /api/health  - Health check")
    print(f"\n📦 Loaded {len(chains_data)} chain(s)")
    print("\n" + "="*50 + "\n")
    
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        debug=True,
        threaded=True,
        host='0.0.0.0',
        port=port
    )
