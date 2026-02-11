from flask import Flask, render_template, jsonify, request
import random
import time

app = Flask(__name__)

# --- Mock Data & Constants ---

POSES_DB = {
    "Joyful": [
        {"title": "The Sunshine Spin", "desc": "Spin slowly with arms wide open, head tilted back slightly laughing.", "tips": "Let your dress flow!", "tags": ["Solo", "Sun"]},
        {"title": "Candid Laughter", "desc": "Hand covering mouth gently while laughing at a friend's joke.", "tips": "Natural smiles are best.", "tags": ["Friends", "Close-up"]},
        {"title": "Jump for Joy", "desc": "Mid-air jump with knees tucked, hands reaching for the sky.", "tips": "Use a fast shutter speed.", "tags": ["Energy", "Fun"]}
    ],
    "Serene": [
        {"title": "Book & Tea", "desc": "Sitting cross-legged, holding a favorite book and looking out a window.", "tips": "Soft lighting is key.", "tags": ["Relaxation", "Cozy"]},
        {"title": "Nature Walk", "desc": "Walking away from camera, looking back over shoulder with a soft smile.", "tips": "Great for forest paths.", "tags": ["Nature", "Walk"]},
        {"title": "Meditative Calm", "desc": "Eyes closed, hands resting on knees, sitting peacefully.", "tips": "Breathe deeply.", "tags": ["Wellness", "Peace"]}
    ],
    "Confident": [
        {"title": "The Power Stance", "desc": "Feet shoulder-width apart, hands on hips, chin up.", "tips": "Shoulders back!", "tags": ["Empowerment", "Bold"]},
        {"title": "Walking Strut", "desc": "Walking towards camera, looking slightly away, hair flowing.", "tips": "Walk with purpose.", "tags": ["Street Style", "Motion"]},
        {"title": "Arms Crossed", "desc": "Casual lean against a wall, arms loosely crossed, confident gaze.", "tips": "Relax your jaw.", "tags": ["Casual", "Cool"]}
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
    ]
}

DEFAULT_POSES = [
    {"title": "Classic Smile", "desc": "Simple, genuine smile looking straight at the camera.", "tips": "Think of a happy memory.", "tags": ["Classic"]}
]

DEFAULT_MUSIC = [
    {"title": "Daily Inspiration", "artist": "Life Tunes", "desc": "Background music for any moment."}
]

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_poses():
    data = request.json
    tone = data.get('tone', 'Joyful')
    scenario = data.get('scenario', 'General')
    
    # Simulate AI processing latency
    time.sleep(1.5) 
    
    # Select poses based on Tone (mock logic)
    # In a real app, this would query an AI model or a vector DB
    results = POSES_DB.get(tone, [])
    if not results:
        # Fallback if tone not found, mix random ones
        all_poses = [p for sublist in POSES_DB.values() for p in sublist]
        results = random.sample(all_poses, min(3, len(all_poses)))
    else:
        # Add some variation
        results = random.sample(results, min(len(results), 3))

    # Add AI-generated style metadata
    for pose in results:
        pose['id'] = str(random.randint(1000, 9999))
        pose['image_url'] = f"https://picsum.photos/seed/{pose['id']}/400/600" # Placeholder for AI image
        pose['affirmation'] = "You look radiant!"

    return jsonify({
        "success": True,
        "poses": results,
        "message": f"Generated {len(results)} poses for a {tone} vibe in {scenario}."
    })

@app.route('/api/music', methods=['POST'])
def recommend_music():
    data = request.json
    tone = data.get('tone', 'Joyful')
    tracks = MUSIC_DB.get(tone, DEFAULT_MUSIC)
    return jsonify({"tracks": tracks})

@app.route('/api/analyze_photo', methods=['POST'])
def analyze_photo():
    # Mock analysis
    time.sleep(2)
    return jsonify({
        "detected_mood": random.choice(["Joyful", "Serene", "Confident", "Playful"]),
        "suggestion": "Your smile is contagious! We recommend 'Joyful' poses."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
