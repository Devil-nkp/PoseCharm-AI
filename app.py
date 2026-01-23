import os
import random
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
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

class PoseLibrary:
    def __init__(self):
        self.all_poses = [
            # Classic
            "Forehead Touch couple", "Forehead Kiss couple", "Hand Kiss couple", 
            "Hand-in-Hand Walk couple", "Back Hug couple", "Hug from Behind couple", 
            "Standing Face-to-Face couple", "Nose-to-Nose couple", "Brief Kiss cheek or lips couple", 
            "Classic Kiss couple", "Close Cheek Kiss couple", "Finger Interlock couple", 
            "Wrapped Arms Around Waist couple", "Mutual Back Rub couple", "Looking into Each Other’s Eyes couple", 
            "Silhouette Kiss at Sunset couple", "Leaning on Shoulder couple", "Snuggle Under Blanket couple", 
            "Seated Close Snuggle couple", "Wind-Blown Hair Look couple", "Leaning on Wall Together couple", 
            "Back to Back with Looking Over Shoulder couple", "Seated Leg Wrap couple", 
            "Sitting Close Heart-to-Heart couple", "Forehead to Chest couple",
            
            # Creative
            "Piggyback Ride couple", "Twirl in the Field couple", "Walking Toward Camera Holding Hands couple", 
            "Running Hand in Hand couple", "Dancing in Street couple", "Mini Spin Lift couple", 
            "Lift and Dip Dance Pose couple", "Jump Together couple", "Confetti Toss Shot couple", 
            "Sunglasses Pose couple", "Matchy Outfits Pose couple", "Sneak a Kiss over Shoulder couple", 
            "Surprise Whisper couple", "Laughing Together couple", "Peek-a-Boo Pose couple", 
            "Playing with Hair couple", "Skipping Together couple", "Beach Splash Pose couple", 
            "Carrying on Back Pose couple", "Cheek Pinch Smile couple",
            
            # Scenic
            "Sunset Walk on Beach couple", "Cuddling on Cliff Edge couple", "Hiking Trail Pause couple", 
            "Mountain Vista Embrace couple", "Lakeside Sit and Touch couple", "Picnic Together couple", 
            "City Street Walk couple", "Scenic Roadside Lean couple", "Bridge Silhouette Pose couple", 
            "Old Town Stare couple", "Countryside Stroll couple", "Camper Adventure Pose couple", 
            "Vintage Scooter Pose couple", "Suitcase Pose couple", "Walking in Meadow couple",
            
            # Candid
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
        self.modifiers = {
            'real': "modest fully clothed aesthetic 4k portrait photography beautiful lighting joy",
            'animated': "anime style illustration digital art magical wallpaper 4k"
        }

    def _search_single_topic(self, topic, style):
        """Worker function with built-in retry and stagger."""
        # STAGGER: Wait a random amount (0.5 to 2.0s) to avoid bot detection
        time.sleep(random.uniform(0.5, 2.0))
        
        full_query = f"{topic} {self.modifiers[style]}"
        
        try:
            with DDGS() as ddgs:
                results = ddgs.images(
                    full_query, 
                    region="wt-wt", 
                    safesearch="on", 
                    max_results=5
                )
                return [r['image'] for r in results if r.get('image')]
        except Exception as e:
            logger.warning(f"Timeout/Error on '{topic}': {e}")
            return []

    def get_legendary_grid(self, style):
        # 1. Select 10 Topics
        selected_topics = random.sample(self.library.all_poses, 10)
        logger.info(f"🚀 Starting Stabilized Search for: {selected_topics}")

        all_images = []
        
        # 2. Parallel Execution (Capped at 5 workers for stability)
        # Reducing workers prevents "Connection Refused" errors from DDG
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_topic = {executor.submit(self._search_single_topic, topic, style): topic for topic in selected_topics}
            
            for future in as_completed(future_to_topic):
                images = future.result()
                if images:
                    # Take top 3 from each successful search
                    all_images.extend(images[:3])

        # 3. SAFETY NET: If we have too few images, run a Guaranteed Backup
        if len(all_images) < 10:
            logger.warning("⚠️ Parallel search restricted. Running Safety Net Search...")
            try:
                # A single simple search is rarely blocked
                with DDGS() as ddgs:
                    backup_query = f"romantic couple aesthetic poses variety {self.modifiers[style]}"
                    backup_results = ddgs.images(backup_query, region="wt-wt", safesearch="on", max_results=30)
                    all_images.extend([r['image'] for r in backup_results if r.get('image')])
            except Exception as e:
                logger.error(f"CRITICAL: Backup failed too: {e}")

        # 4. Shuffle & Serve
        random.shuffle(all_images)
        return all_images[:30]

agent = RomanticSoulAI()

@app.route('/api/generate', methods=['GET'])
def generate():
    gender_mode = request.args.get('gender', 'feminine') 
    tone = request.args.get('tone', 'romantic')
    style = request.args.get('style', 'real') 
    
    if style == 'real':
        msg = "I've curated these genuine moments from across the world."
    else:
        msg = "I've gathered these dreamy illustrations from magical storybooks."

    image_list = agent.get_legendary_grid(style)
    
    return jsonify({
        "status": "success",
        "message": msg,
        "data": image_list
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
