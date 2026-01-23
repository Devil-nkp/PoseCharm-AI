import os
import random
import time
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from duckduckgo_search import DDGS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

class RomanticSoulAI:
    def __init__(self):
        self.master_title = "romantic couple poses"

    def get_live_images(self, style):
        all_images = []
        
        # 3-STAGE CASCADE STRATEGY
        # If Stage 1 fails, it falls through to Stage 2, then Stage 3.
        
        if style == 'real':
            queries = [
                "romantic couple poses modest aesthetic 4k portrait photography", # Stage 1: Specific
                "happy couple in love photography poses",                       # Stage 2: Broad
                "cute couple poses"                                             # Stage 3: Simple
            ]
        else:
            queries = [
                "anime romantic couple illustration 4k wallpaper magical",
                "anime couple in love art",
                "cute anime couple"
            ]

        # Try each query until we find images
        for query in queries:
            if len(all_images) >= 20: 
                break # We have enough
            
            try:
                logger.info(f"🔍 Hunting Live: '{query}'")
                with DDGS() as ddgs:
                    # Random pause to look human
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    results = ddgs.images(
                        query, 
                        region="wt-wt", 
                        safesearch="on", 
                        max_results=30
                    )
                    
                    # Extract valid links
                    found = [r['image'] for r in results if r.get('image')]
                    
                    if found:
                        logger.info(f"✅ Found {len(found)} images in this stage.")
                        all_images.extend(found)
                        # If we found good images, stop hunting to save time
                        if len(all_images) > 10:
                            break
                    else:
                        logger.warning(f"⚠️ No results for '{query}'. Trying next stage...")

            except Exception as e:
                logger.error(f"❌ Error hunting '{query}': {e}")
                continue

        # Final Shuffle for variety
        random.shuffle(all_images)
        
        # Return unique images only (remove duplicates) and cap at 20
        unique_images = list(dict.fromkeys(all_images))
        return unique_images[:20]

agent = RomanticSoulAI()

@app.route('/api/generate', methods=['GET'])
def generate():
    style = request.args.get('style', 'real') 
    
    if style == 'real':
        msg = "I've hunted down these genuine moments for you."
    else:
        msg = "I've found these dreamy illustrations live from the web."

    image_list = agent.get_live_images(style)
    
    return jsonify({
        "status": "success",
        "message": msg,
        "data": image_list
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
