from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --- Streamlit page setup ---
st.set_page_config(page_title="QuantAI Nexus", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
            padding: 2rem;
        }
        h1 {
            color: #2c3e50;
            font-family: 'Segoe UI', sans-serif;
        }
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background-color: #ecf0f1;
            padding: 10px;
            text-align: center;
            font-size: 14px;
            color: #7f8c8d;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("logo.png", use_column_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Chat", "History", "Pro Plans"])

# --- Title & Branding ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=60)
with col2:
    st.title("🤖 QuantAI Nexus")
    st.write("Your Personal AI Assistant")

st.markdown("---")

# --- Page Routing ---
if page == "Dashboard":
    st.subheader("📊 Dashboard Overview")
    st.info("This is your dashboard. You can show usage stats, graphs, or notifications here.")

elif page == "Chat":
    st.subheader("💬 Chat with Quanta AI")
    prompt = st.text_input("You:", "")
    if prompt:
        with st.spinner("Thinking..."):
            try:
                chat_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                reply = chat_response.choices[0].message.content
                st.markdown(f"**AI:** {reply}")
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "History":
    st.switch_page("pages/history.py")

elif page == "Pro Plans":
    st.switch_page("pages/pro_plans.py")

# --- Footer ---
st.markdown('<div class="footer">© 2025 QuantAI Nexus | Built with ❤️ using Streamlit & OpenAI</div>', unsafe_allow_html=True)
