# Stuverse AI — Your Personal AI Teacher (v3.0 Cosmos Edition)
# Run: streamlit run stuverse.py

import os
import json
import time
import uuid
import random
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
from google import genai
from google.genai import types

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Stuverse AI - Your Personal AI Teacher",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Generate Starfield (deterministic seed for stability) ----------
rng = random.Random(42)
stars_s = ", ".join(f"{rng.randint(1,2500)}px {rng.randint(1,2500)}px rgba(255,255,255,{round(rng.uniform(0.4,1.0),2)})" for _ in range(260))
stars_m = ", ".join(f"{rng.randint(1,2500)}px {rng.randint(1,2500)}px rgba(196,181,253,{round(rng.uniform(0.5,1.0),2)})" for _ in range(130))
stars_l = ", ".join(f"{rng.randint(1,2500)}px {rng.randint(1,2500)}px rgba(56,189,248,{round(rng.uniform(0.6,1.0),2)})" for _ in range(60))

# ---------- Cosmic CSS & 3D Styling ----------
st.markdown(f"""
<style>
/* ===== GLOBAL COSMOS BACKGROUND ===== */
[data-testid="stApp"] {{
    background: radial-gradient(ellipse at 15% 75%, rgba(109, 40, 217, 0.18) 0%, transparent 45%),
                radial-gradient(ellipse at 85% 25%, rgba(14, 165, 233, 0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(15, 10, 30, 0.95) 0%, #050210 100%) !important;
    background-attachment: fixed;
    color: #f1f5f9;
    overflow-x: hidden;
}}

/* Smooth scroll */
html {{
    scroll-behavior: smooth;
}}

/* Sidebar cosmic styling */
[data-testid="stSidebar"] {{
    background: rgba(8, 4, 22, 0.92) !important;
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
}}

/* Star layers */
#cosmic-stars-1, #cosmic-stars-2, #cosmic-stars-3 {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
}}
#cosmic-stars-1 {{
    width: 1px; height: 1px;
    box-shadow: {stars_s};
    animation: starDrift 140s linear infinite;
}}
#cosmic-stars-2 {{
    width: 2px; height: 2px;
    box-shadow: {stars_m};
    animation: starDrift 90s linear infinite;
}}
#cosmic-stars-3 {{
    width: 3px; height: 3px;
    border-radius: 50%;
    box-shadow: {stars_l};
    animation: starDrift 60s linear infinite, starTwinkle 3.5s ease-in-out infinite alternate;
}}

@keyframes starDrift {{
    from {{ transform: translateY(0px); }}
    to {{ transform: translateY(-2500px); }}
}}
@keyframes starTwinkle {{
    0% {{ opacity: 0.5; }}
    50% {{ opacity: 1; }}
    100% {{ opacity: 0.6; }}
}}

/* ===== 3D BLACK HOLE ANIMATION ===== */
.blackhole-container {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.8rem 1rem 1.2rem;
    margin-bottom: 1.2rem;
    perspective: 1000px;
}}
.blackhole-core {{
    position: relative;
    width: 170px;
    height: 170px;
    margin: 0 auto 1.2rem;
    transform-style: preserve-3d;
    transition: transform 0.4s ease-out;
}}
.blackhole-core:hover {{
    transform: scale(1.06) rotateX(10deg);
}}
.blackhole-event-horizon {{
    position: absolute;
    width: 68px; height: 68px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: radial-gradient(circle, #000000 65%, rgba(0,0,0,0.95) 85%, transparent 100%);
    box-shadow: 0 0 45px 20px #000000,
                0 0 90px 35px rgba(139, 92, 246, 0.35),
                0 0 130px 60px rgba(56, 189, 248, 0.15);
    z-index: 4;
}}
.blackhole-accretion {{
    position: absolute;
    width: 160px; height: 160px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: conic-gradient(
        from 0deg,
        rgba(236, 72, 153, 0.0) 0%,
        rgba(236, 72, 153, 0.85) 15%,
        rgba(168, 85, 247, 0.9) 35%,
        rgba(56, 189, 248, 0.85) 55%,
        rgba(139, 92, 246, 0.2) 75%,
        rgba(236, 72, 153, 0.0) 100%
    );
    animation: bhRotate 7s linear infinite;
    z-index: 2;
    filter: blur(2.5px);
}}
.blackhole-glow {{
    position: absolute;
    width: 170px; height: 170px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: radial-gradient(circle, transparent 30%, rgba(168,85,247,0.15) 55%, transparent 75%);
    box-shadow: 0 0 70px 25px rgba(168, 85, 247, 0.2),
                0 0 140px 70px rgba(56, 189, 248, 0.12);
    animation: bhPulse 3.5s ease-in-out infinite alternate;
    z-index: 1;
}}
.blackhole-ring {{
    position: absolute;
    width: 145px; height: 145px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotateX(75deg);
    border-radius: 50%;
    border: 2px solid rgba(192, 132, 252, 0.45);
    box-shadow: 0 0 20px rgba(192, 132, 252, 0.35);
    animation: bhRotate 12s linear infinite reverse;
    z-index: 3;
}}
.blackhole-ring-2 {{
    position: absolute;
    width: 125px; height: 125px;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotateX(75deg) rotateZ(55deg);
    border-radius: 50%;
    border: 1.5px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
    animation: bhRotate 16s linear infinite;
    z-index: 3;
}}

@keyframes bhRotate {{
    from {{ transform: translate(-50%, -50%) rotate(0deg); }}
    to {{ transform: translate(-50%, -50%) rotate(360deg); }}
}}
@keyframes bhPulse {{
    0% {{ opacity: 0.65; transform: translate(-50%, -50%) scale(0.98); }}
    100% {{ opacity: 1; transform: translate(-50%, -50%) scale(1.08); }}
}}

.cosmos-title {{
    font-size: 2.7rem;
    font-weight: 900;
    background: linear-gradient(135deg, #f472b6 0%, #c084fc 35%, #818cf8 70%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: -0.5px;
    margin: 0;
    text-shadow: 0 0 30px rgba(192, 132, 252, 0.3);
}}
.cosmos-subtitle {{
    color: #c7d2fe;
    font-size: 1.05rem;
    text-align: center;
    margin-top: 0.3rem;
    margin-bottom: 0.8rem;
    opacity: 0.9;
    letter-spacing: 0.3px;
}}

/* ===== 3D FEATURE PILLS ===== */
.feature-pill {{
    display: inline-block;
    background: rgba(139, 92, 246, 0.12);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 24px;
    padding: 0.45rem 1.1rem;
    margin: 0.25rem;
    font-size: 0.88rem;
    color: #e0e7ff;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
    backdrop-filter: blur(8px);
}}
.feature-pill:hover {{
    background: rgba(139, 92, 246, 0.28);
    border-color: rgba(192, 132, 252, 0.65);
    transform: translateY(-3px) scale(1.04);
    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.35);
}}

/* ===== 3D BUTTON & CARD EFFECTS ===== */
.stButton > button {{
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border-radius: 10px !important;
    perspective: 600px;
}}
.stButton > button:hover {{
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3) !important;
    border-color: rgba(192, 132, 252, 0.5) !important;
}}
.stButton > button:active {{
    transform: translateY(0px) scale(0.98) !important;
}}

/* Chat messages 3D card lift & Alignment */
[data-testid="stChatMessage"] {{
    animation: fadeSlideUp 0.35s ease-out;
    border-radius: 18px !important;
    transition: all 0.3s ease;
    margin-bottom: 0.9rem !important;
    display: flex !important;
}}

/* SENDER / USER MESSAGE (ALIGNED TO RIGHT) */
[data-testid="stChatMessage"]:has(.sender-msg-marker),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
    flex-direction: row-reverse !important;
    margin-left: auto !important;
    margin-right: 0 !important;
    width: fit-content !important;
    max-width: 82% !important;
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.45) 0%, rgba(99, 102, 241, 0.38) 100%) !important;
    border: 1px solid rgba(168, 85, 247, 0.55) !important;
    border-radius: 20px 20px 4px 20px !important;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.28) !important;
    backdrop-filter: blur(12px);
}}
[data-testid="stChatMessage"]:has(.sender-msg-marker):hover,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]):hover {{
    border-color: rgba(216, 180, 254, 0.7) !important;
    box-shadow: 0 8px 28px rgba(168, 85, 247, 0.4) !important;
    transform: translateY(-2px);
}}
[data-testid="stChatMessage"]:has(.sender-msg-marker) [data-testid="stChatMessageAvatar"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageAvatar"] {{
    margin-left: 12px !important;
    margin-right: 0 !important;
}}
[data-testid="stChatMessage"]:has(.sender-msg-marker) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {{
    text-align: right !important;
}}
[data-testid="stChatMessage"]:has(.sender-msg-marker) p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p {{
    text-align: right !important;
}}

/* RECEIVER / AI ANSWER (ALIGNED TO LEFT) */
[data-testid="stChatMessage"]:has(.receiver-msg-marker),
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {{
    flex-direction: row !important;
    margin-right: auto !important;
    margin-left: 0 !important;
    width: fit-content !important;
    min-width: 55% !important;
    max-width: 88% !important;
    background: rgba(14, 9, 32, 0.85) !important;
    border: 1px solid rgba(56, 189, 248, 0.35) !important;
    border-radius: 20px 20px 20px 4px !important;
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.15) !important;
    backdrop-filter: blur(12px);
}}
[data-testid="stChatMessage"]:has(.receiver-msg-marker):hover,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]):hover {{
    border-color: rgba(56, 189, 248, 0.6) !important;
    box-shadow: 0 8px 28px rgba(56, 189, 248, 0.25) !important;
    transform: translateY(-2px);
}}
[data-testid="stChatMessage"]:has(.receiver-msg-marker) [data-testid="stChatMessageAvatar"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageAvatar"] {{
    margin-right: 12px !important;
    margin-left: 0 !important;
}}
[data-testid="stChatMessage"]:has(.receiver-msg-marker) [data-testid="stChatMessageContent"],
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {{
    text-align: left !important;
}}

/* Hidden zero-height layout markers */
.sender-msg-marker, .receiver-msg-marker {{
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}}

/* Chat input glow animation */
[data-testid="stChatInput"] {{
    animation: glowPulse 3.5s ease-in-out infinite;
    border-radius: 14px !important;
}}
[data-testid="stChatInput"] > div {{
    border-color: rgba(139, 92, 246, 0.3) !important;
    background: rgba(10, 6, 24, 0.8) !important;
}}

/* Expander 3D styling */
[data-testid="stExpander"] {{
    background: rgba(15, 10, 32, 0.5) !important;
    border: 1px solid rgba(139, 92, 246, 0.2) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
}}
[data-testid="stExpander"]:hover {{
    border-color: rgba(168, 85, 247, 0.4) !important;
    box-shadow: 0 8px 25px rgba(139, 92, 246, 0.18);
}}

/* Shooting stars */
.shooting-star {{
    position: fixed;
    width: 120px;
    height: 1px;
    background: linear-gradient(90deg, rgba(236,72,153,0.9), rgba(56,189,248,0.9), transparent);
    animation: shootingStar 4s ease-in infinite;
    pointer-events: none;
    z-index: 0;
    top: 15%;
    left: -120px;
    transform: rotate(-35deg);
}}
.shooting-star:nth-child(2) {{
    animation-delay: 5.5s;
    top: 35%;
    transform: rotate(-25deg);
}}
.shooting-star:nth-child(3) {{
    animation-delay: 9s;
    top: 55%;
    transform: rotate(-40deg);
}}

@keyframes shootingStar {{
    0% {{ left: -120px; opacity: 0; }}
    5% {{ opacity: 1; }}
    50% {{ opacity: 1; }}
    100% {{ left: 110%; opacity: 0; }}
}}

@keyframes fadeSlideUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes glowPulse {{
    0%, 100% {{ box-shadow: 0 0 8px rgba(139,92,246,0.25); }}
    50% {{ box-shadow: 0 0 25px rgba(168,85,247,0.45); }}
}}

/* Cosmic Scrollbar */
::-webkit-scrollbar {{
    width: 8px;
}}
::-webkit-scrollbar-track {{
    background: rgba(5, 2, 16, 0.8);
}}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, #ec4899, #8b5cf6, #38bdf8);
    border-radius: 4px;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
}}
::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient(180deg, #f472b6, #a855f7, #60a5fa);
}}
</style>

<!-- Starfield layers -->
<div id="cosmic-stars-1"></div>
<div id="cosmic-stars-2"></div>
<div id="cosmic-stars-3"></div>

<!-- Shooting stars -->
<div class="shooting-star"></div>
<div class="shooting-star"></div>
<div class="shooting-star"></div>
""", unsafe_allow_html=True)

