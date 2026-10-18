# Stuverse AI — Your Personal AI Teacher (v2.0)
# Run: python -m streamlit run stuverse.py

import os
import json
import time
import uuid
from datetime import datetime
import streamlit as st
from google import genai
from google.genai import types

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Stuverse AI - Your Personal AI Teacher",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling to match the Stuverse AI Neon Purple Aesthetic
st.markdown("""
<style>
    /* Gradient App Header */
    .stuverse-header {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(139, 92, 246, 0.1);
    }
    .stuverse-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #c084fc, #818cf8, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .stuverse-subtitle {
        color: #d1d5db;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    /* Feature Badges */
    .pillar-card {
        background: rgba(26, 17, 40, 0.7);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .pillar-icon {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    .pillar-title {
        font-weight: 700;
        color: #c084fc;
        font-size: 1rem;
    }
    .pillar-desc {
        color: #9ca3af;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

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
    "📐 Quadratic formula": "Quadratic formula kya hoti hai aur isse step-by-step kaise solve karte hain?",
    "⚛️ Newton's laws of motion": "Newton ke teen laws of motion simple Hinglish mein daily-life examples ke sath samjhao",
    "💻 Python loops": "Python mein for loop aur while loop kaise kaam karte hain with practical example?",
    "🌿 Photosynthesis": "Photosynthesis ka biological process step by step easy language mein samjhao",
}

# ---------- API Key Initialization ----------
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
        st.error(
            "GEMINI_API_KEY nahi mili! Streamlit Cloud par Secrets mein GEMINI_API_KEY add karo ya locally .streamlit/secrets.toml mein rakho."
        )
        st.stop()
    return genai.Client(api_key=api_key)

client = get_gemini_client()

# ---------- Chat Persistence Helpers ----------
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

# Initialize session state for chats
if "all_chats" not in st.session_state:
    st.session_state.all_chats = load_all_chats()

# Ensure at least one active chat session
if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in st.session_state.all_chats:
    if st.session_state.all_chats:
        first_id = list(st.session_state.all_chats.keys())[-1]
        st.session_state.current_chat_id = first_id
    else:
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "id": new_id,
            "title": "Naya Chat",
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
    "title": "Naya Chat",
    "created_at": datetime.now().strftime("%d %b, %I:%M %p"),
    "messages": [],
    "level": "College",
    "subject": "All subjects",
})

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 🎓 **Stuverse AI**")
    st.caption("Your Personal AI Study Companion")

    # New Chat Button
    if st.button("➕ **Naya Chat Shuru Karo**", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "id": new_id,
            "title": "Naya Chat",
            "created_at": datetime.now().strftime("%d %b, %I:%M %p"),
            "messages": [],
            "level": current_chat.get("level", "College"),
            "subject": current_chat.get("subject", "All subjects"),
        }
        st.session_state.current_chat_id = new_id
        save_all_chats(st.session_state.all_chats)
        st.rerun()

    st.divider()

    # Settings Section
    st.markdown("#### ⚙️ Settings")
    current_level = current_chat.get("level", "College")
    current_level_idx = LEVELS.index(current_level) if current_level in LEVELS else 0
    level = st.selectbox(
        "Tumhara level",
        LEVELS,
        index=current_level_idx,
        key=f"level_sel_{current_id}",
    )

    current_subj = current_chat.get("subject", "All subjects")
    current_subj_idx = SUBJECTS.index(current_subj) if current_subj in SUBJECTS else 0
    subject = st.selectbox(
        "Subject",
        SUBJECTS,
        index=current_subj_idx,
        key=f"subj_sel_{current_id}",
    )

    # Save level & subject changes to current chat
    if current_chat.get("level") != level or current_chat.get("subject") != subject:
        current_chat["level"] = level
        current_chat["subject"] = subject
        st.session_state.all_chats[current_id] = current_chat
        save_all_chats(st.session_state.all_chats)

    st.divider()

    # Chat History Section
    st.markdown("#### 📜 Purani Chat History")
    chat_ids = list(st.session_state.all_chats.keys())
    chat_ids.reverse()  # Show newest first

    for cid in chat_ids:
        cinfo = st.session_state.all_chats[cid]
        col_btn, col_del = st.columns([0.82, 0.18])
        is_active = (cid == current_id)
        btn_label = f"{'👉 ' if is_active else '💬 '}{cinfo.get('title', 'Chat')}"
        if col_btn.button(
            btn_label,
            key=f"hist_btn_{cid}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.current_chat_id = cid
            st.rerun()

        if col_del.button("🗑️", key=f"del_btn_{cid}", help="Chat delete karo"):
            del st.session_state.all_chats[cid]
            if not st.session_state.all_chats:
                new_id = str(uuid.uuid4())
                st.session_state.all_chats[new_id] = {
                    "id": new_id,
                    "title": "Naya Chat",
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

    # Daily Usage Meter
    used = st.session_state.daily_count
    remaining = DAILY_LIMIT - used
    st.caption(f"📊 **{used}/{DAILY_LIMIT}** sawaal use hue")
    st.progress(min(used / DAILY_LIMIT, 1.0))
    if 0 < remaining <= 3:
        st.warning(f"Sirf {remaining} sawaal bache hain aaj ke!")

    # Export Notes Button
    if current_chat.get("messages"):
        export_text = f"# 🎓 Stuverse AI Study Notes\n"
        export_text += f"**Topic / Chat**: {current_chat.get('title')}\n"
        export_text += f"**Date**: {current_chat.get('created_at')}\n"
        export_text += f"**Level**: {current_chat.get('level')} | **Subject**: {current_chat.get('subject')}\n\n"
        export_text += "---\n\n"
        for m in current_chat["messages"]:
            speaker = "🧑‍🎓 Student" if m["role"] == "user" else "🤖 Stuverse AI Teacher"
            file_info = f" *(Attached: {m['file_name']})*" if m.get("file_name") else ""
            export_text += f"### {speaker}{file_info}:\n{m['text']}\n\n"
        st.download_button(
            "📥 **Download Notes (.md)**",
            data=export_text,
            file_name=f"Stuverse_Notes_{current_id[:6]}.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ---------- System Prompt ----------
subject_text = "koi bhi subject" if subject == "All subjects" else subject
TEACHER_PROMPT = f"""\
Tum Stuverse AI ke friendly, encouraging aur highly knowledgeable personal AI teacher ho.
Student ka level: {level}. Subject: {subject_text}.
Student ko natural, simple Hinglish mein samjhao aur 'tum' bol ke baat karo.

Teacher Rules:
1. Clear, simple aur easy-to-understand language use karo.
2. Pehle core concept samjhao, phir ek practical real-life example do.
3. Agar student ne koi sawaal ya photo/PDF upload ki hai:
   - Problem ko step-by-step solve karo.
   - Formulas aur key steps ko bold ya code block mein highlight karo.
   - Common exam mistakes se bachne ki tip do.
4. Student ke level ({level}) ke hisaab se difficulty maintain karo.
5. End mein student ki concept clarity check karne ke liye ek chhota follow-up sawaal puchho.
"""

# ---------- App Header ----------
st.markdown("""
<div class="stuverse-header">
    <div class="stuverse-title">✨ Stuverse AI</div>
    <p class="stuverse-subtitle">Your Personal AI Teacher • <b>Ask. Learn. Grow.</b></p>
</div>
""", unsafe_allow_html=True)

# ---------- About Stuverse & Official Posters ----------
with st.expander("🌟 **About Stuverse AI & Official Posters (Dekho Stuverse kya hai)**", expanded=False):
    # Four Pillars Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">💬</div>
            <div class="pillar-title">Ask</div>
            <div class="pillar-desc">Get instant, step-by-step answers in simple Hinglish</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">📖</div>
            <div class="pillar-title">Learn</div>
            <div class="pillar-desc">Summaries, notes, and crystal-clear concepts</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">🔬</div>
            <div class="pillar-title">Explore</div>
            <div class="pillar-desc">New ideas, coding, science, and essential skills</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">📈</div>
            <div class="pillar-title">Grow</div>
            <div class="pillar-desc">Build your future with smarter AI tools</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📸 **Official Posters**")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        if os.path.exists("assets/poster1.jpeg"):
            st.image("assets/poster1.jpeg", caption="🚀 Stuverse AI is here — Ask. Learn. Grow.", use_container_width=True)
    with p_col2:
        if os.path.exists("assets/poster2.jpeg"):
            st.image("assets/poster2.jpeg", caption="📚 Your Study Companion in One Place", use_container_width=True)

    st.markdown("""
    ---
    **Smarter Studying. Bigger Dreams.** 🚀  
    Stuverse AI is crafted specially for students to make learning stress-free, engaging, and accessible.
    
    📲 **Share with friends:** [Share on WhatsApp](https://api.whatsapp.com/send?text=Check%20out%20Stuverse%20AI%20-%20Your%20Personal%20AI%20Teacher!%20https://stuverseai.streamlit.app/)
    """)

# ---------- File Upload Section ----------
with st.expander("📎 **Upload Study Material / Question Photo (Image / PDF / Notes)**", expanded=False):
    uploaded_file = st.file_uploader(
        "Textbook question ki photo, handwritten notes, ya PDF upload karo:",
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
            st.markdown("**Quick Actions for this file:**")
            col_q1, col_q2 = st.columns(2)
            solve_btn = col_q1.button("📐 Step-by-step Solve Karo", use_container_width=True)
            summary_btn = col_q2.button("📝 Short Summary Banao", use_container_width=True)

# ---------- Render Existing Messages ----------
messages = current_chat.get("messages", [])

for msg in messages:
    with st.chat_message(msg["role"]):
        if msg.get("file_name"):
            st.caption(f"📎 Attached: **{msg['file_name']}**")
        st.markdown(msg["text"])

# ---------- Suggestion Pills (If no messages in chat) ----------
selected_prompt = None
if not messages and uploaded_file is None:
    st.markdown("##### 💡 Try asking:")
    chips = list(SUGGESTIONS.keys())
    cols = st.columns(len(chips))
    for i, chip_text in enumerate(chips):
        if cols[i].button(chip_text, key=f"chip_{i}", use_container_width=True):
            selected_prompt = SUGGESTIONS[chip_text]

# Handle quick prompt buttons from file uploader
if uploaded_file is not None:
    if 'solve_btn' in locals() and solve_btn:
        selected_prompt = "Kripya is uploaded image/document ke question ko step-by-step solve karo aur detail mein samjhao."
    elif 'summary_btn' in locals() and summary_btn:
        selected_prompt = "Kripya is uploaded file ka easy language mein comprehensive summary aur main bullet points bana do."

# Chat input
user_input = st.chat_input(
    "Apna doubt yahan likho ya sawaal puchho..." if uploaded_file is None else f"📎 '{uploaded_file.name}' ke bare mein kya puchhna hai?",
)

active_prompt = selected_prompt or user_input

# ---------- Handle Question Submission ----------
if active_prompt:
    if st.session_state.daily_count >= DAILY_LIMIT:
        st.warning(
            f"⚠️ Aaj ke {DAILY_LIMIT} free sawaal complete ho gaye. Kal subah phir se continue karo!",
            icon="⏳",
        )
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
            active_prompt = f"Document Content ({file_display_name}):\n```\n{text_content[:8000]}\n```\n\nStudent Doubt: {active_prompt}"

    # Display user query in UI
    with st.chat_message("user"):
        if file_display_name:
            st.caption(f"📎 Attached: **{file_display_name}**")
        st.markdown(active_prompt)

    # Prepare chat history for API
    gemini_contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        gemini_contents.append({"role": role, "parts": [{"text": m["text"]}]})

    # Add current prompt (+ file if present)
    current_parts = []
    if file_part:
        current_parts.append(file_part)
    current_parts.append(types.Part.from_text(text=active_prompt))
    gemini_contents.append({"role": "user", "parts": current_parts})

    # Generate Response
    with st.chat_message("assistant"):
        answer = None
        ok = False

        with st.status("🧠 Stuverse AI soch raha hai...", expanded=False) as status:
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
                        answer = "AI ne khali jawab diya. Kripya sawaal dobara puchho."
                    break
                except Exception as e:
                    err_msg = str(e)
                    if "503" in err_msg and attempt < 2:
                        time.sleep(2)
                    else:
                        answer = f"Maaf karna, ek takneeki samasya aayi: {err_msg}"
                        break
            status.update(
                label="Taiyaar!" if ok else "Error",
                state="complete" if ok else "error",
            )

        st.markdown(answer)

    # Save to history & update state
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
