from dotenv import load_dotenv
import os
import streamlit as st
import openai

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # ✅ Only one line needed here

# Streamlit UI
st.set_page_config(page_title="QuantAI Nexus", layout="centered")
st.title("🤖 Welcome to QuantAI Nexus")
st.write("Talk to your own AI assistant!")

# Input from user
prompt = st.text_input("You:", "")

# If there's a prompt, generate response
if prompt:
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(  # ✅ Fix this line
            model="gpt-3.5-turbo",  # ✅ Use the correct model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        st.markdown(f"**AI:** {reply}")
