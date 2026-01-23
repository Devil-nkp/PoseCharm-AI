import os
import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from duckduckgo_search import DDGS

# Set up logging to track the AI's "thought process" on Render
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')
CORS(app)

# --- SERVE THE APP ---
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# --- THE MASTER POSE LIBRARY (70+ Scenarios) ---
class PoseLibrary:
    def __init__(self):
        self.all_poses = [
            # Classic Romantics
            "Forehead Touch couple", "Forehead Kiss couple", "Hand Kiss couple", 
            "Hand-in-Hand Walk couple", "Back Hug couple", "Hug from Behind couple", 
            "Standing Face-to-Face couple", "Nose-to-Nose couple", "Brief Kiss cheek or lips couple", 
            "Classic Kiss couple", "Close Cheek Kiss couple", "Finger Interlock couple", 
            "Wrapped Arms Around Waist couple", "Mutual Back Rub couple", "Looking into Each Other’s Eyes couple", 
            "Silhouette Kiss at Sunset couple", "Leaning on Shoulder couple", "Snuggle Under Blanket couple", 
            "Seated Close Snuggle couple", "Wind-Blown Hair Look couple", "Leaning on Wall Together couple", 
            "Back to Back with Looking Over Shoulder couple", "Seated Leg Wrap couple", 
            "Sitting Close Heart-to-Heart couple", "Forehead to Chest couple",
            
            # Creative & Playful
            "Piggyback Ride couple", "Twirl in the Field couple", "Walking Toward Camera Holding Hands couple", 
            "Running Hand in Hand couple", "Dancing in Street couple", "Mini Spin Lift couple", 
            "Lift and Dip Dance Pose couple", "Jump Together couple", "Confetti Toss Shot couple", 
            "Sunglasses Pose couple", "Matchy Outfits Pose couple", "Sneak a Kiss over Shoulder couple", 
            "Surprise Whisper couple", "Laughing Together couple", "Peek-a-Boo Pose couple", 
            "Playing with Hair couple", "Skipping Together couple", "Beach Splash Pose couple", 
            "Carrying on Back Pose couple", "Cheek Pinch Smile couple",
            
            # Scenic & Travel
            "Sunset Walk on Beach couple", "Cuddling on Cliff Edge couple", "Hiking Trail Pause couple", 
            "Mountain Vista Embrace couple", "Lakeside Sit and Touch couple", "Picnic Together couple", 
            "City Street Walk couple", "Scenic Roadside Lean couple", "Bridge Silhouette Pose couple", 
            "Old Town Stare couple", "Countryside Stroll couple", "Camper Adventure Pose couple", 
            "Vintage Scooter Pose couple", "Suitcase Pose couple", "Walking in Meadow couple",
            
            # Candid Moments
            "Shared Laughter Look couple", "Whisper in Ear couple", "Feeding Each Other couple", 
            "Shoulder Lean with Laugh couple", "Casual Coffee Shop Cuddle couple", "Candid Shopping Walk couple", 
            "Sharing Umbrella in Rain couple", "Mid-Step Look Back couple", "Gazing at Horizon Together couple", 
            "Looking at Phone & Laughing couple", "Resting Head on Partner’s Chest couple", 
            "Riding Bike Together couple", "Hand on Knee Close Shot couple", "Snuggle by Fire Pit couple", 
            "Couples Selfie Close-Up",
            
            # Festive & Styled
            "Champagne Pop Shot couple", "Valentine Hearts Prop couple", "Christmas Lights Cuddle couple", 
            "New Year Kiss couple", "Autumn Leaves Toss couple", "Pumpkin Patch Play couple", 
            "Snow Snuggle Pose couple", "Autumn Blanket Throw couple", "Spring Flowers Pose couple", 
            "Summer Pool Float Pose couple", "Rainy Day Hug couple", "Lantern Walk couple", 
            "Balloon Walk Shot couple", "Festival Dance Together couple",
            "Veil Lift couple", "First Dance Pose couple", "Ring Focus Close-Up couple", 
            "Groom Carrying Bride couple", "Soft Kiss by Arch couple", "Slow Dance Walk couple", 
            "Retro Vintage Car Pose couple", "Retro Film Camera Pose couple", "Road Trip Map Look couple", 
            "Rustic Barn Door Embrace couple", "Candlelit Dinner Pose couple", "Tea Shop Window Pose couple", 
            "Vinyl Record Dance couple", "Bookstore Close Reading Pose couple"
        ]

class RomanticSoulAI:
    def __init__(self):
        self.library = PoseLibrary()
        # Modifiers enforce quality (4k, lighting) and Safety (modest, fully clothed)
        self.modifiers = {
            'real': "modest fully clothed aesthetic 4k portrait photography beautiful lighting joy",
            'animated': "anime style illustration digital art magical wallpaper 4k"
        }

    def _search_single_topic(self, topic, style):
        """Worker function: Searches for ONE specific topic (e.g., 'Piggyback Ride')."""
        full_query = f"{topic} {self.modifiers[style]}"
        try:
            # Create a fresh search instance for this thread
            with DDGS() as ddgs:
                # We ask for 5 results to ensure we get at least 2-3 valid ones
                results = ddgs.images(
                    full_query, 
                    region="wt-wt", 
                    safesearch="on", 
                    max_results=5
                )
                return [r['image'] for r in results if r.get('image')]
        except Exception as e:
            logger.error(f"Failed to fetch topic '{topic}': {e}")
            return []

    def get_legendary_grid(self, style):
        # 1. INTELLIGENCE: Select 10 Distinct Topics
        # This ensures the grid is never boring. It's always a mix of 10 different vibes.
        selected_topics = random.sample(self.library.all_poses, 10)
        logger.info(f"🚀 Launching 10-Core Search for: {selected_topics}")

        all_images = []
        
        # 2. SPEED: Execute 10 Parallel Searches
        # We use ThreadPoolExecutor to run all 10 searches at the exact same time.
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self._search_single_topic, topic, style) for topic in selected_topics]
            
            for future in futures:
                images = future.result()
                # Take the top 3 images from each topic
                all_images.extend(images[:3]) 

        # 3. RELIABILITY: Fallback if internet is weird
        if len(all_images) < 10:
            logger.warning("Parallel search yielded low results. Running backup...")
            try:
                with DDGS() as ddgs:
                    backup = ddgs.images(f"romantic couple poses variety {self.modifiers[style]}", max_results=20)
                    all_images.extend([r['image'] for r in backup if r.get('image')])
            except: pass

        # 4. PRESENTATION: Shuffle and serve
        random.shuffle(all_images)
        # Return a generous 30 images
        return all_images[:30]

agent = RomanticSoulAI()

@app.route('/api/generate', methods=['GET'])
def generate():
    gender_mode = request.args.get('gender', 'feminine') 
    tone = request.args.get('tone', 'romantic')
    style = request.args.get('style', 'real') 
    
    if style == 'real':
        msg = "I've scouted 10 different worlds to find these genuine moments for you."
    else:
        msg = "I've gathered these dreamy illustrations from 10 magical storybooks."

    # Execute the Mega-Search
    image_list = agent.get_legendary_grid(style)
    
    return jsonify({
        "status": "success",
        "message": msg,
        "data": image_list
    })

if __name__ == '__main__':
    # Required for Render Deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
