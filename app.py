import os
import streamlit as st
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session
import requests
import urllib.parse
import json
import altair as alt

# --- LOAD ENV ---
load_dotenv()

# --- CONFIG PAGE ---
st.set_page_config(page_title="QuantaAI Nexus", page_icon="🤖", layout="wide")

# --- GLOBAL CONFIG ---
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501"  # or deployment URL

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
SCOPE = "openid email profile"
DATA_FILE = "user_data.json"

# --- UTILS ---
def save_user_data(user):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    data[user['email']] = user
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# --- THEME TOGGLE ---
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# --- CUSTOM CSS ---
def local_css(theme):
    if theme == "dark":
        bg_gradient = "linear-gradient(135deg, #1e1e2f 0%, #2f2f4f 100%)"
        text_color = "#f0f0f0"
        card_bg = "rgba(40, 40, 60, 0.9)"
        sidebar_bg = "#2a2a42"
        button_bg = "#5a42a6"
        button_hover = "#7b59d6"
    else:
        bg_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
        text_color = "#111"
        card_bg = "rgba(255, 255, 255, 0.9)"
        sidebar_bg = "#4e3c90"
        button_bg = "#764ba2"
        button_hover = "#a085d8"

    st.markdown(f"""
    <style>
        /* Background gradient */
        .main {{
            background: {bg_gradient};
            color: {text_color};
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 2rem 3rem 5rem 3rem;
        }}
        /* Card style */
        .card {{
            background-color: {card_bg};
            border-radius: 15px;
            padding: 25px 30px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            margin-bottom: 25px;
        }}
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            color: white;
        }}
        /* Sidebar headers */
        .css-1d391kg {{
            color: white !important;
        }}
        /* Button style */
        div.stButton > button {{
            background-color: {button_bg};
            color: white;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: 600;
            transition: background-color 0.3s ease;
            border: none;
        }}
        div.stButton > button:hover {{
            background-color: {button_hover};
            color: white;
        }}
        /* Chat bubbles */
        .chat-user {{
            background-color: #6c757d;
            color: white;
            padding: 10px 15px;
            border-radius: 20px 20px 0 20px;
            margin: 8px 0;
            max-width: 75%;
            align-self: flex-end;
            font-size: 1rem;
            font-weight: 500;
        }}
        .chat-ai {{
            background-color: #764ba2;
            color: white;
            padding: 10px 15px;
            border-radius: 20px 20px 20px 0;
            margin: 8px 0;
            max-width: 75%;
            align-self: flex-start;
            font-size: 1rem;
            font-weight: 500;
        }}
        /* Flex container for chat */
        .chat-container {{
            display: flex;
            flex-direction: column;
        }}
    </style>
    """, unsafe_allow_html=True)

local_css(st.session_state.theme)

# --- AUTH ---
oauth = OAuth2Session(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=SCOPE,
    redirect_uri=REDIRECT_URI,
)

query_params = st.query_params

# --- LOGIN ---
if "user" not in st.session_state:
    if "code" in query_params:
        try:
            full_url = f"{REDIRECT_URI}?{urllib.parse.urlencode(query_params)}"
            token = oauth.fetch_token(
                TOKEN_URL,
                code=query_params["code"],
                authorization_response=full_url,
                include_client_id=True,
            )
            userinfo_response = requests.get(
                USERINFO_URL,
                headers={"Authorization": f"Bearer {token['access_token']}"}
            )
            user_info = userinfo_response.json()
            st.session_state.user = user_info
            save_user_data(user_info)
            st.experimental_set_query_params()  # clear query params
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Login failed: {str(e)}")
    else:
        auth_url, _ = oauth.create_authorization_url(AUTH_URL)
        st.markdown(f"[🔐 Login with Google]({auth_url})", unsafe_allow_html=True)

