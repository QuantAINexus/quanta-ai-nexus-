from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit page setup
st.set_page_config(page_title="QuantAI Nexus", layout="wide")

# Custom CSS for better styling
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

# Logo and heading
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1024px-React-icon.svg.png", width=60)  # replace with your logo
with col2:
    st.title("🤖 QuantAI Nexus")
    st.write("Your Personal AI Assistant")

# Input area
prompt = st.text_input("You:", "")

# Generate response
if prompt:
    with st.spinner("Thinking..."):
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = chat_response.choices[0].message.content
        st.markdown(f"**AI:** {reply}")

# Footer
st.markdown('<div class="footer">© 2025 QuantAI Nexus | Built with ❤️ using Streamlit & OpenAI</div>', unsafe_allow_html=True)
