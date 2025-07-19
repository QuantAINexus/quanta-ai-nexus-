from dotenv import load_dotenv
import os
import streamlit as st
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 🔽 Google site verification tag
st.markdown(
    '<meta name="google-site-verification" content="W8nigqjxcwnZcup1TKclYmcfwYcySWf-DzXpJ4iqh04" />',
    unsafe_allow_html=True
)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="QuantAI Nexus", layout="centered")
st.title("🤖 Welcome to QuantAI Nexus")
st.write("Talk to your own AI assistant!")

# Input prompt
prompt = st.text_input("You:", "")

# Generate response if prompt is entered
if prompt:
    with st.spinner("Thinking..."):
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply = chat_response.choices[0].message.content
        st.markdown(f"**AI:** {reply}")
