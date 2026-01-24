import os
import random
import time
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from duckduckgo_search import DDGS

# Set up logging to track the AI's status
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)

# --- SERVE THE APP ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

class RomanticSoulAI:
    def __init__(self):
        self.master_title = "romantic couple poses"

    def get_live_images(self, style):
        all_images = []
        
        # --- 3-STAGE CASCADE STRATEGY ---
        # 1. Complex Aesthetic Search (Best Quality)
        # 2. Broad Topic Search (Good Quality)
        # 3. Simple Keyword Search (Guaranteed Results)
        
        if style == 'real':
            queries = [
                "romantic couple poses modest aesthetic 4k portrait photography beautiful lighting", # Stage 1
                "happy couple in love photography poses",                                          # Stage 2
                "cute couple poses"                                                                # Stage 3
            ]
        else:
            queries = [
                "anime romantic couple illustration 4k wallpaper magical",
                "anime couple in love art",
                "cute anime couple"
            ]

        # Try each query in order until we find enough images
        for query in queries:
            # If we already have 20+ images from a previous stage, stop hunting
            if len(all_images) >= 20: 
                break 
            
            try:
                logger.info(f"🔍 Hunting Live: '{query}'")
                with DDGS() as ddgs:
                    # Random pause to look like a human user
                    time.sleep(random.uniform(0.5, 1.0))
                    
                    # Perform Search
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
                        
                        # If we found plenty of images, we can stop the cascade early
                        if len(all_images) > 15:
                            break
                    else:
                        logger.warning(f"⚠️ No results for '{query}'. Trying next stage...")

            except Exception as e:
                logger.error(f"❌ Error hunting '{query}': {e}")
                continue

        # Final Polish: Shuffle and Remove Duplicates
        random.shuffle(all_images)
        unique_images = list(dict.fromkeys(all_images))
        
        return unique_images[:20]

agent = RomanticSoulAI()

# --- API ENDPOINT ---
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
