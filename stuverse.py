# Stuverse AI — Your Personal AI Teacher (v2.1)
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
    page_icon="\U0001f393",
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
    "\U0001f4d0 Quadratic formula": "What is the quadratic formula and how do you solve equations with it step by step?",
    "\u269b\ufe0f Newton's laws of motion": "Explain Newton's three laws of motion with simple, real-life examples.",
    "\U0001f4bb Python loops": "How do for loops and while loops work in Python? Give a practical example.",
    "\U0001f33f Photosynthesis": "Explain the process of photosynthesis step by step in simple language.",
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
            "GEMINI_API_KEY not found! Add it in Streamlit Cloud Secrets or locally in `.streamlit/secrets.toml`."
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
    st.markdown("### \U0001f393 **Stuverse AI**")
    st.caption("Your Personal AI Study Companion")

    # New Chat Button
    if st.button("\u2795 **Start New Chat**", use_container_width=True, type="primary"):
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

    # Settings Section
    st.markdown("#### \u2699\ufe0f Settings")
    current_level = current_chat.get("level", "College")
    current_level_idx = LEVELS.index(current_level) if current_level in LEVELS else 0
    level = st.selectbox(
        "Your level",
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
    st.markdown("#### \U0001f4dc Chat History")
    chat_ids = list(st.session_state.all_chats.keys())
    chat_ids.reverse()  # Show newest first

    for cid in chat_ids:
        cinfo = st.session_state.all_chats[cid]
        col_btn, col_del = st.columns([0.82, 0.18])
        is_active = (cid == current_id)
        btn_label = f"{'\U0001f449 ' if is_active else '\U0001f4ac '}{cinfo.get('title', 'Chat')}"
        if col_btn.button(
            btn_label,
            key=f"hist_btn_{cid}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.current_chat_id = cid
            st.rerun()

        if col_del.button("\U0001f5d1\ufe0f", key=f"del_btn_{cid}", help="Delete this chat"):
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

    # Daily Usage Meter
    used = st.session_state.daily_count
    remaining = DAILY_LIMIT - used
    st.caption(f"\U0001f4ca **{used}/{DAILY_LIMIT}** questions used")
    st.progress(min(used / DAILY_LIMIT, 1.0))
    if 0 < remaining <= 3:
        st.warning(f"Only {remaining} questions left for today!")

    # Export Notes Button
    if current_chat.get("messages"):
        export_text = f"# \U0001f393 Stuverse AI Study Notes\n"
        export_text += f"**Topic / Chat**: {current_chat.get('title')}\n"
        export_text += f"**Date**: {current_chat.get('created_at')}\n"
        export_text += f"**Level**: {current_chat.get('level')} | **Subject**: {current_chat.get('subject')}\n\n"
        export_text += "---\n\n"
        for m in current_chat["messages"]:
            speaker = "\U0001f9d1\u200d\U0001f393 Student" if m["role"] == "user" else "\U0001f916 Stuverse AI Teacher"
            file_info = f" *(Attached: {m['file_name']})*" if m.get("file_name") else ""
            export_text += f"### {speaker}{file_info}:\n{m['text']}\n\n"
        st.download_button(
            "\U0001f4e5 **Download Notes (.md)**",
            data=export_text,
            file_name=f"Stuverse_Notes_{current_id[:6]}.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ---------- System Prompt ----------
subject_text = "any subject" if subject == "All subjects" else subject
TEACHER_PROMPT = f"""\
You are Stuverse AI, a friendly, encouraging, and highly knowledgeable personal AI teacher.
Student's level: {level}. Subject: {subject_text}.

LANGUAGE RULE (very important):
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

# ---------- App Header ----------
st.markdown("""
<div class="stuverse-header">
    <div class="stuverse-title">\u2728 Stuverse AI</div>
    <p class="stuverse-subtitle">Your Personal AI Teacher \u2022 <b>Ask. Learn. Grow.</b></p>
</div>
""", unsafe_allow_html=True)

# ---------- About Stuverse & Official Posters ----------
with st.expander("\U0001f31f **About Stuverse AI & Official Posters**", expanded=False):
    # Four Pillars Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">\U0001f4ac</div>
            <div class="pillar-title">Ask</div>
            <div class="pillar-desc">Get instant, step-by-step answers to any question</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">\U0001f4d6</div>
            <div class="pillar-title">Learn</div>
            <div class="pillar-desc">Summaries, notes, and crystal-clear concepts</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">\U0001f52c</div>
            <div class="pillar-title">Explore</div>
            <div class="pillar-desc">New ideas, coding, science, and essential skills</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="pillar-card">
            <div class="pillar-icon">\U0001f4c8</div>
            <div class="pillar-title">Grow</div>
            <div class="pillar-desc">Build your future with smarter AI tools</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### \U0001f4f8 **Official Posters**")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        if os.path.exists("assets/poster1.jpeg"):
            st.image("assets/poster1.jpeg", caption="\U0001f680 Stuverse AI is here \u2014 Ask. Learn. Grow.", use_container_width=True)
    with p_col2:
        if os.path.exists("assets/poster2.jpeg"):
            st.image("assets/poster2.jpeg", caption="\U0001f4da Your Study Companion in One Place", use_container_width=True)

    st.markdown("""
    ---
    **Smarter Studying. Bigger Dreams.** \U0001f680
    Stuverse AI is crafted specially for students to make learning stress-free, engaging, and accessible.

    \U0001f4f2 **Share with friends:** [Share on WhatsApp](https://api.whatsapp.com/send?text=Check%20out%20Stuverse%20AI%20-%20Your%20Personal%20AI%20Teacher!%20https://stuverseai.streamlit.app/)
    """)

# ---------- File Upload Section ----------
with st.expander("\U0001f4ce **Upload Study Material / Question Photo (Image / PDF / Notes)**", expanded=False):
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
                st.image(uploaded_file, caption=f"\U0001f4f8 {file_name} ({file_size_kb:.1f} KB)", use_container_width=True)
            else:
                st.info(f"\U0001f4c4 **{file_name}** ({file_size_kb:.1f} KB)")
        with col_f2:
            st.markdown("**Quick Actions for this file:**")
            col_q1, col_q2 = st.columns(2)
            solve_btn = col_q1.button("\U0001f4d0 Solve Step-by-Step", use_container_width=True)
            summary_btn = col_q2.button("\U0001f4dd Create Short Summary", use_container_width=True)

# ---------- Render Existing Messages ----------
messages = current_chat.get("messages", [])

for msg in messages:
    with st.chat_message(msg["role"]):
        if msg.get("file_name"):
            st.caption(f"\U0001f4ce Attached: **{msg['file_name']}**")
        st.markdown(msg["text"])

# ---------- Suggestion Pills (If no messages in chat) ----------
selected_prompt = None
if not messages and uploaded_file is None:
    st.markdown("##### \U0001f4a1 Try asking:")
    chips = list(SUGGESTIONS.keys())
    cols = st.columns(len(chips))
    for i, chip_text in enumerate(chips):
        if cols[i].button(chip_text, key=f"chip_{i}", use_container_width=True):
            selected_prompt = SUGGESTIONS[chip_text]

# Handle quick prompt buttons from file uploader
if uploaded_file is not None:
    if 'solve_btn' in locals() and solve_btn:
        selected_prompt = "Please solve the question in this uploaded image/document step by step and explain it in detail."
    elif 'summary_btn' in locals() and summary_btn:
        selected_prompt = "Please create a comprehensive summary with the main bullet points from this uploaded file."

# Chat input
user_input = st.chat_input(
    "Type your doubt or question here..." if uploaded_file is None else f"\U0001f4ce What would you like to ask about '{uploaded_file.name}'?",
)

active_prompt = selected_prompt or user_input

# ---------- Handle Question Submission ----------
if active_prompt:
    if st.session_state.daily_count >= DAILY_LIMIT:
        st.warning(
            f"You've used all {DAILY_LIMIT} free questions for today. Come back tomorrow!",
            icon="\u23f3",
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
            active_prompt = f"Document Content ({file_display_name}):\n```\n{text_content[:8000]}\n```\n\nStudent Question: {active_prompt}"

    # Display user query in UI
    with st.chat_message("user"):
        if file_display_name:
            st.caption(f"\U0001f4ce Attached: **{file_display_name}**")
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

        with st.status("\U0001f9e0 Stuverse AI is thinking...", expanded=False) as status:
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
