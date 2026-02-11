// State
let currentUser = "Guest";
let currentMood = "";
let favorites = [];

// DOM Elements
const views = {
    home: document.getElementById('home-view'),
    results: document.getElementById('results-view'),
    favorites: document.getElementById('favorites-view')
};
const navItems = {
    home: document.getElementById('nav-home'),
    create: document.getElementById('nav-create'),
    faves: document.getElementById('nav-faves'),
};

// --- Navigation ---
function startApp() {
    const inputName = document.getElementById('username').value;
    if (inputName) currentUser = inputName;
    document.getElementById('user-display-name').innerText = currentUser;

    document.getElementById('onboarding').classList.add('hidden');
    document.getElementById('app-container').classList.remove('hidden');
    document.getElementById('app-container').classList.add('fade-in');
}

function switchTab(viewId) {
    // Hide all views
    Object.values(views).forEach(el => el.classList.add('hidden'));
    // Show target view
    const target = document.getElementById(viewId);
    target.classList.remove('hidden');
    target.classList.add('fade-in');

    // Update nav state
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

    if (viewId === 'home-view') document.getElementById('nav-home').classList.add('active');
    if (viewId === 'results-view') document.getElementById('nav-create').classList.add('active');
    if (viewId === 'favorites-view') document.getElementById('nav-faves').classList.add('active');

    // Refresh favorites if opening that tab
    if (viewId === 'favorites-view') renderFavorites();
}

function goHome() {
    switchTab('home-view');
}

// --- Features ---

async function selectMood(mood) {
    currentMood = mood;
    switchTab('results-view');
    await generatePoses(mood);
}

async function analyzePhoto(input) {
    if (input.files && input.files[0]) {
        const resultDiv = document.getElementById('analysis-result');
        resultDiv.classList.remove('hidden');
        resultDiv.innerHTML = '<p><i class="fa-solid fa-spinner fa-spin"></i> Analyzing magic...</p>';

        try {
            // Simulate API call
            const response = await fetch('/api/analyze_photo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            const data = await response.json();

            resultDiv.innerHTML = `
                <div style="background: #E0F7FA; padding: 10px; border-radius: 10px; margin-top: 10px; border: 1px solid #B2EBF2;">
                    <strong>Mood Match: ${data.detected_mood}</strong>
                    <p>${data.suggestion}</p>
                    <button class="btn-primary" style="margin-top:5px; padding: 0.5rem;" onclick="selectMood('${data.detected_mood}')">Try This!</button>
                </div>
            `;
        } catch (e) {
            console.error(e);
            resultDiv.innerHTML = '<p>Oops, magic gathering failed. Try again!</p>';
        }
    }
}

async function generatePoses(mood) {
    const loader = document.getElementById('loader');
    const carousel = document.getElementById('pose-carousel');
    const musicSection = document.getElementById('music-suggestions');

    loader.classList.remove('hidden');
    carousel.classList.add('hidden');
    musicSection.classList.add('hidden');
    carousel.innerHTML = '';

    try {
        // Fetch Poses
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tone: mood })
        });
        const data = await response.json();

        // Fetch Music
        const musicResp = await fetch('/api/music', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tone: mood })
        });
        const musicData = await musicResp.json();

        loader.classList.add('hidden');
        carousel.classList.remove('hidden');
        musicSection.classList.remove('hidden');

        // Render Poses
        if (data.poses && data.poses.length > 0) {
            data.poses.forEach(pose => {
                const card = document.createElement('div');
                card.className = 'pose-card';
                card.innerHTML = `
                    <div style="position: relative;">
                        <img src="${pose.image_url}" class="pose-img-placeholder" alt="${pose.title}">
                        <div style="position: absolute; bottom: 10px; right: 10px; background: white; padding: 5px 10px; border-radius: 10px; font-size: 0.8rem; font-weight: bold;">
                             ✨ ${pose.affirmation || 'You glow!'}
                        </div>
                    </div>
                    <div class="pose-details">
                        <h3 class="pose-title">${pose.title}</h3>
                        <p class="pose-desc">${pose.desc}</p>
                        <div class="pose-tips"><i class="fa-regular fa-lightbulb"></i> ${pose.tips}</div>
                        <div class="pose-actions">
                            <button class="action-btn" onclick="sharePose('${pose.title}')"><i class="fa-solid fa-share-nodes"></i></button>
                            <button class="action-btn" onclick="toggleFavorite(this, '${pose.title}')"><i class="fa-solid fa-heart"></i></button>
                        </div>
                    </div>
                `;
                carousel.appendChild(card);
            });
        }

        // Render Music
        const musicList = document.getElementById('music-list');
        musicList.innerHTML = '';
        if (musicData.tracks) {
            musicData.tracks.forEach(track => {
                const row = document.createElement('div');
                row.className = 'music-card';
                row.innerHTML = `
                    <div class="music-icon"><i class="fa-solid fa-play"></i></div>
                    <div>
                        <h4 style="font-size: 0.9rem;">${track.title}</h4>
                        <p style="font-size: 0.7rem; color: gray;">${track.artist}</p>
                    </div>
                `;
                musicList.appendChild(row);
            });
        }

    } catch (e) {
        console.error(e);
        loader.innerHTML = '<p>The pixies dropped the connection. Try again!</p>';
    }
}

// --- Favorites Mock Logic ---
function toggleFavorite(btn, title) {
    btn.classList.toggle('active');
    // In a real app, save to backend/localstorage
    if (btn.classList.contains('active')) {
        // Add confettis effect (placeholder)
        if (!favorites.includes(title)) favorites.push(title);
    } else {
        favorites = favorites.filter(t => t !== title);
    }
}

function renderFavorites() {
    const grid = document.getElementById('favorites-grid');
    if (favorites.length === 0) {
        grid.innerHTML = '<p class="empty-state">No favorites yet! Tap the heart on poses you love.</p>';
        return;
    }
    grid.innerHTML = favorites.map(f => `
        <div class="pose-card">
            <div class="pose-details">
                <h3>${f}</h3>
                <p>Saved to your collection ✨</p>
            </div>
        </div>
    `).join('');
}

function sharePose(title) {
    alert(`Sharing "${title}" to Instagram... (Prototype Mock)`);
}
