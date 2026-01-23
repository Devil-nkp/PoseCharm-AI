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
        # 70+ Poses List (Condensed for brevity, assumed full list is here)
        self.all_poses = [
            "Forehead Touch couple", "Forehead Kiss couple", "Hand Kiss couple", 
            "Hand-in-Hand Walk couple", "Back Hug couple", "Hug from Behind couple", 
            "Standing Face-to-Face couple", "Nose-to-Nose couple", "Brief Kiss cheek or lips couple", 
            "Classic Kiss couple", "Close Cheek Kiss couple", "Finger Interlock couple", 
            "Wrapped Arms Around Waist couple", "Mutual Back Rub couple", "Looking into Each Other’s Eyes couple", 
            "Silhouette Kiss at Sunset couple", "Leaning on Shoulder couple", "Snuggle Under Blanket couple", 
            "Seated Close Snuggle couple", "Wind-Blown Hair Look couple", "Leaning on Wall Together couple", 
            "Back to Back with Looking Over Shoulder couple", "Seated Leg Wrap couple", 
            "Sitting Close Heart-to-Heart couple", "Forehead to Chest couple",
            "Piggyback Ride couple", "Twirl in the Field couple", "Walking Toward Camera Holding Hands couple", 
            "Running Hand in Hand couple", "Dancing in Street couple", "Mini Spin Lift couple", 
            "Lift and Dip Dance Pose couple", "Jump Together couple", "Confetti Toss Shot couple", 
            "Sunglasses Pose couple", "Matchy Outfits Pose couple", "Sneak a Kiss over Shoulder couple", 
            "Surprise Whisper couple", "Laughing Together couple", "Peek-a-Boo Pose couple", 
            "Playing with Hair couple", "Skipping Together couple", "Beach Splash Pose couple", 
            "Carrying on Back Pose couple", "Cheek Pinch Smile couple",
            "Sunset Walk on Beach couple", "Cuddling on Cliff Edge couple", "Hiking Trail Pause couple", 
            "Mountain Vista Embrace couple", "Lakeside Sit and Touch couple", "Picnic Together couple", 
            "City Street Walk couple", "Scenic Roadside Lean couple", "Bridge Silhouette Pose couple", 
            "Old Town Stare couple", "Countryside Stroll couple", "Camper Adventure Pose couple", 
            "Vintage Scooter Pose couple", "Suitcase Pose couple", "Walking in Meadow couple",
            "Shared Laughter Look couple", "Whisper in Ear couple", "Feeding Each Other couple", 
            "Shoulder Lean with Laugh couple", "Casual Coffee Shop Cuddle couple", "Candid Shopping Walk couple", 
            "Sharing Umbrella in Rain couple", "Mid-Step Look Back couple", "Gazing at Horizon Together couple", 
            "Looking at Phone & Laughing couple", "Resting Head on Partner’s Chest couple", 
            "Riding Bike Together couple", "Hand on Knee Close Shot couple", "Snuggle by Fire Pit couple", 
            "Couples Selfie Close-Up",
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
        
        # EMERGENCY BACKUP (Unsplash IDs) - GUARANTEED to work if DDG fails
        self.emergency_images = [
            "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=500",
            "https://images.unsplash.com/photo-1516585427167-9f4af9627e6c?w=500",
            "https://images.unsplash.com/photo-1511285560982-1351cdeb9821?w=500",
            "https://images.unsplash.com/photo-1621605815971-fbc98d665033?w=500",
            "https://images.unsplash.com/photo-1523438885200-e635ba2c371e?w=500",
            "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=500",
            "https://images.unsplash.com/photo-1494774157365-9e04c6720e47?w=500",
            "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=500",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500",
            "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500"
        ]

        self.modifiers = {
            'real': "modest fully clothed aesthetic 4k portrait photography beautiful lighting joy",
            'animated': "anime style illustration digital art magical wallpaper 4k"
        }

    def get_legendary_grid(self, style):
        # 1. Pick 5 distinct topics (Reduced from 10 to ensure speed/success)
        selected_topics = random.sample(self.all_poses, 5)
        logger.info(f"🚀 Searching for: {selected_topics}")

        all_images = []
        
        # 2. Sequential Search (One by One) - Much safer against bot blocks
        for topic in selected_topics:
            full_query = f"{topic} {self.modifiers[style]}"
            try:
                # Force 'html' backend - It is slower but rarely blocked
                with DDGS() as ddgs:
                    results = ddgs.images(
                        full_query, 
                        region="wt-wt", 
                        safesearch="on", 
                        max_results=5,
                        backend="html" 
                    )
                    # Get the top 2-3 images
                    found = [r['image'] for r in results if r.get('image')][:4]
                    all_images.extend(found)
                    time.sleep(0.5) # Gentle pause
            except Exception as e:
                logger.error(f"Failed '{topic}': {e}")
                continue

        # 3. EMERGENCY FALLBACK
        # If we have 0 images (total IP ban), use the hardcoded safety list
        if len(all_images) < 5:
            logger.critical("⚠️ TOTAL SEARCH FAILURE. DEPLOYING EMERGENCY IMAGES.")
            # Shuffle emergency images to simulate variety
            random.shuffle(self.emergency_images)
            all_images.extend(self.emergency_images)

        random.shuffle(all_images)
        return all_images[:30]

agent = RomanticSoulAI()

@app.route('/api/generate', methods=['GET'])
def generate():
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
