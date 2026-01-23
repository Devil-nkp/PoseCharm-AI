import os
import random
import time
import logging
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Import the library (modern versions use this import)
from duckduckgo_search import DDGS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)

# --- SERVE FRONTEND ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# --- THE ROMANTIC AI BRAIN ---
class RomanticSoulAI:
    def __init__(self):
        self.scenarios = {
            'real': [
                "holding hands walking into sunset",
                "forehead touch tender emotional moment",
                "couple laughing sitting on grass park",
                "man giving flower to woman surprise",
                "couple back to back reading books",
                "couple walking in rain with umbrella",
                "picnic date aesthetic modest",
                "proposing on knee romantic scenery",
                "dancing in kitchen couple aesthetic",
                "couple strolling through botanical garden"
            ],
            'animated': [
                "anime couple hugging sunset digital art",
                "lofi hip hop style couple in love art",
                "manhwa romance couple aesthetic wallpaper",
                "ghibli style romantic couple illustration",
                "cute chibi couple love drawing",
                "disney style prince and princess modern art",
                "fantasy romance couple glowing art",
                "cyberpunk couple romance neon art",
                "watercolor illustration romantic couple"
            ]
        }
        self.safety_prompt = "modest outfits fully clothed family friendly aesthetic 4k portrait photography beautiful lighting joy"

    def generate_query(self, category, style):
        scenario = random.choice(self.scenarios[style])
        base_term = "cute romantic couple"
        if category == 'masculine':
            base_term = "cool stylish couple city vibes"
            
        if style == 'animated':
            return f"{base_term} {scenario} {self.safety_prompt} digital art wallpaper"
        else:
            return f"{base_term} {scenario} {self.safety_prompt}"

    def get_images(self, category, style, count=20):
        query = self.generate_query(category, style)
        logger.info(f"❤️ Starting search for: {query}")
        
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Initialize the search engine
                with DDGS() as ddgs:
                    # Random delay to act human
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    logger.info(f"Attempt {attempt+1}/{max_retries}...")
                    
                    # --- FIX IS HERE: REMOVED 'backend' PARAMETER ---
                    results = ddgs.images(
                        query, 
                        region="wt-wt", 
                        safesearch="on", 
                        max_results=count + 10
                    )
                    
                    # Filter and extract URLs
                    image_urls = [r['image'] for r in results if r.get('image')]
                    
                    if image_urls:
                        logger.info(f"✅ Success! Found {len(image_urls)} images.")
                        random.shuffle(image_urls)
                        return image_urls[:count]
                    else:
                        logger.warning(f"⚠️ Attempt {attempt+1} returned no images.")
                        
            except Exception as e:
                logger.error(f"Error on attempt {attempt+1}: {e}")
            
            # Exponential backoff sleep (2s, 4s, 8s)
            sleep_time = (attempt + 1) * 2
            logger.info(f"Sleeping for {sleep_time}s before retry...")
            time.sleep(sleep_time)
            
        logger.error("❌ All retries failed. The agent could not find images.")
        return []

agent = RomanticSoulAI()

# --- API ENDPOINT ---
@app.route('/api/generate', methods=['GET'])
def generate():
    gender_mode = request.args.get('gender', 'feminine') 
    tone = request.args.get('tone', 'romantic')
    style = request.args.get('style', 'real') 
    
    if style == 'real':
        msg = "I've curated these genuine moments of connection. Notice the gentle lighting."
    else:
        msg = "I found these dreamy illustrations from a world where love is magic."

    image_list = agent.get_images(gender_mode, style, count=20)
    
    return jsonify({
        "status": "success",
        "message": msg,
        "data": image_list
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
