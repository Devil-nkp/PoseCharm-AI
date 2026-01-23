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
        # We now only have ONE master title as requested
        self.master_title = "romantic couple poses"
        
        self.modifiers = {
            'real': "modest fully clothed aesthetic 4k portrait photography beautiful lighting joy",
            'animated': "anime style illustration digital art magical wallpaper 4k"
        }

    def get_master_grid(self, style):
        # Construct the single powerful query
        full_query = f"{self.master_title} {self.modifiers[style]}"
        logger.info(f"🚀 Executing Master Search: {full_query}")

        all_images = []
        
        try:
            with DDGS() as ddgs:
                # We ask for 50 results to ensure we have plenty of high-quality choices
                # This is a SINGLE request, so it's very fast and safe.
                results = ddgs.images(
                    full_query, 
                    region="wt-wt", 
                    safesearch="on", 
                    max_results=50
                )
                
                # Extract valid image URLs
                found = [r['image'] for r in results if r.get('image')]
                
                if found:
                    logger.info(f"✅ Success! Found {len(found)} raw images.")
                    all_images = found
                else:
                    logger.warning("⚠️ Search returned 0 results. Trying simplified query...")
                    # Fallback if specific modifiers limit too much
                    fallback = ddgs.images(f"{self.master_title} aesthetic", max_results=30)
                    all_images = [r['image'] for r in fallback if r.get('image')]

        except Exception as e:
            logger.error(f"❌ Search Error: {e}")
            return []

        # Return exactly top 20 images
        return all_images[:20]

agent = RomanticSoulAI()

@app.route('/api/generate', methods=['GET'])
def generate():
    style = request.args.get('style', 'real') 
    
    if style == 'real':
        msg = "I've curated the best genuine romantic moments for you."
    else:
        msg = "I've found these beautiful romantic illustrations."

    # Single Master Search
    image_list = agent.get_master_grid(style)
    
    return jsonify({
        "status": "success",
        "message": msg,
        "data": image_list
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
