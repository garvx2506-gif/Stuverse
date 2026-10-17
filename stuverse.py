# StudyVerse - Premium AI Tutor (v1.0)
# Run: python -m streamlit run stuverse.py

import os
import time
import streamlit as st
from google import genai
from google.genai import types

# ---------- Settings ----------
MODEL_NAME = "gemini-3.8-flash"
DAILY_LIMIT = 10

LEVELS = ["College", "Class 11-12", "Class 9-10"]
SUBJECTS = [
    "All subjects", "Maths", "Physics", "Chemistry",
    "Biology", "Computer / Programming", "English",
]

SUGGESTIONS = {
    ":violet[:material/calculate:] Quadratic formula samjhao": "Quadratic formula kya hoti hai aur isse kaise solve karte hain?",
    ":blue[:material/science:] Newton's laws of motion": "Newton ke teen laws of motion simple mein samjhao with examples",
    ":green[:material/code:] Python loops sikhao": "Python mein for loop aur while loop kaise kaam karte hain?",
    ":orange[:material/biotech:] Photosynthesis explain karo": "Photosynthesis ka process step by step samjhao",
}

# ---------- Page setup ----------
st.set_page_config(
    page_title="StudyVerse",
    page_icon=":material/school:",
    layout="centered",
)

# ---------- API key ----------
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY set nahi hai. `.streamlit/secrets.toml` mein add karo ya environment variable set karo.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------- Session state ----------
st.session_state.setdefault("messages", [])
st.session_state.setdefault("count", 0)

# ---------- Sidebar ----------
st.sidebar.header("Settings", icon=":material/tune:")
level = st.sidebar.selectbox(
    ":material/school: Tumhara level",
    LEVELS,
)
subject = st.sidebar.selectbox(
    ":material/menu_book: Subject",
    SUBJECTS,
)

st.sidebar.space("medium")

if st.sidebar.button(
    "New chat",
    icon=":material/add_comment:",
    use_container_width=True,
):
    st.session_state.messages = []
    st.toast("Naya chat shuru!", icon=":material/check_circle:")
    st.rerun()

st.sidebar.space("small")

# Usage meter
used = st.session_state.count
remaining = DAILY_LIMIT - used
st.sidebar.caption(
    f":material/question_answer: {used}/{DAILY_LIMIT} sawaal use hue"
)
st.sidebar.progress(used / DAILY_LIMIT)
if remaining <= 3 and remaining > 0:
    st.sidebar.caption(f":orange[Sirf {remaining} sawaal bache hain!]")

# ---------- System prompt ----------
subject_text = "koi bhi subject" if subject == "All subjects" else subject
TEACHER_PROMPT = f"""\
Tum StudyVerse ke friendly AI teacher ho.
Student ka level: {level}. Subject: {subject_text}.
Student ko easy Hinglish mein samjhao aur 'tum' bol ke baat karo.
Rules:
1. Chhote aur simple jawab do.
2. Pehle concept samjhao, phir ek real-life example do.
3. Agar maths/science ka sawaal hai toh step-by-step solve karo.
4. Student ke level ke hisaab se difficulty rakho.
5. End mein student ko ek chhota follow-up sawaal puchho.
"""

# ---------- Header ----------
st.title("StudyVerse", icon=":material/auto_awesome:")
st.caption("Tumhara personal AI teacher. Koi bhi doubt puchho!")

# ---------- Chat history ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# ---------- Suggestion chips (only before first message) ----------
prompt = st.chat_input(
    "Apna doubt yahan likho...",
    submit_mode="disable",
)

if not st.session_state.messages:
    suggestions_slot = st.empty()
    selected = suggestions_slot.pills(
        "Try asking:",
        list(SUGGESTIONS.keys()),
        label_visibility="collapsed",
    )
    if selected:
        prompt = SUGGESTIONS[selected]
    if prompt:
        suggestions_slot.empty()

# ---------- Handle question ----------
if prompt:
    # Limit check
    if st.session_state.count >= DAILY_LIMIT:
        st.warning(
            f"Aaj ke {DAILY_LIMIT} free sawaal khatam ho gaye. Kal phir aana!",
            icon=":material/block:",
        )
        st.stop()

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build history for API
    history = []
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "model"
        history.append({"role": role, "parts": [{"text": m["text"]}]})
    history.append({"role": "user", "parts": [{"text": prompt}]})

    # Generate response with thinking indicator
    with st.chat_message("assistant"):
        answer = None
        ok = False

        with st.status(":shimmer[Soch raha hu...]", type="compact") as status:
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=history,
                        config=types.GenerateContentConfig(
                            system_instruction=TEACHER_PROMPT,
                        ),
                    )
                    answer = response.text
                    if answer:
                        ok = True
                    else:
                        reason = (
                            response.candidates[0].finish_reason
                            if response.candidates
                            else "no candidates"
                        )
                        answer = f"AI ne khali jawab diya (reason: {reason}). Dobara try karo."
                    break
                except Exception as e:
                    if "503" in str(e) and attempt < 2:
                        time.sleep(3)
                    else:
                        answer = f"Oops, kuch gadbad ho gayi: {e}"
                        break
            status.update(
                label="Done" if ok else "Error",
                state="complete" if ok else "error",
            )

        st.markdown(answer)

    # Save to history
    if ok:
        st.session_state.messages.append({"role": "user", "text": prompt})
        st.session_state.messages.append({"role": "assistant", "text": answer})
        st.session_state.count += 1