# ---------- Interactive Cursor & Scroll Animation Component ----------
components.html("""
<script>
(function() {
    try {
        const parentDoc = window.parent.document;
        if (!parentDoc || parentDoc.getElementById('cosmic-canvas-overlay')) return;

        // 1. Scroll progress bar indicator at top
        const progressBar = parentDoc.createElement('div');
        progressBar.id = 'cosmic-scroll-progress';
        progressBar.style.position = 'fixed';
        progressBar.style.top = '0';
        progressBar.style.left = '0';
        progressBar.style.height = '3px';
        progressBar.style.width = '0%';
        progressBar.style.background = 'linear-gradient(90deg, #ec4899, #a855f7, #38bdf8)';
        progressBar.style.boxShadow = '0 0 10px rgba(168, 85, 247, 0.8), 0 0 20px rgba(56, 189, 248, 0.5)';
        progressBar.style.zIndex = '9999999';
        progressBar.style.transition = 'width 0.1s ease-out';
        progressBar.style.pointerEvents = 'none';
        parentDoc.body.appendChild(progressBar);

        // 2. Fullscreen canvas for cursor trail & scroll particle bursts
        const canvas = parentDoc.createElement('canvas');
        canvas.id = 'cosmic-canvas-overlay';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '999999';
        parentDoc.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        let width = canvas.width = window.parent.innerWidth;
        let height = canvas.height = window.parent.innerHeight;

        window.parent.addEventListener('resize', () => {
            width = canvas.width = window.parent.innerWidth;
            height = canvas.height = window.parent.innerHeight;
        });

        const particles = [];

        function addParticle(x, y, speedMult, count) {
            for (let i = 0; i < count; i++) {
                if (particles.length > 90) particles.shift();
                const isCyan = Math.random() > 0.5;
                const color = isCyan ? 'rgba(56, 189, 248,' : 'rgba(192, 132, 252,';
                particles.push({
                    x: x + (Math.random() - 0.5) * 10,
                    y: y + (Math.random() - 0.5) * 10,
                    vx: (Math.random() - 0.5) * 2 * speedMult,
                    vy: (Math.random() - 0.5) * 2 * speedMult - 0.4,
                    size: Math.random() * 2.8 + 1,
                    color: color,
                    life: 1.0,
                    decay: Math.random() * 0.025 + 0.015
                });
            }
        }

        let mouseX = -100, mouseY = -100;
        parentDoc.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            addParticle(mouseX, mouseY, 1, 2);
        });

        // Scroll event: update progress bar and spawn cosmic sparkle particles
        window.parent.addEventListener('scroll', () => {
            const scrollTop = window.parent.scrollY || parentDoc.documentElement.scrollTop;
            const docHeight = parentDoc.documentElement.scrollHeight - window.parent.innerHeight;
            if (docHeight > 0) {
                const pct = Math.min(100, Math.max(0, (scrollTop / docHeight) * 100));
                progressBar.style.width = pct + '%';
            }
            if (mouseX > 0 && mouseY > 0) {
                addParticle(mouseX, mouseY, 2.2, 3);
            }
        }, { passive: true });

        // Animation loop
        function render() {
            ctx.clearRect(0, 0, width, height);
            for (let i = particles.length - 1; i >= 0; i--) {
                const p = particles[i];
                p.x += p.vx;
                p.y += p.vy;
                p.life -= p.decay;
                if (p.life <= 0) {
                    particles.splice(i, 1);
                    continue;
                }
                ctx.save();
                ctx.fillStyle = p.color + (p.life * 0.9) + ')';
                ctx.shadowBlur = 8;
                ctx.shadowColor = p.color + '1)';
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
            requestAnimationFrame(render);
        }
        render();
    } catch(err) {
        // Silently continue if iframe security restricts parent access
    }
})();
</script>
""", height=0)

