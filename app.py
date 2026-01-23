import os
import random
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from duckduckgo_search import DDGS

# Initialize Flask
# static_folder='.' allows serving files from the current directory
app = Flask(__name__, static_folder='.')
CORS(app)

# --- ROUTE: SERVE FRONTEND ---
@app.route('/')
def home():
    # Looks for index.html in the same folder
    return send_from_directory('.', 'index.html')

# --- THE ROMANTIC AI BRAIN ---
class RomanticSoulAI:
    def __init__(self):
        self.ddgs = DDGS()
        
        # Intelligent Search Scenarios
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
                "dancing in kitchen couple aesthetic"
            ],
            'animated': [
                "anime couple hugging sunset digital art",
                "lofi hip hop style couple in love art",
                "manhwa romance couple aesthetic wallpaper",
                "ghibli style romantic couple illustration",
                "cute chibi couple love drawing",
                "disney style prince and princess modern art",
                "fantasy romance couple glowing art",
                "cyberpunk couple romance neon art"
            ]
        }

        # Safety & Quality Guardrails
        self.safety_prompt = (
            "modest fully clothed no swimwear no bikini no cleavage "
            "family friendly aesthetic 4k high resolution portrait photography "
            "beautiful lighting joy happiness"
        )

    def generate_query(self, category, style):
        # 1. Pick a random scenario
        scenario = random.choice(self.scenarios[style])
        
        # 2. Adjust for Gender Mode
        base_term = "cute romantic couple"
        if category == 'masculine':
            base_term = "cool stylish couple city vibes"
            
        # 3. Construct Final Search String
        if style == 'animated':
            return f"{base_term} {scenario} {self.safety_prompt} digital art wallpaper"
        else:
            return f"{base_term} {scenario} {self.safety_prompt}"

    def get_images(self, category, style, count=20):
        query = self.generate_query(category, style)
        print(f"❤️ Searching: {query}")
        
        try:
            # Sleep prevents getting blocked by search engine
            time.sleep(0.5)
            
            # Perform Search
            results = self.ddgs.images(
                query, 
                region="wt-wt", 
                safesearch="on", 
                max_results=count + 15 
            )
            
            # Return pure URLs
            return [r['image'] for r in results][:count]
            
        except Exception as e:
            print(f"💔 Error: {e}")
            return []

# Initialize Agent
agent = RomanticSoulAI()

# --- ROUTE: API ENDPOINT ---
@app.route('/api/generate', methods=['GET'])
def generate():
    # Get parameters from frontend
    gender_mode = request.args.get('gender', 'feminine') 
    tone = request.args.get('tone', 'romantic')
    style = request.args.get('style', 'real') 
    
    # Generate Message
    if style == 'real':
        msg = "I've curated these genuine moments of connection. Notice the gentle lighting."
    else:
        msg = "I found these dreamy illustrations from a world where love is magic."

    # Fetch Images
    image_list = agent.get_images(gender_mode, style, count=20)
    
    return jsonify({
        "status": "success",
        "message": msg,
        "data": image_list
    })

# --- START SERVER ---
if __name__ == '__main__':
    # Use the PORT environment variable for Render, default to 5000 for local
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required for cloud deployment
    app.run(host='0.0.0.0', port=port)
