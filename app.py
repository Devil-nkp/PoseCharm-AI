import os
import urllib.parse
import random
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

AESTHETIC_PROFILES = {
    "soft_girl": {
        "search_prefix": "aesthetic soft girl fashion pose, korean street style, dreamy lighting",
        "tags": "soft pastel aesthetic, dreamy bokeh, ethereal glow, high fashion photography, 8k",
        "accent": "#ff85a1"
    },
    "baddie": {
        "search_prefix": "y2k baddie fashion pose, luxury streetwear woman, neon aesthetic",
        "tags": "streetwear luxury, high fashion pose, sharp makeup, cinematic lighting, edgy",
        "accent": "#ff0050"
    },
    "old_money": {
        "search_prefix": "old money aesthetic woman pose, quiet luxury fashion, vintage yacht",
        "tags": "quiet luxury, vintage aesthetic, clean white linen, timeless elegance, 35mm film",
        "accent": "#f7b267"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_poses', methods=['GET'])
def get_poses():
    category = request.args.get('category', 'soft_girl')
    profile = AESTHETIC_PROFILES.get(category, AESTHETIC_PROFILES['soft_girl'])
    gallery = []
    
    for _ in range(12):
        seed = random.randint(1, 1000000)
        prompt_logic = f"{profile['search_prefix']}, {profile['tags']}, professional model"
        encoded_prompt = urllib.parse.quote(prompt_logic)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=600&height=900&nologo=true&seed={seed}"
        gallery.append({"url": image_url, "accent": profile['accent'], "seed": seed})
        
    return jsonify({"status": "success", "data": gallery})

if __name__ == '__main__':
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