# ---------- Constants & Config ----------
MODEL_NAME = "gemini-3.8-flash"
DAILY_LIMIT = 15
HISTORY_FILE = "chat_history.json"

LEVELS = [
    "College",
    "Class 11-12",
    "Class 9-10",
    "Class 6-8",
    "Competitive Exams (JEE / NEET / UPSC / CUET)",
]
SUBJECTS = [
    "All subjects",
    "Maths",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer / Programming",
    "English",
    "History & Civics",
    "General Knowledge",
]

SUGGESTIONS = {
    "📐 Quadratic formula": "What is the quadratic formula and how do you solve equations with it step by step?",
    "⚛️ Newton's laws": "Explain Newton's three laws of motion with simple, real-life examples.",
    "💻 Python loops": "How do for loops and while loops work in Python? Give a practical example.",
    "🌿 Photosynthesis": "Explain the process of photosynthesis step by step in simple language.",
}

# ---------- API Key ----------
def get_gemini_client():
    api_key = None
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found! Please add it in Streamlit Cloud Secrets or in `.streamlit/secrets.toml`.")
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

# ---------- Chat Persistence ----------
def load_all_chats():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "sessions" in data:
                    return data["sessions"]
        except Exception:
            pass
    return {}

def save_all_chats(chats):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"sessions": chats}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_all_chats()

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in st.session_state.all_chats:
    if st.session_state.all_chats:
        st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[-1]
    else:
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "id": new_id,
            "title": "New Chat",
            "created_at": datetime.now().strftime("%d %b, %I:%M %p"),
            "messages": [],
            "level": "College",
            "subject": "All subjects",
        }
        st.session_state.current_chat_id = new_id
        save_all_chats(st.session_state.all_chats)