else:
    user = st.session_state.user

    # Top bar with user info and theme toggle
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.image(user.get("picture", ""), width=60, caption=f"👤 {user.get('name', '')}")
    with col2:
        st.markdown(f"### 🤖 QuantAI Nexus - Welcome, **{user.get('name','')}**!")
    with col3:
        if st.button("🌗 Toggle Theme"):
            toggle_theme()
            st.experimental_rerun()

    st.markdown("---")

    # Sidebar
    with st.sidebar:
        st.image("logo.png", width=150)
        st.title("Navigation")
        page = st.radio("Go to", ["Dashboard 🏠", "Chat 💬", "Upload 📁", "Quiz 🧠", "Leaderboard 🏆", "Profile 👤"], index=0)

        st.markdown("---")
        if st.button("🔓 Logout"):
            del st.session_state.user
            st.experimental_rerun()

    # --- PAGE CONTENT ---
    if page.startswith("Dashboard"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Dashboard Overview")

        # Example usage stats
        total_chats = 124
        tokens_used = 87456

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Chats", total_chats)
        with col2:
            st.metric("Tokens Used", tokens_used)

        st.markdown("### Chat Activity Over Last 7 Days")

        import pandas as pd
        import numpy as np

        dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
        chats_per_day = np.random.randint(5, 20, size=7)
        df = pd.DataFrame({"Date": dates, "Chats": chats_per_day})

        chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3, color="#764ba2").encode(
            x=alt.X('Date:T', axis=alt.Axis(format='%a')),
            y='Chats:Q'
        ).properties(height=300, width=600)

        st.altair_chart(chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif page.startswith("Chat"):
        st.markdown('<div class="card chat-container">', unsafe_allow_html=True)
        st.subheader("💬 Chat with QuantaAI")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        prompt = st.text_input("You:", key="chat_input")

        if prompt:
            st.session_state.chat_history.append({"sender": "user", "message": prompt})

            with st.spinner("QuantaAI is thinking..."):
                # Simulate AI response here (replace with OpenAI API call)
                import time
                time.sleep(1.5)
                ai_response = f"I received your message: '{prompt}'. (This is a simulated response.)"
                st.session_state.chat_history.append({"sender": "ai", "message": ai_response})
                st.experimental_rerun()

        # Display chat messages with bubbles
        for chat in st.session_state.chat_history:
            if chat["sender"] == "user":
                st.markdown(f'<div class="chat-user">{chat["message"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai">{chat["message"]}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    elif page.startswith("Upload"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📁 Upload Files")

        uploaded = st.file_uploader("Upload your file")
        if uploaded:
            filename = f"uploads/{user['email'].replace('@','_')}_{uploaded.name}"
            os.makedirs("uploads", exist_ok=True)
            with open(filename, "wb") as f:
                f.write(uploaded.read())
            st.success("File uploaded successfully.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif page.startswith("Quiz"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🧠 AI Quiz")

        if st.button("Start Quiz"):
            st.session_state.quiz = {
                "q1": {
                    "question": "What is the capital of France?",
                    "options": ["Paris", "London", "Berlin"],
                    "answer": "Paris"
                },
                "q2": {
                    "question": "2 + 2 = ?",
                    "options": ["3", "4", "5"],
                    "answer": "4"
                }
            }

        if "quiz" in st.session_state:
            score = 0
            for key, q in st.session_state.quiz.items():
                ans = st.radio(q["question"], q["options"], key=key)
                if ans == q["answer"]:
                    score += 1
            st.write(f"✅ Your Score: {score} / {len(st.session_state.quiz)}")

        st.markdown('</div>', unsafe_allow_html=True)

    elif page.startswith("Leaderboard"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏆 Leaderboard")
        data = load_user_data()
        for email, info in data.items():
            st.markdown(f"**{info['name']}** - {info['email']}")

        st.markdown('</div>', unsafe_allow_html=True)

    elif page.startswith("Profile"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Profile")
        st.write(user)
        st.markdown('</div>', unsafe_allow_html=True)
