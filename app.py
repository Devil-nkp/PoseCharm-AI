import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from duckduckgo_search import DDGS
import random
import time

app = Flask(__name__)
CORS(app)

# --- SERVE THE FRONTEND ---
@app.route('/')
def home():
    # This serves your index.html file directly
    return send_from_directory('.', 'index.html')

# --- THE AGENT BRAIN ---
class RomanticSoulAI:
    def __init__(self):
        self.ddgs = DDGS()
        
        self.scenarios = {
            'real': [
                "holding hands walking into sunset",
                "forehead touch tender emotional moment",
                "couple laughing sitting on grass park",
                "man giving flower to woman surprise",
                "couple back to back reading books",
                "couple walking in rain with umbrella",
                "picnic date aesthetic modest"
            ],
            'animated': [
                "anime couple hugging sunset digital art",
                "lofi hip hop style couple in love art",
                "manhwa romance couple aesthetic wallpaper",
                "ghibli style romantic couple illustration",
                "cute chibi couple love drawing",
                "disney style prince and princess modern art"
            ]
        }

        self.safety_prompt = (
            "modest fully clothed no swimwear no bikini no cleavage "
            "family friendly aesthetic 4k high resolution portrait photography "
            "beautiful lighting joy happiness"
        )

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
        print(f"❤️ Searching: {query}")
        
        try:
            # Sleep to prevent rate limiting
            time.sleep(0.5)
            
            # Perform Deep Search
            results = self.ddgs.images(
                query, 
                region="wt-wt", 
                safesearch="on", 
                max_results=count + 15 
            )
            return [r['image'] for r in results][:count]
            
        except Exception as e:
            print(f"💔 Error: {e}")
            return []

agent = RomanticSoulAI()

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
    # RENDER CONFIGURATION
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