if "daily_count" not in st.session_state:
    st.session_state.daily_count = 0

current_id = st.session_state.current_chat_id
current_chat = st.session_state.all_chats.get(current_id, {
    "id": current_id,
    "title": "New Chat",
    "created_at": datetime.now().strftime("%d %b, %I:%M %p"),
    "messages": [],
    "level": "College",
    "subject": "All subjects",
})

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### ✨ **Stuverse AI**")
    st.caption("Your Personal AI Study Companion")

    if st.button("➕ **Start New Chat**", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "id": new_id,
            "title": "New Chat",
            "created_at": datetime.now().strftime("%d %b, %I:%M %p"),
            "messages": [],
            "level": current_chat.get("level", "College"),
            "subject": current_chat.get("subject", "All subjects"),
        }
        st.session_state.current_chat_id = new_id
        save_all_chats(st.session_state.all_chats)
        st.rerun()

    st.divider()
    st.markdown("#### ⚙️ Settings")

    current_level = current_chat.get("level", "College")
    level = st.selectbox(
        "Your level",
        LEVELS,
        index=LEVELS.index(current_level) if current_level in LEVELS else 0,
        key=f"level_sel_{current_id}",
    )

    current_subj = current_chat.get("subject", "All subjects")
    subject = st.selectbox(
        "Subject",
        SUBJECTS,
        index=SUBJECTS.index(current_subj) if current_subj in SUBJECTS else 0,
        key=f"subj_sel_{current_id}",
    )

    if current_chat.get("level") != level or current_chat.get("subject") != subject:
        current_chat["level"] = level
        current_chat["subject"] = subject
        st.session_state.all_chats[current_id] = current_chat
        save_all_chats(st.session_state.all_chats)

    st.divider()
    st.markdown("#### 📜 Chat History")
    chat_ids = list(st.session_state.all_chats.keys())
    chat_ids.reverse()

    for cid in chat_ids:
        cinfo = st.session_state.all_chats[cid]
        col_btn, col_del = st.columns([0.82, 0.18])
        is_active = (cid == current_id)
        btn_label = f"{'👉 ' if is_active else '💬 '}{cinfo.get('title', 'Chat')}"
        if col_btn.button(btn_label, key=f"hist_btn_{cid}", use_container_width=True,
            type="primary" if is_active else "secondary"):
            st.session_state.current_chat_id = cid
            st.rerun()
        if col_del.button("🗑️", key=f"del_btn_{cid}", help="Delete this chat"):
            del st.session_state.all_chats[cid]
            if not st.session_state.all_chats:
                new_id = str(uuid.uuid4())
                st.session_state.all_chats[new_id] = {
                    "id": new_id,
                    "title": "New Chat",
                    "created_at": datetime.now().strftime("%d %b, %I:%M %p"),
                    "messages": [],
                    "level": level,
                    "subject": subject,
                }
                st.session_state.current_chat_id = new_id
            else:
                st.session_state.current_chat_id = list(st.session_state.all_chats.keys())[-1]
            save_all_chats(st.session_state.all_chats)
            st.rerun()

    st.divider()

    used = st.session_state.daily_count
    remaining = DAILY_LIMIT - used
    st.caption(f"📊 **{used}/{DAILY_LIMIT}** questions used")
    st.progress(min(used / DAILY_LIMIT, 1.0))
    if 0 < remaining <= 3:
        st.warning(f"Only {remaining} questions left for today!")

    if current_chat.get("messages"):
        export_text = f"# 🎓 Stuverse AI Study Notes\n"
        export_text += f"**Topic**: {current_chat.get('title')}\n"
        export_text += f"**Date**: {current_chat.get('created_at')}\n"
        export_text += f"**Level**: {current_chat.get('level')} | **Subject**: {current_chat.get('subject')}\n\n---\n\n"
        for m in current_chat["messages"]:
            speaker = "🧑‍🎓 Student" if m["role"] == "user" else "🤖 Stuverse AI"
            file_info = f" *(Attached: {m['file_name']})*" if m.get("file_name") else ""
            export_text += f"### {speaker}{file_info}:\n{m['text']}\n\n"
        st.download_button(
            "📥 **Download Notes (.md)**",
            data=export_text,
            file_name=f"Stuverse_Notes_{current_id[:6]}.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ---------- System Prompt (English by default, Hinglish if user speaks Hinglish) ----------
subject_text = "any subject" if subject == "All subjects" else subject
TEACHER_PROMPT = f"""\
You are Stuverse AI, a friendly, encouraging, and highly knowledgeable personal AI teacher.
Student's level: {level}. Subject: {subject_text}.

LANGUAGE RULE (critical):
- By default, reply in clear, simple English.
- If the student writes in Hinglish (a mix of Hindi and English), then mirror their style and reply in Hinglish too, using 'tum' to address them.
- If the student writes in pure Hindi, reply in Hindi.
- Always match the language the student is using.

Teaching Rules:
1. Use clear, simple, and easy-to-understand language.
2. First explain the core concept, then give a practical real-life example.
3. If the student has uploaded a photo, PDF, or document:
   - Solve the problem step by step.
   - Highlight formulas and key steps in bold or code blocks.
   - Give a tip to avoid common exam mistakes.
4. Maintain difficulty appropriate for the student's level ({level}).
5. At the end, ask a short follow-up question to check the student's understanding.
"""

# ---------- Fast Word-by-Word Typing Animation Generator ----------
def stream_words(text, words_per_chunk=1, delay=0.012):
    """Yields text word-by-word with a fast typing stream animation."""
    words = text.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(delay)

# ---------- 3D Black Hole Cosmos Header ----------
st.markdown("""
<div class="blackhole-container">
    <div class="blackhole-core">
        <div class="blackhole-glow"></div>
        <div class="blackhole-accretion"></div>
        <div class="blackhole-ring"></div>
        <div class="blackhole-ring-2"></div>
        <div class="blackhole-event-horizon"></div>
    </div>
    <h1 class="cosmos-title">Stuverse AI</h1>
    <p class="cosmos-subtitle">Your Personal AI Teacher &bull; Ask Doubts &bull; Learn with Confidence</p>
    <div style="margin-top: 0.5rem; text-align: center;">
        <span class="feature-pill">⚡ Instant Solutions</span>
        <span class="feature-pill">📖 Clear Explanations</span>
        <span class="feature-pill">📸 Photo & PDF Doubts</span>
        <span class="feature-pill">🎓 Built for Students</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- File Upload (Doubts & Notes) ----------
with st.expander("📎 **Upload Study Material / Question Photo**", expanded=False):
    uploaded_file = st.file_uploader(
        "Upload a photo of your textbook question, handwritten notes, or a PDF:",
        type=["png", "jpg", "jpeg", "webp", "pdf", "txt", "md"],
        help="Upload photos of doubts, question papers, or PDF lecture notes for step-by-step solutions",
        key="file_uploader",
    )
    if uploaded_file is not None:
        file_mime = uploaded_file.type
        file_name = uploaded_file.name
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        col_f1, col_f2 = st.columns([0.45, 0.55])
        with col_f1:
            if file_mime.startswith("image/"):
                st.image(uploaded_file, caption=f"📸 {file_name} ({file_size_kb:.1f} KB)", use_container_width=True)
            else:
                st.info(f"📄 **{file_name}** ({file_size_kb:.1f} KB)")
        with col_f2:
            st.markdown("**Quick Actions:**")
            col_q1, col_q2 = st.columns(2)
            solve_btn = col_q1.button("📐 Solve Step-by-Step", use_container_width=True)
            summary_btn = col_q2.button("📝 Create Summary", use_container_width=True)

# ---------- Render Existing Messages ----------
messages = current_chat.get("messages", [])
for msg in messages:
    role = msg["role"]
    with st.chat_message(role):
        if role == "user":
            st.markdown('<div class="sender-msg-marker"></div>', unsafe_allow_html=True)
            if msg.get("file_name"):
                st.caption(f"📎 Attached: **{msg['file_name']}**")
            st.markdown(msg["text"])
        else:
            st.markdown('<div class="receiver-msg-marker"></div>', unsafe_allow_html=True)
            st.markdown(msg["text"])

# ---------- Suggestion Pills ----------
selected_prompt = None
if not messages and uploaded_file is None:
    st.markdown("##### 💡 Try asking:")
    chips = list(SUGGESTIONS.keys())
    cols = st.columns(len(chips))
    for i, chip_text in enumerate(chips):
        if cols[i].button(chip_text, key=f"chip_{i}", use_container_width=True):
            selected_prompt = SUGGESTIONS[chip_text]

if uploaded_file is not None:
    if 'solve_btn' in locals() and solve_btn:
        selected_prompt = "Please solve the question in this uploaded image/document step by step and explain it in detail."
    elif 'summary_btn' in locals() and summary_btn:
        selected_prompt = "Please create a comprehensive summary with the main bullet points from this uploaded file."

user_input = st.chat_input(
    "Type your doubt or question here..." if uploaded_file is None else f"📎 What would you like to ask about '{uploaded_file.name}'?",
)
active_prompt = selected_prompt or user_input

# ---------- Handle Question & AI Response ----------
if active_prompt:
    if st.session_state.daily_count >= DAILY_LIMIT:
        st.warning(f"You've used all {DAILY_LIMIT} free questions for today. Come back tomorrow!", icon="⏳")
        st.stop()

    file_part = None
    file_display_name = None

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_mime = uploaded_file.type
        file_display_name = uploaded_file.name
        if file_mime.startswith("image/"):
            file_part = types.Part.from_bytes(data=file_bytes, mime_type=file_mime)
        elif file_mime == "application/pdf":
            file_part = types.Part.from_bytes(data=file_bytes, mime_type="application/pdf")
        else:
            text_content = file_bytes.decode("utf-8", errors="ignore")
            active_prompt = f"Document Content ({file_display_name}):\n```\n{text_content[:8000]}\n```\n\nStudent Question: {active_prompt}"

    with st.chat_message("user"):
        st.markdown('<div class="sender-msg-marker"></div>', unsafe_allow_html=True)
        if file_display_name:
            st.caption(f"📎 Attached: **{file_display_name}**")
        st.markdown(active_prompt)

    gemini_contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_contents.append({"role": role, "parts": [{"text": m["text"]}]})

    current_parts = []
    if file_part:
        current_parts.append(file_part)
    current_parts.append(types.Part.from_text(text=active_prompt))
    gemini_contents.append({"role": "user", "parts": current_parts})

    with st.chat_message("assistant"):
        st.markdown('<div class="receiver-msg-marker"></div>', unsafe_allow_html=True)
        answer = None
        ok = False

        with st.status("🧠 Stuverse AI is thinking...", expanded=False) as status:
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=gemini_contents,
                        config=types.GenerateContentConfig(
                            system_instruction=TEACHER_PROMPT,
                        ),
                    )
                    answer = response.text
                    if answer:
                        ok = True
                    else:
                        answer = "The AI returned an empty response. Please try asking again."
                    break
                except Exception as e:
                    err_msg = str(e)
                    if "503" in err_msg and attempt < 2:
                        time.sleep(2)
                    else:
                        answer = f"Sorry, a technical error occurred: {err_msg}"
                        break
            status.update(
                label="Ready!" if ok else "Error",
                state="complete" if ok else "error",
            )

        # Word-by-word fast typing animation
        if ok:
            st.write_stream(stream_words(answer, delay=0.012))
        else:
            st.markdown(answer)

    if ok:
        if not messages:
            title_text = active_prompt.replace("\n", " ")[:28]
            current_chat["title"] = f"{title_text}..."
            current_chat["created_at"] = datetime.now().strftime("%d %b, %I:%M %p")

        user_entry = {"role": "user", "text": active_prompt}
        if file_display_name:
            user_entry["file_name"] = file_display_name
        current_chat["messages"].append(user_entry)
        current_chat["messages"].append({"role": "assistant", "text": answer})

        st.session_state.all_chats[current_id] = current_chat
        save_all_chats(st.session_state.all_chats)
        st.session_state.daily_count += 1
        st.rerun()
