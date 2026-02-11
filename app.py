from flask import Flask, render_template, jsonify, request
import random
import time
import urllib.parse

app = Flask(__name__)

# --- Mock Data & Constants ---

POSES_DB = {
    "Joyful": [
        {"title": "The Sunshine Spin", "desc": "Spin slowly with arms wide open, head tilted back slightly laughing, wearing a flowy modest dress.", "tips": "Let your dress flow and catch the light!", "tags": ["Solo", "Sun", "Spin"]},
        {"title": "Candid Laughter", "desc": "Hand covering mouth gently while laughing at a friend's joke, sitting in a garden cafe.", "tips": "Natural smiles are best.", "tags": ["Friends", "Close-up", "Laugh"]},
        {"title": "Jump for Joy", "desc": "Mid-air jump with knees tucked, hands reaching for the sky, wearing jeans and a colorful top.", "tips": "Use a fast shutter speed to freeze the motion.", "tags": ["Energy", "Fun", "Jump"]}
    ],
    "Serene": [
        {"title": "Book & Tea", "desc": "Sitting cross-legged on a cozy rug, holding a favorite book and looking out a rainy window.", "tips": "Soft lighting is key for this mood.", "tags": ["Relaxation", "Cozy", "Reading"]},
        {"title": "Nature Walk", "desc": "Walking away from camera on a forest path, looking back over shoulder with a soft smile, wearing a warm coat.", "tips": "Great for forest paths with dappled light.", "tags": ["Nature", "Walk", "Forest"]},
        {"title": "Meditative Calm", "desc": "Eyes closed, hands resting on knees, sitting peacefully by a calm lake at sunrise.", "tips": "Breathe deeply and look relaxed.", "tags": ["Wellness", "Peace", "Sunrise"]}
    ],
    "Confident": [
        {"title": "The Power Stance", "desc": "Standing tall with feet shoulder-width apart, hands on hips, chin up, wearing a sharp blazer.", "tips": "Shoulders back to show strength!", "tags": ["Empowerment", "Bold", "Business"]},
        {"title": "City Stroll", "desc": "Walking confidently down a city street, looking slightly away, hair flowing in the wind.", "tips": "Walk with purpose and rhythm.", "tags": ["Street Style", "Motion", "City"]},
        {"title": "Arms Crossed", "desc": "Casual lean against a brick wall, arms loosely crossed, confident direct gaze, wearing a denim jacket.", "tips": "Relax your jaw and smile with your eyes.", "tags": ["Casual", "Cool", "Denim"]}
    ],
    "Playful": [
        {"title": "Peace Sign Fun", "desc": "Winking at the camera giving a peace sign, joyful expression, colorful background.", "tips": "Don't take it too seriously!", "tags": ["Fun", "Selfie"]},
        {"title": "Blowing Bubbles", "desc": "Blowing bubbles towards the camera, focus on the bubbles and the smile.", "tips": "Capture the reflections in the bubbles.", "tags": ["Whimsical", "Outdoor"]},
        {"title": "Hide and Seek", "desc": "Peeking playfully from behind a tree or colorful wall.", "tips": "Use the object to frame your face.", "tags": ["Cute", "Peeking"]}
    ],
    "Dreamy": [
        {"title": "Cloud Watching", "desc": "Lying on grass looking up at the sky, soft focus, surrounded by flowers.", "tips": "Shot from above.", "tags": ["Clouds", "Sky"]},
        {"title": "Twinkle Lights", "desc": "Wrapped in fairy lights, soft glow on face, magical atmosphere.", "tips": "Use bokeh effect.", "tags": ["Lights", "Night"]},
        {"title": "Flower Crown", "desc": "Wearing a flower crown, looking dreamily into the distance, soft pastel colors.", "tips": "Golden hour works best.", "tags": ["Flowers", "Portrait"]}
    ],
    "Love": [
        {"title": "Heart Hands", "desc": "Making a heart shape with hands against the sky or a sunset.", "tips": "Silhouette looks great here.", "tags": ["Symbol", "Sunset"]},
        {"title": "Bestie Hug", "desc": "Tight hug with a best friend, cheek to cheek, genuine smiles.", "tips": "Squeeze tight!", "tags": ["Friends", "Hug"]},
        {"title": "Pet Cuddle", "desc": "Hugging a puppy or kitten close to face, pure joy.", "tips": "Get on their eye level.", "tags": ["Pets", "Cute"]}
    ]
}

MUSIC_DB = {
    "Joyful": [
        {"title": "Happy Vibes", "artist": "Sunny Sounds", "desc": "Upbeat pop to lift your spirits."},
        {"title": "Morning Coffee", "artist": "Acoustic Life", "desc": "Cheerful acoustic guitar."}
    ],
    "Serene": [
        {"title": "Ocean Breeze", "artist": "Calm Waves", "desc": "Soft ambient pads and piano."},
        {"title": "Forest Rain", "artist": "Nature Melodies", "desc": "Gentle rain sounds with flute."}
    ],
    "Confident": [
        {"title": "Runway Ready", "artist": "Bold Beats", "desc": "Driving bass and electric energy."},
        {"title": "Rise Up", "artist": "Anthem Makers", "desc": "Building orchestral percussion."}
    ],
    "Playful": [
        {"title": "Funky Town", "artist": "Groove Masters", "desc": "Funky bass and brass."},
        {"title": "Sugar Pop", "artist": "Candy Sweets", "desc": "Fast-paced bubbly synth pop."}
    ],
    "Dreamy": [
        {"title": "Starlight", "artist": "Cosmic Drift", "desc": "Ethereal vocals and reverb."},
        {"title": "Lullaby", "artist": "Sleepy Time", "desc": "Slow celesta and strings."}
    ],
     "Love": [
        {"title": "Sweetheart", "artist": "Romance Radio", "desc": "Gentle acoustic ballad."},
        {"title": "Best Friends", "artist": "Duo Harmony", "desc": "Upbeat folk duet."}
    ]
}

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_poses():
    data = request.json
    tone = data.get('tone', 'Joyful')
    
    # Simulate AI processing latency to make it feel "heavy"
    time.sleep(1.0) 
    
    results = POSES_DB.get(tone, [])
    if not results:
        # Fallback
        all_poses = [p for sublist in POSES_DB.values() for p in sublist]
        results = random.sample(all_poses, min(3, len(all_poses)))
    else:
        results = random.sample(results, min(len(results), 3))

    # Add AI-generated image URL using Pollinations.ai
    for pose in results:
        pose['id'] = str(random.randint(1000, 9999))
        
        # Construct a safe, detailed prompt for the AI
        # We ensure safety keywords are always included
        base_prompt = f"photorealistic, 8k, women or girls, modest fashion, fully clothed, {pose['desc']}, {tone} mood, happy, joyful, safe content, no revealing clothes, high quality, soft lighting"
        encoded_prompt = urllib.parse.quote(base_prompt)
        
        # Pollinations.ai generates images on the fly based on the URL
        # Adding a random seed ensures we get different images if we request the same pose again if we wanted, 
        # but here the prompt is specific enough. Adding a timestamp or rand seed helps cache busting.
        seed = random.randint(1, 1000)
        pose['image_url'] = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=400&height=600&nologo=true"
        
        pose['affirmation'] = "You look radiant!"

    return jsonify({
        "success": True,
        "poses": results,
        "message": f"Generated {len(results)} poses for a {tone} vibe."
    })

@app.route('/api/music', methods=['POST'])
def recommend_music():
    data = request.json
    tone = data.get('tone', 'Joyful')
    tracks = MUSIC_DB.get(tone, MUSIC_DB['Joyful'])
    return jsonify({"tracks": tracks})

@app.route('/api/analyze_photo', methods=['POST'])
def analyze_photo():
    # Mock analysis
    time.sleep(2)
    return jsonify({
        "detected_mood": random.choice(["Joyful", "Serene", "Confident", "Playful", "Dreamy", "Love"]),
        "suggestion": "Your smile is contagious! We recommend this mood."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
